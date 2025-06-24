from transforms.api import transform, Input, Output
from pyspark.sql import functions as F
from pyspark.sql.window import Window

@transform(
    raider_kpi_dashboard=Output("ri.foundry.main.dataset.raider_kpi_dashboard"),
    raider_deliveries=Input("ri.foundry.main.dataset.raider_deliveries"),
    raider_drivers=Input("ri.foundry.main.dataset.raider_drivers"),
    raider_vehicles=Input("ri.foundry.main.dataset.raider_vehicles"),
    raider_routes=Input("ri.foundry.main.dataset.raider_routes")
)
def calculate_kpi_dashboard(raider_deliveries, raider_drivers, raider_vehicles, raider_routes):
    """
    Calculate main KPI metrics for RaiderBot dashboard
    """
    current_date = F.current_date()
    
    # Total Deliveries (today)
    total_deliveries_today = (raider_deliveries.df
        .filter(F.col("delivery_date") == current_date)
        .count())
    
    # Total Deliveries (this week)
    total_deliveries_week = (raider_deliveries.df
        .filter(F.col("delivery_date") >= F.date_sub(current_date, 7))
        .count())
    
    # Active Drivers
    active_drivers = (raider_drivers.df
        .filter(F.col("driver_status").isin(["Available", "On Route"]))
        .count())
    
    # On-Time Rate (today)
    on_time_stats_today = (raider_deliveries.df
        .filter(F.col("delivery_date") == current_date)
        .agg(
            F.avg(F.when(F.col("on_time_delivery"), 1.0).otherwise(0.0)).alias("on_time_rate"),
            F.count("delivery_id").alias("total_deliveries")
        )
        .collect()[0])
    
    # On-Time Rate (this week)
    on_time_stats_week = (raider_deliveries.df
        .filter(F.col("delivery_date") >= F.date_sub(current_date, 7))
        .agg(
            F.avg(F.when(F.col("on_time_delivery"), 1.0).otherwise(0.0)).alias("on_time_rate"),
            F.count("delivery_id").alias("total_deliveries")
        )
        .collect()[0])
    
    # Route Efficiency
    route_efficiency_stats = (raider_routes.df
        .filter(F.col("route_date") >= F.date_sub(current_date, 7))
        .agg(
            F.avg("efficiency_score").alias("avg_efficiency_score"),
            F.avg("fuel_efficiency").alias("avg_fuel_efficiency"),
            F.sum("optimization_savings").alias("total_optimization_savings")
        )
        .collect()[0])
    
    # Safety Metrics
    safety_stats = (raider_drivers.df
        .agg(
            F.avg("safety_score").alias("avg_safety_score"),
            F.avg("speed_compliance_rate").alias("avg_speed_compliance"),
            F.sum("safety_violations_count").alias("total_safety_violations")
        )
        .collect()[0])
    
    # Create KPI summary
    kpi_data = [
        {
            "metric_name": "total_deliveries_today",
            "metric_value": total_deliveries_today,
            "metric_type": "count",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "total_deliveries_week", 
            "metric_value": total_deliveries_week,
            "metric_type": "count",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "active_drivers",
            "metric_value": active_drivers,
            "metric_type": "count", 
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "on_time_rate_today",
            "metric_value": on_time_stats_today["on_time_rate"] * 100,
            "metric_type": "percentage",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "on_time_rate_week",
            "metric_value": on_time_stats_week["on_time_rate"] * 100,
            "metric_type": "percentage",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "route_efficiency_score",
            "metric_value": route_efficiency_stats["avg_efficiency_score"],
            "metric_type": "score",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "fuel_efficiency",
            "metric_value": route_efficiency_stats["avg_fuel_efficiency"],
            "metric_type": "mpg",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "safety_score",
            "metric_value": safety_stats["avg_safety_score"],
            "metric_type": "score",
            "last_updated": F.current_timestamp()
        },
        {
            "metric_name": "speed_compliance_rate",
            "metric_value": safety_stats["avg_speed_compliance"],
            "metric_type": "percentage",
            "last_updated": F.current_timestamp()
        }
    ]
    
    return spark.createDataFrame(kpi_data)

@transform(
    driver_performance_summary=Output("ri.foundry.main.dataset.driver_performance_summary"),
    raider_drivers=Input("ri.foundry.main.dataset.raider_drivers"),
    raider_deliveries=Input("ri.foundry.main.dataset.raider_deliveries"),
    raider_routes=Input("ri.foundry.main.dataset.raider_routes")
)
def calculate_driver_performance(raider_drivers, raider_deliveries, raider_routes):
    """
    Calculate comprehensive driver performance metrics
    """
    # Driver delivery performance
    driver_delivery_stats = (raider_deliveries.df
        .filter(F.col("delivery_date") >= F.date_sub(F.current_date(), 30))
        .groupBy("driver_id")
        .agg(
            F.count("delivery_id").alias("total_deliveries_30d"),
            F.avg(F.when(F.col("on_time_delivery"), 1.0).otherwise(0.0)).alias("on_time_rate_30d"),
            F.avg("customer_satisfaction").alias("avg_customer_satisfaction"),
            F.sum(F.when(F.col("temperature_maintained") == False, 1).otherwise(0)).alias("temp_violations_30d")
        ))
    
    # Driver route performance
    driver_route_stats = (raider_routes.df
        .filter(F.col("route_date") >= F.date_sub(F.current_date(), 30))
        .groupBy("driver_id")
        .agg(
            F.avg("efficiency_score").alias("avg_efficiency_score_30d"),
            F.avg("fuel_efficiency").alias("avg_fuel_efficiency_30d"),
            F.sum("speed_violations").alias("speed_violations_30d"),
            F.avg("average_speed").alias("avg_speed_30d")
        ))
    
    # Combine with base driver data
    driver_performance = (raider_drivers.df
        .join(driver_delivery_stats, "driver_id", "left")
        .join(driver_route_stats, "driver_id", "left")
        .fillna(0)
        .withColumn("overall_performance_score",
                   (F.col("safety_score") * 0.3 +
                    F.col("on_time_rate_30d") * 100 * 0.3 +
                    F.col("avg_efficiency_score_30d") * 0.2 +
                    F.col("avg_customer_satisfaction") * 10 * 0.2))
        .withColumn("performance_tier",
                   F.when(F.col("overall_performance_score") >= 90, "Excellent")
                    .when(F.col("overall_performance_score") >= 80, "Good")
                    .when(F.col("overall_performance_score") >= 70, "Satisfactory")
                    .otherwise("Needs Improvement"))
    )
    
    return driver_performance