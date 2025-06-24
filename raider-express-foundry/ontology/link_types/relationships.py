from foundry_ontology_api import LinkType, Property

class DriverOperatesVehicle(LinkType):
    """Relationship between drivers and vehicles"""
    
    def __init__(self):
        super().__init__(
            api_name="DriverOperatesVehicle",
            display_name="Driver Operates Vehicle",
            from_object_type="Driver",
            to_object_type="Vehicle"
        )
        
        self.add_property(Property(
            api_name="assignment_start_date",
            display_name="Assignment Start Date",
            property_type="date",
            description="Date driver was assigned to vehicle"
        ))
        
        self.add_property(Property(
            api_name="assignment_end_date",
            display_name="Assignment End Date",
            property_type="date",
            description="Date assignment ended"
        ))
        
        self.add_property(Property(
            api_name="primary_driver",
            display_name="Primary Driver",
            property_type="boolean",
            description="Whether this is the primary driver for this vehicle"
        ))

class DriverCompletesDelivery(LinkType):
    """Relationship between drivers and deliveries"""
    
    def __init__(self):
        super().__init__(
            api_name="DriverCompletesDelivery",
            display_name="Driver Completes Delivery",
            from_object_type="Driver",
            to_object_type="Delivery"
        )
        
        self.add_property(Property(
            api_name="completion_timestamp",
            display_name="Completion Timestamp",
            property_type="timestamp",
            description="When delivery was completed"
        ))
        
        self.add_property(Property(
            api_name="driver_signature",
            display_name="Driver Signature",
            property_type="string",
            description="Driver's digital signature"
        ))

class VehicleFollowsRoute(LinkType):
    """Relationship between vehicles and routes"""
    
    def __init__(self):
        super().__init__(
            api_name="VehicleFollowsRoute",
            display_name="Vehicle Follows Route",
            from_object_type="Vehicle",
            to_object_type="Route"
        )
        
        self.add_property(Property(
            api_name="route_start_time",
            display_name="Route Start Time",
            property_type="timestamp",
            description="When vehicle started the route"
        ))
        
        self.add_property(Property(
            api_name="route_end_time",
            display_name="Route End Time",
            property_type="timestamp",
            description="When vehicle completed the route"
        ))

class DeliveryOnRoute(LinkType):
    """Relationship between deliveries and routes"""
    
    def __init__(self):
        super().__init__(
            api_name="DeliveryOnRoute",
            display_name="Delivery On Route",
            from_object_type="Delivery",
            to_object_type="Route"
        )
        
        self.add_property(Property(
            api_name="stop_sequence",
            display_name="Stop Sequence",
            property_type="integer",
            description="Order of delivery on the route"
        ))
        
        self.add_property(Property(
            api_name="estimated_arrival",
            display_name="Estimated Arrival",
            property_type="timestamp",
            description="Estimated arrival time at delivery location"
        ))

class SafetyIncidentInvolvesDriver(LinkType):
    """Relationship between safety incidents and drivers"""
    
    def __init__(self):
        super().__init__(
            api_name="SafetyIncidentInvolvesDriver",
            display_name="Safety Incident Involves Driver",
            from_object_type="SafetyIncident",
            to_object_type="Driver"
        )
        
        self.add_property(Property(
            api_name="driver_role",
            display_name="Driver Role",
            property_type="string",
            description="Driver's role in incident (Primary, Witness, etc.)"
        ))

class SafetyIncidentInvolvesVehicle(LinkType):
    """Relationship between safety incidents and vehicles"""
    
    def __init__(self):
        super().__init__(
            api_name="SafetyIncidentInvolvesVehicle",
            display_name="Safety Incident Involves Vehicle",
            from_object_type="SafetyIncident",
            to_object_type="Vehicle"
        )
        
        self.add_property(Property(
            api_name="vehicle_condition",
            display_name="Vehicle Condition",
            property_type="string",
            description="Vehicle condition after incident"
        ))