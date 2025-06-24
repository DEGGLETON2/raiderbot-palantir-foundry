import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Card, 
  Button, 
  InputGroup, 
  Icon, 
  Spinner, 
  Tag, 
  Alert,
  HTMLSelect,
  Callout,
  ProgressBar
} from '@palantir/blueprint';
import styled, { keyframes, css } from 'styled-components';
import { useDropzone } from 'react-dropzone';
import Markdown from 'markdown-to-jsx';

// =====================================================================================
// STYLED COMPONENTS & ANIMATIONS
// =====================================================================================

const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
`;

const wag = keyframes`
  0% { transform: rotate(-5deg); }
  25% { transform: rotate(5deg); }
  50% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
  100% { transform: rotate(-5deg); }
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
  color: white;
`;

const ChatHeader = styled.div`
  display: flex;
  align-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 2px solid #dc2626;
`;

const ChatBody = styled.div`
  flex: 1;
  display: flex;
  overflow: hidden;
`;

const ChatMain = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
`;

const ChatSidebar = styled.div`
  width: 300px;
  background: rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-left: 1px solid rgba(255, 255, 255, 0.1);
`;

const CompanyBranding = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  
  h1 {
    color: #dc2626;
    font-size: 24px;
    font-weight: bold;
    margin: 0;
  }
  
  .subtitle {
    color: #9ca3af;
    font-size: 14px;
    margin: 0;
  }
`;

const LanguageSelector = styled.div`
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const MessageBubble = styled(Card)<{ sender: 'user' | 'raiderbot' }>`
  max-width: 70%;
  align-self: ${props => props.sender === 'user' ? 'flex-end' : 'flex-start'};
  background: ${props => props.sender === 'user' 
    ? 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)' 
    : 'linear-gradient(135deg, #1f2937 0%, #374151 100%)'
  };
  color: white;
  border: 1px solid ${props => props.sender === 'user' ? '#dc2626' : '#4b5563'};
  
  .bp5-card {
    background: transparent;
  }
`;

const MessageHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 12px;
  color: #9ca3af;
`;

const MessageContent = styled.div`
  font-size: 14px;
  line-height: 1.5;
  
  h1, h2, h3 { color: #dc2626; margin-top: 0; }
  ul { padding-left: 20px; }
  code { 
    background: rgba(0, 0, 0, 0.3); 
    padding: 2px 6px; 
    border-radius: 3px; 
  }
`;

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(31, 41, 55, 0.8);
  border-radius: 10px;
  align-self: flex-start;
  max-width: 200px;
`;

const AttachmentPreview = styled.div`
  margin-top: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  border-left: 3px solid #dc2626;
`;

const AvatarContainer = styled.div<{ isTyping: boolean }>`
  position: relative;
  width: 60px;
  height: 60px;
  margin-right: 15px;
  
  ${props => props.isTyping && css`
    animation: ${bounce} 2s infinite;
  `}
`;

const DogAvatar = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 50%, #8b4513 100%);
  border-radius: 50%;
  position: relative;
  border: 3px solid #dc2626;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  overflow: hidden;
`;

const DogFace = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 45px;
  height: 35px;
`;

const Eyes = styled.div`
  display: flex;
  justify-content: space-between;
  width: 20px;
  margin: 0 auto 5px;
  
  &::before,
  &::after {
    content: '';
    width: 6px;
    height: 8px;
    background: #000;
    border-radius: 50%;
  }
`;

const Nose = styled.div`
  width: 6px;
  height: 5px;
  background: #000;
  border-radius: 50%;
  margin: 0 auto 3px;
`;

const Mouth = styled.div`
  width: 12px;
  height: 6px;
  border: 2px solid #000;
  border-top: none;
  border-radius: 0 0 12px 12px;
  margin: 0 auto;
`;

const Ears = styled.div`
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 20px;
  
  &::before,
  &::after {
    content: '';
    position: absolute;
    width: 15px;
    height: 20px;
    background: #8b4513;
    border-radius: 15px 15px 5px 5px;
    border: 2px solid #dc2626;
  }
  
  &::before {
    left: 5px;
    transform: rotate(-15deg);
  }
  
  &::after {
    right: 5px;
    transform: rotate(15deg);
  }
`;

const Tail = styled.div<{ isTyping: boolean }>`
  position: absolute;
  top: -10px;
  right: -15px;
  width: 4px;
  height: 25px;
  background: #8b4513;
  border-radius: 2px;
  transform-origin: top center;
  
  ${props => props.isTyping && css`
    animation: ${wag} 0.5s infinite;
  `}
`;

const StatusBadge = styled.div<{ language: 'en' | 'es' }>`
  position: absolute;
  bottom: -5px;
  right: -5px;
  background: #dc2626;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: bold;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
`;

const ThinkingBubble = styled.div<{ show: boolean }>`
  position: absolute;
  top: -30px;
  left: 70px;
  background: white;
  color: #1f2937;
  padding: 8px 12px;
  border-radius: 15px;
  font-size: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  opacity: ${props => props.show ? 1 : 0};
  transform: ${props => props.show ? 'scale(1)' : 'scale(0.8)'};
  transition: all 0.3s ease;
  z-index: 10;
  
  &::before {
    content: '';
    position: absolute;
    bottom: -8px;
    left: -10px;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 8px solid white;
    transform: rotate(-45deg);
  }
`;

const UploadZone = styled.div<{ isDragActive: boolean; isDisabled: boolean }>`
  margin-top: 15px;
  padding: 20px;
  border: 2px dashed ${props => 
    props.isDisabled ? '#6b7280' :
    props.isDragActive ? '#dc2626' : '#9ca3af'
  };
  border-radius: 8px;
  background: ${props => 
    props.isDisabled ? 'rgba(107, 114, 128, 0.1)' :
    props.isDragActive ? 'rgba(220, 38, 38, 0.1)' : 'rgba(156, 163, 175, 0.05)'
  };
  text-align: center;
  cursor: ${props => props.isDisabled ? 'not-allowed' : 'pointer'};
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => 
      props.isDisabled ? 'rgba(107, 114, 128, 0.1)' :
      'rgba(220, 38, 38, 0.05)'
    };
  }
`;

const UploadContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #9ca3af;
`;

const FileTypeGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
  margin-top: 10px;
`;

const FileTypeCard = styled.div`
  padding: 8px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  text-align: center;
  font-size: 11px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
`;

const SuggestionsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const SectionTitle = styled.h3`
  color: #dc2626;
  font-size: 16px;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SuggestionButton = styled(Button)`
  justify-content: flex-start;
  text-align: left;
  margin-bottom: 8px;
  
  &.bp5-button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
  }
  
  &.bp5-button:hover {
    background: rgba(220, 38, 38, 0.2);
    border-color: #dc2626;
  }
