"""
RaiderBot Logistics Ontology Definition
Defines the core data model for logistics operations
"""

from foundry_ontology import Ontology, ObjectType, Property, LinkType
from foundry_ontology.data_types import String, Integer, Double, Boolean, Timestamp, GeoPoint


# Define the RaiderBot Logistics Ontology
raiderbot_ontology = Ontology(
    name="RaiderBot Logistics Operations",
    description="Comprehensive ontology for logistics and transportation operations",
    version="1.0.0"
)

# ===== CORE OBJECT TYPES =====

# Shipment Object Type
shipment_type = ObjectType(
    name="Shipment",
    description="Individual shipment or delivery",
    primary_key="shipment_id",
    properties=[
        Property("shipment_id", String, required=True, description="Unique shipment identifier"),
        Property("tracking_number", String, required=True, description="Customer-facing tracking number"),
        Property("origin_address", String, required=True, description="Pickup location"),
        Property("destination_address", String, required=True, description="Delivery location"),
        Property("origin_coordinates", GeoPoint, description="Pickup GPS coordinates"),
        Property("destination_coordinates", GeoPoint, description="Delivery GPS coordinates"),
        Property("scheduled_pickup_time", Timestamp, description="Planned pickup time"),
        Property("actual_pickup_time", Timestamp, description="Actual pickup time"),
        Property("scheduled_delivery_time", Timestamp, description="Planned delivery time"),
        Property("actual_delivery_time", Timestamp, description="Actual delivery time"),
        Property("delivery_status", String, required=True, description="Current delivery status"),
        Property("package_weight_lbs", Double, description="Package weight in pounds"),
        Property("package_dimensions", String, description="Package dimensions (LxWxH)"),
        Property("special_instructions", String, description="Delivery instructions"),
        Property("customer_signature", String, description="Digital signature upon delivery"),
        Property("delivery_photo", String, description="Photo evidence of delivery"),
        Property("priority_level", String, description="Shipment priority (standard, express, urgent)"),
        Property("service_type", String, description="Service type (ground, air, overnight)"),
        Property("insurance_value", Double, description="Declared insurance value"),
        Property("delivery_attempts", Integer, description="Number of delivery attempts"),
        Property("created_at", Timestamp, required=True, description="Shipment creation timestamp"),
        Property("updated_at", Timestamp, required=True, description="Last update timestamp")
    ]
)

# Driver Object Type
driver_type = ObjectType(
    name="Driver",
    description="Delivery driver or operator",
    primary_key="driver_id",
    properties=[
        Property("driver_id", String, required=True, description="Unique driver identifier"),
        Property("employee_id", String, required=True, description="Employee ID number"),
        Property("first_name", String, required=True, description="Driver first name"),
        Property("last_name", String, required=True, description="Driver last name"),
        Property("email", String, description="Driver email address"),
        Property("phone_number", String, description="Driver phone number"),
        Property("license_number", String, required=True, description="Driver's license number"),
        Property("license_expiry", Timestamp, description="License expiration date"),
        Property("hire_date", Timestamp, description="Date of hire"),
        Property("status", String, required=True, description="Driver status (active, inactive, suspended)"),
        Property("safety_score", Double, description="Driver safety rating (0-100)"),
        Property("performance_rating", Double, description="Overall performance rating (0-5)"),
        Property("total_deliveries", Integer, description="Total completed deliveries"),
        Property("on_time_percentage", Double, description="On-time delivery percentage"),
        Property("accident_count", Integer, description="Number of reported accidents"),
        Property("vehicle_violations", Integer, description="Traffic violations count"),
        Property("current_location", GeoPoint, description="Current GPS location"),
        Property("shift_start_time", Timestamp, description="Current shift start time"),
        Property("shift_end_time", Timestamp, description="Current shift end time"),
        Property("is_available", Boolean, description="Driver availability status"),
        Property("certification_level", String, description="Driver certification level"),
        Property("created_at", Timestamp, required=True, description="Driver record creation"),
        Property("updated_at", Timestamp, required=True, description="Last update timestamp")
    ]
)

# Vehicle Object Type
vehicle_type = ObjectType(
    name="Vehicle",
    description="Delivery vehicle or truck",
    primary_key="vehicle_id",
    properties=[
        Property("vehicle_id", String, required=True, description="Unique vehicle identifier"),
        Property("fleet_number", String, required=True, description="Fleet identification number"),
        Property("license_plate", String, required=True, description="Vehicle license plate"),
        Property("make", String, description="Vehicle manufacturer"),
        Property("model", String, description="Vehicle model"),
        Property("year", Integer, description="Vehicle year"),
        Property("vin", String, description="Vehicle identification number"),
        Property("vehicle_type", String, description="Type of vehicle (van, truck, trailer)"),
        Property("capacity_cubic_feet", Double, description="Cargo capacity in cubic feet"),
        Property("max_weight_lbs", Double, description="Maximum weight capacity"),
        Property("fuel_type", String, description="Fuel type (gas, diesel, electric)"),
        Property("fuel_efficiency_mpg", Double, description="Fuel efficiency in miles per gallon"),
        Property("current_mileage", Integer, description="Current odometer reading"),
        Property("maintenance_due_mileage", Integer, description="Next maintenance due mileage"),
        Property("last_maintenance_date", Timestamp, description="Last maintenance date"),
        Property("insurance_expiry", Timestamp, description="Insurance expiration date"),
        Property("registration_expiry", Timestamp, description="Registration expiration date"),
        Property("status", String, required=True, description="Vehicle status (active, maintenance, retired)"),
        Property("current_location", GeoPoint, description="Current GPS coordinates"),
        Property("telematics_device_id", String, description="Telematics device identifier"),
        Property("created_at", Timestamp, required=True, description="Vehicle record creation"),
        Property("updated_at", Timestamp, required=True, description="Last update timestamp")
    ]
)

