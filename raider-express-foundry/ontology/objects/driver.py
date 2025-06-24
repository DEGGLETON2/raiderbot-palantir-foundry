from foundry_ontology_api import ObjectType, Property, LinkType

class Driver(ObjectType):
    """Driver object for Raider Express transportation ontology"""
    
    def __init__(self):
        super().__init__(
            api_name="Driver",
            display_name="Driver",
            description="Raider Express truck drivers with performance and safety tracking"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="driver_id",
            display_name="Driver ID", 
            property_type="string",
            required=True,
            description="Unique identifier for driver"
        ))
        
        self.add_property(Property(
            api_name="driver_name",
            display_name="Driver Name",
            property_type="string", 
            required=True,
            description="Full name of driver"
        ))
        
        self.add_property(Property(
            api_name="employee_number",
            display_name="Employee Number",
            property_type="string",
            required=True,
            description="Raider Express employee number"
        ))
        
        # Contact Information
        self.add_property(Property(
            api_name="phone_number",
            display_name="Phone Number",
            property_type="string",
            description="Primary contact phone number"
        ))
        
        self.add_property(Property(
            api_name="emergency_contact",
            display_name="Emergency Contact",
            property_type="string",
            description="Emergency contact information"
        ))
        
        # Employment Details
        self.add_property(Property(
            api_name="hire_date",
            display_name="Hire Date",
            property_type="date",
            required=True,
            description="Date driver was hired"
        ))
        
        self.add_property(Property(
            api_name="years_experience",
            display_name="Years Experience",
            property_type="double",
            description="Total years of driving experience"
        ))
        
        # Licensing
        self.add_property(Property(
            api_name="cdl_number",
            display_name="CDL Number",
            property_type="string",
            required=True,
            description="Commercial Driver's License number"
        ))
        
        self.add_property(Property(
            api_name="cdl_class",
            display_name="CDL Class",
            property_type="string",
            description="CDL classification (A, B, C)"
        ))
        
        self.add_property(Property(
            api_name="cdl_expiration",
            display_name="CDL Expiration",
            property_type="date",
            required=True,
            description="CDL expiration date"
        ))
        
        # Language Support (RaiderBot bilingual feature)
        self.add_property(Property(
            api_name="preferred_language",
            display_name="Preferred Language", 
            property_type="string",
            description="Primary language (English/Spanish)"
        ))
        
        # Performance Metrics
        self.add_property(Property(
            api_name="safety_score",
            display_name="Safety Score",
            property_type="double",
            description="Current safety performance score (0-100)"
        ))
        
        self.add_property(Property(
            api_name="performance_score", 
            display_name="Performance Score",
            property_type="double",
            description="Overall performance rating (0-100)"
        ))
        
        self.add_property(Property(
            api_name="on_time_rate",
            display_name="On-Time Rate",
            property_type="double",
            description="Percentage of on-time deliveries"
        ))
        
        # Status
        self.add_property(Property(
            api_name="driver_status",
            display_name="Driver Status",
            property_type="string",
            description="Current status (Active, On Route, Off Duty, etc.)"
        ))
        
        self.add_property(Property(
            api_name="current_location",
            display_name="Current Location",
            property_type="geopoint",
            description="Last known GPS location"
        ))
        
        # Safety-First Properties (60mph compliance)
        self.add_property(Property(
            api_name="speed_compliance_rate",
            display_name="Speed Compliance Rate",
            property_type="double",
            description="Percentage of time maintaining ≤60mph"
        ))
        
        self.add_property(Property(
            api_name="safety_violations_count",
            display_name="Safety Violations Count",
            property_type="integer",
            description="Number of safety violations (last 12 months)"
        ))