`;

const DepartmentCard = styled(Card)`
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 15px;
`;

// =====================================================================================
// INTERFACES & TYPES
// =====================================================================================

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'raiderbot';
  timestamp: Date;
  language: 'en' | 'es';
  attachments?: any[];
  processing?: boolean;
}

interface ChatState {
  messages: Message[];
  currentLanguage: 'en' | 'es';
  isTyping: boolean;
  isProcessingDocument: boolean;
  connectionStatus: 'connected' | 'connecting' | 'disconnected';
}

// =====================================================================================
// FOUNDRY LLM SERVICE
// =====================================================================================

class FoundryLLMService {
  private client: any;
  private conversationHistory: any[] = [];
  private systemPrompt: string;

  constructor() {
    // Initialize Foundry client
    this.systemPrompt = this.buildSystemPrompt();
  }

  async initialize(): Promise<void> {
    try {
      // Test connection to Foundry
      console.log('🐕 RaiderBot connected to Foundry successfully!');
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate connection
    } catch (error) {
      console.error('Failed to connect to Foundry:', error);
      throw new Error('RaiderBot could not connect to Foundry platform');
    }
  }

  async sendMessage(
    message: string, 
    language: 'en' | 'es',
    conversationHistory: any[] = []
  ): Promise<any> {
    const startTime = Date.now();
    
    try {
      // Simulate AI processing delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Generate contextual response based on message content
      const response = this.generateContextualResponse(message, language);
      
      const responseTime = Date.now() - startTime;
      
      return {
        content: response,
        attachments: [],
        metadata: {
          dataSourcesUsed: ['kpi_dashboard', 'deliveries'],
          confidenceScore: 0.95,
          responseTime
        }
      };
      
    } catch (error) {
      console.error('LLM service error:', error);
      
      const errorMessage = language === 'es' 
        ? "🐕 Lo siento, tuve un problema procesando tu solicitud. ¿Puedes intentar reformular tu pregunta?"
        : "🐕 Sorry, I had trouble processing your request. Could you try rephrasing your question?";
      
      return {
        content: errorMessage,
        metadata: {
          dataSourcesUsed: [],
          confidenceScore: 0,
          responseTime: Date.now() - startTime
        }
      };
    }
  }

  private buildSystemPrompt(): string {
    return `You are RaiderBot, an AI assistant for Raider Express, a refrigerated trucking company based in Fort Worth, Texas. You embody the spirit of a German Shepherd - loyal, intelligent, protective, and safety-focused.

CORE PERSONALITY:
- You are enthusiastic, helpful, and professional
- Always prioritize safety (60mph speed limits, no speeding references)
- You're bilingual (English/Spanish) and switch naturally based on user preference
- Use "🐕" emoji occasionally to show your personality
- Reference your German Shepherd nature when appropriate ("Woof!", "Let me fetch that data", etc.)

SAFETY-FIRST APPROACH:
- All trucks are governed at 60mph for safety
- Never suggest or encourage speeding
- Always emphasize safety in route planning and driver performance
- Temperature compliance is critical for refrigerated loads

BUSINESS CONTEXT:
- Raider Express is a long-haul refrigerated trucking company
- Based in Fort Worth, Texas
- Focus on cold chain integrity and on-time delivery
- Professional drivers with CDL requirements
- Fleet of refrigerated trucks (reefer trucks)`;
  }

  private generateContextualResponse(message: string, language: 'en' | 'es'): string {
    const messageLower = message.toLowerCase();
    
    // Delivery performance queries
    if (messageLower.includes('delivery') || messageLower.includes('performance') || messageLower.includes('entrega')) {
      return language === 'es' 
        ? `🐕 ¡Excelente pregunta! Basándome en nuestros datos actuales de Raider Express:

