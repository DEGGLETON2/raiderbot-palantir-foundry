from transforms.api import transform, Input, Output
from pyspark.sql import functions as F
from pyspark.sql.types import *

@transform(
    raider_drivers=Output("ri.foundry.main.dataset.raider_drivers"),
    snowflake_hr_data=Input("ri.foundry.main.dataset.snowflake_hr_data"),
    snowflake_driver_performance=Input("ri.foundry.main.dataset.snowflake_driver_performance")
)
def sync_driver_data(snowflake_hr_data, snowflake_driver_performance):
    """
    Sync driver data from Snowflake HR and performance systems
    """
    hr_data = snowflake_hr_data.df
    performance_data = snowflake_driver_performance.df
    
    # Join HR and performance data
    driver_data = hr_data.join(
        performance_data,
        hr_data.employee_id == performance_data.driver_id,
        "left"
    )
    
    # Add RaiderBot-specific calculations
    enhanced_drivers = (driver_data
        .withColumn("years_experience", 
                   F.datediff(F.current_date(), F.col("hire_date")) / 365.25)
        .withColumn("safety_score", 
                   F.when(F.col("safety_violations") == 0, 100)
                    .when(F.col("safety_violations") <= 2, 85)
                    .when(F.col("safety_violations") <= 5, 70)
                    .otherwise(50))
        .withColumn("speed_compliance_rate",
                   F.when(F.col("avg_speed") <= 60, 100)
                    .when(F.col("avg_speed") <= 62, 90)
                    .when(F.col("avg_speed") <= 65, 75)
                    .otherwise(50))
        .withColumn("preferred_language",
                   F.when(F.col("spanish_speaker") == True, "Spanish")
                    .otherwise("English"))
        .withColumn("driver_status",
                   F.when(F.col("currently_driving") == True, "On Route")
                    .when(F.col("available") == True, "Available")
                    .otherwise("Off Duty"))
    )
    
    return enhanced_drivers

@transform(
    raider_vehicles=Output("ri.foundry.main.dataset.raider_vehicles"),
    snowflake_fleet_data=Input("ri.foundry.main.dataset.snowflake_fleet_data"),
    snowflake_maintenance_data=Input("ri.foundry.main.dataset.snowflake_maintenance_data")
)
def sync_vehicle_data(snowflake_fleet_data, snowflake_maintenance_data):
    """
    Sync vehicle data from Snowflake fleet management system
    """
    fleet_data = snowflake_fleet_data.df
    maintenance_data = snowflake_maintenance_data.df
    
    # Join fleet and maintenance data
    vehicle_data = fleet_data.join(
        maintenance_data,
        fleet_data.vehicle_id == maintenance_data.vehicle_id,
        "left"
    )
    
    # Add RaiderBot-specific enhancements
    enhanced_vehicles = (vehicle_data
        .withColumn("max_speed", F.lit(60))  # All trucks governed at 60mph
        .withColumn("speed_limiter_active", F.lit(True))
        .withColumn("refrigeration_unit", 
                   F.when(F.col("unit_type").contains("REEFER"), True).otherwise(False))
        .withColumn("vehicle_status",
                   F.when(F.col("in_maintenance") == True, "Maintenance")
                    .when(F.col("out_of_service") == True, "Out of Service")
                    .otherwise("Active"))
        .withColumn("fuel_efficiency",
                   F.col("total_miles") / F.col("total_fuel_consumed"))
        .withColumn("next_maintenance_due",
                   F.date_add(F.col("last_maintenance_date"), 
                             F.col("maintenance_interval_days")))
    )
    
    return enhanced_vehicles

