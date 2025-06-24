from foundry_transforms_api import transform, Input, Output
from pyspark.sql import functions as F
from pyspark.sql.window import Window

@transform(
    telematics_processed=Output("ri.foundry.main.dataset.telematics_processed"),
    telematics_raw=Input("ri.foundry.main.dataset.telematics_stream")
)
def process_telematics_data(telematics_raw):
    """
    Process real-time telematics data with safety-first approach
    """
    
    # Window specification for time-based calculations
    window_1hour = Window.partitionBy("vehicle_id").orderBy("timestamp").rangeBetween(-3600, 0)
    window_daily = Window.partitionBy("vehicle_id", F.date_format("timestamp", "yyyy-MM-dd"))
    
    return (telematics_raw.df
            # Safety-first: Flag speed violations (60mph limit)
            .withColumn("speed_violation",
                F.when(F.col("speed_mph") > 60, 1).otherwise(0))
            
            # Calculate safety metrics
            .withColumn("harsh_braking_event",
                F.when(F.col("deceleration_g") < -0.5, 1).otherwise(0))
            
            .withColumn("harsh_acceleration_event",
                F.when(F.col("acceleration_g") > 0.5, 1).otherwise(0))
            
            .withColumn("hard_cornering_event",
                F.when(F.abs(F.col("lateral_g")) > 0.5, 1).otherwise(0))
            
            # Following distance safety
            .withColumn("safe_following_distance",
                F.when(F.col("following_distance_sec") >= 3, 1).otherwise(0))
            
            # Fuel efficiency calculations
            .withColumn("instantaneous_mpg",
                F.when(F.col("fuel_rate_gph") > 0,
                    F.col("speed_mph") / F.col("fuel_rate_gph"))
                .otherwise(0))
            
            # Rolling averages for smoother metrics
            .withColumn("avg_speed_1hr",
                F.avg("speed_mph").over(window_1hour))
            
            .withColumn("safety_events_1hr",
                (F.sum("harsh_braking_event").over(window_1hour) +
                 F.sum("harsh_acceleration_event").over(window_1hour) +
                 F.sum("hard_cornering_event").over(window_1hour)))
            
            # Daily aggregates
            .withColumn("daily_miles",
                F.sum(F.col("speed_mph") / 60).over(window_daily))  # Approximate miles
            
            .withColumn("daily_fuel_consumption",
                F.sum("fuel_rate_gph").over(window_daily) / 60)  # Convert to gallons
            
            # Idle time calculation
            .withColumn("idle_time_minutes",
                F.when((F.col("speed_mph") == 0) & (F.col("engine_rpm") > 600), 1)
                .otherwise(0))
            
            # Driver behavior score (real-time)
            .withColumn("behavior_score",
                F.greatest(F.lit(0),
                    F.lit(100) - 
                    (F.col("speed_violation") * 20) -
                    (F.col("harsh_braking_event") * 10) -
                    (F.col("harsh_acceleration_event") * 10) -
                    (F.col("hard_cornering_event") * 5) -
                    (F.when(F.col("safe_following_distance") == 0, 15).otherwise(0))))
            
            # Temperature monitoring for refrigerated units
            .withColumn("reefer_temp_alarm",
                F.when(F.col("reefer_temp").isNotNull(),
                    F.when((F.col("reefer_temp") < F.col("target_temp") - 5) |
                           (F.col("reefer_temp") > F.col("target_temp") + 5), 1)
                    .otherwise(0))
                .otherwise(0))
            
            # Location-based insights
            .withColumn("in_fort_worth_area",
                F.when((F.abs(F.col("latitude") - 32.7555) < 0.5) &
                       (F.abs(F.col("longitude") - (-97.3308)) < 0.5), 1)
                .otherwise(0))
    )