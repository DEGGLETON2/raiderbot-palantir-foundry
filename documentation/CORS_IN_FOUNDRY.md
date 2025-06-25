# CORS in Palantir Foundry - Complete Guide

## What is CORS in Foundry?

CORS (Cross-Origin Resource Sharing) in Palantir Foundry controls how external applications can access your Foundry resources, including:
- Foundry Functions
- Foundry APIs
- Foundry Applications
- Foundry Datasets (via APIs)

## Why CORS Matters in Foundry

### 1. **Security**
- Prevents unauthorized websites from accessing your Foundry data
- Protects sensitive transportation data (driver info, routes, etc.)
- Ensures only approved applications can call your Foundry Functions

### 2. **Integration Scenarios**
- External dashboards accessing Foundry data
- Third-party applications calling RaiderBot
- Mobile apps connecting to Foundry
- Customer portals accessing delivery data

## CORS Configuration in Foundry

### For Foundry Functions (RaiderBot Example)

```python
# In your Foundry Function
from foundry_functions import function, cors_policy

@function(
    cors_policy=cors_policy(
        allowed_origins=[
            "https://raiderexpress.com",
            "https://app.raiderexpress.com",
            "http://localhost:3000"  # For development
        ],
        allowed_methods=["GET", "POST"],
        allowed_headers=["Content-Type", "Authorization"],
        max_age=3600
    )
)
def raiderbot_chat(message: str, language: str = "en"):
    """RaiderBot with CORS enabled for external access"""
    # Function implementation
    pass
```

### For Foundry Applications

```yaml
# In foundry.yml
applications:
  raiderbot_dashboard:
    type: foundry-react-application
    cors:
      enabled: true
      allowed_origins:
        - "https://raiderexpress.com"
        - "https://customer-portal.raiderexpress.com"
      allowed_methods:
        - GET
        - POST
        - OPTIONS
      credentials: true  # Allow cookies/auth headers
```

## Common CORS Scenarios in Foundry

### 1. **External Website Calling Foundry Function**
```javascript
// From raiderexpress.com website
fetch('https://foundry.palantir.com/api/functions/raiderbot_chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN'
    },
    body: JSON.stringify({
        message: "Track my delivery",
        language: "en"
    })
})
```

### 2. **Mobile App Accessing Foundry Data**
```swift
// iOS app accessing Foundry
let url = URL(string: "https://foundry.palantir.com/api/datasets/deliveries")
var request = URLRequest(url: url!)
request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
```

### 3. **Third-Party Integration**
```python
# Partner system accessing RaiderBot
import requests

response = requests.post(
    'https://foundry.palantir.com/api/functions/route_optimization',
    headers={'Authorization': f'Bearer {token}'},
    json={'delivery_ids': ['DEL001', 'DEL002']}
)
```

## CORS Errors and Solutions

### Common Error:
```
Access to XMLHttpRequest at 'https://foundry.palantir.com/api/...' 
from origin 'https://myapp.com' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present.
```

### Solutions:

1. **Add Origin to Allowed List**
```python
cors_policy(
    allowed_origins=[
        "https://myapp.com"  # Add this
    ]
)
```

2. **Enable Credentials (if using auth)**
```python
cors_policy(
    allowed_origins=["https://myapp.com"],
    allow_credentials=True
)
```

3. **Handle Preflight Requests**
```python
cors_policy(
    allowed_methods=["GET", "POST", "OPTIONS"],  # Include OPTIONS
    allowed_headers=["Content-Type", "Authorization"]
)
```

## Best Practices for CORS in Foundry

### 1. **Security First**
```python
# ❌ Don't do this - too permissive
cors_policy(allowed_origins=["*"])

# ✅ Do this - specific origins
cors_policy(allowed_origins=[
    "https://raiderexpress.com",
    "https://app.raiderexpress.com"
])
```

### 2. **Environment-Specific Origins**
```python
import os

if os.environ.get('ENVIRONMENT') == 'development':
    origins = ["http://localhost:3000", "http://localhost:8080"]
else:
    origins = ["https://raiderexpress.com", "https://app.raiderexpress.com"]

@function(cors_policy=cors_policy(allowed_origins=origins))
```

### 3. **Validate Origins Dynamically**
```python
def validate_origin(origin):
    allowed_patterns = [
        r"https://.*\.raiderexpress\.com$",
        r"https://raiderexpress\.com$"
    ]
    return any(re.match(pattern, origin) for pattern in allowed_patterns)
```

## RaiderBot CORS Configuration

For the RaiderBot application specifically:

```python
# palantir-functions/raiderbot_core.py
@function(
    runtime="foundry-python-3.9",
    cors_policy=cors_policy(
        allowed_origins=[
            "https://raiderexpress.com",
            "https://app.raiderexpress.com",
            "https://customer.raiderexpress.com",
            "http://localhost:3000"  # Development
        ],
        allowed_methods=["POST", "OPTIONS"],
        allowed_headers=["Content-Type", "Authorization", "X-Request-ID"],
        expose_headers=["X-Response-ID", "X-RateLimit-Remaining"],
        max_age=3600,
        allow_credentials=True
    )
)
def raiderbot_chat(message: str, language: str = "en", user_context: dict = None):
    """
    🐕 RaiderBot with CORS enabled for external access
    Allows customer portals and mobile apps to interact
    """
    # Implementation
    pass
```

## Troubleshooting CORS in Foundry

### 1. **Check Browser Console**
```javascript
// Look for CORS errors
console.log("CORS Error Details:", error);
```

### 2. **Verify Headers**
```bash
curl -I -X OPTIONS \
  -H "Origin: https://myapp.com" \
  -H "Access-Control-Request-Method: POST" \
  https://foundry.palantir.com/api/functions/raiderbot_chat
```

### 3. **Foundry Logs**
- Check Foundry Function logs for CORS rejections
- Monitor API Gateway logs
- Review security audit logs

## Summary

CORS in Palantir Foundry is essential for:
- 🔒 **Security**: Protecting your data from unauthorized access
- 🌐 **Integration**: Enabling legitimate external applications
- 📱 **Multi-Platform**: Supporting web, mobile, and partner access
- 🚛 **Business Value**: Allowing customers to track deliveries

For RaiderBot, proper CORS configuration ensures:
- Customer portals can access delivery tracking
- Mobile apps can interact with the German Shepherd AI
- Partner systems can integrate safely
- Development remains smooth with localhost access

🐕 Remember: Good CORS policies are like a well-trained German Shepherd - protective but friendly to authorized visitors!
