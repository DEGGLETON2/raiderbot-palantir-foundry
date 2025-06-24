"""
Palantir Foundry Ontology Link Types: Relationships
Defines relationships between objects in Foundry's ontology system
"""

from foundry_ontology_api import LinkType

# Driver-Vehicle Relationship
driver_operates_vehicle = LinkType(
    api_name="driver_operates_vehicle",
    display_name="Driver Operates Vehicle",
    description="Links drivers to their assigned vehicles in Foundry",
    source_object_type="Driver",
    target_object_type="Vehicle",
    cardinality="ONE_TO_MANY"
)

# Driver-Delivery Relationship
driver_completes_delivery = LinkType(
    api_name="driver_completes_delivery",
    display_name="Driver Completes Delivery",
    description="Links drivers to their deliveries in Foundry",
    source_object_type="Driver",
    target_object_type="Delivery",
    cardinality="ONE_TO_MANY"
)

# Vehicle-Route Relationship
vehicle_assigned_route = LinkType(
    api_name="vehicle_assigned_route",
    display_name="Vehicle Assigned to Route",
    description="Links vehicles to their routes in Foundry",
    source_object_type="Vehicle",
    target_object_type="Route",
    cardinality="ONE_TO_MANY"
)

# Route-Delivery Relationship
route_contains_delivery = LinkType(
    api_name="route_contains_delivery",
    display_name="Route Contains Delivery",
    description="Links routes to their deliveries in Foundry",
    source_object_type="Route",
    target_object_type="Delivery",
    cardinality="ONE_TO_MANY"
)

# Customer-Delivery Relationship
customer_receives_delivery = LinkType(
    api_name="customer_receives_delivery",
    display_name="Customer Receives Delivery",
    description="Links customers to their deliveries in Foundry",
    source_object_type="Customer",
    target_object_type="Delivery",
    cardinality="ONE_TO_MANY"
)

# Driver-SafetyIncident Relationship
driver_involved_incident = LinkType(
    api_name="driver_involved_incident",
    display_name="Driver Involved in Incident",
    description="Links drivers to safety incidents in Foundry",
    source_object_type="Driver",
    target_object_type="SafetyIncident",
    cardinality="ONE_TO_MANY"
)

# Vehicle-SafetyIncident Relationship
vehicle_involved_incident = LinkType(
    api_name="vehicle_involved_incident",
    display_name="Vehicle Involved in Incident",
    description="Links vehicles to safety incidents in Foundry",
    source_object_type="Vehicle",
    target_object_type="SafetyIncident",
    cardinality="ONE_TO_MANY"
)
