"""
RaiderBot KPI Functions for Foundry
Replaces existing Next.js API routes with Foundry Functions

Based on app/api/kpis.js and semantic layer queries
"""

from foundry_functions import Function, Input, Output
from foundry_functions.decorators import function
from foundry_datasets import Dataset, DatasetReader
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json


@function("get_delivery_kpis")
def get_delivery_kpis(
    days_back: Input[int] = 30,
    include_forecast: Input[bool] = False
) -> Output[Dict[str, Any]]:
    """
    Get key delivery performance indicators
    
    Replaces: app/api/kpis.js delivery metrics
    """
    
    # Access core datasets
    deliveries = DatasetReader("raiderbot.core.deliveries")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Filter deliveries within date range
    recent_deliveries = deliveries.filter(
        deliveries.actual_delivery >= start_date
    ).filter(
        deliveries.actual_delivery <= end_date
    )
    
    # Calculate KPIs
    total_deliveries = recent_deliveries.count()
    
    # On-time delivery rate
    on_time_deliveries = recent_deliveries.filter(
        recent_deliveries.on_time_flag == True
    ).count()
    
    on_time_rate = (on_time_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0
    
    # Average delivery variance
    avg_variance = recent_deliveries.select(
        recent_deliveries.delivery_variance_minutes
    ).agg({"delivery_variance_minutes": "mean"}).collect()[0][0] or 0
    
    # Daily delivery trend
    daily_deliveries = recent_deliveries.groupBy(
        deliveries.actual_delivery.cast("date").alias("delivery_date")
    ).agg(
        {"delivery_id": "count"}
    ).orderBy("delivery_date").collect()
    
    # Revenue metrics
    total_revenue = recent_deliveries.agg(
        {"revenue": "sum"}
    ).collect()[0][0] or 0
    
    avg_revenue_per_delivery = total_revenue / total_deliveries if total_deliveries > 0 else 0
    
    # Prepare response
    kpis = {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_back
        },
        "delivery_metrics": {
            "total_deliveries": total_deliveries,
            "on_time_rate": round(on_time_rate, 2),
            "avg_delivery_variance_minutes": round(avg_variance, 2),
            "daily_trend": [
                {
                    "date": row["delivery_date"].isoformat(),
                    "deliveries": row["count(delivery_id)"]
                }
                for row in daily_deliveries
            ]
        },
        "financial_metrics": {
            "total_revenue": round(total_revenue, 2),
            "avg_revenue_per_delivery": round(avg_revenue_per_delivery, 2)
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Add forecast if requested
    if include_forecast:
        kpis["forecast"] = _generate_delivery_forecast(recent_deliveries)
    
    return kpis


@function("get_driver_kpis")
def get_driver_kpis(
    days_back: Input[int] = 30,
    top_n: Input[int] = 10
) -> Output[Dict[str, Any]]:
    """
    Get driver performance indicators
    
    Replaces: driver-related KPI calculations
    """
    
    # Access datasets
    drivers = DatasetReader("raiderbot.core.drivers")
    driver_performance = DatasetReader("raiderbot.core.driver_performance")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Active drivers
    active_drivers = drivers.filter(
        drivers.status == "ACTIVE"
    ).filter(
        drivers.activity_status == "ACTIVE"
    )
    
    total_active_drivers = active_drivers.count()
    
    # Recent performance data
    recent_performance = driver_performance.filter(
        driver_performance.performance_date >= start_date
    )
    
    # Average safety score
    avg_safety_score = recent_performance.agg(
        {"safety_score": "mean"}
    ).collect()[0][0] or 0
    
    # Average fuel efficiency
    avg_fuel_efficiency = recent_performance.agg(
        {"avg_mpg": "mean"}
    ).collect()[0][0] or 0
    
    # Top performing drivers
    top_drivers = recent_performance.orderBy(
        recent_performance.safety_score.desc(),
        recent_performance.avg_mpg.desc()
    ).limit(top_n).collect()
    
    # Safety incidents
    safety_incidents = recent_performance.filter(
        recent_performance.accident_count > 0
    ).count()
    
    # Days since last incident
    last_incident_date = recent_performance.filter(
        recent_performance.accident_count > 0
    ).agg(
        {"performance_date": "max"}
    ).collect()[0][0]
    
    incident_free_days = 0
    if last_incident_date:
        incident_free_days = (datetime.now().date() - last_incident_date).days
    else:
        incident_free_days = days_back  # No incidents in period
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_back
        },
        "driver_metrics": {
            "total_active_drivers": total_active_drivers,
            "avg_safety_score": round(avg_safety_score, 2),
            "avg_fuel_efficiency": round(avg_fuel_efficiency, 2),
            "incident_free_days": incident_free_days,
            "safety_incidents_period": safety_incidents
        },
        "top_performers": [
            {
                "driver_id": row["driver_id"],
                "driver_name": f"{row['first_name']} {row['last_name']}",
                "safety_score": row["safety_score"],
                "fuel_efficiency": row["avg_mpg"],
                "total_moves": row["total_moves"]
            }
            for row in top_drivers
        ],
        "timestamp": datetime.now().isoformat()
    }