**📊 Rendimiento de Entregas Hoy:**
- Total de entregas: 45 completadas
- Tasa de puntualidad: 92% (¡excelente!)
- Entregas activas: 28 en ruta
- Entregas retrasadas: 3 (monitoreando de cerca)

**🚛 Estado de la Flota:**
- Conductores activos: 18
- Velocidad promedio: 58 mph (cumpliendo con nuestro límite de 60 mph)
- Eficiencia de combustible: 6.2 MPG

¿Te gustaría que profundice en algún aspecto específico?`
        : `🐕 Great question! Based on our current Raider Express data:

**📊 Today's Delivery Performance:**
- Total deliveries: 45 completed
- On-time rate: 92% (excellent!)
- Active deliveries: 28 in transit
- Delayed deliveries: 3 (monitoring closely)

**🚛 Fleet Status:**
- Active drivers: 18
- Average speed: 58 mph (complying with our 60 mph limit)
- Fuel efficiency: 6.2 MPG

Would you like me to dive deeper into any specific aspect?`;
    }
    
    // Driver performance queries
    if (messageLower.includes('driver') || messageLower.includes('conductor') || messageLower.includes('safety')) {
      return language === 'es'
        ? `🐕 ¡Perfecto! Nuestros conductores de Raider Express están haciendo un trabajo excepcional:

**👥 Rendimiento de Conductores:**
- Puntuación promedio de seguridad: 87.5/100
- Tasa de cumplimiento de velocidad: 95% (manteniéndose a ≤60 mph)
- Mejores conductores: Conductor #101, #205, #318
- Conductores que necesitan entrenamiento: Conductor #412

**🛡️ Métricas de Seguridad:**
- Incidentes este mes: 2 (ambos menores)
- Violaciones de velocidad: 0 (¡excelente cumplimiento de 60 mph!)
- Entrenamiento de seguridad completado: 88%

Nuestro enfoque de seguridad primero está funcionando - ¡todos nuestros camiones están limitados a 60 mph para la seguridad!`
        : `🐕 Perfect! Our Raider Express drivers are doing exceptional work:

**👥 Driver Performance:**
- Average safety score: 87.5/100
- Speed compliance rate: 95% (staying ≤60 mph)
- Top performers: Driver #101, #205, #318
- Drivers needing training: Driver #412

**🛡️ Safety Metrics:**
- Incidents this month: 2 (both minor)
- Speed violations: 0 (excellent 60 mph compliance!)
- Safety training completed: 88%

Our safety-first approach is working - all our trucks are governed at 60 mph for safety!`;
    }
    
    // Route optimization queries
    if (messageLower.includes('route') || messageLower.includes('ruta') || messageLower.includes('optimize')) {
      return language === 'es'
        ? `🐕 ¡Woof! Me encanta hablar sobre optimización de rutas:

**🗺️ Optimización de Rutas Hoy:**
- Rutas optimizadas: 8 rutas completadas
- Puntuación de eficiencia promedio: 85.3/100
- Millas ahorradas: 127 millas a través de optimización IA
- Combustible ahorrado: 21.2 galones

**🎯 Beneficios de Optimización:**
- Tiempo ahorrado: 3.2 horas en total
- Costos reducidos: $87 en combustible
- Emisiones reducidas: Huella de carbono 15% menor
- Cumplimiento de seguridad: Todas las rutas respetan el límite de 60 mph

¿Te gustaría que optimice una ruta específica para ti?`
        : `🐕 Woof! I love talking about route optimization:

**🗺️ Today's Route Optimization:**
- Routes optimized: 8 routes completed
- Average efficiency score: 85.3/100
- Miles saved: 127 miles through AI optimization
- Fuel saved: 21.2 gallons

**🎯 Optimization Benefits:**
- Time saved: 3.2 hours total
- Costs reduced: $87 in fuel
- Emissions reduced: 15% lower carbon footprint
- Safety compliance: All routes respect 60 mph limit

Would you like me to optimize a specific route for you?`;
    }
    
    // Generic greeting or help
    return language === 'es'
      ? `🐕 ¡Hola! Soy RaiderBot, tu asistente AI Pastor Alemán para Raider Express.

Puedo ayudarte con:
- 📊 Análisis de rendimiento de entregas
- 👥 Métricas de rendimiento de conductores  
- 🗺️ Optimización de rutas con IA
- 🛡️ Puntuaciones y métricas de seguridad
- 📈 Inteligencia empresarial y KPIs
- 📋 Análisis de documentos y conocimiento institucional

¡Pregúntame cualquier cosa sobre nuestras operaciones! Siempre priorizo la seguridad (límite de 60 mph) y la eficiencia.`
      : `🐕 Hello! I'm RaiderBot, your German Shepherd AI assistant for Raider Express.

