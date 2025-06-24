from foundry_ontology_api import ObjectType, Property

class SafetyIncident(ObjectType):
    """Safety incident tracking for compliance and improvement"""
    
    def __init__(self):
        super().__init__(
            api_name="SafetyIncident",
            display_name="Safety Incident",
            description="Safety incidents with tracking and resolution"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="incident_id",
            display_name="Incident ID",
            property_type="string",
            required=True,
            description="Unique incident identifier"
        ))
        
        self.add_property(Property(
            api_name="incident_date",
            display_name="Incident Date",
            property_type="timestamp",
            required=True,
            description="Date and time of incident"
        ))
        
        self.add_property(Property(
            api_name="incident_type",
            display_name="Incident Type",
            property_type="string",
            description="Category of safety incident"
        ))
        
        self.add_property(Property(
            api_name="severity",
            display_name="Severity",
            property_type="string",
            description="Incident severity (Low, Medium, High, Critical)"
        ))
        
        # Location and Context
        self.add_property(Property(
            api_name="incident_location",
            display_name="Incident Location",
            property_type="geopoint",
            description="GPS coordinates of incident"
        ))
        
        self.add_property(Property(
            api_name="incident_address",
            display_name="Incident Address",
            property_type="string",
            description="Street address of incident"
        ))
        
        # Details
        self.add_property(Property(
            api_name="description",
            display_name="Description",
            property_type="string",
            description="Detailed incident description"
        ))
        
        self.add_property(Property(
            api_name="contributing_factors",
            display_name="Contributing Factors",
            property_type="string",
            description="Factors that contributed to incident"
        ))
        
        # Speed-Related Properties (60mph focus)
        self.add_property(Property(
            api_name="speed_at_incident",
            display_name="Speed at Incident",
            property_type="double",
            description="Vehicle speed at time of incident"
        ))
        
        self.add_property(Property(
            api_name="speed_related",
            display_name="Speed Related",
            property_type="boolean",
            description="Whether incident was speed-related"
        ))
        
        # Resolution
        self.add_property(Property(
            api_name="reported_by",
            display_name="Reported By",
            property_type="string",
            description="Person who reported the incident"
        ))
        
        self.add_property(Property(
            api_name="investigated_by",
            display_name="Investigated By",
            property_type="string",
            description="Person who investigated the incident"
        ))
        
        self.add_property(Property(
            api_name="corrective_actions",
            display_name="Corrective Actions",
            property_type="string",
            description="Actions taken to prevent recurrence"
        ))
        
        self.add_property(Property(
            api_name="incident_status",
            display_name="Incident Status",
            property_type="string",
            description="Current status (Open, Under Investigation, Resolved)"
        ))
        
        self.add_property(Property(
            api_name="resolved_date",
            display_name="Resolved Date",
            property_type="date",
            description="Date incident was resolved"
        ))