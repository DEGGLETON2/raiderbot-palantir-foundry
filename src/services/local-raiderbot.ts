import { mockData } from './mock-data';

export class LocalRaiderBot {
  chat(message: string, language: 'en' | 'es' = 'en') {
    const response = this.generateResponse(message, language);
    return response;
  }

  private generateResponse(message: string, language: 'en' | 'es') {
    const msg = message.toLowerCase();
    
    if (msg.includes('delivery') || msg.includes('entrega')) {
      return language === 'es' 
        ? `🐕 ¡Guau! Tenemos ${mockData.kpis.totalDeliveries} entregas hoy con ${mockData.kpis.onTimeRate}% a tiempo.`
        : `🐕 Woof! We have ${mockData.kpis.totalDeliveries} deliveries today with ${mockData.kpis.onTimeRate}% on-time rate.`;
    }
    
    if (msg.includes('driver') || msg.includes('conductor')) {
      return language === 'es'
        ? `🐕 Tenemos ${mockData.kpis.activeDrivers} conductores activos con puntuación de seguridad promedio de ${mockData.kpis.safetyScore}.`
        : `🐕 We have ${mockData.kpis.activeDrivers} active drivers with average safety score of ${mockData.kpis.safetyScore}.`;
    }
    
    if (msg.includes('dashboard')) {
      return language === 'es'
        ? `🐕 ¡Excelente! Estoy generando un dashboard para ti... (Funcionalidad completa próximamente)`
        : `🐕 Excellent! I'm generating a dashboard for you... (Full functionality coming soon)`;
    }
    
    return language === 'es'
      ? `🐕 ¡Hola! Soy RaiderBot, tu asistente Pastor Alemán. ¿Cómo puedo ayudarte con las operaciones de Raider Express?`
      : `🐕 Hello! I'm RaiderBot, your German Shepherd assistant. How can I help with Raider Express operations?`;
  }
} 