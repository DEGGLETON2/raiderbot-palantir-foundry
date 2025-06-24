from foundry_ontology_api import ObjectType, Property

class Customer(ObjectType):
    """Customer object for tracking client relationships and performance"""
    
    def __init__(self):
        super().__init__(
            api_name="Customer",
            display_name="Customer",
            description="Customer companies served by Raider Express with performance tracking"
        )
        
        # Core Properties
        self.add_property(Property(
            api_name="customer_id",
            display_name="Customer ID",
            property_type="string",
            required=True,
            description="Unique customer identifier"
        ))
        
        self.add_property(Property(
            api_name="company_name",
            display_name="Company Name",
            property_type="string",
            required=True,
            description="Customer company name"
        ))
        
        self.add_property(Property(
            api_name="dba_name",
            display_name="DBA Name",
            property_type="string",
            description="Doing Business As name"
        ))
        
        # Contact Information
        self.add_property(Property(
            api_name="primary_contact_name",
            display_name="Primary Contact Name",
            property_type="string",
            description="Primary contact person"
        ))
        
        self.add_property(Property(
            api_name="primary_contact_email",
            display_name="Primary Contact Email",
            property_type="string",
            description="Primary contact email address"
        ))
        
        self.add_property(Property(
            api_name="primary_contact_phone",
            display_name="Primary Contact Phone",
            property_type="string",
            description="Primary contact phone number"
        ))
        
        # Address Information
        self.add_property(Property(
            api_name="billing_address",
            display_name="Billing Address",
            property_type="string",
            description="Customer billing address"
        ))
        
        self.add_property(Property(
            api_name="shipping_address",
            display_name="Shipping Address",
            property_type="string",
            description="Primary shipping address"
        ))
        
        self.add_property(Property(
            api_name="headquarters_location",
            display_name="Headquarters Location",
            property_type="geopoint",
            description="GPS coordinates of headquarters"
        ))
        
        # Business Information
        self.add_property(Property(
            api_name="industry_type",
            display_name="Industry Type",
            property_type="string",
            description="Customer's industry classification"
        ))
        
        self.add_property(Property(
            api_name="business_size",
            display_name="Business Size",
            property_type="string",
            description="Business size (Small, Medium, Large, Enterprise)"
        ))
        
        self.add_property(Property(
            api_name="customer_since",
            display_name="Customer Since",
            property_type="date",
            description="Date customer relationship began"
        ))
        
        # Account Information
        self.add_property(Property(
            api_name="account_status",
            display_name="Account Status",
            property_type="string",
            description="Current account status (Active, Inactive, Suspended)"
        ))
        
        self.add_property(Property(
            api_name="credit_limit",
            display_name="Credit Limit",
            property_type="double",
            description="Customer credit limit in dollars"
        ))
        
        self.add_property(Property(
            api_name="payment_terms",
            display_name="Payment Terms",
            property_type="string",
            description="Payment terms (Net 30, Net 15, COD, etc.)"
        ))
        
        # Service Preferences
        self.add_property(Property(
            api_name="preferred_service_level",
            display_name="Preferred Service Level",
            property_type="string",
            description="Preferred service level (Standard, Expedited, Express)"
        ))
        
        self.add_property(Property(
            api_name="temperature_requirements",
            display_name="Temperature Requirements",
            property_type="string",
            description="Typical temperature requirements"
        ))
        
        self.add_property(Property(
            api_name="special_handling_requirements",
            display_name="Special Handling Requirements",
            property_type="string",
            description="Any special handling requirements"
        ))
        
        # Performance Metrics
        self.add_property(Property(
            api_name="total_deliveries_ytd",
            display_name="Total Deliveries YTD",
            property_type="integer",
            description="Total deliveries year-to-date"
        ))
        
        self.add_property(Property(
            api_name="average_satisfaction_score",
            display_name="Average Satisfaction Score",
            property_type="double",
            description="Average customer satisfaction score (1-10)"
        ))
        
        self.add_property(Property(
            api_name="on_time_delivery_rate",
            display_name="On-Time Delivery Rate",
            property_type="double",
            description="Percentage of on-time deliveries"
        ))
        
        self.add_property(Property(
            api_name="revenue_ytd",
            display_name="Revenue YTD",
            property_type="double",
            description="Total revenue from customer year-to-date"
        ))
        
        # Relationship Management
        self.add_property(Property(
            api_name="account_manager",
            display_name="Account Manager",
            property_type="string",
            description="Assigned account manager"
        ))
        
        self.add_property(Property(
            api_name="customer_tier",
            display_name="Customer Tier",
            property_type="string",
            description="Customer tier (Bronze, Silver, Gold, Platinum)"
        ))
        
        self.add_property(Property(
            api_name="last_contact_date",
            display_name="Last Contact Date",
            property_type="date",
            description="Date of last business contact"
        ))
        
        # Communication Preferences
        self.add_property(Property(
            api_name="preferred_language",
            display_name="Preferred Language",
            property_type="string",
            description="Preferred communication language (English/Spanish)"
        ))
        
        self.add_property(Property(
            api_name="communication_preferences",
            display_name="Communication Preferences",
            property_type="string",
            description="Preferred communication methods"
        ))