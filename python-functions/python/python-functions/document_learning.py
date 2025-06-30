"""
Document Learning Function - Multimodal Document Processing
Built on Palantir Foundry Functions with ML capabilities
"""

from foundry_functions import function, String, Dict, List
from foundry_ml_api import FoundryML
from foundry_datasets_api import DatasetClient
import base64
import json

@function(
    runtime="foundry-python-3.9",
    memory=8192,
    description="Process documents for RaiderBot knowledge base using Foundry ML"
)
def process_document(
    document_id: String,
    document_type: String = "auto",
    extract_entities: bool = True
) -> Dict:
    """
    Process documents using Foundry's ML capabilities.
    Extracts knowledge for RaiderBot's German Shepherd AI.
    
    Supported document types:
    - PDFs (safety manuals, regulations)
    - Images (delivery confirmations, incidents)
    - Text files (policies, procedures)
    """
    
    try:
        # Initialize Foundry ML client
        ml_client = FoundryML()
        dataset_client = DatasetClient()
        
        # Get document from Foundry dataset
        documents = dataset_client.get_dataset("raider_documents").to_pandas()
        doc = documents[documents['document_id'] == document_id].iloc[0]
        
        # Detect document type if auto
        if document_type == "auto":
            document_type = _detect_document_type(doc['file_extension'])
        
        # Process based on type
        if document_type == "pdf":
            extracted_data = _process_pdf(doc['content'], ml_client)
        elif document_type == "image":
            extracted_data = _process_image(doc['content'], ml_client)
        else:
            extracted_data = _process_text(doc['content'], ml_client)
        
        # Extract entities if requested
        entities = []
        if extract_entities:
            entities = _extract_transportation_entities(
                extracted_data['text'], ml_client
            )
        
        # Store in RaiderBot knowledge base
        knowledge_entry = {
            "document_id": document_id,
            "processed_text": extracted_data['text'],
            "entities": entities,
            "key_topics": extracted_data.get('topics', []),
            "safety_relevance_score": _calculate_safety_relevance(
                extracted_data['text']
            ),
            "processed_by": "Palantir Foundry ML",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to Foundry knowledge dataset
        _save_to_knowledge_base(knowledge_entry, dataset_client)
        
        return {
            "success": True,
            "document_id": document_id,
            "extracted_entities": len(entities),
            "safety_relevance": knowledge_entry['safety_relevance_score'],
            "foundry_ml_processed": True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "foundry_function": "document_learning",
            "status": "failed"
        }


def _detect_document_type(file_extension):
    """Detect document type from extension"""
    extension_map = {
        '.pdf': 'pdf',
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image',
        '.txt': 'text', '.md': 'text', '.doc': 'text', '.docx': 'text'
    }
    return extension_map.get(file_extension.lower(), 'text')

def _process_pdf(content, ml_client):
    """Process PDF using Foundry ML"""
    # Foundry ML PDF extraction
    return ml_client.extract_text_from_pdf(content)

def _process_image(content, ml_client):
    """Process image using Foundry ML OCR"""
    # Foundry ML OCR and image analysis
    return ml_client.analyze_image(content, enable_ocr=True)

def _process_text(content, ml_client):
    """Process text content"""
    return {"text": content, "topics": ml_client.extract_topics(content)}

def _extract_transportation_entities(text, ml_client):
    """Extract transportation-specific entities"""
    # Use Foundry ML NER for transportation entities
    entities = ml_client.extract_entities(
        text,
        entity_types=["LOCATION", "VEHICLE", "PERSON", "TIME", "SPEED"]
    )
    return entities

def _calculate_safety_relevance(text):
    """Calculate safety relevance score"""
    safety_keywords = [
        '60mph', 'speed limit', 'safety', 'accident', 'incident',
        'compliance', 'regulation', 'hours of service', 'maintenance'
    ]
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in safety_keywords if keyword in text_lower)
    return min(100, keyword_count * 10)

def _save_to_knowledge_base(entry, dataset_client):
    """Save processed document to Foundry knowledge base"""
    kb_dataset = dataset_client.get_dataset("raiderbot_knowledge_base")
    kb_dataset.append_row(entry)
