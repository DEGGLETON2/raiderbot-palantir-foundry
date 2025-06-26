"""
RaiderBot Foundry Ontology Definition
Defines the semantic data model for logistics operations

Based on existing semantic layer and business domain knowledge
"""

from foundry_ontology import Ontology, ObjectType, PropertyType, LinkType
from foundry_ontology.decorators import object_type, property_type, link_type
from datetime import datetime
from typing import Optional, List

# ===== ONTOLOGY DEFINITION =====

@object_type("Delivery")
class Delivery:
    """Individual delivery operation - core business object"""
    
    # Primary identifiers
    delivery_id: str
    order_number: str
    move_number: str
    
    # Scheduling
    scheduled_pickup: datetime
    scheduled_delivery: datetime
    actual_pickup: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    
    # Performance metrics
    on_time_flag: bool = False
    delivery_variance_minutes: Optional[float] = None
    
    # Cargo details
    weight: Optional[float] = None
    pieces: Optional[int] = None
    commodity: Optional[str] = None
    
    # Status tracking
    status: str = "SCHEDULED"  # SCHEDULED, IN_TRANSIT, DELIVERED, CANCELLED
    
    # Location context
    origin_city: Optional[str] = None
    origin_state: Optional[str] = None
    destination_city: Optional[str] = None
    destination_state: Optional[str] = None
    
    # Financial
    revenue: Optional[float] = None
    cost: Optional[float] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime


@object_type("Driver")
class Driver:
    """Driver entity with performance and safety metrics"""
    
    # Personal information
    driver_id: str
    first_name: str
    last_name: str
    license_number: str
    hire_date: datetime
    
    # Contact information
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    
    # Employment status
    status: str = "ACTIVE"  # ACTIVE, INACTIVE, TERMINATED
    activity_status: str = "ACTIVE"  # ACTIVE, INACTIVE, DORMANT
    
    # Performance metrics
    total_moves: int = 0
    total_miles: float = 0.0
    avg_miles_per_move: Optional[float] = None
    
    # Safety metrics
    safety_score: float = 100.0
    total_inspections: int = 0
    passed_inspections: int = 0
    accident_count: int = 0
    violation_count: int = 0
    
    # Efficiency metrics
    avg_mpg: Optional[float] = None
    avg_fuel_per_move: Optional[float] = None
    total_fuel_cost: Optional[float] = None
    
    # Language preferences (for bilingual support)
    preferred_language: str = "EN"  # EN, ES
    
    # Metadata
    last_activity: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


@object_type("Vehicle")
class Vehicle:
    """Vehicle/Tractor entity with maintenance and performance data"""
    
    # Vehicle identification
    vehicle_id: str
    tractor_number: str
    vin: Optional[str] = None
    license_plate: Optional[str] = None
    
    # Specifications
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine_type: Optional[str] = None
    
    # Operational status
    status: str = "ACTIVE"  # ACTIVE, MAINTENANCE, OUT_OF_SERVICE
    current_location: Optional[str] = None
    
    # Performance metrics
    total_miles: float = 0.0
    engine_hours: float = 0.0
    avg_mpg: Optional[float] = None
    
    # Maintenance tracking
    last_service_date: Optional[datetime] = None
    next_service_due: Optional[datetime] = None
    maintenance_cost_ytd: Optional[float] = None
    
    # Real-time telematics (when available)
    current_speed: Optional[float] = None
    fuel_level_percent: Optional[float] = None
    engine_rpm: Optional[int] = None
    coolant_temperature: Optional[float] = None
    idle_time_minutes: Optional[float] = None
    harsh_braking_events: int = 0
    harsh_acceleration_events: int = 0
    
    # GPS coordinates
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None
    location_timestamp: Optional[datetime] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime


@object_type("Route")
class Route:
    """Route entity representing planned or executed paths"""
    
    # Route identification
    route_id: str
    route_name: Optional[str] = None
    
    # Geographic data
    origin_city: str
    origin_state: str
    destination_city: str
    destination_state: str
    total_distance: float
    
    # Performance metrics
    estimated_duration_hours: Optional[float] = None
    actual_duration_hours: Optional[float] = None
    fuel_efficiency_mpg: Optional[float] = None
    
    # Optimization data
    is_optimized: bool = False
    optimization_score: Optional[float] = None
    fuel_savings_potential: Optional[float] = None
    
    # Traffic and conditions
    traffic_delay_minutes: Optional[float] = None
    weather_conditions: Optional[str] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime


@object_type("Customer")
class Customer:
    """Customer/Shipper/Consignee entity"""
    
    # Customer identification
    customer_id: str
    customer_name: str
    customer_type: str  # SHIPPER, CONSIGNEE, BOTH
    
    # Location information
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    
    # Contact information
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    # Business metrics
    total_shipments: int = 0
    total_revenue: Optional[float] = None
    avg_shipment_value: Optional[float] = None
    
    # Service level
    on_time_rate: Optional[float] = None
    satisfaction_score: Optional[float] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime


@object_type("Inspection")
class Inspection:
    """Safety inspection entity"""
    
    # Inspection identification
    inspection_id: str
    inspection_type: str  # DOT, COMPANY, RANDOM
    inspection_date: datetime
    
    # Results
    result: str  # PASS, FAIL, WARNING
    score: Optional[float] = None
    
    # Violations and issues
    violations_count: int = 0
    violation_categories: Optional[List[str]] = None
    notes: Optional[str] = None
    
    # Inspector information
    inspector_name: Optional[str] = None
    inspection_location: Optional[str] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime


# ===== LINK TYPES =====

