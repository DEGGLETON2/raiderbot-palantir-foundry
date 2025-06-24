# Palantir Foundry Deployment Guide for RaiderBot

## Prerequisites

### 1. Foundry Access Requirements
- Valid Palantir Foundry account with appropriate permissions
- Access to Raider Express Foundry workspace
- Foundry CLI installed and configured
- API tokens for programmatic access

### 2. Development Environment
```bash
# Install Foundry CLI
curl -L https://docs.palantir.com/foundry/cli/install.sh | bash

# Verify installation
foundry --version

# Configure authentication
foundry auth login
```

## Deployment Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/raider-express/raiderbot-palantir-foundry.git
cd raiderbot-palantir-foundry
```

### Step 2: Configure Foundry Credentials
```bash
# Copy template and add your credentials
cp .foundry/credentials.template .foundry/credentials.json

# Edit with your Foundry details
nano .foundry/credentials.json
```

### Step 3: Deploy Foundry Ontology
```bash
# Deploy all ontology objects to Foundry
foundry ontology deploy palantir-ontology/

# Verify deployment
foundry ontology list --workspace raider-express-raiderbot
```

### Step 4: Deploy Foundry Functions
```bash
# Deploy all functions to Foundry's serverless platform
foundry functions deploy palantir-functions/

# Test RaiderBot core function
foundry functions invoke raiderbot_core \
  --input '{"message": "Hello RaiderBot!", "language": "en"}'
```

### Step 5: Deploy Foundry Transforms
```bash
# Deploy data transformation pipelines
foundry transforms deploy palantir-transforms/

# Schedule transform execution
foundry transforms schedule snowflake_ingestion --cron "*/15 * * * *"
foundry transforms schedule kpi_calculations --cron "*/5 * * * *"
```

### Step 6: Deploy Foundry Applications
```bash
# Build React applications
cd palantir-applications/dashboard
npm install && npm run build

cd ../chat-interface
npm install && npm run build

# Deploy to Foundry Applications platform
foundry applications deploy
```

## Production Deployment

### Environment Configuration
```yaml
# Production settings for foundry.yml
environment:
  FOUNDRY_WORKSPACE: raider-express-production
  PALANTIR_HOSTNAME: raiderexpress.palantirfoundry.com
  ENVIRONMENT: production
  SAFETY_SPEED_LIMIT: "60"  # Non-negotiable
```

### Security Checklist
- [ ] All API keys stored in Foundry Secrets
- [ ] Role-based access control configured
- [ ] Data encryption enabled
- [ ] Audit logging activated
- [ ] SSL/TLS certificates valid

### Monitoring Setup
```bash
# Enable Foundry monitoring
foundry monitoring enable --workspace raider-express-raiderbot

# Set up alerts
foundry alerts create \
  --name "RaiderBot Function Errors" \
  --metric function_errors \
  --threshold 5 \
  --window 5m
```

## Rollback Procedures

### Function Rollback
```bash
# List function versions
foundry functions versions raiderbot_core

# Rollback to previous version
foundry functions rollback raiderbot_core --version v1.2.3
```

### Dataset Rollback
```bash
# Restore dataset to previous state
foundry datasets restore raider_kpi_dashboard --timestamp "2024-01-01T00:00:00Z"
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   ```bash
   foundry auth refresh
   foundry auth validate
   ```

2. **Transform Failures**
   ```bash
   foundry transforms logs kpi_calculations --tail 100
   ```

3. **Function Timeout**
   - Increase timeout in meta.yaml
   - Optimize query performance
   - Check Foundry resource limits

## Support

- **Foundry Issues**: support@palantir.com
- **RaiderBot Issues**: raiderbot-team@raiderexpress.com
- **Documentation**: https://docs.palantir.com/foundry

🐕 Remember: Safety first! All deployments must maintain 60mph compliance.
