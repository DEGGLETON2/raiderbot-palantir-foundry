# Complete Foundry Environment Audit
# Works with multiple SDK configurations

def audit_foundry_environment():
    """
    Complete Foundry environment audit - tries multiple SDK approaches
    """
    print("=== FOUNDRY ENVIRONMENT AUDIT ===\n")
    
    # Try different SDK approaches
    client = None
    sdk_type = "unknown"
    
    # Approach 1: Official Palantir SDK (as shown in your example)
    try:
        from palantir_foundry_sdk import FoundryRestClient
        from palantir_foundry_sdk.datasets import Dataset
        from palantir_foundry_sdk.ontology import OntologyClient
        from palantir_foundry_sdk.catalog import CatalogClient
        from palantir_foundry_sdk.applications import ApplicationsClient
        
        foundry_url = "roiderxpress.palantirfoundry.com"
        auth_token = "eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncIVEOWZkeFNCeVZGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFRFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
        
        client = FoundryRestClient(
            hostname=foundry_url,
            auth_token=auth_token
        )
        
        # Test the connection
        catalog = CatalogClient(client)
        ontology = OntologyClient(client)
        applications = ApplicationsClient(client)
        
        sdk_type = "palantir_foundry_sdk"
        print("✅ Using Official Palantir Foundry SDK")
        
    except ImportError:
        print("⚠️  Official Palantir SDK not available")
    except Exception as e:
        print(f"⚠️  Official Palantir SDK error: {e}")
    
    # Approach 2: Foundry Dev Tools (already installed)
    if client is None:
        try:
            from foundry_dev_tools import CachedFoundryClient, FoundryContext, JWTTokenProvider
            
            token_provider = JWTTokenProvider(
                host="roiderxpress.palantirfoundry.com",
                jwt="eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncKVEOWZkeFNCeVpGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFJFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
            )
            
            ctx = FoundryContext(token_provider=token_provider)
            client = CachedFoundryClient(ctx=ctx)
            sdk_type = "foundry_dev_tools"
            print("✅ Using Foundry Dev Tools SDK")
            
        except Exception as e:
            print(f"⚠️  Foundry Dev Tools error: {e}")
    
    # Approach 3: Assume client exists in environment (original code)
    if client is None:
        try:
            # This assumes 'client' is available globally (like in Foundry environments)
            globals()['client'] = client  # This will fail, but let's see what happens
            sdk_type = "environment_client"
            print("✅ Using Environment Client")
        except:
            print("❌ No client available in environment")
    
    if client is None:
        print("\n❌ UNABLE TO INITIALIZE FOUNDRY CLIENT")
        print("\n💡 SOLUTIONS:")
        print("1. Run this inside Palantir Foundry (Code Repository/Notebook)")
        print("2. Install the official Palantir Foundry SDK")
        print("3. Ensure you have proper network access to Foundry")
        return {'error': 'no_client_available'}
    
    print(f"\n🔧 SDK TYPE: {sdk_type}")
    print("\n" + "="*60)
    
    results = {}
    
    # Dataset audit - adapted for different SDKs
    try:
        print("\n📊 DATASETS:")
        
        if sdk_type == "palantir_foundry_sdk":
            datasets = catalog.list_datasets()
            for dataset in datasets:
                print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
            results['datasets'] = len(list(datasets))
            
        elif sdk_type == "foundry_dev_tools":  
            # This SDK focuses on dataset operations
            print("  - Using foundry-dev-tools (dataset-focused SDK)")
            print("  - Available methods:", [m for m in dir(client.api) if 'dataset' in m.lower()][:5])
            results['datasets'] = 'foundry_dev_tools_detected'
            
        else:
            # Original approach
            datasets = client.catalog.list_datasets()
            for dataset in datasets:
                print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
            results['datasets'] = len(list(datasets))
            
    except Exception as e:
        print(f"  ❌ Dataset audit error: {e}")
        results['datasets'] = f'error: {e}'
    
    # Ontology audit - adapted for different SDKs  
    try:
        print("\n🏗️ ONTOLOGY:")
        
        if sdk_type == "palantir_foundry_sdk":
            ontology_data = ontology.get_ontology()
            object_types = list(ontology_data.object_types.keys())
            print(f"  - Object Types: {object_types}")
            results['ontology'] = len(object_types)
            
        elif sdk_type == "foundry_dev_tools":
            print("  - Ontology operations not available in foundry-dev-tools")
            results['ontology'] = 'not_available_in_dev_tools'
            
        else:
            # Original approach
            ontology_data = client.ontology.get_ontology()
            object_types = list(ontology_data.object_types.keys())
            print(f"  - Object Types: {object_types}")
            results['ontology'] = len(object_types)
            
    except Exception as e:
        print(f"  ❌ Ontology audit error: {e}")
        results['ontology'] = f'error: {e}'
    
    # Applications audit - adapted for different SDKs
    try:
        print("\n📱 APPLICATIONS:")
        
        if sdk_type == "palantir_foundry_sdk":
            apps = applications.list_applications()
            for app in apps:
                print(f"  - App: {app.name} - Type: {app.type}")
            results['applications'] = len(list(apps))
            
        elif sdk_type == "foundry_dev_tools":
            print("  - Application operations not available in foundry-dev-tools")
            results['applications'] = 'not_available_in_dev_tools'
            
        else:
            # Original approach
            apps = client.applications.list_applications()
            for app in apps:
                print(f"  - App: {app.name} - Type: {app.type}")
            results['applications'] = len(list(apps))
            
    except Exception as e:
        print(f"  ❌ Applications audit error: {e}")
        results['applications'] = f'error: {e}'
    
    print("\n✅ AUDIT COMPLETE")
    print(f"\n📋 SUMMARY:")
    for key, value in results.items():
        print(f"  - {key}: {value}")
    
    return results

# Run the audit
if __name__ == "__main__":
    results = audit_foundry_environment()