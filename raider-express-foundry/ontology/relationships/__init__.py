"""
Ontology relationships for Raider Express
Defines the relationships between entities in the transportation domain
"""

from .transportation_links import (
    DriverAssignedToVehicle,
    VehicleAssignedToRoute,
    DeliveryOnRoute,
    CustomerReceivesDelivery,
    DriverInvolvedInIncident,
    VehicleOnRoute,
    RouteServicesCustomer,
    DriverDeliveresToCustomer
)

__all__ = [
    "DriverAssignedToVehicle",
    "VehicleAssignedToRoute", 
    "DeliveryOnRoute",
    "CustomerReceivesDelivery",
    "DriverInvolvedInIncident",
    "VehicleOnRoute",
    "RouteServicesCustomer",
    "DriverDeliveresToCustomer"
]