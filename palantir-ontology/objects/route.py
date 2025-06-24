"""
Palantir Foundry Ontology Object: Route
Defines the route data model in Foundry's ontology system
"""

from foundry_ontology_api import ObjectType, Property, LinkType

class Route(ObjectType):
    """Route object for optimization in Palantir Foundry Ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="Route",
            display_name="Delivery Route", 
            description="Optimized routes with safety constraints in Foundry"
        )
        
        # Core route properties
        self.add_property(Property(
            api_name="route_id",
            display_name="Route ID",
            property_type="string", 
            required=True,
            description="Unique route identifier in Foundry"
        ))
        
        self.add_property(Property(
            api_name="optimization_score",
            display_name="Route Optimization Score",
            property_type="double",
            description="Efficiency score from Foundry optimization"
        ))
        
        # Route details
        self.add_property(Property(
            api_name="total_distance",
            display_name="Total Distance",
            property_type="double",
            description="Total route distance in miles"
        ))
        
        self.add_property(Property(
            api_name="estimated_duration",
            display_name="Estimated Duration", 
            property_type="integer",
            description="Estimated time in minutes (accounting for 60mph limit)"
        ))
        
        self.add_property(Property(
            api_name="stop_count",
            display_name="Number of Stops",
            property_type="integer",
            required=True
        ))
        
        # Foundry optimization metadata
        self.add_property(Property(
            api_name="foundry_optimized_at",
            display_name="Foundry Optimization Time",
            property_type="timestamp",
            description="When route was optimized by Foundry Functions"
        ))
