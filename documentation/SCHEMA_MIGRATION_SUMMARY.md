# RaiderBot Schema Migration Summary

## Database Migration Update (January 24, 2024)

### Key Changes
- **Database**: All tables now in `MCLEOD_DB`
- **Schema**: All tables now in `dbo` schema
- **Format**: `MCLEOD_DB.dbo.table_name`

### Updated Table References

| Object | Old Reference | New Reference |
|--------|--------------|---------------|
| Drivers | `drivers` | `MCLEOD_DB.dbo.drivers` |
| Vehicles | `vehicles` | `MCLEOD_DB.dbo.vehicles` |
| Deliveries | `deliveries` | `MCLEOD_DB.dbo.deliveries` |
| Routes | `routes` | `MCLEOD_DB.dbo.routes` |
| Safety Incidents | `safety_incidents` | `MCLEOD_DB.dbo.safety_incidents` |
| Customers | `customers` | `MCLEOD_DB.dbo.customers` |

### Quick Reference - Core Tables

#### 1. MCLEOD_DB.dbo.drivers
- Primary Key: `driver_id`
- Key Fields: `first_name`, `last_name`, `safety_score`, `status`, `cdl_number`
- 60mph Tracking: `speed_compliance_60mph`

#### 2. MCLEOD_DB.dbo.vehicles  
- Primary Key: `vehicle_id`
- Key Fields: `vin`, `make`, `model`, `year`
- Safety: `speed_governor_active`, `max_speed_setting` (must be 60)

#### 3. MCLEOD_DB.dbo.deliveries
- Primary Key: `delivery_id`
- Key Fields: `order_number`, `customer_id`, `driver_id`, `vehicle_id`
- Tracking: `scheduled_delivery`, `actual_delivery`, `temperature_controlled`

#### 4. MCLEOD_DB.dbo.routes
- Primary Key: `route_id`
- Key Fields: `driver_id`, `vehicle_id`, `route_date`
- Metrics: `total_distance`, `estimated_duration`, `stop_count`

#### 5. MCLEOD_DB.dbo.safety_incidents
- Primary Key: `incident_id`
- Key Fields: `driver_id`, `vehicle_id`, `incident_date`, `severity_level`
- Speed Tracking: `speed_related`, `recorded_speed`

#### 6. MCLEOD_DB.dbo.customers
- Primary Key: `customer_id`
- Key Fields: `company_name`, `contact_name`, `satisfaction_score`
- Preferences: `preferred_delivery_window`, `temperature_requirements`

### Example Updated Query
```sql
-- Old
SELECT * FROM drivers WHERE status = 'active'

-- New
SELECT * FROM MCLEOD_DB.dbo.drivers WHERE status = 'active'
```

### Foundry Transform Updates Required
All Foundry transforms must update their source references:
```yaml
# Example transform update
source: "MCLEOD_DB.dbo.drivers"  # Updated from just "drivers"
```

### Files Updated
- ✅ Complete schema documentation: `/documentation/COMPLETE_SCHEMA.yaml`
- ✅ All Snowflake references updated to MCLEOD_DB.dbo format
- ✅ 713 lines of comprehensive schema documentation

🐕 All schema work has been updated for the new McLeod data ingestion platform!
