"""
RaiderBot Core Function - German Shepherd AI Assistant
Built on Palantir Foundry for Raider Express Transportation
"""

from foundry_functions_api import function
import openai
from typing import Dict, Any, List
from datetime import datetime
import os

@function()
def handle_raiderbot_chat(
    message: str,
    language: str = "en",
    user_context: Dict[str, Any] = None,
    conversation_history: List[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    RaiderBot's main chat handling function in Palantir Foundry.
    Implements German Shepherd personality with safety-first focus.
    """
    
    # System prompt defining RaiderBot's personality
    system_prompt = """
    You are RaiderBot, an AI assistant for Raider Express trucking, embodying a German Shepherd's traits:
    - Use 🐕 emoji and occasional "Woof!" in responses
    - Always emphasize safety (60mph speed limit is non-negotiable)
    - Support both English and Spanish naturally
    - Focus on practical transportation insights
    - Show loyalty and dedication to the Raider Express team
    """
    
    # Initialize conversation
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history if available
    if conversation_history:
        messages.extend(conversation_history[-5:])  # Last 5 messages for context
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    try:
        # Get operational context from Foundry datasets
        context = get_operational_context()
        messages.append({
            "role": "system",
            "content": f"Current operations status: {context}"
        })
        
        # Generate response using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Log interaction in Foundry
        log_interaction(message, response.choices[0].message.content, user_context)
        
        return {
            "response": response.choices[0].message.content,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "operational_context": context,
            "success": True
        }
        
    except Exception as e:
        error_message = {
            "en": "🐕 Woof! I'm having trouble accessing my systems. Please try again shortly.",
            "es": "🐕 ¡Guau! Tengo problemas accediendo a mis sistemas. Por favor intenta de nuevo pronto."
        }
        
        return {
            "response": error_message[language],
            "error": str(e),
            "success": False
        }

def get_operational_context() -> Dict[str, Any]:
    """
    Get real-time operational data from Foundry datasets
    """
    from foundry_dev_tools import FoundryRestClient
    
    client = FoundryRestClient()
    
    # Access Foundry datasets
    deliveries = client.datasets.get("raider_deliveries")
    drivers = client.datasets.get("raider_drivers")
    kpis = client.datasets.get("raider_kpi_dashboard")
    
    return {
        "total_deliveries": deliveries.count(),
        "active_drivers": drivers.filter("status = 'active'").count(),
        "on_time_rate": kpis.get_metric("on_time_percentage"),
        "safety_score": kpis.get_metric("fleet_safety_score"),
        "max_speed": "60mph"  # Safety-first: Always enforce speed limit
    }

def log_interaction(
    user_message: str,
    bot_response: str,
    user_context: Dict[str, Any]
) -> None:
    """
    Log chat interactions to Foundry for analysis
    """
    from foundry_dev_tools import FoundryRestClient
    
    client = FoundryRestClient()
    chat_logs = client.datasets.get("raiderbot_chat_logs")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "bot_response": bot_response,
        "user_id": user_context.get("user_id", "anonymous"),
        "user_role": user_context.get("role", "guest"),
        "language": user_context.get("language", "en")
    }
    
    chat_logs.append(log_entry)

# Foundry function configuration
config = {
    "name": "raiderbot_chat",
    "description": "German Shepherd AI Assistant for Raider Express",
    "version": "1.0.0",
    "memory": 4096,
    "timeout": 300,
    "environment": {
        "OPENAI_API_KEY": "${FOUNDRY_SECRET:openai_api_key}",
        "MAX_SPEED_LIMIT": "60",
        "LANGUAGE_SUPPORT": "en,es"
    }
} 