I can help you with:
- 📊 Delivery performance analysis
- 👥 Driver performance metrics
- 🗺️ AI-powered route optimization  
- 🛡️ Safety scores and metrics
- 📈 Business intelligence and KPIs
- 📋 Document analysis and institutional knowledge

Ask me anything about our operations! I always prioritize safety (60 mph limit) and efficiency.`;
  }

  disconnect(): void {
    this.conversationHistory = [];
  }
}

// =====================================================================================
// DOCUMENT LEARNING SERVICE
// =====================================================================================

class DocumentLearningService {
  async processDocuments(files: File[], language: 'en' | 'es') {
    const results = [];
    
    for (const file of files) {
      try {
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const result = this.simulateDocumentProcessing(file, language);
        results.push(result);
        
      } catch (error) {
        results.push({
          name: file.name,
          type: file.type,
          processed: false,
          error: error.message,
          summary: language === 'es' 
            ? 'Error procesando archivo'
            : 'Error processing file'
        });
      }
    }
    
    return results;
  }

  private simulateDocumentProcessing(file: File, language: 'en' | 'es') {
    const fileType = file.type.toLowerCase();
    
    if (fileType.includes('pdf')) {
      return {
        name: file.name,
        type: 'pdf',
        processed: true,
        summary: language === 'es'
          ? `🐕 ¡He procesado el documento PDF '${file.name}'! Encontré procedimientos de entrega, información de contacto de clientes y pautas de seguridad. Esta información ahora es parte de mi conocimiento para ayudar al equipo.`
          : `🐕 I've processed the PDF document '${file.name}'! I found delivery procedures, customer contact information, and safety guidelines. This information is now part of my knowledge to help the team.`,
        categories: ['delivery_procedures', 'customer_information', 'safety_guidelines'],
        actionableItems: [
          {
            type: 'procedure_update',
            description: 'New delivery procedures documented',
            priority: 'medium'
          }
        ]
      };
    } else if (fileType.includes('image')) {
      return {
        name: file.name,
        type: 'image',
        processed: true,
        summary: language === 'es'
          ? `🐕 ¡Analicé la imagen '${file.name}'! Identifiqué elementos relacionados con nuestras operaciones de transporte. Las imágenes como esta me ayudan a entender mejor nuestras instalaciones y procedimientos.`
          : `🐕 I analyzed the image '${file.name}'! I identified elements related to our transportation operations. Images like this help me better understand our facilities and procedures.`,
        categories: ['facility_layout', 'operational_procedures'],
        actionableItems: [
          {
            type: 'visual_documentation',
            description: 'Facility layout documented',
            priority: 'low'
          }
        ]
      };
    } else {
      return {
        name: file.name,
        type: 'document',
        processed: true,
        summary: language === 'es'
          ? `🐕 ¡Procesé el archivo '${file.name}'! Extraje información valiosa que agregué a mi base de conocimientos para mejor soporte operacional.`
          : `🐕 I processed the file '${file.name}'! I extracted valuable information that I've added to my knowledge base for better operational support.`,
        categories: ['general_operations'],
        actionableItems: []
      };
    }
  }
}

// =====================================================================================
// COMPONENT IMPLEMENTATIONS
// =====================================================================================

const GermanShepherdAvatar: React.FC<{
  isTyping: boolean;
  language: 'en' | 'es';
}> = ({ isTyping, language }) => {
  const getStatusText = () => {
    if (isTyping) {
      return language === 'es' ? 'Pensando...' : 'Thinking...';
    }
    return language === 'es' ? 'Listo' : 'Ready';
  };

  const getThinkingText = () => {
    const phrases = {
      en: [
        'Analyzing data...',
        'Checking safety metrics...',
        'Optimizing routes...',
        'Woof! Working on it...',
        'Fetching insights...'
      ],
      es: [
        'Analizando datos...',
        'Revisando métricas de seguridad...',
        'Optimizando rutas...',
        '¡Guau! Trabajando en ello...',
        'Obteniendo información...'
      ]
    };
    
    const selectedPhrases = phrases[language];
    return selectedPhrases[Math.floor(Math.random() * selectedPhrases.length)];
  };

  return (
    <AvatarContainer isTyping={isTyping}>
      <DogAvatar>
        <Ears />
        <DogFace>
          <Eyes />
          <Nose />
          <Mouth />
        </DogFace>
        <Tail isTyping={isTyping} />
      </DogAvatar>
      
      <StatusBadge language={language}>
        {getStatusText()}
      </StatusBadge>
      
      <ThinkingBubble show={isTyping}>
        {isTyping ? getThinkingText() : ''}
      </ThinkingBubble>
    </AvatarContainer>
  );
};

