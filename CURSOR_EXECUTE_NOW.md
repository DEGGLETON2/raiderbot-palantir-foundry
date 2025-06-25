# Cursor Tasks - Execute These Commands

## 1. Git Operations
```bash
# Add new files
git add CURSOR_GITHUB_DEPLOY_INSTRUCTIONS.md CURSOR_MCP_SETUP.md documentation/CORS_IN_FOUNDRY.md

# Commit changes
git commit -m "Add Cursor integration docs and CORS guide 📚"

# Create and push to GitHub
gh repo create raiderbot-palantir-foundry \
  --public \
  --description "🐕 German Shepherd AI Assistant built entirely on Palantir Foundry for Raider Express trucking operations" \
  --source=. \
  --push
```

## 2. If GitHub CLI not available, use git directly:
```bash
# Create repo on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/raiderbot-palantir-foundry.git
git push -u origin main
```

## 3. After push, add topics:
```bash
gh repo edit raiderbot-palantir-foundry \
  --add-topic palantir-foundry \
  --add-topic german-shepherd-ai \
  --add-topic transportation
```

## 4. Test Palantir Connection (if MCP configured):
```
/palantir test connection
/palantir list datasets
/palantir function raiderbot_core test
```

## 5. Current Status Check:
```bash
pwd
git status
git remote -v
```

---
**Execute these commands in order to complete the GitHub deployment**
