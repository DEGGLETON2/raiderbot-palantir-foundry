"""
Palantir Foundry Ontology Object: Customer
Defines the customer data model in Foundry's ontology system
"""

from foundry_ontology_api import ObjectType, Property, LinkType

class Customer(ObjectType):
    """Customer object for relationship management in Palantir Foundry Ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="Customer",
            display_name="Raider Express Customer",
            description="Customer relationship tracking in Foundry"
        )
        
        # Core customer properties
        self.add_property(Property(
            api_name="customer_id",
            display_name="Customer ID",
            property_type="string",
            required=True,
            description="Unique customer identifier in Foundry"
        ))
        
        self.add_property(Property(
            api_name="company_name",
            display_name="Company Name",
            property_type="string",
            required=True
        ))
        
        # Service preferences
        self.add_property(Property(
            api_name="preferred_delivery_window",
            display_name="Preferred Delivery Window",
            property_type="string",
            description="Customer's preferred delivery times"
        ))
        
        self.add_property(Property(
            api_name="temperature_requirements",
            display_name="Temperature Requirements",
            property_type="boolean",
            description="Requires temperature-controlled deliveries"
        ))
        
        # Relationship metrics
        self.add_property(Property(
            api_name="satisfaction_score",
            display_name="Customer Satisfaction Score",
            property_type="double",
            description="Overall satisfaction rating (0-100)"
        ))
        
        self.add_property(Property(
            api_name="lifetime_value",
            display_name="Customer Lifetime Value",
            property_type="double",
            description="Total revenue from customer"
        ))
        
        # Foundry integration
        self.add_property(Property(
            api_name="foundry_segment",
            display_name="Foundry Customer Segment",
            property_type="string",
            description="Customer segment from Foundry analytics"
        ))