# Route Object Type
route_type = ObjectType(
    name="Route",
    description="Delivery route or path",
    primary_key="route_id",
    properties=[
        Property("route_id", String, required=True, description="Unique route identifier"),
        Property("route_name", String, required=True, description="Route name or description"),
        Property("date", Timestamp, required=True, description="Route date"),
        Property("start_location", String, description="Route starting point"),
        Property("end_location", String, description="Route ending point"),
        Property("planned_distance_miles", Double, description="Planned route distance"),
        Property("actual_distance_miles", Double, description="Actual distance traveled"),
        Property("planned_duration_minutes", Integer, description="Planned route duration"),
        Property("actual_duration_minutes", Integer, description="Actual route duration"),
        Property("optimization_score", Double, description="Route optimization score (0-100)"),
        Property("fuel_consumed_gallons", Double, description="Fuel consumption"),
        Property("toll_costs", Double, description="Toll road costs"),
        Property("traffic_delay_minutes", Integer, description="Traffic-related delays"),
        Property("weather_conditions", String, description="Weather during route"),
        Property("route_status", String, required=True, description="Route status (planned, active, completed)"),
        Property("shipment_count", Integer, description="Number of shipments on route"),
        Property("delivery_success_rate", Double, description="Successful deliveries percentage"),
        Property("created_at", Timestamp, required=True, description="Route creation timestamp"),
        Property("updated_at", Timestamp, required=True, description="Last update timestamp")
    ]
)

# Customer Object Type
customer_type = ObjectType(
    name="Customer",
    description="Customer or client",
    primary_key="customer_id",
    properties=[
        Property("customer_id", String, required=True, description="Unique customer identifier"),
        Property("company_name", String, description="Company or business name"),
        Property("contact_first_name", String, description="Primary contact first name"),
        Property("contact_last_name", String, description="Primary contact last name"),
        Property("email", String, description="Customer email address"),
        Property("phone_number", String, description="Customer phone number"),
        Property("billing_address", String, description="Billing address"),
        Property("preferred_delivery_window", String, description="Preferred delivery time window"),
        Property("account_status", String, description="Account status (active, suspended, closed)"),
        Property("credit_rating", String, description="Customer credit rating"),
        Property("payment_terms", String, description="Payment terms agreement"),
        Property("total_shipments", Integer, description="Total shipments to date"),
        Property("average_monthly_volume", Integer, description="Average monthly shipment volume"),
        Property("customer_satisfaction_score", Double, description="Satisfaction rating (0-5)"),
        Property("special_requirements", String, description="Special handling requirements"),
        Property("created_at", Timestamp, required=True, description="Customer record creation"),
        Property("updated_at", Timestamp, required=True, description="Last update timestamp")
    ]
)

# ===== LINK TYPES (RELATIONSHIPS) =====

# Driver-Shipment Assignment
driver_shipment_link = LinkType(
    name="AssignedTo",
    description="Driver assigned to deliver shipment",
    from_object_type=shipment_type,
    to_object_type=driver_type,
    properties=[
        Property("assignment_date", Timestamp, description="Date of assignment"),
        Property("estimated_delivery_time", Timestamp, description="Estimated delivery time"),
        Property("assignment_status", String, description="Assignment status")
    ]
)

# Vehicle-Driver Assignment
vehicle_driver_link = LinkType(
    name="OperatedBy",
    description="Vehicle operated by driver",
    from_object_type=vehicle_type,
    to_object_type=driver_type,
    properties=[
        Property("assignment_start_date", Timestamp, description="Start date of assignment"),
        Property("assignment_end_date", Timestamp, description="End date of assignment"),
        Property("primary_operator", Boolean, description="Whether this is the primary operator")
    ]
)

# Route-Shipment Inclusion
route_shipment_link = LinkType(
    name="IncludesShipment",
    description="Shipment included in route",
    from_object_type=route_type,
    to_object_type=shipment_type,
    properties=[
        Property("stop_sequence", Integer, description="Order of stop on route"),
        Property("estimated_arrival_time", Timestamp, description="Estimated arrival time"),
        Property("actual_arrival_time", Timestamp, description="Actual arrival time")
    ]
)

# Customer-Shipment Ownership
customer_shipment_link = LinkType(
    name="ShipmentOwner",
    description="Customer who owns the shipment",
    from_object_type=customer_type,
    to_object_type=shipment_type,
    properties=[
        Property("billing_code", String, description="Customer billing code"),
        Property("service_level", String, description="Service level agreement")
    ]
)

# ===== REGISTER ONTOLOGY COMPONENTS =====

# Add object types to ontology
raiderbot_ontology.add_object_type(shipment_type)
raiderbot_ontology.add_object_type(driver_type)
raiderbot_ontology.add_object_type(vehicle_type)
raiderbot_ontology.add_object_type(route_type)
raiderbot_ontology.add_object_type(customer_type)

# Add link types to ontology
raiderbot_ontology.add_link_type(driver_shipment_link)
raiderbot_ontology.add_link_type(vehicle_driver_link)
raiderbot_ontology.add_link_type(route_shipment_link)
raiderbot_ontology.add_link_type(customer_shipment_link)

# Export ontology for Foundry registration
__all__ = ["raiderbot_ontology"]
