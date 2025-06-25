# 🚀 RaiderBot Palantir Foundry Quick Deploy Guide

## ✅ Prerequisites Check
- [x] Palantir VS Code Extension installed (v0.425.38)
- [x] Repository ready at: `/Users/daneggleton/raiderbot-palantir-foundry`
- [x] VS Code configuration files created

## 🎯 Quick Deploy Steps

### 1️⃣ Open Command Palette
Press: `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows)

### 2️⃣ Connect to Foundry
Type: `Palantir: Connect to Foundry`
- Enter credentials
- Select workspace: `raider-express-raiderbot`

### 3️⃣ Deploy Everything
Type: `Palantir: Deploy All`

This will deploy:
- ✅ 6 Ontology Objects (Driver, Vehicle, Delivery, Route, SafetyIncident, Customer)
- ✅ 4 Functions (raiderbot_core, route_optimization, safety_scoring, document_learning)
- ✅ 2 Transforms (snowflake_ingestion, kpi_calculations)
- ✅ 2 Applications (dashboard, chat-interface)

### 4️⃣ Test RaiderBot
Type: `Palantir: Test Function`
- Select: `raiderbot_core`
- Test input:
```json
{
  "message": "Hello RaiderBot!",
  "language": "en"
}
```

Expected response:
```json
{
  "message": "🐕 Woof! I'm RaiderBot, built entirely on Palantir Foundry...",
  "language": "en",
  "powered_by": "Palantir Foundry"
}
```

## 📊 Post-Deployment Verification

### Check Datasets
Type: `Palantir: View Dataset`
- Verify MCLEOD_DB.dbo tables are syncing
- Check data freshness

### Monitor Transforms
Type: `Palantir: View Transform Logs`
- `snowflake_ingestion` - Should run every 15 minutes
- `kpi_calculations` - Should run every 5 minutes

### View Function Logs
Type: `Palantir: View Logs`
- Check for any deployment errors
- Monitor function execution

## 🐕 Common Commands Reference

| Action | Command Palette Entry |
|--------|----------------------|
| Deploy All | `Palantir: Deploy All` |
| Deploy Functions Only | `Palantir: Deploy Functions` |
| Test Function | `Palantir: Test Function` |
| View Logs | `Palantir: View Logs` |
| Run Transform | `Palantir: Run Transform` |
| View Dataset | `Palantir: View Dataset` |
| Connect to Foundry | `Palantir: Connect to Foundry` |

## 🚨 Troubleshooting

### Authentication Issues
- Re-run: `Palantir: Connect to Foundry`
- Check VPN connection if required
- Verify workspace permissions

### Deployment Failures
- Check `foundry.yml` syntax
- Verify Python syntax in functions
- Review logs: `Palantir: View Logs`

### Dataset Sync Issues
- Check MCLEOD_DB credentials
- Verify table names: `MCLEOD_DB.dbo.*`
- Run manual sync: `Palantir: Run Transform`

## 🎉 Success Indicators

When deployment is successful, you should see:
- ✅ "Deployment successful" notification
- ✅ Functions appear in Foundry UI
- ✅ Transforms show "Active" status
- ✅ Datasets updating on schedule
- ✅ RaiderBot responds to test messages

---

**Ready to deploy! Press `Cmd+Shift+P` and start with `Palantir: Connect to Foundry`** 🐕🚀
