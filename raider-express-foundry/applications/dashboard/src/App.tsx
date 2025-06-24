import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { FocusStyleManager } from '@palantir/blueprint';
import { Navbar, NavbarGroup, NavbarHeading, NavbarDivider, Button, Icon } from '@palantir/blueprint';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import DispatchView from './pages/DispatchView';
import FleetManagement from './pages/FleetManagement';
import SafetyDashboard from './pages/SafetyDashboard';
import RaiderBotChat from '../chat-interface/src/components/RaiderBotChat';
import './App.css';

// Disable focus outline for mouse users
FocusStyleManager.onlyShowFocusOnTabs();

const App: React.FC = () => {
  return (
    <div className="raiderbot-app">
      <Router>
        {/* Main Navigation */}
        <Navbar className="raiderbot-navbar">
          <NavbarGroup>
            <div className="raiderbot-logo">
              <img src="/assets/raiderbot-logo.png" alt="RaiderBot" height="32" />
              <NavbarHeading>RaiderBot Analytics</NavbarHeading>
            </div>
            <NavbarDivider />
            <Button icon="dashboard" text="Executive" minimal />
            <Button icon="drive-time" text="Dispatch" minimal />
            <Button icon="truck" text="Fleet" minimal />
            <Button icon="shield" text="Safety" minimal />
          </NavbarGroup>
          
          <NavbarGroup align="right">
            <div className="company-info">
              <span>Raider Express • Fort Worth, TX</span>
            </div>
            <NavbarDivider />
            <Button icon="chat" text="RaiderBot Chat" minimal />
            <Button icon="user" minimal />
          </NavbarGroup>
        </Navbar>

        {/* Main Content */}
        <div className="main-content">
          <Routes>
            <Route path="/" element={<ExecutiveDashboard />} />
            <Route path="/dispatch" element={<DispatchView />} />
            <Route path="/fleet" element={<FleetManagement />} />
            <Route path="/safety" element={<SafetyDashboard />} />
          </Routes>
        </div>

        {/* Floating Chat Interface */}
        <div className="floating-chat">
          <RaiderBotChat />
        </div>
      </Router>
    </div>
  );
};

export default App;