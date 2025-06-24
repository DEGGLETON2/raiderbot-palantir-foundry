from foundry_ontology_api import ObjectType, Property

class Route(ObjectType):
    """Route object for tracking delivery routes and optimization"""
    
    def __init__(self):
        super().__init__(
            api_name="Route",
            display_name="Route",
            description="Delivery routes with optimization and efficiency tracking"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="route_id",
            display_name="Route ID",
            property_type="string",
            required=True,
            description="Unique route identifier"
        ))
        
        self.add_property(Property(
            api_name="route_name",
            display_name="Route Name",
            property_type="string",
            description="Descriptive route name"
        ))
        
        self.add_property(Property(
            api_name="route_date",
            display_name="Route Date",
            property_type="date",
            required=True,
            description="Date of route execution"
        ))
        
        # Planning Properties
        self.add_property(Property(
            api_name="planned_miles",
            display_name="Planned Miles",
            property_type="double",
            description="Planned route distance in miles"
        ))
        
        self.add_property(Property(
            api_name="actual_miles",
            display_name="Actual Miles",
            property_type="double",
            description="Actual route distance traveled"
        ))
        
        self.add_property(Property(
            api_name="planned_duration",
            display_name="Planned Duration",
            property_type="double",
            description="Planned route duration in hours"
        ))
        
        self.add_property(Property(
            api_name="actual_duration",
            display_name="Actual Duration",
            property_type="double",
            description="Actual route duration in hours"
        ))
        
        # Fuel and Efficiency
        self.add_property(Property(
            api_name="fuel_consumed",
            display_name="Fuel Consumed",
            property_type="double",
            description="Total fuel consumed in gallons"
        ))
        
        self.add_property(Property(
            api_name="fuel_efficiency",
            display_name="Fuel Efficiency",
            property_type="double",
            description="Miles per gallon for this route"
        ))
        
        # Optimization Properties
        self.add_property(Property(
            api_name="optimized_route",
            display_name="Optimized Route",
            property_type="boolean",
            description="Whether route was AI-optimized"
        ))
        
        self.add_property(Property(
            api_name="efficiency_score",
            display_name="Efficiency Score",
            property_type="double",
            description="Overall route efficiency score (0-100)"
        ))
        
        self.add_property(Property(
            api_name="optimization_savings",
            display_name="Optimization Savings",
            property_type="double",
            description="Miles saved through optimization"
        ))
        
        # Safety Properties (60mph compliance)
        self.add_property(Property(
            api_name="average_speed",
            display_name="Average Speed",
            property_type="double",
            description="Average speed throughout route"
        ))
        
        self.add_property(Property(
            api_name="max_speed_recorded",
            display_name="Max Speed Recorded",
            property_type="double",
            description="Maximum speed recorded (should be ≤60mph)"
        ))
        
        self.add_property(Property(
            api_name="speed_violations",
            display_name="Speed Violations",
            property_type="integer",
            description="Number of speed violations on route"
        ))
        
        # Performance
        self.add_property(Property(
            api_name="delivery_count",
            display_name="Delivery Count",
            property_type="integer",
            description="Number of deliveries on route"
        ))
        
        self.add_property(Property(
            api_name="on_time_deliveries",
            display_name="On-Time Deliveries",
            property_type="integer",
            description="Number of on-time deliveries"
        ))
        
        self.add_property(Property(
            api_name="route_status",
            display_name="Route Status",
            property_type="string",
            description="Current route status (Planned, Active, Completed)"
        ))