import React, { useState, useEffect } from 'react';
import { Card, Elevation, Tabs, Tab, Button, Icon } from '@palantir/blueprint';
import KPIDashboard from '../components/KPIDashboard';
import LiveMap from '../components/LiveMap';
import PerformanceCharts from '../components/PerformanceCharts';
import SafetyAlerts from '../components/SafetyAlerts';
import { foundryApi } from '../services/foundryApi';

const ExecutiveDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [executiveSummary, setExecutiveSummary] = useState(null);

  useEffect(() => {
    const fetchExecutiveSummary = async () => {
      try {
        const summary = await foundryApi.getExecutiveSummary();
        setExecutiveSummary(summary);
      } catch (error) {
        console.error('Error fetching executive summary:', error);
      }
    };

    fetchExecutiveSummary();
  }, []);

  return (
    <div className="executive-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="title-section">
          <h1>
            <img src="/assets/german-shepherd-icon.png" alt="RaiderBot" className="mascot-icon" />
            Executive Operations Dashboard
          </h1>
          <p>Raider Express • Fort Worth, Texas • Refrigerated Transportation Excellence</p>
        </div>
        
        <div className="action-buttons">
          <Button icon="refresh" text="Refresh Data" />
          <Button icon="export" text="Export Report" />
          <Button icon="chat" text="Ask RaiderBot" intent="primary" />
        </div>
      </div>

      {/* Main Content */}
      <Tabs
        id="executive-tabs"
        selectedTabId={activeTab}
        onChange={(tabId) => setActiveTab(tabId as string)}
        large
      >
        <Tab
          id="overview"
          title={
            <span>
              <Icon icon="dashboard" />
              Overview
            </span>
          }
          panel={
            <div className="overview-panel">
              {/* KPI Dashboard */}
              <KPIDashboard department="executive" />
              
              {/* Quick Stats Row */}
              <div className="quick-stats">
                <Card elevation={Elevation.ONE}>
                  <h4>Today's Operations</h4>
                  <div className="stat-row">
                    <div className="stat">
                      <Icon icon="drive-time" />
                      <span className="value">47</span>
                      <span className="label">Active Routes</span>
                    </div>
                    <div className="stat">
                      <Icon icon="people" />
                      <span className="value">23</span>
                      <span className="label">Available Drivers</span>
                    </div>
                    <div className="stat">
                      <Icon icon="truck" />
                      <span className="value">89</span>
                      <span className="label">Fleet Utilization %</span>
                    </div>
                  </div>
                </Card>

                <Card elevation={Elevation.ONE}>
                  <h4>Performance Highlights</h4>
                  <div className="highlight-list">
                    <div className="highlight positive">
                      <Icon icon="tick-circle" />
                      <span>Zero safety violations today</span>
                    </div>
                    <div className="highlight positive">
                      <Icon icon="trending-up" />
                      <span>On-time delivery rate: 94.2%</span>
                    </div>
                    <div className="highlight positive">
                      <Icon icon="oil-field" />
                      <span>Fuel efficiency up 3% vs last month</span>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          }
        />

        <Tab
          id="operations"
          title={
            <span>
              <Icon icon="map" />
              Live Operations
            </span>
          }
          panel={
            <div className="operations-panel">
              <LiveMap />
              <div className="operations-sidebar">
                <SafetyAlerts />
                <Card elevation={Elevation.ONE}>
                  <h4>Active Routes Status</h4>
                  <div className="route-status-list">
                    {/* Route status items would be mapped here */}
                  </div>
                </Card>
              </div>
            </div>
          }
        />

        <Tab
          id="analytics"
          title={
            <span>
              <Icon icon="timeline-line-chart" />
              Analytics
            </span>
          }
          panel={
            <div className="analytics-panel">
              <PerformanceCharts />
            </div>
          }
        />

        <Tab
          id="reports"
          title={
            <span>
              <Icon icon="document" />
              Reports
            </span>
          }
          panel={
            <div className="reports-panel">
              <Card elevation={Elevation.ONE}>
                <h3>Executive Reports</h3>
                <div className="report-grid">
                  <Button 
                    icon="chart" 
                    text="Daily Operations Summary"
                    large
                    fill
                  />
                  <Button 
                    icon="people" 
                    text="Driver Performance Report"
                    large
                    fill
                  />
                  <Button 
                    icon="oil-field" 
                    text="Fuel Efficiency Analysis"
                    large
                    fill
                  />
                  <Button 
                    icon="shield" 
                    text="Safety & Compliance Report"
                    large
                    fill
                  />
                </div>
              </Card>
            </div>
          }
        />
      </Tabs>

      {/* Footer with RaiderBot branding */}
      <div className="dashboard-footer">
        <span>Powered by RaiderBot AI • Your German Shepherd Analytics Assistant</span>
        <span>Safety First • 60mph Governed Fleet • Fort Worth Proud</span>
      </div>
    </div>
  );
};

export default ExecutiveDashboard;