"""
Palantir Foundry Transform: KPI Calculations
Calculates real-time KPIs for RaiderBot dashboard
"""

from foundry_transforms import transform, Input, Output
from foundry_datasets_api import Dataset
import pandas as pd
from datetime import datetime, timedelta

@transform(
    raider_drivers=Input("ri.foundry.main.dataset.raider_drivers"),
    raider_deliveries=Input("ri.foundry.main.dataset.raider_deliveries"), 
    raider_vehicles=Input("ri.foundry.main.dataset.raider_vehicles"),
    raider_safety_incidents=Input("ri.foundry.main.dataset.raider_safety_incidents"),
    raider_kpi_dashboard=Output("ri.foundry.main.dataset.raider_kpi_dashboard")
)
def calculate_kpi_dashboard(
    raider_drivers, 
    raider_deliveries,
    raider_vehicles,
    raider_safety_incidents,
    raider_kpi_dashboard
):
    """
    Calculate KPIs using Foundry's transform engine.
    Powers the RaiderBot dashboard with real-time metrics.
    Runs every 5 minutes for fresh data.
    """
    
    # Load dataframes from Foundry inputs
    drivers_df = raider_drivers.dataframe()
    deliveries_df = raider_deliveries.dataframe()
    vehicles_df = raider_vehicles.dataframe()
    incidents_df = raider_safety_incidents.dataframe()
    
    # Current timestamp for this calculation run
    now = pd.Timestamp.now()
    today = now.date()
    
    # Driver KPIs
    total_drivers = len(drivers_df)
    active_drivers = len(drivers_df[drivers_df['status'] == 'active'])
    avg_safety_score = drivers_df[drivers_df['status'] == 'active']['safety_score'].mean()
    
    # Delivery KPIs (today's metrics)
    todays_deliveries = deliveries_df[
        pd.to_datetime(deliveries_df['scheduled_delivery']).dt.date == today
    ]
    total_deliveries_today = len(todays_deliveries)
    completed_deliveries = len(todays_deliveries[todays_deliveries['status'] == 'completed'])
    on_time_deliveries = len(todays_deliveries[
        (todays_deliveries['status'] == 'completed') &
        (todays_deliveries['actual_delivery'] <= todays_deliveries['scheduled_delivery'])
    ])
    on_time_rate = (on_time_deliveries / max(completed_deliveries, 1)) * 100
    
    # Vehicle KPIs (60mph compliance focus)
    total_vehicles = len(vehicles_df)
    compliant_vehicles = len(vehicles_df[
        (vehicles_df['speed_governor_active'] == True) &
        (vehicles_df['max_speed_setting'] == 60)
    ])
    compliance_rate = (compliant_vehicles / max(total_vehicles, 1)) * 100
    avg_maintenance_score = vehicles_df['maintenance_score'].mean()
    
    # Safety KPIs (last 30 days)
    recent_incidents = incidents_df[
        pd.to_datetime(incidents_df['incident_date']) >= (now - timedelta(days=30))
    ]
    total_incidents = len(recent_incidents)
    speed_related_incidents = len(recent_incidents[recent_incidents['speed_related'] == True])
    
    # Build KPI summary dictionary
    kpi_summary = {
        # Driver metrics
        'total_drivers': total_drivers,
        'active_drivers': active_drivers,
        'avg_safety_score': round(avg_safety_score, 2) if not pd.isna(avg_safety_score) else 0,
        
        # Delivery metrics
        'total_deliveries_today': total_deliveries_today,
        'completed_deliveries_today': completed_deliveries,
        'on_time_rate': round(on_time_rate, 2),
        
        # Vehicle metrics (60mph emphasis)
        'total_vehicles': total_vehicles,
        'speed_compliant_vehicles': compliant_vehicles,
        'speed_compliance_rate': round(compliance_rate, 2),
        'avg_maintenance_score': round(avg_maintenance_score, 2) if not pd.isna(avg_maintenance_score) else 0,
        
        # Safety metrics
        'incidents_last_30_days': total_incidents,
        'speed_related_incidents': speed_related_incidents,
        
        # Metadata
        'calculated_at': now,
        'foundry_transform': 'kpi_calculations',
        'data_freshness': 'real-time',
        'update_frequency': '5 minutes',
        'safety_focus': '60mph compliance'
    }
    
    # Convert to DataFrame for Foundry output
    kpi_df = pd.DataFrame([kpi_summary])
    
    # Write to Foundry output dataset
    raider_kpi_dashboard.write_dataframe(kpi_df)
    
    return f"KPI calculation complete at {now}. Metrics: {total_deliveries_today} deliveries, {on_time_rate:.1f}% on-time, {compliance_rate:.1f}% speed compliant"