@transform(
    raider_deliveries=Output("ri.foundry.main.dataset.raider_deliveries"),
    snowflake_orders=Input("ri.foundry.main.dataset.snowflake_orders"),
    snowflake_tracking=Input("ri.foundry.main.dataset.snowflake_tracking")
)
def sync_delivery_data(snowflake_orders, snowflake_tracking):
    """
    Sync delivery data from Snowflake order management and tracking systems
    """
    orders = snowflake_orders.df
    tracking = snowflake_tracking.df
    
    # Join orders and tracking data
    delivery_data = orders.join(
        tracking,
        orders.order_id == tracking.order_id,
        "left"
    )
    
    # Calculate performance metrics
    enhanced_deliveries = (delivery_data
        .withColumn("on_time_pickup",
                   F.when(F.col("actual_pickup_time") <= F.col("scheduled_pickup_time"), True)
                    .otherwise(False))
        .withColumn("on_time_delivery",
                   F.when(F.col("actual_delivery_time") <= F.col("scheduled_delivery_time"), True)
                    .otherwise(False))
        .withColumn("delivery_status",
                   F.when(F.col("actual_delivery_time").isNotNull(), "Delivered")
                    .when(F.col("actual_pickup_time").isNotNull(), "In Transit")
                    .when(F.col("scheduled_pickup_time") < F.current_timestamp(), "Delayed")
                    .otherwise("Scheduled"))
        .withColumn("temperature_maintained",
                   F.when((F.col("min_temp_recorded") >= F.col("required_temperature") - 2) &
                         (F.col("max_temp_recorded") <= F.col("required_temperature") + 2), True)
                    .otherwise(False))
        .withColumn("customer_satisfaction",
                   F.when(F.col("on_time_delivery") & F.col("temperature_maintained"), 10)
                    .when(F.col("on_time_delivery") | F.col("temperature_maintained"), 8)
                    .otherwise(6))
    )
    
    return enhanced_deliveries

@transform(
    raider_routes=Output("ri.foundry.main.dataset.raider_routes"),
    raider_deliveries=Input("ri.foundry.main.dataset.raider_deliveries"),
    snowflake_gps_data=Input("ri.foundry.main.dataset.snowflake_gps_data")
)
def calculate_route_data(raider_deliveries, snowflake_gps_data):
    """
    Calculate route data and performance metrics
    """
    deliveries = raider_deliveries.df
    gps_data = snowflake_gps_data.df
    
    # Group deliveries by route
    route_deliveries = (deliveries
        .groupBy("route_id", "route_date", "driver_id", "vehicle_id")
        .agg(
            F.count("delivery_id").alias("delivery_count"),
            F.sum(F.when(F.col("on_time_delivery"), 1).otherwise(0)).alias("on_time_deliveries"),
            F.min("actual_pickup_time").alias("route_start_time"),
            F.max("actual_delivery_time").alias("route_end_time")
        )
    )
    
    # Calculate route metrics from GPS data
    route_gps = (gps_data
        .groupBy("route_id")
        .agg(
            F.sum("distance_traveled").alias("actual_miles"),
            F.sum("fuel_consumed").alias("fuel_consumed"),
            F.avg("speed").alias("average_speed"),
            F.max("speed").alias("max_speed_recorded"),
            F.sum(F.when(F.col("speed") > 60, 1).otherwise(0)).alias("speed_violations")
        )
    )
    
    # Combine route data
    complete_routes = route_deliveries.join(route_gps, "route_id", "left")
    
    # Calculate efficiency metrics
    enhanced_routes = (complete_routes
        .withColumn("fuel_efficiency", F.col("actual_miles") / F.col("fuel_consumed"))
        .withColumn("efficiency_score",
                   F.when(F.col("speed_violations") == 0, 
                         F.greatest(F.lit(0), 100 - (F.col("actual_miles") - F.col("planned_miles")) * 2))
                    .otherwise(F.greatest(F.lit(0), 75 - F.col("speed_violations") * 5)))
        .withColumn("route_status",
                   F.when(F.col("route_end_time").isNotNull(), "Completed")
                    .when(F.col("route_start_time").isNotNull(), "Active")
                    .otherwise("Planned"))
        .withColumn("optimization_savings",
                   F.greatest(F.lit(0), F.col("planned_miles") - F.col("actual_miles")))
    )
    
    return enhanced_routes