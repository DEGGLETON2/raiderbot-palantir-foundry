"""
RaiderBot Chat Interface Workshop Application
Replaces React-based chat interface with Foundry Workshop

Based on src.legacy/components/Chat/ChatInterface.jsx and useChatMessages.js
"""

from foundry_workshop import App, Page, Component
from foundry_workshop.components import (
    Card, Container, Row, Column, Text, Input, Button, ScrollView,
    Alert, Badge, Divider, FileUpload, Select, ProgressBar
)
from foundry_workshop.layouts import VStack, HStack, Spacer
from foundry_workshop.styling import Theme, Color, Spacing, Typography
from foundry_functions import FunctionCall
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import uuid


class RaiderBotChatApp(App):
    """AI-Powered Chat Interface for RaiderBot Analytics"""
    
    def __init__(self):
        super().__init__(
            name="RaiderBot AI Chat",
            description="Natural language interface for logistics analytics and insights",
            version="1.0.0"
        )
        
        # Initialize state
        self.state = {
            "messages": [],
            "current_input": "",
            "is_typing": False,
            "language": "EN",
            "conversation_id": str(uuid.uuid4()),
            "file_upload_enabled": True,
            "quick_suggestions": [
                "Show me today's delivery performance",
                "How are our drivers performing?", 
                "Optimize routes for maximum efficiency",
                "Customer satisfaction insights",
                "Mostrar el rendimiento de entregas de hoy",
                "¿Cómo están funcionando nuestros conductores?",
                "Optimizar rutas para máxima eficiencia",
                "Insights de satisfacción del cliente"
            ]
        }
        
        # Set up theme
        self.theme = Theme(
            primary_color=Color.RED,
            secondary_color=Color.BLUE,
            accent_color=Color.GREEN,
            background_color=Color.WHITE,
            text_color=Color.BLACK
        )
        
        # Initialize with welcome message
        self._add_welcome_message()
    
    def create_layout(self):
        """Create main chat interface layout"""
        
        return Container([
            # Header Section
            self._create_chat_header(),
            
            # Messages Area
            self._create_messages_area(),
            
            # Input Area
            self._create_input_area(),
            
            # Quick Suggestions
            self._create_quick_suggestions()
        ], 
        style={
            "height": "100vh",
            "display": "flex",
            "flex_direction": "column"
        })
    
    def _create_chat_header(self):
        """Create chat header with controls"""
        
        return Card([
            HStack([
                # RaiderBot Icon and Title
                VStack([
                    Text("🤖 RaiderBot AI", style=Typography.H3, color=self.theme.primary_color),
                    Text(
                        "Your AI transportation analytics assistant" if self.state["language"] == "EN" 
                        else "Tu asistente de IA para análisis de transporte",
                        style=Typography.CAPTION,
                        color=Color.GRAY
                    )
                ], spacing=Spacing.SMALL),
                
                Spacer(),
                
                # Language Toggle
                Select(
                    options=[
                        {"value": "EN", "label": "English"},
                        {"value": "ES", "label": "Español"}
                    ],
                    value=self.state["language"],
                    on_change=self._on_language_change,
                    width=120
                ),
                
                # Clear Chat Button
                Button(
                    "Clear Chat" if self.state["language"] == "EN" else "Limpiar Chat",
                    on_click=self._clear_chat,
                    variant="outline",
                    size="small",
                    icon="trash"
                )
            ], spacing=Spacing.MEDIUM)
        ], padding=Spacing.MEDIUM)
    
    def _create_messages_area(self):
        """Create scrollable messages area"""
        
        messages_components = []
        
        # Render each message
        for message in self.state["messages"]:
            messages_components.append(self._create_message_component(message))
        
        # Add typing indicator if bot is typing
        if self.state["is_typing"]:
            messages_components.append(self._create_typing_indicator())
        
        return Card([
            ScrollView(
                VStack(messages_components, spacing=Spacing.MEDIUM),
                height=400,
                auto_scroll_to_bottom=True
            )
        ], 
        padding=Spacing.MEDIUM,
        style={"flex": "1", "overflow": "hidden"})
    
    def _create_message_component(self, message: Dict[str, Any]):
        """Create individual message component"""
        
        is_user = message["sender"] == "user"
        
        # Message bubble
        message_bubble = Card([
            Text(message["text"], style=Typography.BODY, wrap=True),
            Text(
                message["timestamp"],
                style=Typography.CAPTION,
                color=Color.WHITE if is_user else Color.GRAY
            )
        ],
        background_color=self.theme.primary_color if is_user else Color.LIGHT_GRAY,
        text_color=Color.WHITE if is_user else Color.BLACK,
        padding=Spacing.SMALL,
        border_radius=12,
        max_width=400)
        
        # Add file attachment if present
        if message.get("file_attachment"):
            attachment_component = self._create_file_attachment_component(message["file_attachment"])
            message_content = VStack([message_bubble, attachment_component], spacing=Spacing.SMALL)
        else:
            message_content = message_bubble
        
        # Add insights/actions if present (for bot messages)
        if not is_user and message.get("insights"):
            insights_component = self._create_insights_component(message["insights"])
            message_content = VStack([message_content, insights_component], spacing=Spacing.SMALL)
        
        # Align message based on sender
        if is_user:
            return HStack([Spacer(), message_content])
        else:
            return HStack([message_content, Spacer()])
    
    def _create_typing_indicator(self):
        """Create typing indicator component"""
        
        return HStack([
            Card([
                HStack([
                    ProgressBar(indeterminate=True, width=60),
                    Text(
                        "RaiderBot is typing..." if self.state["language"] == "EN" 
                        else "RaiderBot está escribiendo...",
                        style=Typography.CAPTION,
                        color=Color.GRAY
                    )
                ], spacing=Spacing.SMALL)
            ], 
            background_color=Color.LIGHT_GRAY,
            padding=Spacing.SMALL,
            border_radius=12),
            Spacer()
        ])
    
    def _create_input_area(self):
        """Create message input area"""
        
        return Card([
            VStack([
                # File Upload (if enabled)
                self._create_file_upload_section() if self.state["file_upload_enabled"] else None,
                
                # Message Input
                HStack([
                    Input(
                        placeholder=(
                            "Ask RaiderBot about deliveries, routes, drivers, or performance..." 
                            if self.state["language"] == "EN"
                            else "Pregunta a RaiderBot sobre entregas, rutas, conductores o rendimiento..."
                        ),
                        value=self.state["current_input"],
                        on_change=self._on_input_change,
                        on_key_press=self._on_key_press,
                        multiline=True,
                        max_rows=3,
                        style={"flex": "1"}
                    ),
                    
                    Button(
                        icon="send",
                        on_click=self._send_message,
                        disabled=not self.state["current_input"].strip(),
                        variant="primary",
                        size="large"
                    )
                ], spacing=Spacing.MEDIUM)
            ], spacing=Spacing.SMALL)
        ], padding=Spacing.MEDIUM)
    
    def _create_file_upload_section(self):
        """Create file upload section"""
        
        return HStack([
            FileUpload(
                accept=[".pdf", ".doc", ".docx", ".txt", ".csv", ".xlsx"],
                on_upload=self._on_file_upload,
                max_size_mb=10,
                placeholder="Upload document for analysis" if self.state["language"] == "EN" 
                           else "Subir documento para análisis"
            ),
            Text(
                "Supported: PDF, DOC, TXT, CSV, XLSX" if self.state["language"] == "EN"
                else "Soportados: PDF, DOC, TXT, CSV, XLSX",
                style=Typography.CAPTION,
                color=Color.GRAY
            )
        ], spacing=Spacing.SMALL)
    
    def _create_quick_suggestions(self):
        """Create quick suggestion buttons"""
        
        # Filter suggestions by language
        suggestions = [
            s for s in self.state["quick_suggestions"] 
            if (self.state["language"] == "EN" and not any(spanish_word in s.lower() for spanish_word in ["mostrar", "cómo", "optimizar", "insights", "satisfacción", "conductores", "entregas", "rutas", "eficiencia", "máxima"]))
            or (self.state["language"] == "ES" and any(spanish_word in s.lower() for spanish_word in ["mostrar", "cómo", "optimizar", "insights", "satisfacción", "conductores", "entregas", "rutas", "eficiencia", "máxima"]))
        ]
        
        suggestion_buttons = [
            Button(
                suggestion,
                on_click=lambda s=suggestion: self._send_quick_suggestion(s),
                variant="outline",
                size="small",
                style={"margin": "2px"}
            )
            for suggestion in suggestions[:4]  # Show only first 4
        ]
        
        return Card([
            VStack([
                Text(
                    "Quick suggestions:" if self.state["language"] == "EN" else "Sugerencias rápidas:",
                    style=Typography.CAPTION,
                    color=Color.GRAY
                ),
                HStack(suggestion_buttons, spacing=Spacing.SMALL, wrap=True)
            ], spacing=Spacing.SMALL)
        ], padding=Spacing.MEDIUM)
    
    def _create_file_attachment_component(self, file_info: Dict[str, Any]):
        """Create file attachment display component"""
        
        return Card([
            HStack([
                Text("📎", style=Typography.H4),
                VStack([
                    Text(file_info["name"], style=Typography.BODY_BOLD),
                    Text(f"{file_info['size']} bytes", style=Typography.CAPTION, color=Color.GRAY)
                ], spacing=Spacing.TINY)
            ], spacing=Spacing.SMALL)
        ], 
        background_color=Color.LIGHT_BLUE,
        padding=Spacing.SMALL,
        border_radius=8)
    
    def _create_insights_component(self, insights: List[Dict[str, Any]]):
        """Create insights/actions component for bot responses"""
        
        insights_components = []
        
        for insight in insights[:3]:  # Show max 3 insights
            insights_components.append(
                Card([
                    Text(insight["insight"], style=Typography.BODY_SMALL),
                    Badge(
                        f"Confidence: {insight['confidence']:.0%}",
                        color=Color.GREEN if insight["confidence"] > 0.8 else Color.ORANGE
                    )
                ], 
                background_color=Color.LIGHT_GREEN,
                padding=Spacing.SMALL,
                border_radius=6)
            )
        
        return VStack([
            Text(
                "💡 Insights:" if self.state["language"] == "EN" else "💡 Insights:",
                style=Typography.CAPTION,
                color=Color.GRAY
            ),
            VStack(insights_components, spacing=Spacing.SMALL)
        ], spacing=Spacing.SMALL)
    
    # ===== EVENT HANDLERS =====
    
    def _on_input_change(self, new_value: str):
        """Handle input text change"""
        self.state["current_input"] = new_value
    
    def _on_key_press(self, event):
        """Handle key press in input field"""
        if event.key == "Enter" and not event.shift_key:
            event.prevent_default()
            self._send_message()
    
    def _on_language_change(self, new_language: str):
        """Handle language change"""
        self.state["language"] = new_language
        self._add_system_message(
            "Language changed to English" if new_language == "EN" else "Idioma cambiado a Español"
        )
        self.refresh()
    
    def _on_file_upload(self, file_info: Dict[str, Any]):
        """Handle file upload"""
        
        # Add file message
        file_message = {
            "id": str(uuid.uuid4()),
            "text": f"Uploaded file: {file_info['name']}" if self.state["language"] == "EN" 
                   else f"Archivo subido: {file_info['name']}",
            "sender": "user",
            "timestamp": datetime.now().strftime("%H:%M"),
            "file_attachment": file_info
        }
        
        self.state["messages"].append(file_message)
        
        # Process file with AI
        self._process_uploaded_file(file_info)
        self.refresh()
    
    def _send_message(self):
        """Send user message and get AI response"""
        
        if not self.state["current_input"].strip():
            return
        
        user_message = {
            "id": str(uuid.uuid4()),
            "text": self.state["current_input"].strip(),
            "sender": "user",
            "timestamp": datetime.now().strftime("%H:%M")
        }
        
        self.state["messages"].append(user_message)
        self.state["current_input"] = ""
        self.state["is_typing"] = True
        
        # Get AI response
        self._get_ai_response(user_message["text"])
        self.refresh()
    
    def _send_quick_suggestion(self, suggestion: str):
        """Send quick suggestion as message"""
        self.state["current_input"] = suggestion
        self._send_message()
    
    def _clear_chat(self):
        """Clear all messages"""
        self.state["messages"] = []
        self.state["conversation_id"] = str(uuid.uuid4())
        self._add_welcome_message()
        self.refresh()
    
    # ===== AI INTEGRATION =====
    
    def _get_ai_response(self, user_message: str):
        """Get AI response using Foundry Functions"""
        
        try:
            # Call natural language query function
            function_call = FunctionCall("natural_language_query")
            result = function_call.execute(
                user_question=user_message,
                language=self.state["language"],
                include_context=True,
                max_context_length=4000
            )
            
            if result["success"]:
                bot_message = {
                    "id": str(uuid.uuid4()),
                    "text": result["response"]["answer"],
                    "sender": "bot",
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "insights": result["response"].get("insights", []),
                    "suggested_actions": result["response"].get("suggested_actions", []),
                    "confidence": result["response"].get("confidence_score", 0.0)
                }
            else:
                bot_message = {
                    "id": str(uuid.uuid4()),
                    "text": result.get("fallback_response", self._get_fallback_response()),
                    "sender": "bot",
                    "timestamp": datetime.now().strftime("%H:%M")
                }
            
        except Exception as e:
            print(f"Error getting AI response: {e}")
            bot_message = {
                "id": str(uuid.uuid4()),
                "text": self._get_fallback_response(),
                "sender": "bot",
                "timestamp": datetime.now().strftime("%H:%M")
            }
        
        finally:
            self.state["is_typing"] = False
            self.state["messages"].append(bot_message)
            self.refresh()
    
    def _process_uploaded_file(self, file_info: Dict[str, Any]):
        """Process uploaded file with AI"""
        
        try:
            # Extract text content from file (simplified)
            file_content = file_info.get("content", "")
            
            # Call document analysis function
            function_call = FunctionCall("document_analysis")
            result = function_call.execute(
                document_content=file_content,
                document_type=self._detect_document_type(file_info["name"]),
                extract_entities=True
            )
            
            if result["success"]:
                analysis_message = {
                    "id": str(uuid.uuid4()),
                    "text": result["analysis"],
                    "sender": "bot",
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "insights": [{"insight": entity, "confidence": 0.8} for entity in result.get("extracted_entities", {}).values()]
                }
            else:
                analysis_message = {
                    "id": str(uuid.uuid4()),
                    "text": "File uploaded successfully but analysis failed. Please try again." if self.state["language"] == "EN"
                           else "Archivo subido exitosamente pero falló el análisis. Por favor intenta de nuevo.",
                    "sender": "bot", 
                    "timestamp": datetime.now().strftime("%H:%M")
                }
            
            self.state["messages"].append(analysis_message)
            
        except Exception as e:
            print(f"Error processing file: {e}")
    
    # ===== HELPER METHODS =====
    
    def _add_welcome_message(self):
        """Add welcome message to chat"""
        
        welcome_text = """
        👋 Welcome to RaiderBot AI! I'm here to help you with:
        
        📊 **Analytics & KPIs** - Delivery performance, driver metrics, fleet efficiency
        🚛 **Operations** - Route optimization, vehicle maintenance, safety insights  
        🤖 **AI Insights** - Business intelligence and predictive analytics
        📄 **Document Analysis** - Upload files for automated processing
        
        Ask me anything about your logistics operations!
        """ if self.state["language"] == "EN" else """
        👋 ¡Bienvenido a RaiderBot AI! Estoy aquí para ayudarte con:
        
        📊 **Análisis y KPIs** - Rendimiento de entregas, métricas de conductores, eficiencia de flota
        🚛 **Operaciones** - Optimización de rutas, mantenimiento de vehículos, insights de seguridad
        🤖 **AI Insights** - Inteligencia de negocio y análisis predictivo
        📄 **Análisis de Documentos** - Sube archivos para procesamiento automatizado
        
        ¡Pregúntame cualquier cosa sobre tus operaciones logísticas!
        """
        
        welcome_message = {
            "id": str(uuid.uuid4()),
            "text": welcome_text.strip(),
            "sender": "bot",
            "timestamp": datetime.now().strftime("%H:%M")
        }
        
        self.state["messages"].append(welcome_message)
    
    def _add_system_message(self, message: str):
        """Add system message to chat"""
        
        system_message = {
            "id": str(uuid.uuid4()),
            "text": message,
            "sender": "system",
            "timestamp": datetime.now().strftime("%H:%M")
        }
        
        self.state["messages"].append(system_message)
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when AI fails"""
        
        if self.state["language"] == "EN":
            return "I apologize, but I'm having trouble processing your request right now. Please try rephrasing your question or contact support if the issue persists."
        else:
            return "Me disculpo, pero tengo problemas para procesar tu solicitud en este momento. Por favor intenta reformular tu pregunta o contacta soporte si el problema persiste."
    
    def _detect_document_type(self, filename: str) -> str:
        """Detect document type from filename"""
        
        filename_lower = filename.lower()
        
        if any(word in filename_lower for word in ["invoice", "bill", "factura"]):
            return "invoice"
        elif any(word in filename_lower for word in ["manifest", "shipment", "manifiesto"]):
            return "manifest"  
        elif any(word in filename_lower for word in ["report", "reporte", "analysis", "analisis"]):
            return "report"
        elif any(word in filename_lower for word in ["safety", "incident", "seguridad", "incidente"]):
            return "safety_doc"
        else:
            return "general"


# ===== APP REGISTRATION =====

def create_raiderbot_chat():
    """Create and configure the RaiderBot chat app"""
    
    app = RaiderBotChatApp()
    
    # Configure app settings
    app.set_permissions(["chat_with_ai", "upload_documents", "view_logistics_data"])
    app.set_responsive(True)
    app.set_real_time_updates(True)
    
    return app


# Export the app
RAIDERBOT_CHAT_APP = create_raiderbot_chat()
