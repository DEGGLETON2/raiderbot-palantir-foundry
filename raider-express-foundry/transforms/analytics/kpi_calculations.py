from foundry_transforms_api import transform, Input, Output
from pyspark.sql import functions as F

@transform(
    kpi_dashboard=Output("ri.foundry.main.dataset.kpi_dashboard"),
    processed_deliveries=Input("ri.foundry.main.dataset.processed_deliveries"),
    processed_drivers=Input("ri.foundry.main.dataset.processed_drivers"),
    processed_vehicles=Input("ri.foundry.main.dataset.processed_vehicles"),
    telematics_processed=Input("ri.foundry.main.dataset.telematics_processed")
)
def calculate_raiderbot_kpis(processed_deliveries, processed_drivers, processed_vehicles, telematics_processed):
    """
    Calculate main KPIs for RaiderBot dashboard
    """
    
    # Get current date for filtering
    today = F.current_date()
    
    # Total Deliveries (Today)
    total_deliveries_today = (processed_deliveries.df
                             .filter(F.col("delivery_date") == today)
                             .count())
    
    # Total Deliveries (This Week)
    total_deliveries_week = (processed_deliveries.df
                            .filter(F.col("delivery_date") >= F.date_sub(today, 7))
                            .count())
    
    # Active Drivers
    active_drivers = (processed_drivers.df
                     .filter(F.col("driver_status_category") == "Available")
                     .count())
    
    # On-Time Rate (Today)
    on_time_stats = (processed_deliveries.df
                    .filter(F.col("delivery_date") == today)
                    .agg(
                        F.avg("on_time_flag").alias("on_time_rate"),
                        F.count("*").alias("total_deliveries_calc")
                    ).collect()[0])
    
    on_time_rate = on_time_stats["on_time_rate"] if on_time_stats["on_time_rate"] else 0
    
    # Route Efficiency
    route_efficiency = (telematics_processed.df
                       .filter(F.date_format("timestamp", "yyyy-MM-dd") == F.date_format(today, "yyyy-MM-dd"))
                       .agg(
                           F.avg("instantaneous_mpg").alias("avg_fuel_efficiency"),
                           F.avg("behavior_score").alias("avg_safety_score")
                       ).collect()[0])
    
    fuel_efficiency = route_efficiency["avg_fuel_efficiency"] if route_efficiency["avg_fuel_efficiency"] else 0
    
    # Customer Satisfaction
    customer_satisfaction = (processed_deliveries.df
                            .filter(F.col("delivery_date") >= F.date_sub(today, 7))
                            .agg(F.avg("customer_satisfaction_score").alias("avg_satisfaction"))
                            .collect()[0]["avg_satisfaction"]) or 0
    
    # Safety Metrics
    safety_violations_today = (telematics_processed.df
                              .filter(F.date_format("timestamp", "yyyy-MM-dd") == F.date_format(today, "yyyy-MM-dd"))
                              .agg(F.sum("speed_violation").alias("total_violations"))
                              .collect()[0]["total_violations"]) or 0
    
    # Create KPI summary DataFrame
    kpi_data = [
        {
            "kpi_name": "Total Deliveries",
            "kpi_value": total_deliveries_today,
            "kpi_trend": total_deliveries_week - (total_deliveries_today * 7),  # Approximate trend
            "kpi_target": 50,  # Daily target
            "kpi_category": "Operations",
            "last_updated": F.current_timestamp(),
            "time_period": "Today"
        },
        {
            "kpi_name": "Active Drivers", 
            "kpi_value": active_drivers,
            "kpi_trend": 0,  # Will be calculated with historical data
            "kpi_target": 25,  # Target active drivers
            "kpi_category": "Resources",
            "last_updated": F.current_timestamp(),
            "time_period": "Current"
        },
        {
            "kpi_name": "On-Time Rate",
            "kpi_value": round(on_time_rate * 100, 2),
            "kpi_trend": 0,  # Will be calculated with historical data
            "kpi_target": 95.0,  # 95% on-time target
            "kpi_category": "Performance", 
            "last_updated": F.current_timestamp(),
            "time_period": "Today"
        },
        {
            "kpi_name": "Route Efficiency",
            "kpi_value": round(fuel_efficiency, 2),
            "kpi_trend": 0,
            "kpi_target": 6.5,  # Target MPG
            "kpi_category": "Efficiency",
            "last_updated": F.current_timestamp(),
            "time_period": "Today"
        },
        {
            "kpi_name": "Customer Satisfaction",
            "kpi_value": round(customer_satisfaction, 1),
            "kpi_trend": 0,
            "kpi_target": 90.0,
            "kpi_category": "Quality",
            "last_updated": F.current_timestamp(),
            "time_period": "This Week"
        },
        {
            "kpi_name": "Safety Violations",
            "kpi_value": safety_violations_today,
            "kpi_trend": 0,
            "kpi_target": 0,  # Zero tolerance for speed violations
            "kpi_category": "Safety",
            "last_updated": F.current_timestamp(),
            "time_period": "Today"
        }
    ]
    
    return spark.createDataFrame(kpi_data)

