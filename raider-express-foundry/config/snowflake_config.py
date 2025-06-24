"""
Snowflake Configuration for Raider Express
Database connection and query configuration
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SnowflakeConfig:
    """Snowflake database configuration"""
    
    # Connection settings
    account: str = os.getenv("SNOWFLAKE_ACCOUNT", "raider-express.snowflakecomputing.com")
    username: str = os.getenv("SNOWFLAKE_USERNAME", "")
    password: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    database: str = os.getenv("SNOWFLAKE_DATABASE", "RAIDER_EXPRESS")
    schema: str = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    role: str = os.getenv("SNOWFLAKE_ROLE", "ANALYST")
    
    # Connection pool settings
    max_connections: int = 10
    connection_timeout: int = 60
    query_timeout: int = 300
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 5
    
    # Security settings
    ssl_verify: bool = True
    private_key_path: Optional[str] = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    
    def get_connection_params(self) -> Dict[str, str]:
        """Get connection parameters for Snowflake"""
        params = {
            "account": self.account,
            "user": self.username,
            "password": self.password,
            "warehouse": self.warehouse,
            "database": self.database,
            "schema": self.schema,
            "role": self.role
        }
        
        # Add private key authentication if available
        if self.private_key_path:
            params["private_key_path"] = self.private_key_path
            params.pop("password", None)  # Remove password when using key auth
            
        return params

@dataclass 
class SnowflakeTableConfig:
    """Configuration for Snowflake tables and views"""
    
    # Customer data tables
    customers_table: str = "CUSTOMERS"
    customer_addresses_table: str = "CUSTOMER_ADDRESSES"
    customer_contacts_table: str = "CUSTOMER_CONTACTS"
    
    # Order and delivery tables
    orders_table: str = "ORDERS"
    order_items_table: str = "ORDER_ITEMS"
    deliveries_table: str = "DELIVERIES"
    delivery_status_table: str = "DELIVERY_STATUS"
    
    # Fleet management tables
    vehicles_table: str = "VEHICLES"
    drivers_table: str = "DRIVERS"
    vehicle_maintenance_table: str = "VEHICLE_MAINTENANCE"
    driver_assignments_table: str = "DRIVER_ASSIGNMENTS"
    
    # Route and logistics tables
    routes_table: str = "ROUTES"
    route_stops_table: str = "ROUTE_STOPS"
    route_history_table: str = "ROUTE_HISTORY"
    
    # Financial tables
    invoices_table: str = "INVOICES"
    payments_table: str = "PAYMENTS"
    fuel_costs_table: str = "FUEL_COSTS"
    
    # Analytics views
    kpi_summary_view: str = "VW_KPI_SUMMARY"
    driver_performance_view: str = "VW_DRIVER_PERFORMANCE"
    route_efficiency_view: str = "VW_ROUTE_EFFICIENCY"
    
def get_snowflake_config() -> SnowflakeConfig:
    """Get Snowflake configuration"""
    return SnowflakeConfig()

def get_table_config() -> SnowflakeTableConfig:
    """Get table configuration"""
    return SnowflakeTableConfig()

def get_common_queries() -> Dict[str, str]:
    """Get common SQL queries for Raider Express data"""
    return {
        "active_drivers": """
            SELECT driver_id, first_name, last_name, status, hire_date
            FROM {schema}.DRIVERS 
            WHERE status = 'ACTIVE'
            ORDER BY last_name, first_name
        """,
        
        "fleet_status": """
            SELECT 
                vehicle_id,
                make,
                model,
                year,
                status,
                last_maintenance_date,
                mileage
            FROM {schema}.VEHICLES
            WHERE status IN ('ACTIVE', 'IN_USE')
            ORDER BY vehicle_id
        """,
        
        "daily_deliveries": """
            SELECT 
                DATE(delivery_date) as delivery_day,
                COUNT(*) as total_deliveries,
                COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_deliveries,
                COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed_deliveries
            FROM {schema}.DELIVERIES
            WHERE delivery_date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY DATE(delivery_date)
            ORDER BY delivery_day DESC
        """,
        
        "route_performance": """
            SELECT 
                route_id,
                AVG(actual_duration_minutes) as avg_duration,
                AVG(fuel_consumed_gallons) as avg_fuel_consumption,
                COUNT(*) as total_trips,
                AVG(on_time_percentage) as avg_on_time_rate
            FROM {schema}.ROUTE_HISTORY
            WHERE route_date >= CURRENT_DATE - INTERVAL '90 days'
            GROUP BY route_id
            ORDER BY avg_on_time_rate DESC
        """
    }

# Global configuration instances
SNOWFLAKE_CONFIG = get_snowflake_config()
TABLE_CONFIG = get_table_config()
COMMON_QUERIES = get_common_queries()