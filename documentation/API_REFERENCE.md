# RaiderBot API Reference - Palantir Foundry Functions

## Overview
RaiderBot exposes its functionality through Palantir Foundry Functions, providing a serverless API for all operations.

## Base Configuration
```
Base URL: https://raiderexpress.palantirfoundry.com/api/functions
Authentication: Bearer token (Foundry API token)
Content-Type: application/json
```

## Core Functions

### 1. RaiderBot Chat
Main German Shepherd AI chat interface.

**Function**: `raiderbot_core`

**Request**:
```json
POST /raiderbot_core/invoke
{
  "message": "string",
  "language": "en|es", 
  "user_context": {
    "user_id": "string",
    "role": "driver|dispatcher|executive"
  },
  "conversation_history": [
    {"role": "user", "content": "string"},
    {"role": "assistant", "content": "string"}
  ]
}
```

**Response**:
```json
{
  "message": "🐕 Woof! Here's your response...",
  "language": "en",
  "timestamp": "2024-01-15T10:30:00Z",
  "powered_by": "Palantir Foundry",
  "data_source": "foundry_datasets"
}
```

### 2. Route Optimization
Optimize delivery routes with 60mph safety constraints.

**Function**: `route_optimization`

**Request**:
```json
POST /route_optimization/invoke
{
  "delivery_ids": ["DEL001", "DEL002", "DEL003"],
  "start_location": {
    "lat": 32.7357,
    "lon": -97.1081
  },
  "max_driving_hours": 11.0
}
```

**Response**:
```json
{
  "optimized_route": [0, 2, 1, 3, 0],
  "total_distance_miles": 156.8,
  "estimated_duration_minutes": 157,
  "max_speed_enforced": 60,
  "foundry_optimized": true,
  "optimization_algorithm": "TSP_nearest_neighbor",
  "safety_compliant": true
}
```

### 3. Safety Scoring
Calculate comprehensive driver safety scores.

**Function**: `safety_scoring`

**Request**:
```json
POST /safety_scoring/invoke
{
  "driver_id": "DRV123",
  "time_period_days": 90
}
```

**Response**:
```json
{
  "driver_id": "DRV123",
  "safety_score": 87.5,
  "speed_compliance_rate": 98.5,
  "components": {
    "speed_score": 39.4,
    "incident_score": 24.0,
    "braking_score": 12.75,
    "hos_score": 11.35
  },
  "evaluation_period_days": 90,
  "calculated_by": "Palantir Foundry Functions",
  "emphasis": "60mph speed compliance"
}
```

### 4. Document Learning
Process documents for RaiderBot knowledge base.

**Function**: `document_learning`

**Request**:
```json
POST /document_learning/invoke
{
  "document_id": "DOC456",
  "document_type": "auto|pdf|image|text",
  "extract_entities": true
}
```

**Response**:
```json
{
  "success": true,
  "document_id": "DOC456",
  "extracted_entities": 12,
  "safety_relevance": 80,
  "foundry_ml_processed": true
}
```

## Foundry Datasets API

### Get Real-time KPIs
```bash
GET /datasets/raider_kpi_dashboard/latest
```

### Get Driver Data
```bash
GET /datasets/raider_drivers/query?filter=status:active
```

## Error Handling

All errors follow Foundry's standard format:

```json
{
  "error": "Error description",
  "foundry_function": "function_name",
  "status": "failed",
  "trace_id": "foundry-trace-123"
}
```

## Rate Limits

- **Functions**: 1000 requests/minute per workspace
- **Datasets**: 500 queries/minute per dataset
- **Burst**: 100 requests/second maximum

## SDK Examples

### Python
```python
from foundry_functions_sdk import FoundryClient

client = FoundryClient(token="your-foundry-token")
response = client.invoke_function(
    "raiderbot_core",
    {"message": "Hello RaiderBot!", "language": "en"}
)
```

### JavaScript
```javascript
const { FoundryClient } = require('@palantir/foundry-sdk');

const client = new FoundryClient({ token: 'your-foundry-token' });
const response = await client.functions.invoke('raiderbot_core', {
  message: 'Hello RaiderBot!',
  language: 'en'
});
```

## Webhooks

Configure webhooks for real-time events:

```json
POST /webhooks/configure
{
  "event_type": "delivery_completed|route_optimized|safety_alert",
  "endpoint_url": "https://your-endpoint.com/webhook",
  "secret": "your-webhook-secret"
}
```

## Best Practices

1. **Always include authentication headers**
2. **Use appropriate timeout values (30s recommended)**
3. **Implement exponential backoff for retries**
4. **Cache responses when appropriate**
5. **Monitor rate limits via X-RateLimit headers**

## Support

- **API Issues**: api-support@palantir.com
- **RaiderBot Specific**: raiderbot-api@raiderexpress.com
- **Status Page**: https://status.palantirfoundry.com

🐕 Built with German Shepherd reliability on Palantir Foundry!
