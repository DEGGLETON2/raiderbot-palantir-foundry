"""
RaiderBot Foundry Dataset Definitions
Based on existing Snowflake semantic layer from raiderbot-semantic-layer-complete.sql
"""

from foundry_dataset import Dataset
from foundry_transforms import transform
from pyspark.sql import functions as F
from pyspark.sql.types import *

# ===== RAW DATA SOURCES =====

# LoadMaster (McLeod) TMS System
ORDER_MASTER_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/order_master")
MOVEMENT_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/movement") 
STOPS_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/stops")
DRIVERS_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/drivers")
TRACTORS_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/tractors")
TRAILERS_RAW = Dataset("/RAIDER_EXPRESS/raw/loadmaster/trailers")

# TMWSuite (Trimble) Maintenance System
MAINTENANCE_RAW = Dataset("/RAIDER_EXPRESS/raw/tmw/maintenance_orders")
INSPECTION_RAW = Dataset("/RAIDER_EXPRESS/raw/tmw/inspections")
FUEL_DETAIL_RAW = Dataset("/RAIDER_EXPRESS/raw/tmw/fuel_detail")

# Volvo Telematics Real-time Data  
VOLVO_TELEMATICS_RAW = Dataset("/RAIDER_EXPRESS/raw/volvo/telematics")
GPS_TRACKING_RAW = Dataset("/RAIDER_EXPRESS/raw/volvo/gps_tracking")

# ===== FOUNDRY TRANSFORMS =====

@transform(
    order_master=ORDER_MASTER_RAW,
    movement=MOVEMENT_RAW,
    stops=STOPS_RAW,
    drivers=DRIVERS_RAW,
    tractors=TRACTORS_RAW,
    trailers=TRAILERS_RAW
)
def raiderbot_operations_core(order_master, movement, stops, drivers, tractors, trailers):
    """
    Core operational dataset - replaces RAIDERBOT_OPERATIONS view
    Combines order management, movement execution, and stop details
    """
    
    # Join core operational data
    operations = (
        order_master.alias("om")
        .join(movement.alias("m"), F.col("om.ID") == F.col("m.ORDER_ID"), "inner")
        .join(stops.alias("s"), F.col("m.ID") == F.col("s.MOVE_ID"), "inner") 
        .join(drivers.alias("d1"), F.col("m.DRIVER1_ID") == F.col("d1.ID"), "left")
        .join(drivers.alias("d2"), F.col("m.DRIVER2_ID") == F.col("d2.ID"), "left")
        .join(tractors.alias("t"), F.col("m.TRACTOR_ID") == F.col("t.ID"), "left")
        .join(trailers.alias("tr"), F.col("m.TRAILER_ID") == F.col("tr.ID"), "left")
    )
    
    # Calculate derived metrics
    operations_with_metrics = operations.select(
        # Order Context
        F.col("om.ID").alias("order_id"),
        F.col("om.ORDER_NUMBER").alias("order_number"),
        F.col("om.STATUS").alias("order_status"),
        F.col("om.SHIPPER_ID").alias("shipper_id"),
        F.col("om.CONSIGNEE_ID").alias("consignee_id"),
        F.col("om.SCHED_PICKUP").alias("scheduled_pickup"),
        F.col("om.SCHED_DELIVERY").alias("scheduled_delivery"),
        
        # Movement Execution
        F.col("m.ID").alias("move_id"),
        F.col("m.MOVE_NUMBER").alias("move_number"),
        F.col("m.DRIVER1_ID").alias("primary_driver_id"),
        F.col("m.DRIVER2_ID").alias("secondary_driver_id"),
        F.col("m.TRACTOR_ID").alias("tractor_id"),
        F.col("m.TRAILER_ID").alias("trailer_id"),
        F.col("m.ACTUAL_ARRIVAL").alias("actual_arrival"),
        F.col("m.ACTUAL_DEPARTURE").alias("actual_departure"),
        F.col("m.MOVE_DISTANCE").alias("move_distance"),
        
        # Stop Details
        F.col("s.STOP_TYPE").alias("stop_type"),
        F.col("s.LOCATION_ID").alias("location_id"),
        F.col("s.WEIGHT").alias("weight"),
        F.col("s.PIECES").alias("pieces"),
        F.col("s.ACTUAL_ARRIVAL").alias("stop_arrival"),
        F.col("s.ACTUAL_DEPARTURE").alias("stop_departure"),
        
        # Driver Information
        F.col("d1.FIRST_NAME").alias("primary_driver_first_name"),
        F.col("d1.LAST_NAME").alias("primary_driver_last_name"),
        F.col("d1.LICENSE_NUMBER").alias("primary_driver_license"),
        
        # Equipment Information
        F.col("t.TRACTOR_NUMBER").alias("tractor_number"),
        F.col("tr.TRAILER_NUMBER").alias("trailer_number"),
        
        # Calculated Performance Metrics
        F.when(
            F.col("m.ACTUAL_ARRIVAL") <= F.col("om.SCHED_DELIVERY"), 1
        ).otherwise(0).alias("on_time_flag"),
        
        F.round(
            (F.unix_timestamp("m.ACTUAL_ARRIVAL") - F.unix_timestamp("om.SCHED_DELIVERY")) / 60.0, 2
        ).alias("delivery_variance_minutes"),
        
        F.round(
            F.col("m.MOVE_DISTANCE") / F.greatest(
                (F.unix_timestamp("m.ACTUAL_ARRIVAL") - F.unix_timestamp("m.ACTUAL_DEPARTURE")) / 3600.0,
                F.lit(0.1)
            ), 2
        ).alias("average_mph"),
        
        # Timestamps
        F.current_timestamp().alias("processed_at")
    )
    
    return operations_with_metrics


