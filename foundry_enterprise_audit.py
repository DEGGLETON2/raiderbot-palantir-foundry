"""
Foundry Environment Audit - Enterprise Edition
This script is designed to work with official Palantir Foundry SDK packages.

NOTE: The packages 'palantir-foundry-sdk' and 'palantir-foundry-transforms' 
are enterprise packages that are only available:
1. Inside Palantir Foundry environments (pre-installed)
2. With enterprise authentication/private repositories
3. They are NOT available on public PyPI

To use this script:
- Run it inside a Palantir Foundry Code Repository
- Or ensure you have access to Palantir's private package repository
"""

def audit_foundry_environment():
    """Complete Foundry environment audit using enterprise SDK"""
    
    print("=== FOUNDRY ENVIRONMENT AUDIT - ENTERPRISE EDITION ===\n")
    
    # Check if we have the enterprise packages
    enterprise_sdk_available = False
    
    try:
        # Try to import the enterprise SDK
        from palantir_foundry_sdk import FoundryRestClient
        from palantir_foundry_sdk.datasets import Dataset
        from palantir_foundry_sdk.ontology import OntologyClient
        from palantir_foundry_sdk.catalog import CatalogClient
        from palantir_foundry_sdk.applications import ApplicationsClient
        
        print("✅ Enterprise Palantir Foundry SDK detected")
        enterprise_sdk_available = True
        
    except ImportError as e:
        print(f"❌ Enterprise SDK not available: {e}")
        print("\n💡 This is expected if you're running outside of Foundry")
        print("   The enterprise packages are only available inside Foundry environments")
        
    if not enterprise_sdk_available:
        print("\n🔄 Falling back to foundry-dev-tools...")
        
        try:
            from foundry_dev_tools import CachedFoundryClient, FoundryContext, JWTTokenProvider
            
            # Your RaiderExpress credentials
            token_provider = JWTTokenProvider(
                host="roiderxpress.palantirfoundry.com",
                jwt="eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncIVEOWZkeFNCeVpGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFRFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
            )
            
            ctx = FoundryContext(token_provider=token_provider)
            client = CachedFoundryClient(ctx=ctx)
            
            print("✅ Using foundry-dev-tools as fallback")
            print("⚠️  Limited functionality - datasets only, no ontology/applications")
            
            # Show what's available
            print(f"\n📊 Available dataset methods:")
            dataset_methods = [m for m in dir(client.api) if 'dataset' in m.lower()]
            for method in dataset_methods[:10]:
                print(f"  - {method}")
            
            return {
                'sdk_type': 'foundry_dev_tools_fallback',
                'enterprise_sdk_available': False,
                'dataset_methods': len(dataset_methods)
            }
            
        except Exception as e:
            print(f"❌ Fallback also failed: {e}")
            return {'error': 'no_sdk_available'}
    
    # If we get here, we have the enterprise SDK
    print(f"\n🚀 Proceeding with full enterprise audit...\n")
    
    # Initialize enterprise clients
    foundry_url = "roiderxpress.palantirfoundry.com"
    auth_token = "eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncIVEOWZkeFNCeVpGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFRFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
    
    try:
        # Initialize the enterprise client
        client = FoundryRestClient(
            hostname=foundry_url,
            auth_token=auth_token
        )
        
        # Initialize service clients
        catalog = CatalogClient(client)
        ontology = OntologyClient(client)
        applications = ApplicationsClient(client)
        
        print("✅ Enterprise clients initialized successfully")
        
    except Exception as e:
        print(f"❌ Enterprise client initialization failed: {e}")
        return {'error': f'client_init_failed: {e}'}
    
    results = {
        'datasets': [],
        'ontology': {},
        'applications': [],
        'sdk_type': 'enterprise'
    }
    
    # Dataset audit
    try:
        print("\n📊 DATASETS:")
        datasets = catalog.list_datasets()
        for dataset in datasets:
            dataset_info = {
                'name': dataset.name,
                'rid': dataset.rid
            }
            results['datasets'].append(dataset_info)
            print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
        
        print(f"\nTotal datasets: {len(results['datasets'])}")
        
    except Exception as e:
        print(f"❌ Dataset audit failed: {e}")
        results['datasets'] = f'error: {e}'
    
    # Ontology audit  
    try:
        print("\n🏗️ ONTOLOGY:")
        ontology_data = ontology.get_ontology()
        object_types = list(ontology_data.object_types.keys())
        
        results['ontology'] = {
            'object_types': object_types,
            'count': len(object_types)
        }
        
        print(f"  - Object Types ({len(object_types)}):")
        for obj_type in object_types[:10]:
            print(f"    • {obj_type}")
        
        if len(object_types) > 10:
            print(f"    ... and {len(object_types) - 10} more")
            
    except Exception as e:
        print(f"❌ Ontology audit failed: {e}")
        results['ontology'] = f'error: {e}'
    
    # Applications audit
    try:
        print("\n📱 APPLICATIONS:")
        apps = applications.list_applications()
        for app in apps:
            app_info = {
                'name': app.name,
                'type': app.type
            }
            results['applications'].append(app_info)
            print(f"  - App: {app.name} - Type: {app.type}")
        
        print(f"\nTotal applications: {len(results['applications'])}")
        
    except Exception as e:
        print(f"❌ Applications audit failed: {e}")
        results['applications'] = f'error: {e}'
    
    print("\n✅ ENTERPRISE AUDIT COMPLETE")
    print(f"\n📋 SUMMARY:")
    print(f"  - Datasets: {len(results['datasets']) if isinstance(results['datasets'], list) else results['datasets']}")
    print(f"  - Ontology Objects: {results['ontology'].get('count', 'error') if isinstance(results['ontology'], dict) else results['ontology']}")
    print(f"  - Applications: {len(results['applications']) if isinstance(results['applications'], list) else results['applications']}")
    
    return results

# Execute the audit
if __name__ == "__main__":
    results = audit_foundry_environment()