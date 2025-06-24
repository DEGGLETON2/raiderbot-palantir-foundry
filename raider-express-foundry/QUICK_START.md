# 🐕 RaiderBot Quick Start Guide

## 🎯 **Minimal Deployment (Recommended First Step)**

Use the simplified configuration to get RaiderBot working quickly:

### **Step 1: Deploy with Minimal Config**
```bash
# Use the minimal configuration
foundry ai create-bot raiderbot --config raiderbot-minimal-config.yml
```

### **Step 2: Test Basic Functionality**
```bash
# Test basic chat
foundry ai chat raiderbot "Hello RaiderBot, how are deliveries today?"

# Test bilingual support
foundry ai chat raiderbot "¿Cómo están nuestros conductores?"

# Test data access
foundry ai chat raiderbot "Show me driver performance metrics"

# Test dashboard generation
foundry ai chat raiderbot "Create a simple KPI dashboard"
```

## 📋 **Minimal RaiderBot Configuration**

**[`raiderbot-minimal-config.yml`](raiderbot-minimal-config.yml)** contains:

- **🐕 German Shepherd personality** with safety-first focus
- **Bilingual support** (English/Spanish)
- **Data access** to core datasets (deliveries, drivers, vehicles, KPIs)
- **Core capabilities** (chat, data analysis, dashboard generation, code creation)

## 🚀 **If Minimal Works, Then Scale Up**

Once the minimal bot is working, you can:

1. **Deploy full ontology**: Use [`deploy-raiderbot.sh`](deploy-raiderbot.sh)
2. **Add advanced features**: Use [`raiderbot-deployment-config.yml`](raiderbot-deployment-config.yml)
3. **Deploy chat interface**: Use [`applications/dashboard/src/components/RaiderBotChat.tsx`](applications/dashboard/src/components/RaiderBotChat.tsx)

## ✅ **Success Test**

RaiderBot should respond like:
```
🐕 Woof! Based on today's data from Raider Express:

📊 Delivery Performance:
- 45 deliveries completed 
- 92% on-time rate
- 18 active drivers
- Average speed: 58 mph (complying with 60 mph limit)

¿Te gustaría que profundice en algún aspecto específico?
```

**Start simple, then scale! 🐕**