@transform(
    drivers=DRIVERS_RAW,
    movement=MOVEMENT_RAW,
    inspections=INSPECTION_RAW,
    fuel_detail=FUEL_DETAIL_RAW
)
def raiderbot_driver_performance(drivers, movement, inspections, fuel_detail):
    """
    Driver performance analytics - replaces RAIDERBOT_DRIVER_PERFORMANCE view
    Comprehensive driver metrics including safety, efficiency, and compliance
    """
    
    # Calculate driver performance metrics
    driver_stats = (
        drivers.alias("d")
        .join(movement.alias("m"), F.col("d.ID") == F.col("m.DRIVER1_ID"), "left")
        .join(inspections.alias("i"), F.col("d.ID") == F.col("i.DRIVER_ID"), "left")
        .join(fuel_detail.alias("fd"), F.col("m.ID") == F.col("fd.MOVE_ID"), "left")
        .groupBy(
            "d.ID", "d.FIRST_NAME", "d.LAST_NAME", "d.LICENSE_NUMBER",
            "d.HIRE_DATE", "d.STATUS", "d.PHONE", "d.ADDRESS"
        )
        .agg(
            # Performance Metrics
            F.count("m.ID").alias("total_moves"),
            F.sum("m.MOVE_DISTANCE").alias("total_miles"),
            F.avg("m.MOVE_DISTANCE").alias("avg_miles_per_move"),
            
            # Safety Metrics
            F.countDistinct("i.ID").alias("total_inspections"),
            F.sum(F.when(F.col("i.RESULT") == "PASS", 1).otherwise(0)).alias("passed_inspections"),
            
            # Fuel Efficiency
            F.avg("fd.GALLONS").alias("avg_fuel_per_move"),
            F.sum("fd.COST").alias("total_fuel_cost"),
            
            # Time-based Metrics
            F.min("m.ACTUAL_DEPARTURE").alias("first_departure"),
            F.max("m.ACTUAL_ARRIVAL").alias("last_arrival"),
            
            # Processing timestamp
            F.current_timestamp().alias("processed_at")
        )
    )
    
    # Calculate additional derived metrics
    driver_performance = driver_stats.select(
        "*",
        # Safety Score (0-100)
        F.round(
            F.when(F.col("total_inspections") > 0,
                (F.col("passed_inspections") / F.col("total_inspections")) * 100
            ).otherwise(100), 2
        ).alias("safety_score"),
        
        # Fuel Efficiency (MPG)
        F.round(
            F.when(F.col("avg_fuel_per_move") > 0,
                F.col("avg_miles_per_move") / F.col("avg_fuel_per_move")
            ).otherwise(0), 2
        ).alias("avg_mpg"),
        
        # Activity Status
        F.when(
            F.datediff(F.current_date(), F.col("last_arrival")) <= 7, "ACTIVE"
        ).when(
            F.datediff(F.current_date(), F.col("last_arrival")) <= 30, "INACTIVE"
        ).otherwise("DORMANT").alias("activity_status")
    )
    
    return driver_performance


