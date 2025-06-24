from foundry_ontology_api import ObjectType, Property

class Vehicle(ObjectType):
    """Vehicle object for Raider Express fleet management"""
    
    def __init__(self):
        super().__init__(
            api_name="Vehicle",
            display_name="Vehicle",
            description="Raider Express refrigerated trucks with telemetry and maintenance tracking"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="vehicle_id",
            display_name="Vehicle ID",
            property_type="string",
            required=True,
            description="Unique vehicle identifier"
        ))
        
        self.add_property(Property(
            api_name="truck_number",
            display_name="Truck Number",
            property_type="string",
            required=True,
            description="Raider Express truck fleet number"
        ))
        
        self.add_property(Property(
            api_name="vin",
            display_name="VIN",
            property_type="string",
            required=True,
            description="Vehicle Identification Number"
        ))
        
        # Vehicle Specifications
        self.add_property(Property(
            api_name="make",
            display_name="Make",
            property_type="string",
            description="Vehicle manufacturer"
        ))
        
        self.add_property(Property(
            api_name="model",
            display_name="Model",
            property_type="string",
            description="Vehicle model"
        ))
        
        self.add_property(Property(
            api_name="year",
            display_name="Year",
            property_type="integer",
            description="Model year"
        ))
        
        # Safety-First Properties (60mph governed)
        self.add_property(Property(
            api_name="max_speed",
            display_name="Max Speed",
            property_type="integer",
            description="Maximum governed speed (60mph for safety)"
        ))
        
        self.add_property(Property(
            api_name="speed_limiter_active",
            display_name="Speed Limiter Active",
            property_type="boolean",
            description="Whether 60mph speed limiter is active"
        ))
        
        # Refrigeration Properties
        self.add_property(Property(
            api_name="refrigeration_unit",
            display_name="Refrigeration Unit",
            property_type="boolean",
            description="Has refrigeration capability"
        ))
        
        self.add_property(Property(
            api_name="refrigeration_model",
            display_name="Refrigeration Model",
            property_type="string",
            description="Refrigeration unit model number"
        ))
        
        self.add_property(Property(
            api_name="min_temp_capability",
            display_name="Min Temperature Capability",
            property_type="double",
            description="Minimum temperature capability (Fahrenheit)"
        ))
        
        # Maintenance Properties
        self.add_property(Property(
            api_name="mileage",
            display_name="Current Mileage",
            property_type="double",
            description="Current odometer reading"
        ))
        
        self.add_property(Property(
            api_name="last_maintenance_date",
            display_name="Last Maintenance Date",
            property_type="date",
            description="Date of last maintenance service"
        ))
        
        self.add_property(Property(
            api_name="next_maintenance_due",
            display_name="Next Maintenance Due",
            property_type="date",
            description="Scheduled next maintenance date"
        ))
        
        # Performance Metrics
        self.add_property(Property(
            api_name="fuel_efficiency",
            display_name="Fuel Efficiency",
            property_type="double",
            description="Miles per gallon average"
        ))
        
        self.add_property(Property(
            api_name="vehicle_status",
            display_name="Vehicle Status",
            property_type="string",
            description="Current status (Active, Maintenance, Out of Service)"
        ))
        
        self.add_property(Property(
            api_name="current_location",
            display_name="Current Location",
            property_type="geopoint",
            description="Last known GPS location"
        ))