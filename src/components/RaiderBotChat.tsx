import React, { useState } from 'react';
import { Box, TextField, Button, Paper, Typography, Container, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import TranslateIcon from '@mui/icons-material/Translate';
import styled from 'styled-components';
import { LocalRaiderBot } from '../services/local-raiderbot';

const MessageContainer = styled(Paper)`
  padding: 16px;
  margin: 8px 0;
  max-width: 80%;
  ${props => props.role === 'user' ? 'margin-left: auto;' : 'margin-right: auto;'}
  background-color: ${props => props.role === 'user' ? '#e3f2fd' : '#f5f5f5'};
`;

const ChatContainer = styled(Box)`
  height: 500px;
  display: flex;
  flex-direction: column;
`;

const MessagesArea = styled(Box)`
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
`;

const InputArea = styled(Box)`
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 8px;
`;

interface Message {
  text: string;
  role: 'user' | 'bot';
  timestamp: Date;
}

export const RaiderBotChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [language, setLanguage] = useState<'en' | 'es'>('en');
  const localBot = new LocalRaiderBot();

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      text: inputMessage,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');

    // Get bot response
    const response = localBot.chat(inputMessage, language);
    
    const botMessage: Message = {
      text: response,
      role: 'bot',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, botMessage]);
  };

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'es' : 'en');
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom align="center" sx={{ mt: 4 }}>
        RaiderBot Chat 🐕
      </Typography>
      
      <ChatContainer>
        <MessagesArea>
          {messages.map((message, index) => (
            <MessageContainer key={index} role={message.role} elevation={1}>
              <Typography>
                {message.text}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                {message.timestamp.toLocaleTimeString()}
              </Typography>
            </MessageContainer>
          ))}
        </MessagesArea>
        
        <InputArea>
          <IconButton onClick={toggleLanguage} color="primary">
            <TranslateIcon />
          </IconButton>
          <TextField
            fullWidth
            variant="outlined"
            placeholder={language === 'en' ? "Type your message..." : "Escribe tu mensaje..."}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <Button
            variant="contained"
            color="primary"
            endIcon={<SendIcon />}
            onClick={handleSendMessage}
          >
            {language === 'en' ? 'Send' : 'Enviar'}
          </Button>
        </InputArea>
      </ChatContainer>
    </Container>
  );
}; 