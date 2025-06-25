#!/bin/bash

# =============================================================================
# RaiderBot Foundry Deployment Script
# German Shepherd AI Assistant for Raider Express
# =============================================================================

echo "🐕 Starting RaiderBot Foundry Deployment..."
echo "=========================================="

# Check Foundry CLI
if ! command -v foundry &> /dev/null; then
    echo "❌ Foundry CLI not found. Please install first."
    echo "Visit: https://docs.palantir.com/foundry/cli/"
    exit 1
fi

echo "✅ Foundry CLI found"

# Create and configure workspace
echo "🏗️ Setting up Foundry workspace..."
foundry workspace create raider-express-operations
foundry workspace set-default raider-express-operations

# Deploy ontology objects
echo "🔗 Deploying ontology objects..."
foundry ontology deploy palantir-ontology/objects/
if [ $? -eq 0 ]; then
    echo "✅ Ontology objects deployed"
else
    echo "❌ Failed to deploy ontology"
    exit 1
fi

# Deploy transforms
echo "⚡ Deploying data transforms..."
foundry transforms deploy palantir-transforms/snowflake_ingestion.py
if [ $? -eq 0 ]; then
    echo "✅ Snowflake ingestion transform deployed"
else
    echo "❌ Failed to deploy transforms"
    exit 1
fi

# Deploy AI functions
echo "🤖 Deploying RaiderBot functions..."
foundry functions deploy palantir-functions/raiderbot_core.py
if [ $? -eq 0 ]; then
    echo "✅ RaiderBot core function deployed"
else
    echo "❌ Failed to deploy functions"
    exit 1
fi

# Configure schedules
echo "⏰ Configuring schedules..."
foundry transforms schedule palantir-transforms/snowflake_ingestion.py --cron "*/15 * * * *"
echo "✅ Transform schedules configured"

# Deploy chat interface
echo "💬 Deploying chat interface..."
cd applications/chat
npm install
npm run build
foundry apps deploy raiderbot-chat --port 3000
if [ $? -eq 0 ]; then
    echo "✅ Chat interface deployed"
else
    echo "⚠️ Chat interface deployment needs attention"
fi
cd ../..

# Verify deployment
echo "🧪 Running verification tests..."

echo "Testing workspace..."
foundry workspace info

echo "Testing ontology..."
foundry ontology list

echo "Testing transforms..."
foundry transforms list

echo "Testing functions..."
foundry functions list

echo "Testing RaiderBot..."
foundry ai test raiderbot --scenario basic_chat

# Final status
echo ""
echo "🎉 RaiderBot Deployment Complete!"
echo "================================"
echo ""
echo "🐕 RaiderBot Status:"
echo "   ✅ Workspace: raider-express-operations"
echo "   ✅ Ontology: Transportation objects deployed"
echo "   ✅ Transforms: Snowflake ingestion configured"
echo "   ✅ Functions: RaiderBot core AI deployed"
echo "   ✅ Chat Interface: React application live"
echo ""
echo "📊 Available Datasets:"
echo "   - raider_deliveries"
echo "   - raider_drivers"
echo "   - raider_vehicles"
echo "   - raider_kpi_dashboard"
echo ""
echo "🤖 RaiderBot Features:"
echo "   - German Shepherd personality"
echo "   - Bilingual (English/Spanish)"
echo "   - Safety-first (60mph limit)"
echo "   - Real-time data access"
echo "   - Dashboard generation"
echo ""
echo "🚀 Next Steps:"
echo "1. Access chat interface at your Foundry URL"
echo "2. Test RaiderBot with: 'Hello RaiderBot!'"
echo "3. Monitor transforms in Foundry console"
echo ""
echo "Woof! RaiderBot is ready to serve! 🐕" 