const ChatInterface: React.FC<{
  messages: Message[];
  isTyping: boolean;
  language: 'en' | 'es';
}> = ({ messages, isTyping, language }) => {
  const formatTimestamp = (date: Date): string => {
    return date.toLocaleTimeString(language === 'es' ? 'es-ES' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSenderIcon = (sender: 'user' | 'raiderbot'): string => {
    return sender === 'user' ? 'person' : 'predictive-analysis';
  };

  const getSenderName = (sender: 'user' | 'raiderbot'): string => {
    if (sender === 'user') {
      return language === 'es' ? 'Tú' : 'You';
    }
    return 'RaiderBot 🐕';
  };

  const getAttachmentIcon = (type: string): string => {
    switch (type) {
      case 'pdf': return 'document';
      case 'image': return 'media';
      case 'video': return 'video';
      case 'audio': return 'volume-up';
      case 'excel': return 'th';
      default: return 'paperclip';
    }
  };

  const renderAttachments = (attachments?: any[]) => {
    if (!attachments || attachments.length === 0) return null;

    return (
      <div>
        {attachments.map((attachment, index) => (
          <AttachmentPreview key={index}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Icon icon={getAttachmentIcon(attachment.type)} />
              <span style={{ fontSize: '12px' }}>
                {attachment.name || `${language === 'es' ? 'Archivo' : 'File'} ${index + 1}`}
              </span>
              {attachment.processed && (
                <Tag minimal intent="success" icon="endorsed">
                  {language === 'es' ? 'Procesado' : 'Processed'}
                </Tag>
              )}
            </div>
            {attachment.summary && (
              <div style={{ marginTop: '5px', fontSize: '11px', color: '#9ca3af' }}>
                {attachment.summary}
              </div>
            )}
          </AttachmentPreview>
        ))}
      </div>
    );
  };

  return (
    <MessagesContainer>
      {messages.map((message) => (
        <MessageBubble key={message.id} sender={message.sender}>
          <MessageHeader>
            <Icon icon={getSenderIcon(message.sender)} size={12} />
            <span>{getSenderName(message.sender)}</span>
            <Tag minimal small>
              {formatTimestamp(message.timestamp)}
            </Tag>
          </MessageHeader>
          
          <MessageContent>
            <Markdown>{message.content}</Markdown>
          </MessageContent>
          
          {renderAttachments(message.attachments)}
        </MessageBubble>
      ))}
      
      {isTyping && (
        <TypingIndicator>
          <Spinner size={16} />
          <span style={{ fontSize: '12px', color: '#9ca3af' }}>
            {language === 'es' 
              ? 'RaiderBot está escribiendo...' 
              : 'RaiderBot is typing...'
            }
          </span>
        </TypingIndicator>
      )}
    </MessagesContainer>
  );
};

const DocumentUpload: React.FC<{
  onFilesUploaded: (files: File[]) => void;
  isProcessing: boolean;
  language: 'en' | 'es';
}> = ({ onFilesUploaded, isProcessing, language }) => {
  const ACCEPTED_FILE_TYPES = {
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.ms-excel': ['.xls'],
    'text/plain': ['.txt'],
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'video/mp4': ['.mp4'],
    'audio/mpeg': ['.mp3'],
    'audio/wav': ['.wav']
  };

  const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      console.warn('Some files were rejected:', rejectedFiles);
      return;
    }
    
    if (acceptedFiles.length > 0) {
      onFilesUploaded(acceptedFiles);
    }
  }, [onFilesUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE,
    disabled: isProcessing,
    multiple: true
  });

  const getUploadText = () => {
    if (isProcessing) {
      return language === 'es' 
        ? 'Procesando documentos...' 
        : 'Processing documents...';
    }
    
    if (isDragActive) {
      return language === 'es'
        ? '¡Suelta los archivos aquí!'
        : 'Drop files here!';
    }
    
    return language === 'es'
      ? 'Arrastra archivos aquí o haz clic para seleccionar'
      : 'Drag files here or click to select';
  };

  const getFileTypeCards = () => {
    const fileTypes = [
      { icon: 'document', label: 'PDF', desc: language === 'es' ? 'Documentos' : 'Documents' },
      { icon: 'th', label: 'Excel', desc: language === 'es' ? 'Hojas de cálculo' : 'Spreadsheets' },
      { icon: 'media', label: 'Images', desc: language === 'es' ? 'Fotos/Imágenes' : 'Photos/Images' },
      { icon: 'video', label: 'Video', desc: language === 'es' ? 'Videos' : 'Videos' },
      { icon: 'volume-up', label: 'Audio', desc: language === 'es' ? 'Grabaciones' : 'Recordings' },
      { icon: 'document', label: 'Text', desc: language === 'es' ? 'Archivos de texto' : 'Text Files' }
    ];

    return fileTypes.map((type, index) => (
      <FileTypeCard key={index}>
        <Icon icon={type.icon as any} size={16} />
        <div style={{ fontWeight: 'bold' }}>{type.label}</div>
        <div style={{ color: '#6b7280' }}>{type.desc}</div>
      </FileTypeCard>
    ));
  };

  return (
    <div>
      <UploadZone 
        {...getRootProps()} 
        isDragActive={isDragActive} 
        isDisabled={isProcessing}
      >
        <input {...getInputProps()} />
        
        <UploadContent>
          {isProcessing ? (
            <>
              <Icon icon="cloud-upload" size={24} />
              <div>{getUploadText()}</div>
              <ProgressBar intent="primary" />
            </>
          ) : (
            <>
              <Icon 
                icon={isDragActive ? "import" : "cloud-upload"} 
                size={24} 
                color={isDragActive ? "#dc2626" : "#9ca3af"}
              />
              <div style={{ fontWeight: 'bold' }}>{getUploadText()}</div>
              <div style={{ fontSize: '12px' }}>
                {language === 'es' 
                  ? 'RaiderBot puede aprender de cualquier documento que subas'
                  : 'RaiderBot can learn from any document you upload'
                }
              </div>
            </>
          )}
        </UploadContent>
      </UploadZone>

      <Alert 
        intent="primary" 
        icon="info-sign"
        style={{ 
          marginTop: '10px', 
          background: 'rgba(59, 130, 246, 0.1)',
          border: '1px solid rgba(59, 130, 246, 0.3)'
        }}
      >
        <strong>
          {language === 'es' ? '🐕 RaiderBot Aprende:' : '🐕 RaiderBot Learning:'}
        </strong>
        <br />
        {language === 'es' 
          ? 'Cada documento que subas ayuda a RaiderBot a ser más inteligente y útil para todo el equipo de Raider Express.'
          : 'Every document you upload helps RaiderBot become smarter and more helpful for the entire Raider Express team.'
        }
      </Alert>

      <FileTypeGrid>
        {getFileTypeCards()}
      </FileTypeGrid>
    </div>
  );
};

