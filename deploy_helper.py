#!/usr/bin/env python3
"""
RaiderBot Automated Deployment Helper
Triggers Palantir Foundry deployment through VS Code
"""

import os
import subprocess
import time
import json

def deploy_to_foundry():
    """Deploy RaiderBot to Palantir Foundry"""
    
    print("🐕 RaiderBot Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("foundry.yml"):
        print("❌ Error: foundry.yml not found. Are you in the right directory?")
        return False
    
    print("✅ Found foundry.yml")
    
    # Create a deployment manifest
    deployment_manifest = {
        "workspace": "raider-express-raiderbot",
        "components": {
            "ontology": {
                "objects": [
                    "Driver", "Vehicle", "Delivery", 
                    "Route", "SafetyIncident", "Customer"
                ],
                "path": "palantir-ontology/"
            },
            "functions": {
                "functions": [
                    "raiderbot_core", "route_optimization",
                    "safety_scoring", "document_learning"
                ],
                "path": "palantir-functions/"
            },
            "transforms": {
                "transforms": [
                    "snowflake_ingestion", "kpi_calculations"
                ],
                "path": "palantir-transforms/"
            }
        },
        "deployment_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save deployment manifest
    with open(".foundry_deployment.json", "w") as f:
        json.dump(deployment_manifest, f, indent=2)
    
    print("📋 Created deployment manifest")
    
    # Try to open VS Code with deployment command
    print("\n🚀 Attempting deployment via VS Code...")
    
    # Create a VS Code command file
    vscode_commands = """
// RaiderBot Deployment Commands
// Run these in VS Code Command Palette (Cmd+Shift+P)

1. Palantir: Connect to Foundry
   - Workspace: raider-express-raiderbot
   
2. Palantir: Deploy All
   - This will deploy all components

3. Palantir: Test Function
   - Function: raiderbot_core
   - Input: {"message": "Hello RaiderBot!", "language": "en"}

4. Palantir: View Logs
   - Check deployment status
"""
    
    with open("DEPLOY_COMMANDS.txt", "w") as f:
        f.write(vscode_commands)
    
    # Try to trigger VS Code
    try:
        # Open VS Code with the project
        subprocess.run(["code", "."], check=False)
        print("✅ Opened VS Code")
        
        # Open the deployment commands file
        subprocess.run(["code", "DEPLOY_COMMANDS.txt"], check=False)
        print("✅ Opened deployment commands")
        
        print("\n" + "="*50)
        print("📌 NEXT STEPS:")
        print("1. VS Code should now be open")
        print("2. Press Cmd+Shift+P to open Command Palette")
        print("3. Run the commands shown in DEPLOY_COMMANDS.txt")
        print("4. Start with: 'Palantir: Connect to Foundry'")
        print("="*50)
        
    except Exception as e:
        print(f"⚠️ Could not open VS Code automatically: {e}")
        print("Please open VS Code manually and run the commands in DEPLOY_COMMANDS.txt")
    
    return True

def check_deployment_status():
    """Check if deployment was successful"""
    if os.path.exists(".foundry_deployment.json"):
        with open(".foundry_deployment.json", "r") as f:
            manifest = json.load(f)
        print(f"\n📊 Last deployment attempt: {manifest['deployment_time']}")
        print(f"Workspace: {manifest['workspace']}")
        print("\nComponents to deploy:")
        for component, details in manifest['components'].items():
            print(f"- {component}: {len(details[component])} items")

if __name__ == "__main__":
    os.chdir("/Users/daneggleton/raiderbot-palantir-foundry")
    deploy_to_foundry()
    check_deployment_status()