@function("get_vehicle_kpis")
def get_vehicle_kpis(
    days_back: Input[int] = 30,
    include_maintenance: Input[bool] = True
) -> Output[Dict[str, Any]]:
    """
    Get vehicle and fleet performance indicators
    """
    
    # Access datasets
    vehicles = DatasetReader("raiderbot.core.vehicles")
    vehicle_performance = DatasetReader("raiderbot.core.vehicle_performance")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Active vehicles
    active_vehicles = vehicles.filter(
        vehicles.status == "ACTIVE"
    )
    
    total_active_vehicles = active_vehicles.count()
    
    # Recent performance
    recent_performance = vehicle_performance.filter(
        vehicle_performance.performance_date >= start_date
    )
    
    # Fleet fuel efficiency
    avg_fleet_mpg = recent_performance.agg(
        {"avg_mpg": "mean"}
    ).collect()[0][0] or 0
    
    # Total miles driven
    total_miles = recent_performance.agg(
        {"total_miles": "sum"}
    ).collect()[0][0] or 0
    
    # Maintenance metrics
    maintenance_due = vehicles.filter(
        vehicles.next_service_due <= datetime.now() + timedelta(days=7)
    ).count()
    
    vehicles_in_maintenance = vehicles.filter(
        vehicles.status == "MAINTENANCE"
    ).count()
    
    # Utilization rate
    utilization_rate = ((total_active_vehicles - vehicles_in_maintenance) / 
                       total_active_vehicles * 100) if total_active_vehicles > 0 else 0
    
    kpis = {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_back
        },
        "fleet_metrics": {
            "total_active_vehicles": total_active_vehicles,
            "avg_fleet_mpg": round(avg_fleet_mpg, 2),
            "total_miles_period": round(total_miles, 2),
            "utilization_rate": round(utilization_rate, 2),
            "vehicles_in_maintenance": vehicles_in_maintenance
        },
        "timestamp": datetime.now().isoformat()
    }
    
    if include_maintenance:
        kpis["maintenance_metrics"] = {
            "maintenance_due_soon": maintenance_due,
            "currently_in_maintenance": vehicles_in_maintenance,
            "maintenance_schedule": _get_maintenance_schedule(vehicles)
        }
    
    return kpis


@function("get_route_optimization_kpis")
def get_route_optimization_kpis(
    days_back: Input[int] = 30
) -> Output[Dict[str, Any]]:
    """
    Get route optimization and efficiency metrics
    """
    
    # Access datasets
    routes = DatasetReader("raiderbot.core.routes")
    route_performance = DatasetReader("raiderbot.core.route_performance")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Recent route performance
    recent_routes = route_performance.filter(
        route_performance.performance_date >= start_date
    )
    
    # Optimization metrics
    total_routes = recent_routes.count()
    optimized_routes = recent_routes.filter(
        recent_routes.is_optimized == True
    ).count()
    
    optimization_rate = (optimized_routes / total_routes * 100) if total_routes > 0 else 0
    
    # Fuel savings
    total_fuel_savings = recent_routes.agg(
        {"fuel_savings_gallons": "sum"}
    ).collect()[0][0] or 0
    
    # Average route efficiency
    avg_route_efficiency = recent_routes.agg(
        {"route_efficiency_score": "mean"}
    ).collect()[0][0] or 0
    
    # Routes with high optimization potential
    high_potential_routes = routes.filter(
        routes.fuel_savings_potential > 5.0
    ).filter(
        routes.is_optimized == False
    ).count()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_back
        },
        "optimization_metrics": {
            "total_routes": total_routes,
            "optimization_rate": round(optimization_rate, 2),
            "fuel_savings_gallons": round(total_fuel_savings, 2),
            "avg_route_efficiency": round(avg_route_efficiency, 2),
            "high_potential_routes": high_potential_routes
        },
        "timestamp": datetime.now().isoformat()
    }


