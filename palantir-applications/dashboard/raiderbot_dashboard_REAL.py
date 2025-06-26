"""
RaiderBot Dashboard Workshop Application
Replaces React-based dashboard with Foundry Workshop

Based on src.legacy/components/Dashboard/KPIDashboard.jsx
"""

from foundry_workshop import App, Page, Component
from foundry_workshop.components import (
    Card, Grid, Text, Metric, Chart, Table, Button, 
    Select, DatePicker, ProgressBar, Alert, Tabs, TabPanel
)
from foundry_workshop.layouts import Container, Row, Column
from foundry_workshop.styling import Theme, Color, Spacing
from foundry_functions import FunctionCall
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px


class RaiderBotDashboardApp(App):
    """Main RaiderBot Dashboard Application"""
    
    def __init__(self):
        super().__init__(
            name="RaiderBot Analytics Dashboard",
            description="Comprehensive logistics analytics and KPI monitoring",
            version="1.0.0"
        )
        
        # Initialize state
        self.state = {
            "selected_period": 30,
            "selected_language": "EN",
            "auto_refresh": True,
            "last_refresh": datetime.now(),
            "dashboard_data": None
        }
        
        # Set up theme
        self.theme = Theme(
            primary_color=Color.BLUE,
            secondary_color=Color.GREEN,
            accent_color=Color.RED,
            background_color=Color.WHITE,
            text_color=Color.BLACK
        )
    
    def create_layout(self):
        """Create main dashboard layout"""
        
        return Container([
            # Header Section
            Row([
                Column([
                    Text(
                        "RaiderBot Analytics Dashboard",
                        style="h1",
                        color=self.theme.primary_color
                    ),
                    Text(
                        f"Last Updated: {self.state['last_refresh'].strftime('%Y-%m-%d %H:%M:%S')}",
                        style="caption",
                        color=Color.GRAY
                    )
                ], width=8),
                Column([
                    self._create_controls_panel()
                ], width=4)
            ], margin=Spacing.MEDIUM),
            
            # KPI Summary Cards
            Row([
                self._create_kpi_cards()
            ], margin=Spacing.MEDIUM),
            
            # Main Content Tabs
            Tabs([
                TabPanel(
                    label="Performance Overview",
                    content=self._create_performance_tab()
                ),
                TabPanel(
                    label="Fleet Management",
                    content=self._create_fleet_tab()
                ),
                TabPanel(
                    label="Driver Analytics",
                    content=self._create_driver_tab()
                ),
                TabPanel(
                    label="Route Optimization",
                    content=self._create_route_tab()
                ),
                TabPanel(
                    label="AI Insights",
                    content=self._create_ai_insights_tab()
                )
            ])
        ])
    
    def _create_controls_panel(self):
        """Create dashboard controls"""
        
        return Card([
            Text("Dashboard Controls", style="h3"),
            
            # Period Selection
            Select(
                label="Time Period",
                options=[
                    {"value": 7, "label": "Last 7 Days"},
                    {"value": 30, "label": "Last 30 Days"},
                    {"value": 90, "label": "Last 90 Days"}
                ],
                value=self.state["selected_period"],
                on_change=self._on_period_change
            ),
            
            # Language Selection
            Select(
                label="Language",
                options=[
                    {"value": "EN", "label": "English"},
                    {"value": "ES", "label": "Español"}
                ],
                value=self.state["selected_language"],
                on_change=self._on_language_change
            ),
            
            # Refresh Button
            Button(
                "Refresh Data",
                on_click=self._refresh_dashboard,
                variant="primary",
                icon="refresh"
            )
        ], padding=Spacing.MEDIUM)
    
    def _create_kpi_cards(self):
        """Create KPI summary cards"""
        
        # Get dashboard data
        dashboard_data = self._get_dashboard_data()
        
        if not dashboard_data or not dashboard_data.get("success"):
            return Alert("Error loading dashboard data", type="error")
        
        summary = dashboard_data["summary"]
        
        kpi_cards = [
            # Total Deliveries
            Card([
                Metric(
                    value=summary["total_deliveries"],
                    label="Total Deliveries" if self.state["selected_language"] == "EN" else "Entregas Totales",
                    icon="truck",
                    color=Color.BLUE,
                    trend=self._calculate_trend("deliveries", dashboard_data)
                )
            ], width=3),
            
            # On-Time Rate
            Card([
                Metric(
                    value=f"{summary['on_time_rate']}%",
                    label="On-Time Rate" if self.state["selected_language"] == "EN" else "Tasa de Puntualidad",
                    icon="clock",
                    color=Color.GREEN if summary["on_time_rate"] >= 95 else Color.ORANGE,
                    trend=self._calculate_trend("on_time_rate", dashboard_data)
                )
            ], width=3),
            
            # Active Drivers
            Card([
                Metric(
                    value=summary["active_drivers"],
                    label="Active Drivers" if self.state["selected_language"] == "EN" else "Conductores Activos",
                    icon="users",
                    color=Color.PURPLE,
                    trend="All routes covered" if self.state["selected_language"] == "EN" else "Todas las rutas cubiertas"
                )
            ], width=3),
            
            # Fleet Utilization
            Card([
                Metric(
                    value=f"{summary['fleet_utilization']}%",
                    label="Fleet Utilization" if self.state["selected_language"] == "EN" else "Utilización de Flota",
                    icon="activity",
                    color=Color.RED if summary["fleet_utilization"] < 80 else Color.GREEN,
                    trend=self._calculate_trend("fleet_utilization", dashboard_data)
                )
            ], width=3)
        ]
        
        return Grid(kpi_cards, columns=4, gap=Spacing.MEDIUM)
    
    def _create_performance_tab(self):
        """Create performance overview tab"""
        
        dashboard_data = self._get_dashboard_data()
        
        if not dashboard_data:
            return Alert("No data available", type="warning")
        
        delivery_data = dashboard_data["delivery_performance"]
        
        return Container([
            Row([
                # Delivery Trend Chart
                Column([
                    Card([
                        Text("Delivery Trend", style="h3"),
                        Chart(
                            self._create_delivery_trend_chart(delivery_data),
                            height=300
                        )
                    ])
                ], width=8),
                
                # Performance Metrics
                Column([
                    Card([
                        Text("Performance Metrics", style="h3"),
                        self._create_performance_metrics_table(delivery_data)
                    ])
                ], width=4)
            ]),
            
            Row([
                # On-Time Performance by Route
                Column([
                    Card([
                        Text("On-Time Performance by Route", style="h3"),
                        Chart(
                            self._create_route_performance_chart(delivery_data),
                            height=250
                        )
                    ])
                ], width=12)
            ])
        ])
    
    def _create_fleet_tab(self):
        """Create fleet management tab"""
        
        dashboard_data = self._get_dashboard_data()
        fleet_data = dashboard_data["fleet_performance"]
        
        return Container([
            Row([
                # Fleet Status Overview
                Column([
                    Card([
                        Text("Fleet Status", style="h3"),
                        Grid([
                            Metric(
                                value=fleet_data["fleet_metrics"]["total_active_vehicles"],
                                label="Active Vehicles",
                                icon="truck",
                                color=Color.BLUE
                            ),
                            Metric(
                                value=f"{fleet_data['fleet_metrics']['avg_fleet_mpg']} MPG",
                                label="Average Fuel Efficiency",
                                icon="fuel",
                                color=Color.GREEN
                            ),
                            Metric(
                                value=fleet_data["fleet_metrics"]["vehicles_in_maintenance"],
                                label="In Maintenance",
                                icon="wrench",
                                color=Color.ORANGE
                            )
                        ], columns=3)
                    ])
                ], width=12)
            ]),
            
            Row([
                # Maintenance Schedule
                Column([
                    Card([
                        Text("Upcoming Maintenance", style="h3"),
                        Table(
                            data=fleet_data.get("maintenance_metrics", {}).get("maintenance_schedule", []),
                            columns=[
                                {"key": "tractor_number", "label": "Vehicle"},
                                {"key": "service_due_date", "label": "Due Date"},
                                {"key": "days_until_due", "label": "Days Until Due"},
                                {"key": "service_type", "label": "Service Type"}
                            ]
                        )
                    ])
                ], width=8),
                
                # Vehicle Utilization
                Column([
                    Card([
                        Text("Utilization Rate", style="h3"),
                        ProgressBar(
                            value=fleet_data["fleet_metrics"]["utilization_rate"],
                            max_value=100,
                            label=f"{fleet_data['fleet_metrics']['utilization_rate']}%",
                            color=Color.GREEN if fleet_data["fleet_metrics"]["utilization_rate"] >= 80 else Color.ORANGE
                        )
                    ])
                ], width=4)
            ])
        ])
    
    def _create_driver_tab(self):
        """Create driver analytics tab"""
        
        dashboard_data = self._get_dashboard_data()
        driver_data = dashboard_data["driver_performance"]
        
        return Container([
            Row([
                # Driver KPIs
                Column([
                    Card([
                        Text("Driver Performance", style="h3"),
                        Grid([
                            Metric(
                                value=f"{driver_data['driver_metrics']['avg_safety_score']}",
                                label="Average Safety Score",
                                icon="shield",
                                color=Color.GREEN
                            ),
                            Metric(
                                value=f"{driver_data['driver_metrics']['avg_fuel_efficiency']} MPG",
                                label="Average Fuel Efficiency",
                                icon="fuel",
                                color=Color.BLUE
                            ),
                            Metric(
                                value=driver_data["driver_metrics"]["incident_free_days"],
                                label="Incident Free Days",
                                icon="calendar",
                                color=Color.GREEN
                            )
                        ], columns=3)
                    ])
                ], width=12)
            ]),
            
            Row([
                # Top Performers
                Column([
                    Card([
                        Text("Top Performing Drivers", style="h3"),
                        Table(
                            data=driver_data["top_performers"],
                            columns=[
                                {"key": "driver_name", "label": "Driver"},
                                {"key": "safety_score", "label": "Safety Score"},
                                {"key": "fuel_efficiency", "label": "Fuel Efficiency"},
                                {"key": "total_moves", "label": "Total Moves"}
                            ]
                        )
                    ])
                ], width=12)
            ])
        ])
    
    def _create_route_tab(self):
        """Create route optimization tab"""
        
        dashboard_data = self._get_dashboard_data()
        route_data = dashboard_data["route_optimization"]
        
        return Container([
            Row([
                # Route Optimization KPIs
                Column([
                    Card([
                        Text("Route Optimization", style="h3"),
                        Grid([
                            Metric(
                                value=f"{route_data['optimization_metrics']['optimization_rate']}%",
                                label="Optimization Rate",
                                icon="map",
                                color=Color.GREEN
                            ),
                            Metric(
                                value=f"{route_data['optimization_metrics']['fuel_savings_gallons']} gal",
                                label="Fuel Savings",
                                icon="dollar-sign",
                                color=Color.GREEN
                            ),
                            Metric(
                                value=route_data["optimization_metrics"]["high_potential_routes"],
                                label="High Potential Routes",
                                icon="trending-up",
                                color=Color.ORANGE
                            )
                        ], columns=3)
                    ])
                ], width=12)
            ]),
            
            Row([
                # Route Efficiency Chart
                Column([
                    Card([
                        Text("Route Efficiency Trends", style="h3"),
                        Chart(
                            self._create_route_efficiency_chart(route_data),
                            height=300
                        )
                    ])
                ], width=12)
            ])
        ])
    
    def _create_ai_insights_tab(self):
        """Create AI insights tab"""
        
        return Container([
            Row([
                Column([
                    Card([
                        Text("AI-Powered Business Insights", style="h3"),
                        Button(
                            "Generate New Insights",
                            on_click=self._generate_ai_insights,
                            variant="primary",
                            icon="brain"
                        )
                    ])
                ], width=12)
            ]),
            
            Row([
                Column([
                    Card([
                        Text("Recent Insights", style="h3"),
                        self._display_ai_insights()
                    ])
                ], width=12)
            ])
        ])
    
    # ===== DATA FETCHING METHODS =====
    
    def _get_dashboard_data(self):
        """Fetch dashboard data from Foundry Functions"""
        
        if self.state["dashboard_data"] is None or self._should_refresh_data():
            try:
                # Call Foundry Function
                function_call = FunctionCall("get_comprehensive_dashboard_data")
                result = function_call.execute(
                    days_back=self.state["selected_period"],
                    include_forecasts=True,
                    language=self.state["selected_language"]
                )
                
                self.state["dashboard_data"] = result
                self.state["last_refresh"] = datetime.now()
                
            except Exception as e:
                print(f"Error fetching dashboard data: {e}")
                return None
        
        return self.state["dashboard_data"]
    
    def _should_refresh_data(self):
        """Check if data should be refreshed"""
        
        if not self.state["auto_refresh"]:
            return False
        
        # Refresh every 5 minutes
        time_since_refresh = datetime.now() - self.state["last_refresh"]
        return time_since_refresh.total_seconds() > 300
    
    # ===== CHART CREATION METHODS =====
    
    def _create_delivery_trend_chart(self, delivery_data):
        """Create delivery trend chart"""
        
        daily_trend = delivery_data["delivery_metrics"]["daily_trend"]
        
        dates = [item["date"] for item in daily_trend]
        deliveries = [item["deliveries"] for item in daily_trend]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=deliveries,
            mode='lines+markers',
            name='Daily Deliveries',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Daily Delivery Trend",
            xaxis_title="Date",
            yaxis_title="Number of Deliveries",
            template="plotly_white"
        )
        
        return fig
    
    def _create_route_performance_chart(self, delivery_data):
        """Create route performance chart"""
        
        # Mock data for demonstration
        routes = ["Route A", "Route B", "Route C", "Route D", "Route E"]
        on_time_rates = [94.5, 87.2, 96.1, 89.8, 92.3]
        
        fig = go.Figure(data=[
            go.Bar(x=routes, y=on_time_rates, marker_color='green')
        ])
        
        fig.update_layout(
            title="On-Time Performance by Route",
            xaxis_title="Route",
            yaxis_title="On-Time Rate (%)",
            template="plotly_white"
        )
        
        return fig
    
    def _create_route_efficiency_chart(self, route_data):
        """Create route efficiency chart"""
        
        # Mock data for demonstration
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        efficiency_scores = [82.5, 85.1, 87.8, 84.2, 89.6, 91.3]
        
        fig = go.Figure(data=[
            go.Scatter(x=months, y=efficiency_scores, mode='lines+markers', name='Efficiency Score')
        ])
        
        fig.update_layout(
            title="Route Efficiency Trends",
            xaxis_title="Month",
            yaxis_title="Efficiency Score",
            template="plotly_white"
        )
        
        return fig
    
    # ===== EVENT HANDLERS =====
    
    def _on_period_change(self, new_period):
        """Handle period selection change"""
        self.state["selected_period"] = new_period
        self.state["dashboard_data"] = None  # Force refresh
        self.refresh()
    
    def _on_language_change(self, new_language):
        """Handle language change"""
        self.state["selected_language"] = new_language
        self.state["dashboard_data"] = None  # Force refresh
        self.refresh()
    
    def _refresh_dashboard(self):
        """Handle manual refresh"""
        self.state["dashboard_data"] = None
        self.refresh()
    
    def _generate_ai_insights(self):
        """Generate new AI insights"""
        try:
            function_call = FunctionCall("generate_business_insights")
            insights = function_call.execute(
                focus_area="performance",
                days_back=self.state["selected_period"],
                language=self.state["selected_language"]
            )
            
            self.state["ai_insights"] = insights
            self.refresh()
            
        except Exception as e:
            print(f"Error generating AI insights: {e}")
    
    # ===== HELPER METHODS =====
    
    def _calculate_trend(self, metric, dashboard_data):
        """Calculate trend for metrics"""
        
        # Simplified trend calculation
        # In production, would compare with previous period
        
        trends = {
            "deliveries": "↗ +12% from last period",
            "on_time_rate": "↗ +2.3% improvement",
            "fleet_utilization": "→ Stable"
        }
        
        return trends.get(metric, "→ No trend data")
    
    def _create_performance_metrics_table(self, delivery_data):
        """Create performance metrics table"""
        
        metrics_data = [
            {"metric": "Total Deliveries", "value": delivery_data["delivery_metrics"]["total_deliveries"]},
            {"metric": "On-Time Rate", "value": f"{delivery_data['delivery_metrics']['on_time_rate']}%"},
            {"metric": "Avg Variance", "value": f"{delivery_data['delivery_metrics']['avg_delivery_variance_minutes']} min"}
        ]
        
        return Table(
            data=metrics_data,
            columns=[
                {"key": "metric", "label": "Metric"},
                {"key": "value", "label": "Value"}
            ]
        )
    
    def _display_ai_insights(self):
        """Display AI insights"""
        
        ai_insights = self.state.get("ai_insights")
        
        if not ai_insights:
            return Text("Click 'Generate New Insights' to get AI-powered analysis", style="body")
        
        insights_list = []
        for insight in ai_insights.get("insights", []):
            insights_list.append(
                Card([
                    Text(insight["insight"], style="body"),
                    Text(f"Confidence: {insight['confidence']:.0%}", style="caption", color=Color.GRAY)
                ], margin=Spacing.SMALL)
            )
        
        return Container(insights_list)


# ===== APP REGISTRATION =====

def create_raiderbot_dashboard():
    """Create and configure the RaiderBot dashboard app"""
    
    app = RaiderBotDashboardApp()
    
    # Configure app settings
    app.set_permissions(["view_logistics_data", "manage_dashboard"])
    app.set_auto_refresh(True)
    app.set_responsive(True)
    
    return app


# Export the app
RAIDERBOT_DASHBOARD_APP = create_raiderbot_dashboard()
