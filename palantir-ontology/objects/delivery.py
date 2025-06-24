"""
Palantir Foundry Ontology Object: Delivery
Defines the delivery data model in Foundry's ontology system
"""

from foundry_ontology_api import ObjectType, Property, LinkType

class Delivery(ObjectType):
    """Delivery object for shipment tracking in Palantir Foundry Ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="Delivery", 
            display_name="Raider Express Delivery",
            description="Delivery tracking with temperature compliance in Foundry"
        )
        
        # Core delivery properties
        self.add_property(Property(
            api_name="delivery_id",
            display_name="Delivery ID", 
            property_type="string",
            required=True,
            description="Unique delivery identifier in Foundry"
        ))
        
        self.add_property(Property(
            api_name="status",
            display_name="Delivery Status",
            property_type="string",
            required=True
        ))
        
        # Temperature compliance
        self.add_property(Property(
            api_name="temperature_controlled",
            display_name="Temperature Controlled",
            property_type="boolean",
            description="Requires temperature monitoring"
        ))
        
        self.add_property(Property(
            api_name="temperature_range",
            display_name="Required Temperature Range",
            property_type="string",
            description="Required temperature range in Fahrenheit"
        ))
        
        # Timing properties
        self.add_property(Property(
            api_name="scheduled_delivery",
            display_name="Scheduled Delivery Time",
            property_type="timestamp",
            required=True
        ))
        
        self.add_property(Property(
            api_name="actual_delivery",
            display_name="Actual Delivery Time", 
            property_type="timestamp"
        ))
        
        # Foundry tracking
        self.add_property(Property(
            api_name="foundry_dataset_source",
            display_name="Foundry Dataset Source",
            property_type="string",
            default="raider_deliveries"
        ))