@transform(
    operations_core=raiderbot_operations_core
)
def raiderbot_delivery_performance(operations_core):
    """
    Delivery performance metrics - aggregated view for dashboard KPIs
    """
    
    # Daily delivery performance
    daily_performance = (
        operations_core
        .filter(F.col("stop_type") == "DELIVERY")
        .groupBy(F.to_date("actual_arrival").alias("delivery_date"))
        .agg(
            F.count("*").alias("total_deliveries"),
            F.sum("on_time_flag").alias("on_time_deliveries"),
            F.avg("delivery_variance_minutes").alias("avg_delivery_variance"),
            F.sum("weight").alias("total_weight_delivered"),
            F.sum("pieces").alias("total_pieces_delivered"),
            F.countDistinct("primary_driver_id").alias("active_drivers"),
            F.countDistinct("tractor_id").alias("active_tractors")
        )
        .select(
            "*",
            F.round(
                (F.col("on_time_deliveries") / F.col("total_deliveries")) * 100, 2
            ).alias("on_time_percentage"),
            F.current_timestamp().alias("processed_at")
        )
    )
    
    return daily_performance


@transform(
    volvo_telematics=VOLVO_TELEMATICS_RAW,
    gps_tracking=GPS_TRACKING_RAW,
    operations_core=raiderbot_operations_core
)
def raiderbot_real_time_tracking(volvo_telematics, gps_tracking, operations_core):
    """
    Real-time vehicle tracking and telematics data
    Combines Volvo telematics with operational context
    """
    
    # Join telematics with operational context
    real_time_data = (
        volvo_telematics.alias("vt")
        .join(gps_tracking.alias("gps"), 
              F.col("vt.VEHICLE_ID") == F.col("gps.VEHICLE_ID"), "inner")
        .join(operations_core.alias("ops"),
              F.col("vt.VEHICLE_ID") == F.col("ops.tractor_id"), "left")
        .select(
            # Vehicle Identity
            F.col("vt.VEHICLE_ID").alias("vehicle_id"),
            F.col("ops.tractor_number").alias("tractor_number"),
            F.col("ops.primary_driver_id").alias("driver_id"),
            F.col("ops.move_id").alias("current_move_id"),
            
            # Location Data
            F.col("gps.LATITUDE").alias("latitude"),
            F.col("gps.LONGITUDE").alias("longitude"),
            F.col("gps.HEADING").alias("heading"),
            F.col("gps.SPEED").alias("current_speed"),
            F.col("gps.RECORDED_TIME").alias("location_timestamp"),
            
            # Telematics Data
            F.col("vt.ENGINE_HOURS").alias("engine_hours"),
            F.col("vt.ODOMETER").alias("odometer"),
            F.col("vt.FUEL_LEVEL").alias("fuel_level_percent"),
            F.col("vt.ENGINE_RPM").alias("engine_rpm"),
            F.col("vt.COOLANT_TEMP").alias("coolant_temperature"),
            F.col("vt.HARSH_BRAKING_COUNT").alias("harsh_braking_events"),
            F.col("vt.HARSH_ACCELERATION_COUNT").alias("harsh_acceleration_events"),
            F.col("vt.IDLE_TIME_MINUTES").alias("idle_time_minutes"),
            
            # Operational Context
            F.col("ops.order_number").alias("current_order"),
            F.col("ops.scheduled_delivery").alias("eta"),
            F.col("ops.stop_type").alias("next_stop_type"),
            
            # Processing metadata
            F.current_timestamp().alias("processed_at")
        )
    )
    
    return real_time_data
