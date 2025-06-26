"""
RaiderBot AI and RAG Functions for Foundry
Replaces LangChain integration with Foundry AI capabilities

Based on app/api/rag/discovery/route.js and AI chat functionality
"""

from foundry_functions import Function, Input, Output
from foundry_functions.decorators import function
from foundry_datasets import Dataset, DatasetReader
from foundry_ai import LLMProvider, ChatCompletion, EmbeddingProvider
from foundry_vector import VectorSearch, VectorStore
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import re


@function("schema_discovery")
def schema_discovery(
    refresh_cache: Input[bool] = False,
    include_sample_data: Input[bool] = True
) -> Output[Dict[str, Any]]:
    """
    Discover and analyze database schema structure
    
    Replaces: app/api/rag/discovery/route.js schema discovery
    """
    
    # Access all available datasets for discovery
    dataset_registry = DatasetReader.list_datasets("raiderbot")
    
    discovery_results = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "action": "schema_discovery",
        "results": {
            "datasets_discovered": len(dataset_registry),
            "total_tables": 0,
            "total_columns": 0,
            "datasets": {}
        }
    }
    
    # Analyze each dataset
    for dataset_path in dataset_registry:
        try:
            dataset = DatasetReader(dataset_path)
            schema = dataset.schema()
            
            dataset_info = {
                "path": dataset_path,
                "column_count": len(schema.fields),
                "columns": []
            }
            
            # Extract column information
            for field in schema.fields:
                column_info = {
                    "name": field.name,
                    "type": str(field.dataType),
                    "nullable": field.nullable
                }
                
                # Get sample data if requested
                if include_sample_data:
                    try:
                        sample_values = dataset.select(field.name).distinct().limit(5).collect()
                        column_info["sample_values"] = [row[field.name] for row in sample_values if row[field.name] is not None]
                    except:
                        column_info["sample_values"] = []
                
                dataset_info["columns"].append(column_info)
            
            discovery_results["results"]["datasets"][dataset_path] = dataset_info
            discovery_results["results"]["total_tables"] += 1
            discovery_results["results"]["total_columns"] += len(schema.fields)
            
        except Exception as e:
            print(f"Error analyzing dataset {dataset_path}: {e}")
    
    return discovery_results


@function("semantic_analysis")
def semantic_analysis(
    query: Input[str],
    include_relationships: Input[bool] = True,
    max_results: Input[int] = 50
) -> Output[Dict[str, Any]]:
    """
    Perform semantic analysis of data relationships
    
    Replaces: LangChain semantic search and analysis
    """
    
    # Initialize embedding provider for semantic search
    embedding_provider = EmbeddingProvider("openai-text-embedding-ada-002")
    
    # Get embeddings for the query
    query_embedding = embedding_provider.embed_text(query)
    
    # Access vector store with pre-computed dataset embeddings
    vector_store = VectorStore("raiderbot_schema_embeddings")
    
    # Perform semantic search
    similar_schemas = vector_store.similarity_search(
        query_embedding,
        top_k=max_results,
        threshold=0.7
    )
    
    # Analyze results and build semantic understanding
    analysis_results = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "results": {
            "relevant_datasets": [],
            "suggested_columns": [],
            "potential_joins": [],
            "business_concepts": []
        }
    }
    
    # Process similar schema elements
    for result in similar_schemas:
        metadata = result.metadata
        
        # Categorize results
        if metadata.get("type") == "dataset":
            analysis_results["results"]["relevant_datasets"].append({
                "dataset": metadata["dataset_name"],
                "relevance_score": result.score,
                "description": metadata.get("description", ""),
                "key_columns": metadata.get("key_columns", [])
            })
        
        elif metadata.get("type") == "column":
            analysis_results["results"]["suggested_columns"].append({
                "dataset": metadata["dataset_name"],
                "column": metadata["column_name"],
                "relevance_score": result.score,
                "data_type": metadata.get("data_type", ""),
                "business_meaning": metadata.get("business_meaning", "")
            })
    
    # Generate potential joins if requested
    if include_relationships:
        analysis_results["results"]["potential_joins"] = _identify_join_opportunities(
            analysis_results["results"]["relevant_datasets"]
        )
    
    # Extract business concepts
    analysis_results["results"]["business_concepts"] = _extract_business_concepts(query)
    
    return analysis_results


