# Cursor MCP Integration Instructions for Palantir Foundry

## Setting Up MCP Server for RaiderBot

To enable me to interact with Cursor's MCP setup for Palantir, please configure the following:

### 1. Create MCP Server Configuration

Create or update `.continue/mcpServers/palantir-foundry.yaml`:

```yaml
name: Palantir Foundry MCP
version: 1.0.0
schema: v1
mcpServers:
  - name: palantir-foundry
    command: npx
    args:
      - -y
      - @palantir/mcp-server-foundry
    env:
      FOUNDRY_TOKEN: ${FOUNDRY_TOKEN}
      FOUNDRY_WORKSPACE: raider-express-raiderbot
      FOUNDRY_URL: https://raiderexpress.palantirfoundry.com
```

### 2. Update Continue Configuration

In `.continue/config.yaml`, add the MCP server:

```yaml
mcpServers:
  - name: palantir-foundry
    transport: stdio
```

### 3. Available MCP Commands

Once configured, you can use these commands in Cursor:

#### Query Foundry Datasets
```
/mcp query dataset:raider_drivers
/mcp query dataset:raider_deliveries
```

#### Execute Foundry Functions
```
/mcp function raiderbot_core {"message": "Hello", "language": "en"}
/mcp function route_optimization {"delivery_ids": ["DEL001", "DEL002"]}
```

#### Deploy to Foundry
```
/mcp deploy functions
/mcp deploy transforms
/mcp deploy ontology
```

### 4. Test the Connection

```bash
# Test MCP connection
/mcp test

# List available Foundry resources
/mcp list datasets
/mcp list functions
/mcp list transforms
```

## For Me to Interact with Cursor MCP:

1. **File-Based Commands**: I'll create command files that Cursor MCP can execute
2. **Status Monitoring**: I'll read MCP output files to track execution
3. **Deployment Scripts**: I'll generate deployment configurations

## Example Workflow:

1. I create: `mcp-commands.txt`
```
deploy:functions:raiderbot_core
deploy:transforms:snowflake_ingestion
test:function:raiderbot_core:{"message":"🐕 Woof!"}
```

2. You run in Cursor:
```
/mcp batch mcp-commands.txt
```

3. I read results from: `mcp-results.json`

## Current Tasks for Cursor MCP:

1. **Push to GitHub**
```
/mcp git push origin main
```

2. **Deploy to Foundry**
```
/mcp deploy all
```

3. **Test RaiderBot**
```
/mcp test function:raiderbot_core
```

---

**Note**: If the Palantir MCP server isn't installed, you may need to:
```bash
npm install -g @palantir/mcp-server-foundry
```

Or use the standard Cursor commands without MCP integration.
