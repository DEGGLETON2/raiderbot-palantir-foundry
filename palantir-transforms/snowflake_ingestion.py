"""
Snowflake Data Ingestion Transform for Palantir Foundry
Syncs transportation data from Snowflake to Foundry datasets
"""

from foundry_transforms import Transform, Input, Output
from foundry_transforms.types import DataFrame
from foundry_transforms.utils import log_metric
import snowflake.connector
from typing import Dict, Any
import pandas as pd
from datetime import datetime

class SnowflakeIngestion(Transform):
    """
    Transform to sync Raider Express data from Snowflake to Foundry
    Ensures data consistency for RaiderBot operations
    """
    
    # Input datasets (empty for Snowflake source)
    class Inputs:
        pass
    
    # Output datasets in Foundry
    class Outputs:
        deliveries = Output(
            dataset="raider_deliveries",
            description="Active delivery records"
        )
        drivers = Output(
            dataset="raider_drivers",
            description="Driver information and metrics"
        )
        vehicles = Output(
            dataset="raider_vehicles",
            description="Vehicle fleet data"
        )
        routes = Output(
            dataset="raider_routes",
            description="Delivery route information"
        )
    
    def get_snowflake_connection(self) -> snowflake.connector.SnowflakeConnection:
        """
        Establish connection to Snowflake using Foundry secrets
        """
        return snowflake.connector.connect(
            user="${FOUNDRY_SECRET:snowflake_user}",
            password="${FOUNDRY_SECRET:snowflake_password}",
            account="${FOUNDRY_SECRET:snowflake_account}",
            warehouse="RAIDER_WAREHOUSE",
            database="RAIDER_EXPRESS",
            schema="OPERATIONS"
        )
    
    def fetch_snowflake_data(self, query: str) -> pd.DataFrame:
        """
        Execute query and fetch data from Snowflake
        """
        conn = self.get_snowflake_connection()
        try:
            return pd.read_sql(query, conn)
        finally:
            conn.close()
    
    def transform(self) -> None:
        """
        Main transform logic to sync data from Snowflake to Foundry
        """
        start_time = datetime.now()
        
        # Fetch deliveries
        deliveries_df = self.fetch_snowflake_data("""
            SELECT 
                delivery_id,
                customer_id,
                driver_id,
                vehicle_id,
                route_id,
                status,
                scheduled_time,
                actual_time,
                is_on_time,
                max_speed,
                distance_miles,
                temperature_celsius
            FROM MCLEOD_DB.dbo.deliveries
            WHERE date_trunc('day', scheduled_time) >= current_date - 7
        """)
        
        # Fetch drivers
        drivers_df = self.fetch_snowflake_data("""
            SELECT 
                driver_id,
                name,
                license_number,
                safety_score,
                speed_violations,
                last_safety_training,
                status,
                active,
                total_deliveries,
                on_time_rate
            FROM MCLEOD_DB.dbo.drivers
            WHERE active = TRUE
        """)
        
        # Fetch vehicles
        vehicles_df = self.fetch_snowflake_data("""
            SELECT 
                vehicle_id,
                type,
                status,
                last_maintenance,
                total_miles,
                fuel_efficiency,
                temperature_system_status,
                max_speed_governor_active
            FROM MCLEOD_DB.dbo.vehicles
            WHERE status != 'retired'
        """)
        
        # Fetch routes
        routes_df = self.fetch_snowflake_data("""
            SELECT 
                route_id,
                start_location,
                end_location,
                distance_miles,
                estimated_time_minutes,
                actual_time_minutes,
                max_speed_recorded,
                safety_incidents
            FROM MCLEOD_DB.dbo.routes
            WHERE date_trunc('day', created_at) >= current_date - 7
        """)
        
        # Validate speed compliance
        speed_violations = (
            routes_df['max_speed_recorded'] > 60
        ).sum()
        
        if speed_violations > 0:
            self.log.warning(f"Found {speed_violations} routes exceeding 60mph limit")
        
        # Write to Foundry datasets
        self.outputs.deliveries.write_dataframe(deliveries_df)
        self.outputs.drivers.write_dataframe(drivers_df)
        self.outputs.vehicles.write_dataframe(vehicles_df)
        self.outputs.routes.write_dataframe(routes_df)
        
        # Log metrics
        duration = (datetime.now() - start_time).total_seconds()
        log_metric("snowflake_sync_duration_seconds", duration)
        log_metric("deliveries_synced", len(deliveries_df))
        log_metric("drivers_synced", len(drivers_df))
        log_metric("vehicles_synced", len(vehicles_df))
        log_metric("routes_synced", len(routes_df))
        log_metric("speed_violations", speed_violations)

# Foundry transform configuration
config = {
    "name": "snowflake_ingestion",
    "description": "Sync Raider Express data from Snowflake",
    "schedule": "*/15 * * * *",  # Every 15 minutes
    "timeout": 600,  # 10 minutes
    "retries": 3,
    "tags": ["raiderbot", "data-sync", "snowflake"]
} 