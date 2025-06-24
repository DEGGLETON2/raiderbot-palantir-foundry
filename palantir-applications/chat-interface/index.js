import React, { useState } from 'react';
import { FoundryFunction } from '@palantir/foundry-react';

// RaiderBot Chat Interface - Palantir Foundry Application
export default function RaiderBotChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [language, setLanguage] = useState('en');
  
  const sendMessage = async () => {
    if (!input.trim()) return;
    
    // Add user message
    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    
    // Call Foundry Function
    const response = await FoundryFunction.invoke('raiderbot_core', {
      message: input,
      language: language,
      conversation_history: messages
    });
    
    // Add RaiderBot response
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response.message
    }]);
  };
  
  return (
    <div className="chat-container">
      <header>
        <h1>🐕 RaiderBot - Palantir Foundry AI</h1>
        <button onClick={() => setLanguage(language === 'en' ? 'es' : 'en')}>
          {language === 'en' ? '🇺🇸 EN' : '🇪🇸 ES'}
        </button>
      </header>
      
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder={language === 'en' ? 'Ask RaiderBot...' : 'Pregunta a RaiderBot...'}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      
      <footer>
        <p>Powered by Palantir Foundry Functions</p>
      </footer>
    </div>
  );
}
