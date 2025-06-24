# Foundry Environment Audit Script
# Designed to run inside Palantir Foundry (Code Repositories, Transforms, etc.)

def audit_foundry_environment():
    """
    Audit your Foundry environment - run this inside Foundry for best results.
    """
    try:
        from foundry_platform_sdk import FoundryClient
        client = FoundryClient()
    except ImportError:
        # Fallback to the pattern you provided
        print("Using fallback client initialization...")
        # This assumes 'client' is available in the Foundry environment
        # which is typical in Foundry Code Repositories or Transform contexts
        pass
    
    print("=== FOUNDRY ENVIRONMENT AUDIT ===\n")
    
    try:
        # Dataset audit
        print("📊 DATASETS:")
        datasets = client.catalog.list_datasets()
        dataset_count = 0
        for dataset in datasets:
            print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
            dataset_count += 1
            if dataset_count >= 10:  # Limit output for readability
                remaining = len(list(datasets)) - 10
                if remaining > 0:
                    print(f"  ... and {remaining} more datasets")
                break
        
        print(f"\nTotal datasets found: {len(list(client.catalog.list_datasets()))}")
        
    except Exception as e:
        print(f"  ❌ Error listing datasets: {e}")
    
    try:
        # Ontology audit  
        print("\n🏗️ ONTOLOGY:")
        ontology = client.ontology.get_ontology()
        object_types = list(ontology.object_types.keys())
        print(f"  - Total Object Types: {len(object_types)}")
        
        # Show first 10 object types
        for i, obj_type in enumerate(object_types[:10]):
            print(f"  - {obj_type}")
        
        if len(object_types) > 10:
            print(f"  ... and {len(object_types) - 10} more object types")
            
    except Exception as e:
        print(f"  ❌ Error accessing ontology: {e}")
    
    try:
        # Applications audit
        print("\n📱 APPLICATIONS:")
        apps = client.applications.list_applications()
        app_count = 0
        for app in apps:
            print(f"  - App: {app.name} - Type: {app.type}")
            app_count += 1
            if app_count >= 10:  # Limit output for readability
                remaining = len(list(apps)) - 10
                if remaining > 0:
                    print(f"  ... and {remaining} more applications")
                break
                
        print(f"\nTotal applications found: {len(list(client.applications.list_applications()))}")
        
    except Exception as e:
        print(f"  ❌ Error listing applications: {e}")
    
    try:
        # Additional environment info
        print("\n🔍 ENVIRONMENT INFO:")
        print(f"  - Client type: {type(client)}")
        print(f"  - Available client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
        
    except Exception as e:
        print(f"  ❌ Error getting environment info: {e}")
    
    print("\n✅ AUDIT COMPLETE")
    
    return {
        'audit_completed': True,
        'location': 'inside_foundry_environment'
    }

# Run the audit
if __name__ == "__main__":
    results = audit_foundry_environment()
else:
    # If running in a Foundry notebook or transform, you might want to call it directly
    results = audit_foundry_environment()