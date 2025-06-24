# 🚀 RaiderBot Foundry Deployment Commands

## 📋 **Quick Command Reference**

Execute these commands in sequence in your Cursor terminal:

### **Step 1: Create Foundry Workspace**
```bash
foundry workspace create raider-express-operations
foundry workspace set-default raider-express-operations
```

### **Step 2: Deploy Ontology**
```bash
foundry ontology deploy ontology/objects/
foundry ontology deploy ontology/link_types/
```

### **Step 3: Deploy Data Transforms**
```bash
foundry transforms deploy transforms/snowflake_ingestion.py
foundry transforms deploy transforms/kpi_calculations.py
```

### **Step 4: Deploy AI Functions**
```bash
foundry functions deploy functions/route_optimization.py
foundry functions deploy functions/safety_scoring.py
foundry functions deploy functions/ai_chat_handler.py
```

### **Step 5: Configure Schedules**
```bash
foundry transforms schedule transforms/snowflake_ingestion.py --cron "*/15 * * * *"
foundry transforms schedule transforms/kpi_calculations.py --cron "*/5 * * * *"
```

### **Step 6: Deploy Chat Interface**
```bash
cd applications/dashboard
npm install
npm run build
foundry apps deploy raiderbot-chat --port 3000
cd ../..
```

---

## 🤖 **Automated Deployment Script**

For complete automated deployment, run:

```bash
chmod +x deploy-raiderbot.sh
./deploy-raiderbot.sh
```

This will execute all steps above automatically with error checking and verification.

---

## 🧪 **Testing Commands**

### **Test RaiderBot Functionality**
```bash
# Basic chat test
foundry ai test raiderbot --scenario basic_chat

# Dashboard generation test  
foundry ai test raiderbot --scenario dashboard_generation

# Data analysis test
foundry ai test raiderbot --scenario data_analysis
```

### **Verify Deployment**
```bash
# Check workspace
foundry workspace info

# List ontology objects
foundry ontology list

# List deployed transforms
foundry transforms list

# List deployed functions
foundry functions list

# Check application status
foundry apps list
```

---

## 📊 **Expected Datasets After Deployment**

- `ri.foundry.main.dataset.raider_drivers`
- `ri.foundry.main.dataset.raider_vehicles`
- `ri.foundry.main.dataset.raider_deliveries`
- `ri.foundry.main.dataset.raider_routes`
- `ri.foundry.main.dataset.safety_incidents`
- `ri.foundry.main.dataset.customers`
- `ri.foundry.main.dataset.raider_kpi_dashboard`

---

## 🐕 **Testing RaiderBot After Deployment**

Try these sample queries in the chat interface:

### **English Queries**
- "Hello RaiderBot, how are our deliveries today?"
- "Show me safety metrics for this week"
- "Build me an executive dashboard for today's operations"
- "Which drivers need safety training?"
- "Optimize the downtown delivery route"

### **Spanish Queries**
- "¿Cómo están nuestros conductores hoy?"
- "Muéstrame el rendimiento de entregas de hoy"
- "¿Qué rutas están retrasadas?"
- "Crea un dashboard de seguridad"

---

## 🏆 **Success Indicators**

✅ **RaiderBot responds with German Shepherd personality**  
✅ **Bot can query all datasets and return current data**  
✅ **Bot creates working React dashboards on demand**  
✅ **Bot processes uploaded documents and images**  
✅ **Bot responds appropriately in English and Spanish**  
✅ **Bot maintains 60mph safety-first messaging**  

Woof! RaiderBot should be ready to serve Raider Express! 🐕