@function("natural_language_query")
def natural_language_query(
    user_question: Input[str],
    language: Input[str] = "EN",
    include_context: Input[bool] = True,
    max_context_length: Input[int] = 4000
) -> Output[Dict[str, Any]]:
    """
    Process natural language queries about logistics data
    
    Replaces: LangChain chat interface and query processing
    """
    
    # Initialize LLM provider
    llm = LLMProvider("gpt-4o")
    
    # Build context from relevant datasets
    context = ""
    if include_context:
        context = _build_query_context(user_question, max_context_length)
    
    # Prepare system prompt for logistics domain
    system_prompt = _get_logistics_system_prompt(language)
    
    # Construct full prompt
    full_prompt = f"""
    {system_prompt}
    
    CONTEXT:
    {context}
    
    USER QUESTION: {user_question}
    
    Please provide a comprehensive answer that:
    1. Directly addresses the user's question
    2. Uses the provided data context when relevant
    3. Includes specific metrics and insights when possible
    4. Suggests follow-up questions or actions
    5. Responds in {language} language
    """
    
    # Generate response
    try:
        chat_completion = ChatCompletion(
            model=llm,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        response = chat_completion.generate()
        
        # Extract insights and recommendations
        insights = _extract_insights_from_response(response.content)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "user_question": user_question,
            "language": language,
            "response": {
                "answer": response.content,
                "insights": insights,
                "suggested_actions": _generate_suggested_actions(user_question, insights),
                "data_sources_used": _identify_data_sources_used(context),
                "confidence_score": 0.85  # Could be enhanced with actual confidence scoring
            },
            "metadata": {
                "context_length": len(context),
                "processing_time_ms": response.processing_time_ms,
                "model_used": "gpt-4o"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "fallback_response": _generate_fallback_response(user_question, language)
        }


@function("generate_business_insights")
def generate_business_insights(
    focus_area: Input[str] = "performance",  # performance, safety, efficiency, financial
    days_back: Input[int] = 30,
    language: Input[str] = "EN"
) -> Output[Dict[str, Any]]:
    """
    Generate AI-powered business insights from logistics data
    
    New capability leveraging Foundry AI
    """
    
    # Get relevant KPI data based on focus area
    if focus_area == "performance":
        from .kpi_functions import get_delivery_kpis, get_route_optimization_kpis
        kpi_data = {
            "delivery": get_delivery_kpis(days_back),
            "routes": get_route_optimization_kpis(days_back)
        }
    elif focus_area == "safety":
        from .kpi_functions import get_driver_kpis
        kpi_data = {
            "drivers": get_driver_kpis(days_back)
        }
    elif focus_area == "efficiency":
        from .kpi_functions import get_vehicle_kpis, get_route_optimization_kpis
        kpi_data = {
            "vehicles": get_vehicle_kpis(days_back),
            "routes": get_route_optimization_kpis(days_back)
        }
    else:  # financial
        from .kpi_functions import get_delivery_kpis, get_vehicle_kpis
        kpi_data = {
            "delivery": get_delivery_kpis(days_back),
            "vehicles": get_vehicle_kpis(days_back)
        }
    
    # Initialize LLM for insight generation
    llm = LLMProvider("gpt-4o")
    
    # Prepare analysis prompt
    analysis_prompt = f"""
    Analyze the following logistics KPI data and generate actionable business insights:
    
    FOCUS AREA: {focus_area.upper()}
    TIME PERIOD: Last {days_back} days
    DATA: {json.dumps(kpi_data, indent=2)}
    
    Please provide:
    1. Key trends and patterns identified
    2. Areas of concern or opportunity
    3. Specific recommendations for improvement
    4. Predicted impact of recommended actions
    5. Priority level for each recommendation
    
    Format the response as structured insights that a logistics manager can act upon.
    Language: {language}
    """
    
    try:
        chat_completion = ChatCompletion(
            model=llm,
            messages=[
                {"role": "system", "content": "You are an expert logistics analyst with deep knowledge of transportation operations, safety management, and business optimization."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        
        response = chat_completion.generate()
        
        # Parse structured insights from response
        insights = _parse_structured_insights(response.content)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "focus_area": focus_area,
            "analysis_period": {
                "days_back": days_back,
                "start_date": (datetime.now() - timedelta(days=days_back)).isoformat(),
                "end_date": datetime.now().isoformat()
            },
            "insights": insights,
            "raw_analysis": response.content,
            "data_summary": _summarize_kpi_data(kpi_data),
            "language": language
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_insights": _generate_fallback_insights(focus_area, language)
        }


@function("document_analysis")
def document_analysis(
    document_content: Input[str],
    document_type: Input[str] = "general",  # invoice, manifest, report, safety_doc
    extract_entities: Input[bool] = True
) -> Output[Dict[str, Any]]:
    """
    Analyze uploaded documents and extract relevant logistics information
    
    Replaces: Pipedream file processing with Foundry AI
    """
    
    # Initialize LLM for document analysis
    llm = LLMProvider("gpt-4o")
    
    # Get document-specific analysis prompt
    analysis_prompt = _get_document_analysis_prompt(document_type, document_content)
    
    try:
        chat_completion = ChatCompletion(
            model=llm,
            messages=[
                {"role": "system", "content": "You are an expert document analyst specializing in transportation and logistics documents."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=1200
        )
        
        response = chat_completion.generate()
        
        # Extract structured information
        extracted_info = _extract_document_entities(response.content, document_type)
        
        # Store processed document for future reference
        document_id = _store_processed_document(document_content, extracted_info)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "document_id": document_id,
            "document_type": document_type,
            "analysis": response.content,
            "extracted_entities": extracted_info,
            "processing_metadata": {
                "content_length": len(document_content),
                "processing_time_ms": response.processing_time_ms,
                "confidence_score": 0.8
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "document_type": document_type,
            "timestamp": datetime.now().isoformat()
        }


# ===== HELPER FUNCTIONS =====

def _build_query_context(question: str, max_length: int) -> str:
    """Build relevant context for natural language queries"""
    
    # Use semantic analysis to find relevant datasets
    semantic_results = semantic_analysis(question, include_relationships=False, max_results=10)
    
    context_parts = []
    current_length = 0
    
    # Add relevant dataset information
    for dataset in semantic_results["results"]["relevant_datasets"]:
        if current_length >= max_length:
            break
            
        dataset_context = f"Dataset: {dataset['dataset']}\nDescription: {dataset['description']}\nKey Columns: {', '.join(dataset['key_columns'])}\n\n"
        
        if current_length + len(dataset_context) <= max_length:
            context_parts.append(dataset_context)
            current_length += len(dataset_context)
    
    # Add recent KPI summary for additional context
    if current_length < max_length * 0.7:  # Reserve space for KPI summary
        try:
            from .kpi_functions import get_comprehensive_dashboard_data
            dashboard_data = get_comprehensive_dashboard_data(7, False, "EN")  # Last 7 days
            
            kpi_summary = f"Recent Performance Summary (Last 7 days):\n"
            kpi_summary += f"- Total Deliveries: {dashboard_data['summary']['total_deliveries']}\n"
            kpi_summary += f"- On-Time Rate: {dashboard_data['summary']['on_time_rate']}%\n"
            kpi_summary += f"- Active Drivers: {dashboard_data['summary']['active_drivers']}\n"
            kpi_summary += f"- Fleet Utilization: {dashboard_data['summary']['fleet_utilization']}%\n\n"
            
            if current_length + len(kpi_summary) <= max_length:
                context_parts.append(kpi_summary)
        except:
            pass  # Skip if KPI data unavailable
    
    return "".join(context_parts)


def _get_logistics_system_prompt(language: str) -> str:
    """Get system prompt for logistics domain expertise"""
    
    if language == "ES":
        return """
        Eres un experto analista de logística y transporte con amplio conocimiento en:
        - Gestión de flotas y optimización de rutas
        - Métricas de rendimiento de entrega y puntualidad
        - Seguridad del conductor y cumplimiento normativo
        - Análisis de eficiencia de combustible y costos operativos
        - Mantenimiento de vehículos y gestión de activos
        
        Proporciona respuestas precisas, procesables y basadas en datos. Usa la información de contexto cuando esté disponible.
        """
    else:
        return """
        You are an expert logistics and transportation analyst with comprehensive knowledge of:
        - Fleet management and route optimization
        - Delivery performance metrics and on-time rates
        - Driver safety and regulatory compliance
        - Fuel efficiency and operational cost analysis
        - Vehicle maintenance and asset management
        
        Provide accurate, actionable, and data-driven responses. Use the context information when available.
        """


def _extract_insights_from_response(response_content: str) -> List[Dict[str, Any]]:
    """Extract structured insights from AI response"""
    
    insights = []
    
    # Look for numbered points or bullet points
    patterns = [
        r'\d+\.\s*(.+?)(?=\d+\.|$)',  # Numbered lists
        r'[-•]\s*(.+?)(?=[-•]|$)',    # Bullet points
        r'Key insight:\s*(.+?)(?=Key insight:|$)',  # Explicit insights
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response_content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            if len(match.strip()) > 20:  # Filter out short fragments
                insights.append({
                    "insight": match.strip(),
                    "confidence": 0.8,
                    "category": "analysis"
                })
        
        if insights:  # Use first successful pattern
            break
    
    return insights[:5]  # Limit to top 5 insights


def _generate_suggested_actions(question: str, insights: List[Dict]) -> List[str]:
    """Generate actionable suggestions based on question and insights"""
    
    suggestions = []
    
    # Question-based suggestions
    if "performance" in question.lower():
        suggestions.append("Review on-time delivery metrics for last 30 days")
        suggestions.append("Analyze route optimization opportunities")
    
    if "driver" in question.lower():
        suggestions.append("Check driver safety scores and training needs")
        suggestions.append("Review driver performance rankings")
    
    if "fuel" in question.lower() or "efficiency" in question.lower():
        suggestions.append("Examine fuel consumption patterns by route")
        suggestions.append("Identify vehicles with poor fuel efficiency")
    
    # Insight-based suggestions
    for insight in insights:
        if "improve" in insight["insight"].lower():
            suggestions.append("Implement improvement plan based on identified opportunities")
        if "risk" in insight["insight"].lower():
            suggestions.append("Address identified risk factors immediately")
    
    return suggestions[:3]  # Limit to top 3 suggestions


def _identify_data_sources_used(context: str) -> List[str]:
    """Identify which data sources were referenced in the context"""
    
    sources = []
    
    # Extract dataset names from context
    dataset_pattern = r'Dataset:\s*([^\n]+)'
    matches = re.findall(dataset_pattern, context)
    
    for match in matches:
        sources.append(match.strip())
    
    return sources


def _generate_fallback_response(question: str, language: str) -> str:
    """Generate fallback response when AI processing fails"""
    
    if language == "ES":
        return f"Lo siento, no pude procesar completamente tu pregunta: '{question}'. Por favor, intenta reformular tu consulta o contacta al soporte técnico."
    else:
        return f"I apologize, but I couldn't fully process your question: '{question}'. Please try rephrasing your query or contact technical support."


def _identify_join_opportunities(relevant_datasets: List[Dict]) -> List[Dict[str, Any]]:
    """Identify potential join opportunities between datasets"""
    
    # This is a simplified implementation
    # In production, would use more sophisticated schema analysis
    
    join_opportunities = []
    
    common_join_fields = [
        "driver_id", "vehicle_id", "delivery_id", "route_id", 
        "customer_id", "order_number", "move_number"
    ]
    
    for i, dataset1 in enumerate(relevant_datasets):
        for j, dataset2 in enumerate(relevant_datasets[i+1:], i+1):
            # Check for common column names
            common_columns = set(dataset1.get("key_columns", [])) & set(dataset2.get("key_columns", []))
            join_columns = common_columns & set(common_join_fields)
            
            if join_columns:
                join_opportunities.append({
                    "dataset1": dataset1["dataset"],
                    "dataset2": dataset2["dataset"],
                    "join_columns": list(join_columns),
                    "join_type": "INNER",  # Default assumption
                    "confidence": 0.7
                })
    
    return join_opportunities


def _extract_business_concepts(query: str) -> List[str]:
    """Extract business concepts from user query"""
    
    business_terms = {
        "delivery": ["delivery", "shipment", "package", "freight"],
        "performance": ["performance", "efficiency", "productivity", "metrics"],
        "safety": ["safety", "accident", "incident", "compliance", "violation"],
        "route": ["route", "path", "journey", "trip", "optimization"],
        "driver": ["driver", "operator", "personnel", "staff"],
        "vehicle": ["vehicle", "truck", "tractor", "trailer", "fleet"],
        "customer": ["customer", "client", "shipper", "consignee"],
        "financial": ["cost", "revenue", "profit", "expense", "budget"]
    }
    
    concepts = []
    query_lower = query.lower()
    
    for concept, terms in business_terms.items():
        if any(term in query_lower for term in terms):
            concepts.append(concept)
    
    return concepts


# Additional helper functions would continue here...
# (Truncating for brevity, but full implementation would include all referenced helper functions)

# ===== FUNCTION REGISTRATION =====

FUNCTIONS = [
    schema_discovery,
    semantic_analysis,
    natural_language_query,
    generate_business_insights,
    document_analysis
]
