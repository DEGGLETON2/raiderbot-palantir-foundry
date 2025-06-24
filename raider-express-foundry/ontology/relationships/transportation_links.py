"""
Transportation relationship definitions for Raider Express ontology
"""

from palantir_foundry_sdk.ontology import RelationshipType, Property
from typing import Optional
from datetime import datetime

class DriverAssignedToVehicle(RelationshipType):
    """
    Relationship between Driver and Vehicle representing assignment
    """
    
    # Assignment details
    assignment_id: str = Property(title="Assignment ID", description="Unique assignment identifier")
    assignment_date: datetime = Property(title="Assignment Date", description="Date of assignment")
    assignment_type: str = Property(title="Assignment Type", description="Primary, Backup, Temporary")
    assignment_status: str = Property(title="Status", description="Active, Inactive, Pending")
    
    # Validity period
    effective_date: datetime = Property(title="Effective Date", description="Assignment effective date")
    expiration_date: Optional[datetime] = Property(title="Expiration Date", description="Assignment expiration date")
    
    # Assignment context
    assigned_by: str = Property(title="Assigned By", description="User who made assignment")
    reason: Optional[str] = Property(title="Reason", description="Reason for assignment")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class VehicleAssignedToRoute(RelationshipType):
    """
    Relationship between Vehicle and Route representing route assignment
    """
    
    # Assignment details
    assignment_id: str = Property(title="Assignment ID", description="Unique assignment identifier")
    assignment_date: datetime = Property(title="Assignment Date", description="Date of assignment")
    assignment_type: str = Property(title="Assignment Type", description="Primary, Backup, Seasonal")
    assignment_status: str = Property(title="Status", description="Active, Inactive, Pending")
    
    # Schedule information
    scheduled_start_date: datetime = Property(title="Scheduled Start", description="Scheduled start date")
    scheduled_end_date: Optional[datetime] = Property(title="Scheduled End", description="Scheduled end date")
    frequency: str = Property(title="Frequency", description="Daily, Weekly, Monthly")
    
    # Performance tracking
    total_runs_completed: int = Property(title="Runs Completed", description="Total runs completed")
    average_performance_score: Optional[float] = Property(title="Avg Performance", description="Average performance score")
    
    # Assignment context
    assigned_by: str = Property(title="Assigned By", description="User who made assignment")
    assignment_reason: Optional[str] = Property(title="Reason", description="Reason for assignment")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class DeliveryOnRoute(RelationshipType):
    """
    Relationship between Delivery and Route representing delivery assignment to route
    """
    
    # Route assignment details
    assignment_id: str = Property(title="Assignment ID", description="Unique assignment identifier")
    sequence_number: int = Property(title="Sequence Number", description="Delivery sequence on route")
    assignment_date: datetime = Property(title="Assignment Date", description="Date assigned to route")
    
    # Timing
    planned_arrival_time: datetime = Property(title="Planned Arrival", description="Planned arrival time")
    actual_arrival_time: Optional[datetime] = Property(title="Actual Arrival", description="Actual arrival time")
    estimated_service_time_minutes: int = Property(title="Est Service Time", description="Estimated service time in minutes")
    actual_service_time_minutes: Optional[int] = Property(title="Actual Service Time", description="Actual service time in minutes")
    
    # Status
    delivery_status_on_route: str = Property(title="Status on Route", description="Pending, Completed, Failed, Skipped")
    priority_level: str = Property(title="Priority", description="High, Medium, Low priority")
    
    # Special handling
    requires_special_equipment: bool = Property(title="Special Equipment", description="Requires special equipment")
    loading_dock_required: bool = Property(title="Loading Dock", description="Requires loading dock")
    access_restrictions: Optional[str] = Property(title="Access Restrictions", description="Access restriction notes")
    
    # Assignment context
    assigned_by: str = Property(title="Assigned By", description="User who made assignment")
    route_optimizer_version: Optional[str] = Property(title="Optimizer Version", description="Route optimizer version used")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class CustomerReceivesDelivery(RelationshipType):
    """
    Relationship between Customer and Delivery representing customer receiving delivery
    """
    
    # Delivery relationship details
    relationship_id: str = Property(title="Relationship ID", description="Unique relationship identifier")
    delivery_date: datetime = Property(title="Delivery Date", description="Date of delivery")
    delivery_status: str = Property(title="Delivery Status", description="Delivered, Failed, Pending")
    
    # Customer interaction
    received_by: Optional[str] = Property(title="Received By", description="Name of person who received delivery")
    customer_satisfaction_rating: Optional[int] = Property(title="Satisfaction Rating", description="Customer satisfaction rating (1-5)")
    customer_feedback: Optional[str] = Property(title="Customer Feedback", description="Customer feedback comments")
    
    # Delivery specifics
    delivery_location_type: str = Property(title="Location Type", description="Business, Residence, Warehouse, etc.")
    special_instructions_followed: bool = Property(title="Instructions Followed", description="Special instructions were followed")
    signature_obtained: bool = Property(title="Signature Obtained", description="Signature was obtained")
    
    # Issues and exceptions
    delivery_issues: Optional[str] = Property(title="Delivery Issues", description="Any issues during delivery")
    damage_reported: bool = Property(title="Damage Reported", description="Damage was reported")
    complaint_filed: bool = Property(title="Complaint Filed", description="Customer filed complaint")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class DriverInvolvedInIncident(RelationshipType):
    """
    Relationship between Driver and SafetyIncident representing driver involvement
    """
    
    # Involvement details
    involvement_id: str = Property(title="Involvement ID", description="Unique involvement identifier")
    involvement_type: str = Property(title="Involvement Type", description="Primary, Secondary, Witness")
    responsibility_level: str = Property(title="Responsibility", description="At Fault, Not At Fault, Partial, Unknown")
    
    # Driver status during incident
    driver_status: str = Property(title="Driver Status", description="On Duty, Off Duty, Break")
    hours_on_duty: Optional[float] = Property(title="Hours on Duty", description="Hours on duty at time of incident")
    driving_experience_years: Optional[float] = Property(title="Driving Experience", description="Years of driving experience")
    
    # Performance impact
    performance_impact: Optional[str] = Property(title="Performance Impact", description="Impact on driver performance score")
    training_required: bool = Property(title="Training Required", description="Additional training required")
    disciplinary_action: Optional[str] = Property(title="Disciplinary Action", description="Warning, Suspension, etc.")
    
    # Investigation details
    statement_provided: bool = Property(title="Statement Provided", description="Driver provided statement")
    statement_date: Optional[datetime] = Property(title="Statement Date", description="Date statement was provided")
    cooperative: bool = Property(title="Cooperative", description="Driver was cooperative in investigation")
    
    # Testing and compliance
    drug_test_administered: bool = Property(title="Drug Test Given", description="Drug test was administered")
    alcohol_test_administered: bool = Property(title="Alcohol Test Given", description="Alcohol test was administered")
    drug_test_result: Optional[str] = Property(title="Drug Test Result", description="Pass, Fail, Refused")
    alcohol_test_result: Optional[str] = Property(title="Alcohol Test Result", description="Pass, Fail, Refused")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class VehicleOnRoute(RelationshipType):
    """
    Relationship between Vehicle and Route representing vehicle usage on specific route instance
    """
    
    # Route execution details
    execution_id: str = Property(title="Execution ID", description="Unique route execution identifier")
    execution_date: datetime = Property(title="Execution Date", description="Date route was executed")
    start_time: datetime = Property(title="Start Time", description="Route start time")
    end_time: Optional[datetime] = Property(title="End Time", description="Route end time")
    
    # Performance metrics
    total_distance_miles: float = Property(title="Total Distance", description="Total distance traveled in miles")
    fuel_consumed_gallons: Optional[float] = Property(title="Fuel Consumed", description="Fuel consumed in gallons")
    average_speed_mph: Optional[float] = Property(title="Average Speed", description="Average speed in MPH")
    
    # Route completion
    stops_completed: int = Property(title="Stops Completed", description="Number of stops completed")
    deliveries_completed: int = Property(title="Deliveries Completed", description="Number of deliveries completed")
    route_completion_percentage: float = Property(title="Completion %", description="Route completion percentage")
    
    # Issues and exceptions
    mechanical_issues: bool = Property(title="Mechanical Issues", description="Mechanical issues occurred")
    route_deviations: int = Property(title="Route Deviations", description="Number of route deviations")
    delays_encountered: bool = Property(title="Delays Encountered", description="Delays were encountered")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class RouteServicesCustomer(RelationshipType):
    """
    Relationship between Route and Customer representing route serving customer locations
    """
    
    # Service relationship details
    service_id: str = Property(title="Service ID", description="Unique service relationship identifier")
    service_type: str = Property(title="Service Type", description="Regular, Express, Special")
    frequency: str = Property(title="Frequency", description="Daily, Weekly, Monthly")
    
    # Service level agreement
    promised_delivery_window: str = Property(title="Delivery Window", description="Promised delivery time window")
    service_level_commitment: str = Property(title="SLA Commitment", description="Service level commitment")
    priority_level: str = Property(title="Priority", description="High, Medium, Low priority")
    
    # Performance tracking
    on_time_percentage: Optional[float] = Property(title="On Time %", description="On-time delivery percentage")
    customer_satisfaction_avg: Optional[float] = Property(title="Satisfaction Avg", description="Average customer satisfaction")
    total_deliveries_ytd: int = Property(title="Deliveries YTD", description="Total deliveries year-to-date")
    
    # Service dates
    service_start_date: datetime = Property(title="Service Start", description="Service start date")
    service_end_date: Optional[datetime] = Property(title="Service End", description="Service end date")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")