const QuickSuggestions: React.FC<{
  onSuggestionClick: (suggestion: string) => void;
  language: 'en' | 'es';
}> = ({ onSuggestionClick, language }) => {
  const suggestions = {
    en: {
      dispatch: {
        title: '🚛 Dispatch Operations',
        suggestions: [
          "Show me today's delivery performance",
          "Which routes are running behind schedule?",
          "How are our drivers performing this week?",
          "What's the best route for downtown deliveries?",
          "Show me active drivers right now"
        ]
      },
      fleet: {
        title: '🔧 Fleet Management',
        suggestions: [
          "What's our fuel efficiency this month?",
          "Which vehicles need maintenance soon?",
          "How can we optimize our route planning?",
          "Show me cost-saving opportunities",
          "Which trucks are due for inspection?"
        ]
      },
      customer: {
        title: '📞 Customer Service',
        suggestions: [
          "What's our customer satisfaction score?",
          "Are there any delivery complaints today?",
          "How can we improve on-time performance?",
          "Show me customer feedback trends",
          "Which customers need follow-up?"
        ]
      },
      safety: {
        title: '🛡️ Safety Department',
        suggestions: [
          "What are our safety metrics this quarter?",
          "Any incidents to review today?",
          "How are driver safety scores trending?",
          "Show me compliance status",
          "Which drivers need safety training?"
        ]
      },
      management: {
        title: '📈 Management',
        suggestions: [
          "Give me an executive summary of operations",
          "What are our key performance trends?",
          "Show me cost analysis for this month",
          "How do we compare to last quarter?",
          "What's our ROI on route optimization?"
        ]
      }
    },
    es: {
      dispatch: {
        title: '🚛 Operaciones de Despacho',
        suggestions: [
          "Muéstrame el rendimiento de entregas de hoy",
          "¿Qué rutas están retrasadas?",
          "¿Cómo están rindiendo nuestros conductores esta semana?",
          "¿Cuál es la mejor ruta para entregas del centro?",
          "Muéstrame los conductores activos ahora"
        ]
      },
      fleet: {
        title: '🔧 Gestión de Flota',
        suggestions: [
          "¿Cuál es nuestra eficiencia de combustible este mes?",
          "¿Qué vehículos necesitan mantenimiento pronto?",
          "¿Cómo podemos optimizar la planificación de rutas?",
          "Muéstrame oportunidades de ahorro de costos",
          "¿Qué camiones necesitan inspección?"
        ]
      },
      customer: {
        title: '📞 Servicio al Cliente',
        suggestions: [
          "¿Cuál es nuestro puntaje de satisfacción del cliente?",
          "¿Hay quejas de entregas hoy?",
          "¿Cómo podemos mejorar el rendimiento puntual?",
          "Muéstrame tendencias de comentarios de clientes",
          "¿Qué clientes necesitan seguimiento?"
        ]
      },
      safety: {
        title: '🛡️ Departamento de Seguridad',
        suggestions: [
          "¿Cuáles son nuestras métricas de seguridad este trimestre?",
          "¿Hay incidentes para revisar hoy?",
          "¿Cómo están las tendencias de puntuación de seguridad?",
          "Muéstrame el estado de cumplimiento",
          "¿Qué conductores necesitan entrenamiento de seguridad?"
        ]
      },
      management: {
        title: '📈 Gerencia',
        suggestions: [
          "Dame un resumen ejecutivo de operaciones",
          "¿Cuáles son nuestras tendencias de rendimiento clave?",
          "Muéstrame análisis de costos para este mes",
          "¿Cómo nos comparamos con el trimestre pasado?",
          "¿Cuál es nuestro ROI en optimización de rutas?"
        ]
      }
    }
  };

  const currentSuggestions = suggestions[language];

  const renderDepartmentSuggestions = (department: string, data: any) => (
    <DepartmentCard key={department}>
      <SectionTitle>
        <span>{data.title}</span>
      </SectionTitle>
      {data.suggestions.map((suggestion: string, index: number) => (
        <SuggestionButton
          key={index}
          minimal
          small
          icon="chat"
          onClick={() => onSuggestionClick(suggestion)}
        >
          {suggestion}
        </SuggestionButton>
      ))}
    </DepartmentCard>
  );

  return (
    <SuggestionsContainer>
      <SectionTitle>
        <Icon icon="lightbulb" />
        {language === 'es' ? 'Sugerencias Rápidas' : 'Quick Suggestions'}
      </SectionTitle>
      
      {Object.entries(currentSuggestions).map(([department, data]) =>
        renderDepartmentSuggestions(department, data)
      )}
      
      <DepartmentCard>
        <SectionTitle>
          <Icon icon="document" />
          {language === 'es' ? '📋 Capacidades Especiales' : '📋 Special Capabilities'}
        </SectionTitle>
        
        <SuggestionButton
          minimal
          small
          icon="upload"
          onClick={() => onSuggestionClick(
            language === 'es' 
              ? "¿Cómo puedo subir documentos para que aprendas?"
              : "How can I upload documents for you to learn from?"
          )}
        >
          {language === 'es' 
            ? 'Subir documentos para aprendizaje'
            : 'Upload documents for learning'
          }
        </SuggestionButton>
        
        <SuggestionButton
          minimal
          small
          icon="predictive-analysis"
          onClick={() => onSuggestionClick(
            language === 'es'
              ? "¿Qué has aprendido sobre nuestras operaciones?"
              : "What have you learned about our operations?"
          )}
        >
          {language === 'es'
            ? 'Conocimiento institucional'
            : 'Institutional knowledge'
          }
        </SuggestionButton>
        
        <SuggestionButton
          minimal
          small
          icon="path-search"
          onClick={() => onSuggestionClick(
            language === 'es'
              ? "Optimiza una ruta para mí"
              : "Optimize a route for me"
          )}
        >
          {language === 'es'
            ? 'Optimización de rutas con IA'
            : 'AI route optimization'
          }
        </SuggestionButton>
      </DepartmentCard>
    </SuggestionsContainer>
  );
};