@transform(
    driver_performance_summary=Output("ri.foundry.main.dataset.driver_performance_summary"),
    processed_deliveries=Input("ri.foundry.main.dataset.processed_deliveries"),
    processed_drivers=Input("ri.foundry.main.dataset.processed_drivers"),
    telematics_processed=Input("ri.foundry.main.dataset.telematics_processed")
)
def calculate_driver_performance(processed_deliveries, processed_drivers, telematics_processed):
    """
    Calculate individual driver performance metrics
    """
    
    # Deliveries per driver (last 30 days)
    driver_deliveries = (processed_deliveries.df
                        .filter(F.col("delivery_date") >= F.date_sub(F.current_date(), 30))
                        .groupBy("driver_id")
                        .agg(
                            F.count("*").alias("total_deliveries"),
                            F.avg("on_time_flag").alias("on_time_rate"),
                            F.avg("customer_satisfaction_score").alias("avg_customer_satisfaction"),
                            F.sum("delivery_duration_hours").alias("total_drive_hours")
                        ))
    
    # Safety metrics per driver
    driver_safety = (telematics_processed.df
                    .filter(F.col("timestamp") >= F.date_sub(F.current_timestamp(), 30))
                    .groupBy("driver_id")
                    .agg(
                        F.avg("behavior_score").alias("avg_safety_score"),
                        F.sum("speed_violation").alias("total_speed_violations"),
                        F.sum("harsh_braking_event").alias("total_harsh_braking"),
                        F.sum("harsh_acceleration_event").alias("total_harsh_acceleration"),
                        F.avg("instantaneous_mpg").alias("avg_fuel_efficiency")
                    ))
    
    # Join with driver master data
    return (processed_drivers.df
            .join(driver_deliveries, "driver_id", "left")
            .join(driver_safety, "driver_id", "left")
            .fillna(0)  # Fill nulls with 0 for new drivers
            
            # Calculate composite performance score
            .withColumn("performance_score",
                (F.coalesce(F.col("on_time_rate"), F.lit(0)) * 30) +
                (F.coalesce(F.col("avg_safety_score"), F.lit(0)) * 0.4) +
                (F.coalesce(F.col("avg_customer_satisfaction"), F.lit(0)) * 0.3))
            
            # Performance tier classification
            .withColumn("performance_tier",
                F.when(F.col("performance_score") >= 85, "Excellent")
                .when(F.col("performance_score") >= 75, "Good")
                .when(F.col("performance_score") >= 65, "Average")
                .otherwise("Needs Improvement"))
            
            .select(
                "driver_id", "driver_name", "preferred_language", "years_experience",
                "total_deliveries", "on_time_rate", "avg_customer_satisfaction",
                "avg_safety_score", "total_speed_violations", "avg_fuel_efficiency",
                "performance_score", "performance_tier", "driver_status_category"
            ))