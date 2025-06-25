# Using Palantir VS Code Extension with RaiderBot

## 🎯 Palantir Extension Detected!
Version: `palantir.authoring-vscode-extension-0.425.38`

## Available VS Code Commands

Open VS Code/Cursor command palette (`Cmd+Shift+P`) and type "Palantir" to see all available commands:

### Common Palantir Commands:
- `Palantir: Open Documentation` - Access Foundry docs
- `Palantir: Connect to Foundry` - Authenticate with Foundry
- `Palantir: Deploy Function` - Deploy individual functions
- `Palantir: Deploy All` - Deploy entire project
- `Palantir: Test Function` - Test Foundry functions locally
- `Palantir: Sync Datasets` - Sync with Foundry datasets

## 🚀 Deploy RaiderBot to Foundry

### Step 1: Connect to Foundry
1. Open Command Palette: `Cmd+Shift+P`
2. Type: `Palantir: Connect to Foundry`
3. Enter your Foundry credentials
4. Select workspace: `raider-express-raiderbot`

### Step 2: Configure Project
Ensure `foundry.yml` is in the root directory (✅ Already present)

### Step 3: Deploy Components

#### Deploy Ontology Objects:
```
Palantir: Deploy Ontology
```
This will deploy all objects in `palantir-ontology/`

#### Deploy Functions:
```
Palantir: Deploy Functions
```
This will deploy:
- `raiderbot_core`
- `route_optimization`
- `safety_scoring`  
- `document_learning`

#### Deploy Transforms:
```
Palantir: Deploy Transforms
```
This will deploy:
- `snowflake_ingestion`
- `kpi_calculations`

### Step 4: Test RaiderBot
```
Palantir: Test Function
```
Select `raiderbot_core` and test with:
```json
{
  "message": "Hello RaiderBot!",
  "language": "en"
}
```

## 📝 VS Code Tasks Configuration

Create `.vscode/tasks.json` for quick deployment:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Deploy to Foundry",
      "type": "shell",
      "command": "echo 'Use Command Palette: Palantir: Deploy All'",
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Test RaiderBot",
      "type": "shell", 
      "command": "echo 'Use Command Palette: Palantir: Test Function'",
      "group": "test"
    }
  ]
}
```

## 🔧 Workspace Settings

Create `.vscode/settings.json`:

```json
{
  "palantir.foundry.workspace": "raider-express-raiderbot",
  "palantir.foundry.defaultEnvironment": "production",
  "palantir.foundry.autoSync": true,
  "palantir.foundry.datasets": {
    "raider_drivers": "ri.foundry.main.dataset.raider_drivers",
    "raider_vehicles": "ri.foundry.main.dataset.raider_vehicles",
    "raider_deliveries": "ri.foundry.main.dataset.raider_deliveries"
  }
}
```

## 🐕 Quick Actions for RaiderBot

1. **Deploy Everything:**
   - `Cmd+Shift+P` → `Palantir: Deploy All`

2. **Test German Shepherd AI:**
   - `Cmd+Shift+P` → `Palantir: Test Function`
   - Select `raiderbot_core`
   - Test message: `"¿Cómo están las entregas hoy?"`

3. **View Foundry Logs:**
   - `Cmd+Shift+P` → `Palantir: View Logs`

4. **Sync with MCLEOD_DB:**
   - `Cmd+Shift+P` → `Palantir: Run Transform`
   - Select `snowflake_ingestion`

## 📊 Monitor Deployment

After deployment, verify in Foundry:
1. Check function status
2. Verify transform schedules
3. Test API endpoints
4. Monitor performance metrics

---

🎉 **You're ready to deploy RaiderBot to Palantir Foundry using VS Code!**