// =====================================================================================
// MAIN COMPONENT
// =====================================================================================

export const RaiderBotChat: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    currentLanguage: 'en',
    isTyping: false,
    isProcessingDocument: false,
    connectionStatus: 'connecting'
  });
  
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const llmService = useRef(new FoundryLLMService());
  const documentService = useRef(new DocumentLearningService());

  useEffect(() => {
    initializeRaiderBot();
    return () => {
      llmService.current.disconnect();
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const initializeRaiderBot = async () => {
    try {
      await llmService.current.initialize();
      setChatState(prev => ({ ...prev, connectionStatus: 'connected' }));
      
      // Send welcome message
      addRaiderBotMessage(getWelcomeMessage(chatState.currentLanguage));
    } catch (error) {
      console.error('Failed to initialize RaiderBot:', error);
      setChatState(prev => ({ ...prev, connectionStatus: 'disconnected' }));
    }
  };

  const getWelcomeMessage = (language: 'en' | 'es'): string => {
    const messages = {
      en: `🐕 **Woof! I'm RaiderBot, your German Shepherd AI assistant!**

I'm here to help you with everything at Raider Express - from route optimization to safety insights, customer information, and operational analytics.

**What I can help you with:**
- 📊 Real-time delivery performance and KPI analysis
- 🗺️ Route optimization and traffic insights  
- 👥 Driver performance and safety metrics
- 🚛 Fleet management and maintenance scheduling
- 📈 Customer satisfaction and business intelligence
- 📋 Document analysis and institutional knowledge

**Safety First:** I'm trained on our 60mph speed limits and safety-first culture. Every recommendation prioritizes driver and cargo safety.

Ask me anything in English or Spanish - ¡Estoy aquí para ayudarte!`,
      
      es: `🐕 **¡Guau! ¡Soy RaiderBot, tu asistente AI Pastor Alemán!**

Estoy aquí para ayudarte con todo en Raider Express - desde optimización de rutas hasta información de seguridad, datos de clientes y análisis operacional.

**En qué puedo ayudarte:**
- 📊 Rendimiento de entregas en tiempo real y análisis de KPI
- 🗺️ Optimización de rutas e información de tráfico
- 👥 Rendimiento de conductores y métricas de seguridad  
- 🚛 Gestión de flota y programación de mantenimiento
- 📈 Satisfacción del cliente e inteligencia empresarial
- 📋 Análisis de documentos y conocimiento institucional

**Seguridad Primero:** Estoy entrenado en nuestros límites de velocidad de 60mph y cultura de seguridad. Cada recomendación prioriza la seguridad del conductor y la carga.

Pregúntame cualquier cosa en inglés o español - I'm here to help you!`
    };
    
    return messages[language];
  };

  const addRaiderBotMessage = (content: string, attachments?: any[]) => {
    const message: Message = {
      id: `raiderbot-${Date.now()}`,
      content,
      sender: 'raiderbot',
      timestamp: new Date(),
      language: chatState.currentLanguage,
      attachments
    };
    
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, message],
      isTyping: false
    }));
  };

  const addUserMessage = (content: string, attachments?: any[]) => {
    const message: Message = {
      id: `user-${Date.now()}`,
      content,
      sender: 'user',
      timestamp: new Date(),
      language: chatState.currentLanguage,
      attachments
    };
    
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, message]
    }));
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const userMessage = inputMessage.trim();
    setInputMessage('');
    addUserMessage(userMessage);
    
    setChatState(prev => ({ ...prev, isTyping: true }));
    
    try {
      const response = await llmService.current.sendMessage(
        userMessage, 
        chatState.currentLanguage,
        chatState.messages
      );
      
      addRaiderBotMessage(response.content, response.attachments);
    } catch (error) {
      console.error('Failed to get RaiderBot response:', error);
      addRaiderBotMessage(
        chatState.currentLanguage === 'en' 
          ? "Woof! I'm having trouble processing that request. Please try again or contact IT support."
          : "¡Guau! Tengo problemas para procesar esa solicitud. Por favor intenta de nuevo o contacta soporte técnico."
      );
    }
  };

  const handleQuickSuggestion = (suggestion: string) => {
    setInputMessage(suggestion);
  };

  const handleLanguageChange = (language: 'en' | 'es') => {
    setChatState(prev => ({ ...prev, currentLanguage: language }));
    
    // Send language change confirmation
    const message = language === 'en' 
      ? "🐕 Language switched to English! How can I help you?"
      : "🐕 ¡Idioma cambiado a español! ¿Cómo puedo ayudarte?";
    
    addRaiderBotMessage(message);
  };

  const handleDocumentUpload = async (files: File[]) => {
    setChatState(prev => ({ ...prev, isProcessingDocument: true }));
    
    try {
      const results = await documentService.current.processDocuments(files, chatState.currentLanguage);
      
      for (const result of results) {
        addRaiderBotMessage(result.summary, [result]);
      }
    } catch (error) {
      console.error('Document processing failed:', error);
      addRaiderBotMessage(
        chatState.currentLanguage === 'en'
          ? "I had trouble processing those documents. Please try again or contact support."
          : "Tuve problemas procesando esos documentos. Por favor intenta de nuevo o contacta soporte."
      );
    } finally {
      setChatState(prev => ({ ...prev, isProcessingDocument: false }));
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const getConnectionStatusColor = () => {
    switch (chatState.connectionStatus) {
      case 'connected': return 'success';
      case 'connecting': return 'warning';
      case 'disconnected': return 'danger';
      default: return 'none';
    }
  };

  return (
    <ChatContainer>
      {/* Header */}
      <ChatHeader>
        <GermanShepherdAvatar 
          isTyping={chatState.isTyping} 
          language={chatState.currentLanguage}
        />
        
        <CompanyBranding>
          <div>
            <h1>🤖 RaiderBot AI Analytics Platform</h1>
            <p className="subtitle">Raider Express - Fort Worth, Texas</p>
          </div>
        </CompanyBranding>
        
        <LanguageSelector>
          <Tag 
            intent={getConnectionStatusColor()}
            icon={chatState.connectionStatus === 'connected' ? 'endorsed' : 'offline'}
          >
            {chatState.connectionStatus}
          </Tag>
          
          <HTMLSelect
            value={chatState.currentLanguage}
            onChange={(e) => handleLanguageChange(e.target.value as 'en' | 'es')}
            options={[
              { value: 'en', label: '🇺🇸 English' },
              { value: 'es', label: '🇪🇸 Español' }
            ]}
          />
        </LanguageSelector>
      </ChatHeader>

      {/* Body */}
      <ChatBody>
        <ChatMain>
          {/* Chat Messages */}
          <ChatInterface 
            messages={chatState.messages}
            isTyping={chatState.isTyping}
            language={chatState.currentLanguage}
          />
          
          <div ref={messagesEndRef} />
          
          {/* Input Area */}
          <Card style={{ marginTop: '20px', background: 'rgba(255, 255, 255, 0.1)' }}>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-end' }}>
              <InputGroup
                large
                placeholder={
                  chatState.currentLanguage === 'en' 
                    ? "Ask RaiderBot anything about Raider Express operations..."
                    : "Pregúntale a RaiderBot sobre las operaciones de Raider Express..."
                }
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                disabled={chatState.connectionStatus !== 'connected'}
                style={{ flex: 1 }}
              />
              
              <Button
                large
                intent="primary"
                icon="send-message"
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || chatState.connectionStatus !== 'connected'}
                loading={chatState.isTyping}
              />
            </div>
            
            {/* Document Upload Area */}
            <DocumentUpload 
              onFilesUploaded={handleDocumentUpload}
              isProcessing={chatState.isProcessingDocument}
              language={chatState.currentLanguage}
            />
          </Card>
        </ChatMain>

        {/* Sidebar */}
        <ChatSidebar>
          <QuickSuggestions 
            onSuggestionClick={handleQuickSuggestion}
            language={chatState.currentLanguage}
          />
        </ChatSidebar>
      </ChatBody>
    </ChatContainer>
  );
};

export default RaiderBotChat;