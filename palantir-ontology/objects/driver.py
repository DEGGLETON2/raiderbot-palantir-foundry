"""
Driver Object Definition for Palantir Foundry
Part of RaiderBot's transportation ontology
"""

from foundry_ontology import Object, Property, Link
from foundry_ontology.types import String, Integer, Float, Boolean, DateTime
from foundry_ontology.constraints import Range, Pattern

class Driver(Object):
    """
    Driver object representing a Raider Express truck driver
    Includes safety-focused attributes and performance metrics
    """
    
    # Basic Information
    driver_id = Property(
        type=String,
        description="Unique driver identifier",
        required=True,
        pattern=Pattern(r"DR\d{6}")  # Format: DR123456
    )
    
    name = Property(
        type=String,
        description="Driver's full name",
        required=True
    )
    
    license_number = Property(
        type=String,
        description="Commercial Driver's License (CDL) number",
        required=True
    )
    
    # Safety Metrics
    safety_score = Property(
        type=Float,
        description="Overall safety rating (0-100)",
        required=True,
        constraints=[Range(min=0, max=100)]
    )
    
    speed_violations = Property(
        type=Integer,
        description="Number of times exceeded 60mph limit",
        required=True,
        default=0
    )
    
    last_safety_training = Property(
        type=DateTime,
        description="Date of last safety training completion",
        required=True
    )
    
    # Operational Status
    status = Property(
        type=String,
        description="Current driver status",
        required=True,
        allowed_values=[
            "available",
            "on_route",
            "off_duty",
            "maintenance",
            "training"
        ]
    )
    
    active = Property(
        type=Boolean,
        description="Whether driver is currently active",
        required=True,
        default=True
    )
    
    # Performance Metrics
    total_deliveries = Property(
        type=Integer,
        description="Total number of completed deliveries",
        required=True,
        default=0
    )
    
    on_time_rate = Property(
        type=Float,
        description="Percentage of on-time deliveries",
        required=True,
        constraints=[Range(min=0, max=100)],
        default=100.0
    )
    
    # Relationships
    vehicle = Link(
        target="Vehicle",
        description="Currently assigned vehicle",
        cardinality="one"
    )
    
    deliveries = Link(
        target="Delivery",
        description="Associated deliveries",
        cardinality="many"
    )
    
    routes = Link(
        target="Route",
        description="Assigned routes",
        cardinality="many"
    )
    
    safety_incidents = Link(
        target="SafetyIncident",
        description="Recorded safety incidents",
        cardinality="many"
    )
    
    # Metadata
    created_at = Property(
        type=DateTime,
        description="Record creation timestamp",
        required=True,
        auto_now=True
    )
    
    updated_at = Property(
        type=DateTime,
        description="Last update timestamp",
        required=True,
        auto_now=True
    )
    
    class Meta:
        """Foundry object metadata"""
        description = "Raider Express truck driver with safety focus"
        display_name = "Driver"
        icon = "🚛"
        indexes = ["driver_id", "name", "status"]
        audit_enabled = True 