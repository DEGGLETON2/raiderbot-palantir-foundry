import React, { useState, useEffect } from 'react';
import { Card, Elevation, Icon, Tag, Spinner } from '@palantir/blueprint';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { foundryApi } from '../services/foundryApi';

interface KPIData {
  kpi_name: string;
  kpi_value: number;
  kpi_trend: number;
  kpi_target: number;
  kpi_category: string;
  time_period: string;
}

interface KPIDashboardProps {
  department?: string;
  refreshInterval?: number;
}

const KPIDashboard: React.FC<KPIDashboardProps> = ({ 
  department = 'executive',
  refreshInterval = 30000 
}) => {
  const [kpiData, setKpiData] = useState<KPIData[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const fetchKPIData = async () => {
      try {
        setLoading(true);
        const data = await foundryApi.getKPIData(department);
        setKpiData(data);
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Error fetching KPI data:', error);
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchKPIData();

    // Set up refresh interval
    const interval = setInterval(fetchKPIData, refreshInterval);
    return () => clearInterval(interval);
  }, [department, refreshInterval]);

  const getKPIIcon = (category: string) => {
    const icons = {
      'Operations': 'drive-time',
      'Resources': 'people',
      'Performance': 'time',
      'Efficiency': 'oil-field',
      'Quality': 'star',
      'Safety': 'shield'
    };
    return icons[category] || 'chart';
  };

  const getKPIStatus = (value: number, target: number, trend: number) => {
    const performance = value / target;
    if (performance >= 0.95) return { status: 'success', color: 'green' };
    if (performance >= 0.85) return { status: 'warning', color: 'orange' };
    return { status: 'danger', color: 'red' };
  };

  const formatKPIValue = (value: number, kpiName: string) => {
    if (kpiName.includes('Rate') || kpiName.includes('Satisfaction')) {
      return `${value.toFixed(1)}%`;
    }
    if (kpiName.includes('Efficiency')) {
      return `${value.toFixed(1)} MPG`;
    }
    return Math.round(value).toString();
  };

  if (loading) {
    return (
      <div className="kpi-loading">
        <Spinner size={50} />
        <p>Loading RaiderBot KPIs...</p>
      </div>
    );
  }

  return (
    <div className="kpi-dashboard">
      <div className="kpi-header">
        <h2>
          <Icon icon="dashboard" />
          RaiderBot Analytics Dashboard
        </h2>
        <div className="last-update">
          <Tag minimal>
            Last updated: {lastUpdate.toLocaleTimeString()}
          </Tag>
        </div>
      </div>

      <div className="kpi-grid">
        {kpiData.map((kpi, index) => {
          const status = getKPIStatus(kpi.kpi_value, kpi.kpi_target, kpi.kpi_trend);
          
          return (
            <Card key={index} elevation={Elevation.TWO} className={`kpi-card ${status.status}`}>
              <div className="kpi-header">
                <Icon 
                  icon={getKPIIcon(kpi.kpi_category)} 
                  size={24}
                  color={status.color}
                />
                <div className="kpi-meta">
                  <Tag minimal>{kpi.kpi_category}</Tag>
                  <span className="time-period">{kpi.time_period}</span>
                </div>
              </div>

              <div className="kpi-content">
                <h3>{kpi.kpi_name}</h3>
                <div className="kpi-value">
                  <span className="current-value">
                    {formatKPIValue(kpi.kpi_value, kpi.kpi_name)}
                  </span>
                  <span className="target-value">
                    Target: {formatKPIValue(kpi.kpi_target, kpi.kpi_name)}
                  </span>
                </div>

                <div className="kpi-trend">
                  <Icon 
                    icon={kpi.kpi_trend >= 0 ? 'trending-up' : 'trending-down'}
                    color={kpi.kpi_trend >= 0 ? 'green' : 'red'}
                  />
                  <span className={kpi.kpi_trend >= 0 ? 'positive-trend' : 'negative-trend'}>
                    {Math.abs(kpi.kpi_trend).toFixed(1)}
                  </span>
                </div>
              </div>

              {/* Mini trend chart */}
              <div className="kpi-mini-chart">
                <ResponsiveContainer width="100%" height={40}>
                  <LineChart data={[
                    { value: kpi.kpi_value - kpi.kpi_trend },
                    { value: kpi.kpi_value }
                  ]}>
                    <Line 
                      type="monotone" 
                      dataKey="value" 
                      stroke={status.color}
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Safety Focus Banner */}
      <Card elevation={Elevation.ONE} className="safety-banner">
        <Icon icon="shield" size={20} />
        <span>
          <strong>Safety First:</strong> 60mph Governed Trucks • Zero Speed Violations Today
        </span>
        <Tag intent="success">✓ Compliant</Tag>
      </Card>
    </div>
  );
};

export default KPIDashboard;