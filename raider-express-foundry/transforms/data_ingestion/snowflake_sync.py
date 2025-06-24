from foundry_transforms_api import transform, Input, Output
from pyspark.sql import functions as F
from pyspark.sql.types import *

@transform(
    processed_deliveries=Output("ri.foundry.main.dataset.processed_deliveries"),
    snowflake_deliveries=Input("ri.foundry.main.dataset.snowflake_deliveries")
)
def sync_deliveries_from_snowflake(snowflake_deliveries):
    """
    Sync and process delivery data from Snowflake with RaiderBot enhancements
    """
    return (snowflake_deliveries.df
            .withColumn("company_name", F.lit("Raider Express"))
            .withColumn("home_base", F.lit("Fort Worth, TX"))
            
            # Calculate delivery status
            .withColumn("delivery_status", 
                F.when(F.col("actual_delivery_time").isNotNull(), "completed")
                .when(F.col("estimated_delivery_time") < F.current_timestamp(), "delayed")
                .when(F.col("pickup_time").isNotNull(), "in_transit")
                .otherwise("scheduled"))
            
            # Calculate on-time performance
            .withColumn("on_time_flag", 
                F.when(F.col("actual_delivery_time") <= F.col("scheduled_delivery_time"), 1)
                .otherwise(0))
            
            # Calculate delivery duration
            .withColumn("delivery_duration_hours",
                F.when(F.col("actual_delivery_time").isNotNull(),
                    F.round((F.unix_timestamp("actual_delivery_time") - 
                            F.unix_timestamp("pickup_time")) / 3600, 2)))
            
            # Temperature compliance for refrigerated loads
            .withColumn("temp_compliance",
                F.when(F.col("required_temp").isNotNull(),
                    F.when((F.col("actual_temp_min") >= F.col("required_temp_min")) & 
                           (F.col("actual_temp_max") <= F.col("required_temp_max")), 1)
                    .otherwise(0))
                .otherwise(1))  # Non-refrigerated loads default to compliant
            
            # Customer satisfaction score calculation
            .withColumn("customer_satisfaction_score",
                F.when(F.col("on_time_flag") == 1, 
                    F.when(F.col("temp_compliance") == 1, 100)
                    .otherwise(85))
                .when(F.col("delivery_status") == "delayed",
                    F.when(F.col("delay_hours") <= 2, 75)
                    .when(F.col("delay_hours") <= 4, 60)
                    .otherwise(40))
                .otherwise(50))
            
            # Add safety flags
            .withColumn("safety_incident_flag",
                F.when(F.col("incident_type").isNotNull(), 1).otherwise(0))
            
            # Business hours delivery flag
            .withColumn("business_hours_delivery",
                F.when((F.hour("actual_delivery_time") >= 8) & 
                       (F.hour("actual_delivery_time") <= 17), 1)
                .otherwise(0))
    )

@transform(
    processed_drivers=Output("ri.foundry.main.dataset.processed_drivers"),
    snowflake_drivers=Input("ri.foundry.main.dataset.snowflake_drivers")
)
def sync_drivers_from_snowflake(snowflake_drivers):
    """
    Process driver data with performance metrics
    """
    return (snowflake_drivers.df
            .withColumn("years_experience", 
                F.round((F.unix_timestamp() - F.unix_timestamp("hire_date")) / (365.25 * 24 * 3600), 1))
            
            # Language preference for bilingual support
            .withColumn("preferred_language",
                F.when(F.col("primary_language").isNull(), "English")
                .otherwise(F.col("primary_language")))
            
            # Driver status classification
            .withColumn("driver_status_category",
                F.when(F.col("status") == "active", "Available")
                .when(F.col("status") == "on_route", "Driving")
                .when(F.col("status") == "off_duty", "Off Duty")
                .otherwise("Unknown"))
            
            # CDL classification
            .withColumn("cdl_class_valid",
                F.when(F.col("cdl_expiration") > F.current_date(), 1)
                .otherwise(0))
            
            # Safety score placeholder (will be calculated by functions)
            .withColumn("safety_score", F.lit(0.0))
            .withColumn("performance_score", F.lit(0.0))
    )

@transform(
    processed_vehicles=Output("ri.foundry.main.dataset.processed_vehicles"),
    snowflake_vehicles=Input("ri.foundry.main.dataset.snowflake_vehicles")
)
def sync_vehicles_from_snowflake(snowflake_vehicles):
    """
    Process vehicle data with Raider Express specifications
    """
    return (snowflake_vehicles.df
            # Raider Express specific: 60mph governed trucks
            .withColumn("max_governed_speed", F.lit(60))
            .withColumn("is_governed", F.lit(True))
            
            # Vehicle age calculation
            .withColumn("vehicle_age_years",
                F.year(F.current_date()) - F.col("model_year"))
            
            # Refrigeration capability
            .withColumn("is_refrigerated",
                F.when(F.col("trailer_type") == "refrigerated", True)
                .otherwise(False))
            
            # Maintenance status
            .withColumn("maintenance_due_soon",
                F.when(F.col("next_maintenance_date") <= F.date_add(F.current_date(), 30), 1)
                .otherwise(0))
            
            # Vehicle utilization (will be calculated by analytics)
            .withColumn("daily_utilization_hours", F.lit(0.0))
            .withColumn("fuel_efficiency_mpg", F.lit(0.0))
            
            # Safety equipment status
            .withColumn("safety_equipment_status", F.lit("Compliant"))
    )