@link_type("performs")
class DriverPerformsDelivery:
    """Links Driver to Delivery they performed"""
    
    # Role specification
    role: str = "PRIMARY"  # PRIMARY, SECONDARY, TEAM
    
    # Performance metrics for this specific delivery
    performance_score: Optional[float] = None
    safety_incidents: int = 0
    fuel_efficiency: Optional[float] = None
    
    # Metadata
    linked_at: datetime


@link_type("uses")
class DeliveryUsesVehicle:
    """Links Delivery to Vehicle used"""
    
    # Usage metrics
    start_odometer: Optional[float] = None
    end_odometer: Optional[float] = None
    fuel_consumed: Optional[float] = None
    
    # Metadata
    linked_at: datetime


@link_type("follows")
class DeliveryFollowsRoute:
    """Links Delivery to Route followed"""
    
    # Adherence metrics
    route_adherence_percent: Optional[float] = None
    deviation_miles: Optional[float] = None
    
    # Metadata
    linked_at: datetime


@link_type("serves")
class DeliveryServesCustomer:
    """Links Delivery to Customer (shipper/consignee)"""
    
    # Relationship type
    relationship_type: str  # PICKUP, DELIVERY
    
    # Service metrics
    service_time_minutes: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    
    # Metadata
    linked_at: datetime


@link_type("inspects")
class InspectionInspectsDriver:
    """Links Inspection to Driver being inspected"""
    
    # Context
    inspection_context: str  # ROUTINE, POST_INCIDENT, RANDOM
    
    # Metadata
    linked_at: datetime


@link_type("inspects")
class InspectionInspectsVehicle:
    """Links Inspection to Vehicle being inspected"""
    
    # Context
    inspection_context: str  # ROUTINE, PRE_TRIP, POST_TRIP, MAINTENANCE
    
    # Metadata
    linked_at: datetime


# ===== PROPERTY TYPES =====

@property_type("performance_metric")
class PerformanceMetric:
    """Reusable performance metric property"""
    
    metric_name: str
    metric_value: float
    metric_unit: str
    measurement_date: datetime
    is_target_met: bool = False
    target_value: Optional[float] = None


@property_type("location_data")
class LocationData:
    """Reusable location property"""
    
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    timestamp: datetime


@property_type("safety_event")
class SafetyEvent:
    """Safety-related event property"""
    
    event_type: str  # ACCIDENT, VIOLATION, INCIDENT, NEAR_MISS
    event_date: datetime
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: Optional[str] = None
    cost_impact: Optional[float] = None
    resolved: bool = False


# ===== ONTOLOGY CONFIGURATION =====

def create_raiderbot_ontology() -> Ontology:
    """Create and configure the complete RaiderBot ontology"""
    
    ontology = Ontology(
        name="RaiderBot Logistics Analytics",
        description="Comprehensive ontology for transportation and logistics operations",
        version="1.0.0"
    )
    
    # Register object types
    ontology.register_object_type(Delivery)
    ontology.register_object_type(Driver)
    ontology.register_object_type(Vehicle)
    ontology.register_object_type(Route)
    ontology.register_object_type(Customer)
    ontology.register_object_type(Inspection)
    
    # Register link types
    ontology.register_link_type(DriverPerformsDelivery)
    ontology.register_link_type(DeliveryUsesVehicle)
    ontology.register_link_type(DeliveryFollowsRoute)
    ontology.register_link_type(DeliveryServesCustomer)
    ontology.register_link_type(InspectionInspectsDriver)
    ontology.register_link_type(InspectionInspectsVehicle)
    
    # Register property types
    ontology.register_property_type(PerformanceMetric)
    ontology.register_property_type(LocationData)
    ontology.register_property_type(SafetyEvent)
    
    return ontology


# ===== BUSINESS LOGIC QUERIES =====

class RaiderBotOntologyQueries:
    """Pre-defined queries for common business questions"""
    
    @staticmethod
    def get_delivery_performance_today():
        """Get today's delivery performance metrics"""
        return {
            "query": "SELECT COUNT(*) as total_deliveries, AVG(on_time_flag) as on_time_rate FROM Delivery WHERE actual_delivery >= TODAY()",
            "description": "Today's delivery performance"
        }
    
    @staticmethod
    def get_top_performing_drivers(limit: int = 10):
        """Get top performing drivers by safety score and efficiency"""
        return {
            "query": f"SELECT * FROM Driver ORDER BY safety_score DESC, avg_mpg DESC LIMIT {limit}",
            "description": f"Top {limit} performing drivers"
        }
    
    @staticmethod
    def get_vehicles_needing_maintenance():
        """Get vehicles requiring maintenance"""
        return {
            "query": "SELECT * FROM Vehicle WHERE next_service_due <= TODAY() + 7 OR status = 'MAINTENANCE'",
            "description": "Vehicles needing maintenance in next 7 days"
        }
    
    @staticmethod
    def get_route_optimization_opportunities():
        """Get routes with optimization potential"""
        return {
            "query": "SELECT * FROM Route WHERE is_optimized = false AND fuel_savings_potential > 5.0",
            "description": "Routes with significant optimization potential"
        }
    
    @staticmethod
    def get_safety_alerts():
        """Get current safety alerts and incidents"""
        return {
            "query": "SELECT d.*, i.* FROM Driver d JOIN Inspection i ON d.driver_id = i.driver_id WHERE i.result = 'FAIL' AND i.inspection_date >= TODAY() - 30",
            "description": "Recent safety inspection failures"
        }


# ===== EXPORT =====

if __name__ == "__main__":
    # Create ontology instance
    raiderbot_ontology = create_raiderbot_ontology()
    
    # Validate ontology structure
    print(f"Ontology '{raiderbot_ontology.name}' created successfully")
    print(f"Object types: {len(raiderbot_ontology.object_types)}")
    print(f"Link types: {len(raiderbot_ontology.link_types)}")
    print(f"Property types: {len(raiderbot_ontology.property_types)}")
