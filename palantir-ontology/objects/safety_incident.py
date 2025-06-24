"""
Palantir Foundry Ontology Object: SafetyIncident
Defines the safety incident data model in Foundry's ontology system
"""

from foundry_ontology_api import ObjectType, Property, LinkType

class SafetyIncident(ObjectType):
    """Safety incident tracking in Palantir Foundry Ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="SafetyIncident",
            display_name="Safety Incident",
            description="Safety compliance and incident tracking in Foundry"
        )
        
        # Core incident properties
        self.add_property(Property(
            api_name="incident_id",
            display_name="Incident ID",
            property_type="string",
            required=True,
            description="Unique incident identifier in Foundry"
        ))
        
        self.add_property(Property(
            api_name="severity_level",
            display_name="Severity Level",
            property_type="string",
            required=True,
            description="LOW, MEDIUM, HIGH, CRITICAL"
        ))
        
        # Speed-related properties (60mph emphasis)
        self.add_property(Property(
            api_name="speed_related",
            display_name="Speed Related Incident",
            property_type="boolean",
            description="Was speed a factor in this incident"
        ))
        
        self.add_property(Property(
            api_name="recorded_speed",
            display_name="Recorded Speed at Incident",
            property_type="double",
            description="Vehicle speed at time of incident (mph)"
        ))
        
        # Incident details
        self.add_property(Property(
            api_name="incident_date",
            display_name="Incident Date",
            property_type="timestamp",
            required=True
        ))
        
        self.add_property(Property(
            api_name="description",
            display_name="Incident Description",
            property_type="string",
            description="Detailed description of the safety incident"
        ))
        
        # Foundry tracking
        self.add_property(Property(
            api_name="foundry_analysis_complete",
            display_name="Foundry Analysis Complete",
            property_type="boolean",
            default=False,
            description="Has Foundry ML analyzed this incident"
        ))
