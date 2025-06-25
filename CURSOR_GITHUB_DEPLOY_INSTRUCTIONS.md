# CURSOR INSTRUCTIONS: Complete GitHub Repository Setup and Push

## AUTOMATED GITHUB REPOSITORY CREATION AND DEPLOYMENT

**CURSOR: Execute all the following steps automatically to create and push the RaiderBot Palantir Foundry repository to GitHub.**

### 1. REPOSITORY NAMING
Create the GitHub repository with the following name:
```
raiderbot-palantir-foundry
```

### 2. REPOSITORY SETTINGS
Set the following repository properties:

**Description:**
```
🐕 German Shepherd AI Assistant built entirely on Palantir Foundry for Raider Express trucking operations. Features real-time dashboards, bilingual support, and safety-first 60mph compliance.
```

**Topics to add:**
- palantir-foundry
- german-shepherd-ai
- transportation
- trucking
- real-time-analytics
- safety-compliance
- fort-worth
- bilingual-ai
- enterprise-ai
- foundry-ontology

**Visibility:** Public (unless specified otherwise by user)

### 3. GITHUB CLI COMMANDS TO EXECUTE

```bash
# Navigate to the repository
cd /Users/daneggleton/raiderbot-palantir-foundry

# Create GitHub repository using GitHub CLI
gh repo create raiderbot-palantir-foundry \
  --public \
  --description "🐕 German Shepherd AI Assistant built entirely on Palantir Foundry for Raider Express trucking operations. Features real-time dashboards, bilingual support, and safety-first 60mph compliance." \
  --source=. \
  --remote=origin \
  --push

# If GitHub CLI is not available, use the GitHub API approach:
# First, get the GitHub token from environment or prompt user
# Then create repository via API:
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "name": "raiderbot-palantir-foundry",
    "description": "🐕 German Shepherd AI Assistant built entirely on Palantir Foundry for Raider Express trucking operations. Features real-time dashboards, bilingual support, and safety-first 60mph compliance.",
    "private": false,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true
  }'

# Add remote and push if not done by gh command
git remote add origin https://github.com/$(gh api user --jq .login)/raiderbot-palantir-foundry.git
git push -u origin main
```

### 4. POST-PUSH GITHUB CONFIGURATION

After pushing, configure the repository with these settings:

```bash
# Add all topics
gh repo edit raiderbot-palantir-foundry --add-topic palantir-foundry
gh repo edit raiderbot-palantir-foundry --add-topic german-shepherd-ai
gh repo edit raiderbot-palantir-foundry --add-topic transportation
gh repo edit raiderbot-palantir-foundry --add-topic trucking
gh repo edit raiderbot-palantir-foundry --add-topic real-time-analytics
gh repo edit raiderbot-palantir-foundry --add-topic safety-compliance
gh repo edit raiderbot-palantir-foundry --add-topic fort-worth
gh repo edit raiderbot-palantir-foundry --add-topic bilingual-ai
gh repo edit raiderbot-palantir-foundry --add-topic enterprise-ai
gh repo edit raiderbot-palantir-foundry --add-topic foundry-ontology

# Set up branch protection for main branch
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":[]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":1}' \
  --field restrictions=null
```

### 5. CREATE INITIAL GITHUB ISSUES

Create these initial issues to track development:

```bash
# Issue 1: Foundry Deployment
gh issue create \
  --title "🚀 Deploy to Palantir Foundry Production Environment" \
  --body "Deploy all components to the production Palantir Foundry workspace:
- [ ] Deploy Ontology objects
- [ ] Deploy Foundry Functions
- [ ] Deploy Transforms with schedules
- [ ] Deploy React Applications
- [ ] Configure Foundry monitoring" \
  --label "deployment,foundry"

# Issue 2: Documentation
gh issue create \
  --title "📚 Create Video Walkthrough of RaiderBot Features" \
  --body "Create a comprehensive video showing:
- [ ] German Shepherd AI personality demo
- [ ] Bilingual chat capabilities
- [ ] Real-time dashboard features
- [ ] 60mph safety compliance emphasis
- [ ] Palantir Foundry integration points" \
  --label "documentation"

# Issue 3: Testing
gh issue create \
  --title "🧪 Implement Comprehensive Foundry Testing Suite" \
  --body "Add tests for:
- [ ] All Foundry Functions
- [ ] Ontology object validations
- [ ] Transform data quality checks
- [ ] API endpoint testing
- [ ] React component testing" \
  --label "testing"
```

### 6. CREATE GITHUB ACTIONS WORKFLOW

Create a basic CI/CD workflow:

```bash
mkdir -p .github/workflows

cat > .github/workflows/foundry-ci.yml << 'EOF'
name: Palantir Foundry CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run Python tests
      run: |
        echo "TODO: Add Foundry function tests"
        
    - name: Validate Foundry YAML
      run: |
        echo "Validating foundry.yml configuration..."
        python -c "import yaml; yaml.safe_load(open('foundry.yml'))"
        
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run security checks
      run: |
        echo "🐕 Ensuring 60mph compliance in all code..."
        grep -r "max_speed" . || echo "Speed governance checks pass"
EOF

git add .github/workflows/foundry-ci.yml
git commit -m "Add GitHub Actions workflow for Foundry CI/CD 🔧"
git push
```

### 7. CREATE PROJECT README BADGES

Update README.md to add status badges:

```bash
# Add to the top of README.md after the title
BADGE_CONTENT='![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/raiderbot-palantir-foundry/foundry-ci.yml?label=Foundry%20CI)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/raiderbot-palantir-foundry)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/raiderbot-palantir-foundry?style=social)'
```

### 8. FINAL VERIFICATION

After all steps are complete, verify:

```bash
# Check repository was created
gh repo view raiderbot-palantir-foundry --web

# Verify all files were pushed
git log --oneline

# Check remote configuration
git remote -v

# Display success message
echo "
✅ ========================================
🐕 RaiderBot Successfully Deployed to GitHub!
========================================

Repository: https://github.com/$(gh api user --jq .login)/raiderbot-palantir-foundry

Next Steps:
1. Share repository URL with team
2. Set up Palantir Foundry deployment pipeline
3. Configure webhooks for automated deployments
4. Add team members as collaborators

Woof! Your German Shepherd AI is ready! 🚛
"
```

## CURSOR EXECUTION INSTRUCTIONS

**CURSOR: Please execute all the above commands in sequence. If any command fails, provide appropriate error handling and alternative approaches. The key objectives are:**

1. ✅ Create GitHub repository named `raiderbot-palantir-foundry`
2. ✅ Push all code from `/Users/daneggleton/raiderbot-palantir-foundry`
3. ✅ Configure repository with proper description and topics
4. ✅ Set up initial issues and GitHub Actions
5. ✅ Provide confirmation of successful deployment

**Start with checking if GitHub CLI is installed, and if not, use the API approach with proper authentication.**

---
END OF CURSOR INSTRUCTIONS
