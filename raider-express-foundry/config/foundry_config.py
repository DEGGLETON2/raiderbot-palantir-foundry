"""
Foundry Configuration for Raider Express
Centralized configuration management for the Foundry platform
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class FoundryConfig:
    """Main Foundry configuration class"""
    
    # Foundry connection settings
    foundry_url: str = "https://roiderxpress.palantirfoundry.com"
    auth_token: str = os.getenv("FOUNDRY_AUTH_TOKEN", "")
    
    # Project settings
    project_name: str = "raider-express-foundry"
    organization: str = "raider-express"
    environment: str = os.getenv("FOUNDRY_ENV", "production")
    
    # Dataset paths
    raw_data_path: str = "/raider-express/raw-data"
    processed_data_path: str = "/raider-express/processed"
    analytics_data_path: str = "/raider-express/analytics"
    ml_features_path: str = "/raider-express/ml-features"
    
    # API endpoints
    api_base_url: str = f"{foundry_url}/api/v1"
    functions_base_url: str = f"{foundry_url}/functions"
    
    # Security settings
    ssl_verify: bool = True
    request_timeout: int = 30
    max_retries: int = 3

@dataclass
class DatasetConfig:
    """Dataset-specific configuration"""
    
    # Raw datasets
    telematics_raw: str = "/raider-express/raw-data/telematics"
    snowflake_raw: str = "/raider-express/raw-data/snowflake"
    customer_raw: str = "/raider-express/raw-data/customers"
    
    # Processed datasets
    vehicles_processed: str = "/raider-express/processed/vehicles"
    drivers_processed: str = "/raider-express/processed/drivers"
    routes_processed: str = "/raider-express/processed/routes"
    deliveries_processed: str = "/raider-express/processed/deliveries"
    
    # Analytics datasets
    kpi_metrics: str = "/raider-express/analytics/kpi-metrics"
    driver_performance: str = "/raider-express/analytics/driver-performance"
    route_analytics: str = "/raider-express/analytics/route-analytics"
    safety_metrics: str = "/raider-express/analytics/safety-metrics"
    
    # ML feature datasets
    driver_features: str = "/raider-express/ml-features/driver-features"
    vehicle_features: str = "/raider-express/ml-features/vehicle-features"
    route_features: str = "/raider-express/ml-features/route-features"
    predictive_features: str = "/raider-express/ml-features/predictive-features"

@dataclass
class ApplicationConfig:
    """Application-specific configuration"""
    
    # Dashboard settings
    dashboard_refresh_interval: int = 30  # seconds
    max_chart_data_points: int = 1000
    
    # Mobile app settings
    mobile_sync_interval: int = 300  # 5 minutes
    offline_mode_duration: int = 3600  # 1 hour
    
    # Chat interface settings
    chat_max_context_length: int = 4000
    chat_response_timeout: int = 30
    
    # Map settings
    default_map_center: tuple = (39.8283, -98.5795)  # Geographic center of US
    default_zoom_level: int = 4

def get_foundry_config() -> FoundryConfig:
    """Get the main Foundry configuration"""
    return FoundryConfig()

def get_dataset_config() -> DatasetConfig:
    """Get dataset configuration"""
    return DatasetConfig()

def get_application_config() -> ApplicationConfig:
    """Get application configuration"""
    return ApplicationConfig()

def get_environment_variables() -> Dict[str, Any]:
    """Get all relevant environment variables"""
    return {
        "FOUNDRY_URL": os.getenv("FOUNDRY_URL", "https://roiderxpress.palantirfoundry.com"),
        "FOUNDRY_AUTH_TOKEN": os.getenv("FOUNDRY_AUTH_TOKEN", ""),
        "FOUNDRY_ENV": os.getenv("FOUNDRY_ENV", "production"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "DEBUG": os.getenv("DEBUG", "false").lower() == "true",
        "PROJECT_NAME": os.getenv("PROJECT_NAME", "raider-express-foundry"),
    }

# Global configuration instances
FOUNDRY_CONFIG = get_foundry_config()
DATASET_CONFIG = get_dataset_config()
APPLICATION_CONFIG = get_application_config()
ENV_VARS = get_environment_variables()