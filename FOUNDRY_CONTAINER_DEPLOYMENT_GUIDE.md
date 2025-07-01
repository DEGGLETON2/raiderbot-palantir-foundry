# RaiderBot Foundry Container Deployment Guide

## Overview
Complete step-by-step guide for deploying RaiderBot email pipeline as a Foundry container transform using Docker containers from the Artifacts repository.

## Prerequisites
- Container workflows enabled in Foundry Control Panel
- Access to create model resources in Foundry
- Docker installed locally
- Foundry workspace access

## Phase 1: Container Preparation

### Step 1: Build Foundry-Compatible Docker Image
```bash
# Navigate to repository
cd /Users/daneggleton/raiderbot-palantir-foundry

# Build with Foundry requirements (linux/amd64, non-root user)
docker build --platform linux/amd64 -t raiderbot-email-intelligence-api:v1.0 .

# Verify image was built
docker images | grep raiderbot-email
```

### Step 2: Test Container Locally (Optional)
```bash
# Run container locally to verify functionality
docker run -p 8080:8080 raiderbot-email-intelligence-api:v1.0

# Test health endpoint
curl http://localhost:8080/health

# Test email pipeline endpoint
curl -X POST http://localhost:8080/api/full-pipeline
```

## Phase 2: Push to Foundry Artifacts Repository

### Step 1: Create Model Resource in Foundry
1. Navigate to Foundry workspace
2. Go to modeling objective
3. Select **+ Add model → Import containerized model**
4. Name: `raiderbot-email-pipeline-container`
5. Description: `RaiderBot email intelligence pipeline container`

### Step 2: Generate Push Commands
1. In model creation wizard, select **Generate token**
2. Copy the provided authentication and push commands
3. Commands will look like:
```bash
# Login to Foundry registry
docker login <foundry-registry-url> -u <username> -p <token>

# Tag image for Foundry
docker tag raiderbot-email-intelligence-api:v1.0 <foundry-registry-url>/<model-asset>:v1.0

# Push to Foundry
docker push <foundry-registry-url>/<model-asset>:v1.0
```

### Step 3: Execute Push Commands
```bash
# Replace placeholders with actual values from Foundry
# Execute the generated commands in sequence
```

### Step 4: Verify Upload
- Check model's container images list in Foundry UI
- Image should appear as available for use

## Phase 3: Create Container Transform

### Step 1: Update Container Transform Configuration
Edit `container_transform.py` with actual values:

```python
@sidecar(
    image="<foundry-registry-url>/<model-asset>",  # From step 2
    tag="v1.0",  # Your specific tag
    volumes=[Volume("shared")]
)
@transform(
    output=Output("ri.foundry.main.dataset.<your-dataset-RID>"),  # Your dataset RID
)
```

### Step 2: Create Transform in Foundry
1. In Code Repository, go to Files panel
2. Select **Add → New file from template**
3. Choose container/sidecar transform template
4. Configure input/output datasets
5. Paste container transform code
6. Save and validate

### Step 3: Register Transform (if needed)
Update `setup.py` or equivalent:
```python
entry_points={
    'palantir.transforms': [
        'raiderbot_email_container_transform = container_transform:raiderbot_email_container_transform',
    ]
}
```

## Phase 4: Deploy and Execute

### Step 1: Build Transform
- In Foundry, build the transform
- Resolve any validation errors
- Generate transform file

### Step 2: Create Pipeline
- Add transform to a pipeline
- Configure scheduling if needed
- Set up input datasets (if any)

### Step 3: Execute Transform
- Run pipeline containing the container transform
- Monitor execution logs
- Check output dataset for results

## Key Files Created

### Core Files
- `Dockerfile` - Foundry-compatible container definition
- `app.py` - Flask API server for email pipeline
- `entrypoint.py` - Container execution entry point
- `container_transform.py` - Foundry container transform definition

### Configuration Files
- `requirements.txt` - Updated with Flask dependencies
- `foundry-app.yml` - Application configuration (legacy)
- `FOUNDRY_CONTAINER_DEPLOYMENT_GUIDE.md` - This guide

## Expected Results

### Container Transform Output Dataset Schema
```
email_id: string
subject: string  
sender: string
timestamp: string
content_preview: string
sentiment_score: float
sentiment_label: string
critical_issue: boolean
generated_response: string
pipeline_timestamp: string
deployment_type: string
```

### Execution Flow
1. Foundry triggers container transform
2. Container executes email pipeline via `entrypoint.py`
3. Pipeline results written to shared volume
4. Transform reads results and creates dataset
5. Output dataset available in Foundry

## Troubleshooting

### Common Issues
- **Image push timeout**: Reduce image size or contact Palantir
- **Non-root user errors**: Verify Dockerfile USER directive
- **Platform compatibility**: Ensure linux/amd64 build
- **Shared volume access**: Check file permissions in container

### Debug Commands
```bash
# Check container logs
docker logs <container-id>

# Inspect shared volume
docker exec -it <container-id> ls -la /shared

# Test entrypoint directly
docker run -it raiderbot-email-intelligence-api:v1.0 python entrypoint.py
```

## Validation Checklist

- [ ] Docker image builds successfully with linux/amd64 platform
- [ ] Container runs with non-root user (foundryuser)
- [ ] Image pushed to Foundry Artifacts repository
- [ ] Container transform created in Code Repository
- [ ] Transform validates without errors
- [ ] Pipeline executes successfully
- [ ] Output dataset contains expected results
- [ ] Email pipeline functions accessible and operational

## Next Steps After Deployment

1. **Schedule Pipeline**: Set up automated execution schedule
2. **Monitor Results**: Create dashboard for pipeline outputs
3. **Scale as Needed**: Adjust container resources if required
4. **Integrate with Foundry**: Connect to other Foundry workflows
5. **Maintain Container**: Update image as pipeline evolves

---

This container deployment approach bypasses the function registration issues and provides a robust, scalable way to run the RaiderBot email pipeline within Foundry's infrastructure.
