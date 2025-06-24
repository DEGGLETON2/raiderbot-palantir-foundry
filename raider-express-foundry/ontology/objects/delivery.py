from foundry_ontology_api import ObjectType, Property

class Delivery(ObjectType):
    """Delivery object for tracking shipments and performance"""
    
    def __init__(self):
        super().__init__(
            api_name="Delivery",
            display_name="Delivery",
            description="Individual delivery shipments with tracking and performance metrics"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="delivery_id",
            display_name="Delivery ID",
            property_type="string",
            required=True,
            description="Unique delivery identifier"
        ))
        
        self.add_property(Property(
            api_name="order_number",
            display_name="Order Number",
            property_type="string",
            required=True,
            description="Customer order number"
        ))
        
        # Customer Information
        self.add_property(Property(
            api_name="customer_name",
            display_name="Customer Name",
            property_type="string",
            required=True,
            description="Customer company name"
        ))
        
        self.add_property(Property(
            api_name="customer_contact",
            display_name="Customer Contact",
            property_type="string",
            description="Primary customer contact person"
        ))
        
        self.add_property(Property(
            api_name="customer_phone",
            display_name="Customer Phone",
            property_type="string",
            description="Customer contact phone number"
        ))
        
        # Location Properties
        self.add_property(Property(
            api_name="pickup_location",
            display_name="Pickup Location",
            property_type="geopoint",
            required=True,
            description="Pickup GPS coordinates"
        ))
        
        self.add_property(Property(
            api_name="pickup_address",
            display_name="Pickup Address",
            property_type="string",
            description="Pickup street address"
        ))
        
        self.add_property(Property(
            api_name="delivery_location",
            display_name="Delivery Location",
            property_type="geopoint",
            required=True,
            description="Delivery GPS coordinates"
        ))
        
        self.add_property(Property(
            api_name="delivery_address",
            display_name="Delivery Address",
            property_type="string",
            description="Delivery street address"
        ))
        
        # Timing Properties
        self.add_property(Property(
            api_name="scheduled_pickup_time",
            display_name="Scheduled Pickup Time",
            property_type="timestamp",
            required=True,
            description="Scheduled pickup date and time"
        ))
        
        self.add_property(Property(
            api_name="actual_pickup_time",
            display_name="Actual Pickup Time",
            property_type="timestamp",
            description="Actual pickup date and time"
        ))
        
        self.add_property(Property(
            api_name="scheduled_delivery_time",
            display_name="Scheduled Delivery Time",
            property_type="timestamp",
            required=True,
            description="Scheduled delivery date and time"
        ))
        
        self.add_property(Property(
            api_name="actual_delivery_time",
            display_name="Actual Delivery Time",
            property_type="timestamp",
            description="Actual delivery date and time"
        ))
        
        # Cargo Properties
        self.add_property(Property(
            api_name="cargo_type",
            display_name="Cargo Type",
            property_type="string",
            description="Type of refrigerated cargo"
        ))
        
        self.add_property(Property(
            api_name="required_temperature",
            display_name="Required Temperature",
            property_type="double",
            description="Required temperature (Fahrenheit)"
        ))
        
        self.add_property(Property(
            api_name="temperature_maintained",
            display_name="Temperature Maintained",
            property_type="boolean",
            description="Whether temperature was maintained throughout delivery"
        ))
        
        # Performance Metrics
        self.add_property(Property(
            api_name="delivery_status",
            display_name="Delivery Status",
            property_type="string",
            description="Current status (Scheduled, In Transit, Delivered, Delayed)"
        ))
        
        self.add_property(Property(
            api_name="on_time_pickup",
            display_name="On-Time Pickup",
            property_type="boolean",
            description="Whether pickup was completed on time"
        ))
        
        self.add_property(Property(
            api_name="on_time_delivery",
            display_name="On-Time Delivery",
            property_type="boolean",
            description="Whether delivery was completed on time"
        ))
        
        self.add_property(Property(
            api_name="customer_satisfaction",
            display_name="Customer Satisfaction",
            property_type="double",
            description="Customer satisfaction rating (1-10)"
        ))
        
        # Documentation
        self.add_property(Property(
            api_name="delivery_notes",
            display_name="Delivery Notes",
            property_type="string",
            description="Driver notes about delivery"
        ))
        
        self.add_property(Property(
            api_name="signature_captured",
            display_name="Signature Captured",
            property_type="boolean",
            description="Whether customer signature was captured"
        ))