@function("get_comprehensive_dashboard_data")
def get_comprehensive_dashboard_data(
    days_back: Input[int] = 30,
    include_forecasts: Input[bool] = False,
    language: Input[str] = "EN"
) -> Output[Dict[str, Any]]:
    """
    Get all dashboard KPIs in a single function call
    
    Replaces: Multiple API calls from frontend dashboard
    """
    
    # Get all KPI data
    delivery_kpis = get_delivery_kpis(days_back, include_forecasts)
    driver_kpis = get_driver_kpis(days_back)
    vehicle_kpis = get_vehicle_kpis(days_back)
    route_kpis = get_route_optimization_kpis(days_back)
    
    # Combine into comprehensive dashboard data
    dashboard_data = {
        "summary": {
            "total_deliveries": delivery_kpis["delivery_metrics"]["total_deliveries"],
            "on_time_rate": delivery_kpis["delivery_metrics"]["on_time_rate"],
            "active_drivers": driver_kpis["driver_metrics"]["total_active_drivers"],
            "fleet_utilization": vehicle_kpis["fleet_metrics"]["utilization_rate"],
            "route_optimization_rate": route_kpis["optimization_metrics"]["optimization_rate"],
            "incident_free_days": driver_kpis["driver_metrics"]["incident_free_days"]
        },
        "delivery_performance": delivery_kpis,
        "driver_performance": driver_kpis,
        "fleet_performance": vehicle_kpis,
        "route_optimization": route_kpis,
        "metadata": {
            "language": language,
            "period_days": days_back,
            "includes_forecasts": include_forecasts,
            "generated_at": datetime.now().isoformat()
        }
    }
    
    # Localize labels if Spanish requested
    if language == "ES":
        dashboard_data = _localize_dashboard_data(dashboard_data, "ES")
    
    return dashboard_data


# ===== HELPER FUNCTIONS =====

def _generate_delivery_forecast(recent_deliveries) -> Dict[str, Any]:
    """Generate delivery forecast based on historical data"""
    
    # Simple trend-based forecast
    # In production, this would use more sophisticated ML models
    
    daily_counts = recent_deliveries.groupBy(
        recent_deliveries.actual_delivery.cast("date")
    ).agg(
        {"delivery_id": "count"}
    ).collect()
    
    if len(daily_counts) < 7:
        return {"error": "Insufficient data for forecast"}
    
    # Calculate moving average
    recent_avg = sum(row["count(delivery_id)"] for row in daily_counts[-7:]) / 7
    
    # Generate next 7 days forecast
    forecast_dates = []
    base_date = datetime.now().date()
    
    for i in range(1, 8):
        forecast_date = base_date + timedelta(days=i)
        # Simple trend with small random variation
        predicted_count = int(recent_avg * (0.95 + (i % 3) * 0.05))
        
        forecast_dates.append({
            "date": forecast_date.isoformat(),
            "predicted_deliveries": predicted_count,
            "confidence": 0.75  # Static confidence for demo
        })
    
    return {
        "forecast_period": "7_days",
        "base_average": round(recent_avg, 1),
        "forecast": forecast_dates
    }


def _get_maintenance_schedule(vehicles) -> List[Dict[str, Any]]:
    """Get upcoming maintenance schedule"""
    
    upcoming_maintenance = vehicles.filter(
        vehicles.next_service_due <= datetime.now() + timedelta(days=30)
    ).filter(
        vehicles.next_service_due >= datetime.now()
    ).orderBy(
        vehicles.next_service_due
    ).limit(10).collect()
    
    return [
        {
            "vehicle_id": row["vehicle_id"],
            "tractor_number": row["tractor_number"],
            "service_due_date": row["next_service_due"].isoformat(),
            "days_until_due": (row["next_service_due"].date() - datetime.now().date()).days,
            "service_type": "SCHEDULED_MAINTENANCE"  # Could be enhanced
        }
        for row in upcoming_maintenance
    ]


def _localize_dashboard_data(data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """Localize dashboard data labels for bilingual support"""
    
    if language != "ES":
        return data
    
    # Spanish translations for key labels
    translations = {
        "total_deliveries": "entregas_totales",
        "on_time_rate": "tasa_puntualidad",
        "active_drivers": "conductores_activos",
        "fleet_utilization": "utilizacion_flota",
        "route_optimization_rate": "tasa_optimizacion_rutas",
        "incident_free_days": "dias_sin_incidentes"
    }
    
    # Apply translations to summary section
    if "summary" in data:
        localized_summary = {}
        for key, value in data["summary"].items():
            localized_key = translations.get(key, key)
            localized_summary[localized_key] = value
        data["summary_es"] = localized_summary
    
    return data


# ===== FUNCTION REGISTRATION =====

# Register all functions for Foundry deployment
FUNCTIONS = [
    get_delivery_kpis,
    get_driver_kpis,
    get_vehicle_kpis,
    get_route_optimization_kpis,
    get_comprehensive_dashboard_data
]
