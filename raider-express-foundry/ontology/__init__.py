"""
Ontology module for Raider Express Foundry
Defines the data model and relationships for the transportation domain
"""

from .ontology_setup import setup_ontology, RaiderExpressOntology
from .objects.driver import Driver
from .objects.vehicle import Vehicle  
from .objects.delivery import Delivery
from .objects.route import Route
from .objects.customer import Customer
from .objects.safety_incident import SafetyIncident
from .relationships.transportation_links import (
    DriverAssignedToVehicle,
    VehicleAssignedToRoute,
    DeliveryOnRoute,
    CustomerReceivesDelivery,
    DriverInvolvedInIncident
)

__all__ = [
    # Setup
    "setup_ontology",
    "RaiderExpressOntology",
    
    # Object types
    "Driver",
    "Vehicle", 
    "Delivery",
    "Route",
    "Customer",
    "SafetyIncident",
    
    # Relationships
    "DriverAssignedToVehicle",
    "VehicleAssignedToRoute", 
    "DeliveryOnRoute",
    "CustomerReceivesDelivery",
    "DriverInvolvedInIncident"
]