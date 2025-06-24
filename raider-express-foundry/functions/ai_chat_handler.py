from foundry_functions_api import function
import openai
import json
from datetime import datetime

@function()
def handle_raiderbot_chat(
    user_message: str,
    user_context: dict,
    conversation_history: list = None,
    uploaded_documents: list = None
) -> dict:
    """
    RaiderBot AI Chat Handler - German Shepherd themed assistant for Raider Express
    Supports English and Spanish, focuses on safety and operational efficiency
    """
    
    # RaiderBot system prompt
    system_prompt = """
    You are RaiderBot, an AI assistant for Raider Express, a refrigerated trucking company based in Fort Worth, Texas. 
    You embody the spirit of a loyal German Shepherd - intelligent, reliable, and always safety-focused.

    Key Guidelines:
    - Always prioritize safety (our trucks are governed at 60mph - no "speeding" suggestions)
    - Support both English and Spanish languages naturally
    - Focus on practical, actionable insights for transportation operations
    - Maintain a friendly but professional tone
    - Reference Fort Worth/Texas context when relevant
    - Emphasize our refrigerated trucking specialization
    - Learn from every interaction to help the entire team

    You have access to:
    - Real-time delivery data
    - Driver performance metrics  
    - Vehicle telematics and safety data
    - Route optimization capabilities
    - Customer satisfaction data
    - Weather and traffic information

    When users ask questions, provide specific, data-driven answers with actionable recommendations.
    """
    
    def detect_language(text):
        """Simple language detection"""
        spanish_indicators = ['cómo', 'qué', 'dónde', 'cuándo', 'por favor', 'gracias', 'hola', 'mostrar', 'rendimiento']
        return 'spanish' if any(word in text.lower() for word in spanish_indicators) else 'english'
    
    def get_contextual_data(user_context):
        """Fetch relevant data based on user context"""
        # This would typically make calls to your Foundry datasets
        # For now, return mock structure
        return {
            "current_deliveries": 45,
            "active_drivers": 23, 
            "on_time_rate": 92.5,
            "safety_violations_today": 0,
            "fuel_efficiency": 6.2,
            "user_department": user_context.get('department', 'general')
        }
    
    def generate_department_specific_context(department, contextual_data):
        """Add department-specific context to the conversation"""
        contexts = {
            "dispatch": f"Current active deliveries: {contextual_data['current_deliveries']}, Available drivers: {contextual_data['active_drivers']}",
            "safety": f"Today's safety status: {contextual_data['safety_violations_today']} violations, Fleet compliance: 100%",
            "fleet": f"Fleet fuel efficiency: {contextual_data['fuel_efficiency']} MPG, Maintenance alerts: Check system",
            "management": f"Operations summary - On-time rate: {contextual_data['on_time_rate']}%, Performance trending positive"
        }
        return contexts.get(department, "General operations data available")
    
    # Process the request
    detected_language = detect_language(user_message)
    contextual_data = get_contextual_data(user_context)
    dept_context = generate_department_specific_context(
        user_context.get('department', 'general'), 
        contextual_data
    )
    
    # Build conversation context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Current context: {dept_context}"},
        {"role": "system", "content": f"User language preference: {detected_language}"}
    ]
    
    # Add conversation history
    if conversation_history:
        messages.extend(conversation_history[-10:])  # Last 10 messages for context
    
    # Add current message
    messages.append({"role": "user", "content": user_message})
    
    # Process uploaded documents if any
    document_context = ""
    if uploaded_documents:
        document_context = process_uploaded_documents(uploaded_documents)
        messages.append({"role": "system", "content": f"Document context: {document_context}"})
    
    try:
        # Generate response using OpenAI (or your preferred LLM)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        ai_response = response.choices[0].message.content
        
        # Generate follow-up suggestions
        suggestions = generate_follow_up_suggestions(user_message, user_context, detected_language)
        
        # Log interaction for learning
        log_interaction(user_message, ai_response, user_context)
        
        return {
            "response": ai_response,
            "language_detected": detected_language,
            "follow_up_suggestions": suggestions,
            "contextual_data_used": contextual_data,
            "document_processed": bool(uploaded_documents),
            "timestamp": datetime.now().isoformat(),
            "conversation_id": user_context.get('conversation_id', 'new')
        }
        
    except Exception as e:
        error_response = {
            "english": "I'm having trouble processing your request right now. Please try again or contact IT support.",
            "spanish": "Tengo problemas para procesar tu solicitud ahora. Por favor intenta de nuevo o contacta soporte técnico."
        }
        
        return {
            "response": error_response[detected_language],
            "error": str(e),
            "language_detected": detected_language,
            "timestamp": datetime.now().isoformat()
        }

def process_uploaded_documents(uploaded_documents):
    """Process various document types uploaded to chat"""
    processed_content = []
    
    for doc in uploaded_documents:
        doc_type = doc.get('type', '').lower()
        doc_content = doc.get('content', '')
        
        if doc_type in ['pdf', 'txt', 'docx']:
            # Text document processing
            processed_content.append(f"Document content: {doc_content[:500]}...")
            
        elif doc_type in ['jpg', 'png', 'jpeg']:
            # Image processing (would use OCR/image analysis)
            processed_content.append("Image analyzed - extracting text and visual information")
            
        elif doc_type in ['mp3', 'wav', 'mp4']:
            # Audio/video processing (would use speech-to-text)
            processed_content.append("Audio/video processed - transcript available")
    
    return "; ".join(processed_content)

def generate_follow_up_suggestions(user_message, user_context, language):
    """Generate contextual follow-up suggestions"""
    
    suggestions_en = [
        "Show me today's delivery performance",
        "Which routes are running behind schedule?", 
        "How are our drivers performing this week?",
        "What's our fuel efficiency looking like?",
        "Any safety alerts I should know about?"
    ]
    
    suggestions_es = [
        "Muéstrame el rendimiento de entregas de hoy",
        "¿Qué rutas están retrasadas?",
        "¿Cómo están nuestros conductores esta semana?",
        "¿Cómo está nuestra eficiencia de combustible?",
        "¿Hay alertas de seguridad que deba saber?"
    ]
    
    # Department-specific suggestions
    dept = user_context.get('department', 'general')
    if dept == 'dispatch':
        suggestions_en.extend([
            "Optimize routes for tomorrow",
            "Show driver availability"
        ])
        suggestions_es.extend([
            "Optimizar rutas para mañana", 
            "Mostrar disponibilidad de conductores"
        ])
    
    return suggestions_es if language == 'spanish' else suggestions_en

def log_interaction(user_message, ai_response, user_context):
    """Log interaction for continuous learning"""
    interaction_log = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "ai_response": ai_response,
        "user_department": user_context.get('department'),
        "user_id": user_context.get('user_id'),
        "response_length": len(ai_response),
        "language": detect_language(user_message)
    }
    
    # This would typically write to a Foundry dataset for learning
    # For now, just return the log structure
    return interaction_log

def detect_language(text):
    """Simple language detection helper function"""
    spanish_indicators = ['cómo', 'qué', 'dónde', 'cuándo', 'por favor', 'gracias', 'hola', 'mostrar', 'rendimiento']
    return 'spanish' if any(word in text.lower() for word in spanish_indicators) else 'english'