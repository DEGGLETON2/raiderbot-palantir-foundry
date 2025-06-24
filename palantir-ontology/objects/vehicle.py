"""
Palantir Foundry Ontology Object: Vehicle
Defines the vehicle data model in Foundry's ontology system with 60mph governance emphasis
"""

from foundry_ontology_api import ObjectType, Property, LinkType

class Vehicle(ObjectType):
    """Vehicle object for Raider Express fleet in Palantir Foundry Ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="Vehicle",
            display_name="Raider Express Vehicle",
            description="Vehicle data model with 60mph governance in Palantir Foundry"
        )
        
        # Core vehicle properties
        self.add_property(Property(
            api_name="vehicle_id",
            display_name="Vehicle ID",
            property_type="string",
            required=True,
            description="Unique vehicle identifier in Foundry"
        ))
        
        self.add_property(Property(
            api_name="vin",
            display_name="VIN",
            property_type="string",
            required=True,
            description="Vehicle Identification Number"
        ))
        
        # 60mph Governance Properties
        self.add_property(Property(
            api_name="speed_governor_active",
            display_name="Speed Governor Active",
            property_type="boolean",
            required=True,
            default=True,
            description="60mph speed limiter status - MUST be true for operation"
        ))
        
        self.add_property(Property(
            api_name="max_speed_setting",
            display_name="Maximum Speed Setting",
            property_type="integer",
            required=True,
            default=60,
            description="Maximum speed in mph - governed at 60 for safety"
        ))
        
        # Foundry tracking
        self.add_property(Property(
            api_name="foundry_last_updated",
            display_name="Foundry Last Updated",
            property_type="timestamp",
            description="Last sync timestamp in Foundry datasets"
        ))
        
        # Maintenance properties
        self.add_property(Property(
            api_name="last_maintenance_date",
            display_name="Last Maintenance Date",
            property_type="date",
            description="Most recent maintenance completion"
        ))
        
        self.add_property(Property(
            api_name="maintenance_score",
            display_name="Maintenance Score",
            property_type="double",
            description="Overall maintenance health score (0-100)"
        ))
