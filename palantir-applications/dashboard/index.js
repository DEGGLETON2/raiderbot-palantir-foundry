import React from 'react';
import { FoundryProvider, useFoundryData } from '@palantir/foundry-react';

// RaiderBot Dashboard - Built on Palantir Foundry Applications
export default function RaiderBotDashboard() {
  // Connect to Foundry datasets
  const kpiData = useFoundryData('raider_kpi_dashboard');
  
  return (
    <FoundryProvider workspace="raider-express-raiderbot">
      <div className="dashboard-container">
        <header>
          <h1>🐕 RaiderBot Dashboard - Palantir Foundry</h1>
          <p>Real-time operations powered by Foundry</p>
        </header>
        
        <div className="kpi-grid">
          <div className="kpi-card">
            <h3>Today's Deliveries</h3>
            <div className="kpi-value">{kpiData?.total_deliveries_today || 0}</div>
            <div className="kpi-label">On-time: {kpiData?.on_time_rate || 0}%</div>
          </div>
          
          <div className="kpi-card safety">
            <h3>60mph Compliance</h3>
            <div className="kpi-value">{kpiData?.speed_compliance_rate || 0}%</div>
            <div className="kpi-label">Safety First!</div>
          </div>
          
          <div className="kpi-card">
            <h3>Active Drivers</h3>
            <div className="kpi-value">{kpiData?.active_drivers || 0}</div>
            <div className="kpi-label">Avg Safety: {kpiData?.avg_safety_score || 0}</div>
          </div>
        </div>
        
        <footer>
          <p>Powered by Palantir Foundry | Updated every 5 minutes</p>
        </footer>
      </div>
    </FoundryProvider>
  );
}
