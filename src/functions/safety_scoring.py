"""
Safety Scoring Function - Comprehensive Driver Safety Analysis
Built on Palantir Foundry Functions for Raider Express
"""

from foundry_functions import function, String, Float, Dict
from foundry_ontology_sdk import FoundryClient
from foundry_datasets_api import DatasetClient
from datetime import datetime, timedelta
import pandas as pd

@function(
    runtime="foundry-python-3.9",
    description="Calculate comprehensive safety scores using Foundry data"
)
def calculate_safety_score(
    driver_id: String,
    time_period_days: Float = 90
) -> Dict:
    """
    Calculate driver safety score based on multiple factors.
    Emphasizes 60mph speed compliance as primary metric.
    
    Scoring factors:
    - Speed compliance (40% weight) - 60mph limit
    - Incident history (30% weight)
    - Hard braking events (15% weight)
    - Hours of service compliance (15% weight)
    """
    
    try:
        # Initialize Foundry clients
        dataset_client = DatasetClient()
        
        # Get driver data from multiple Foundry datasets
        end_date = datetime.now()
        start_date = end_date - timedelta(days=time_period_days)
        
        # Speed compliance score (60mph emphasis)
        speed_data = dataset_client.get_dataset("raider_vehicle_telemetry").to_pandas()
        driver_speed = speed_data[speed_data['driver_id'] == driver_id]
        speed_violations = len(driver_speed[driver_speed['speed'] > 60])
        total_readings = len(driver_speed)
        speed_compliance_rate = 1 - (speed_violations / max(total_readings, 1))
        speed_score = speed_compliance_rate * 100 * 0.4  # 40% weight
        
        # Incident history score
        incidents = dataset_client.get_dataset("raider_safety_incidents").to_pandas()
        driver_incidents = incidents[
            (incidents['driver_id'] == driver_id) &
            (incidents['incident_date'] >= start_date)
        ]
        incident_score = max(0, 100 - (len(driver_incidents) * 20)) * 0.3  # 30% weight
        
        # Hard braking score
        braking_events = driver_speed[driver_speed['hard_braking'] == True]
        braking_score = max(0, 100 - (len(braking_events) * 5)) * 0.15  # 15% weight
        
        # Hours of service compliance
        hos_data = dataset_client.get_dataset("raider_driver_logs").to_pandas()
        driver_hos = hos_data[hos_data['driver_id'] == driver_id]
        hos_violations = len(driver_hos[driver_hos['daily_hours'] > 11])
        hos_score = max(0, 100 - (hos_violations * 10)) * 0.15  # 15% weight
        
        # Calculate total score
        total_score = speed_score + incident_score + braking_score + hos_score
        
        return {
            "driver_id": driver_id,
            "safety_score": round(total_score, 2),
            "speed_compliance_rate": round(speed_compliance_rate * 100, 2),
            "components": {
                "speed_score": round(speed_score, 2),
                "incident_score": round(incident_score, 2),
                "braking_score": round(braking_score, 2),
                "hos_score": round(hos_score, 2)
            },
            "evaluation_period_days": time_period_days,
            "calculated_by": "Palantir Foundry Functions",
            "emphasis": "60mph speed compliance"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "foundry_function": "safety_scoring",
            "status": "failed"
        }