class DriverDeliveresToCustomer(RelationshipType):
    """
    Relationship between Driver and Customer representing driver delivering to customer
    """
    
    # Delivery relationship details
    relationship_id: str = Property(title="Relationship ID", description="Unique relationship identifier")
    total_deliveries: int = Property(title="Total Deliveries", description="Total deliveries made by driver to customer")
    first_delivery_date: datetime = Property(title="First Delivery", description="Date of first delivery")
    last_delivery_date: Optional[datetime] = Property(title="Last Delivery", description="Date of last delivery")
    
    # Performance metrics
    on_time_delivery_rate: Optional[float] = Property(title="On Time Rate", description="On-time delivery rate percentage")
    customer_satisfaction_avg: Optional[float] = Property(title="Satisfaction Avg", description="Average customer satisfaction rating")
    damage_incidents: int = Property(title="Damage Incidents", description="Number of damage incidents")
    
    # Customer relationship
    customer_familiarity_score: Optional[float] = Property(title="Familiarity Score", description="Customer familiarity score (0-10)")
    special_instructions_knowledge: bool = Property(title="Knows Instructions", description="Familiar with customer special instructions")
    preferred_driver: bool = Property(title="Preferred Driver", description="Customer's preferred driver")
    
    # Issues and feedback
    complaints_received: int = Property(title="Complaints", description="Number of complaints received")
    compliments_received: int = Property(title="Compliments", description="Number of compliments received")
    
    # Audit fields
    created_date: datetime = Property(title="Created Date", description="Record creation date")
    last_updated: datetime = Property(title="Last Updated", description="Last update timestamp")