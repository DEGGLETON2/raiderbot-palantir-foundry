import React from 'react';
import { RaiderBotChat } from './components/RaiderBotChat';
import { ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <RaiderBotChat />
    </ThemeProvider>
  );
}

export default App; 