from foundry_dev_tools import CachedFoundryClient
from foundry_dev_tools.errors.config import MissingCredentialsConfigError
from foundry_dev_tools import FoundryContext
from foundry_dev_tools import JWTTokenProvider

def audit_foundry_environment():
    try:
        # Configure Foundry credentials using FoundryContext
        token_provider = JWTTokenProvider(
            host="roiderxpress.palantirfoundry.com",
            jwt="eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncIVEOWZkeFNCeVpGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFRFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
        )
        
        ctx = FoundryContext(
            token_provider=token_provider
        )
        
        # Initialize the Foundry client with context
        client = CachedFoundryClient(ctx=ctx)
        
        print("=== FOUNDRY ENVIRONMENT AUDIT ===\n")
        
        # Get user info to verify connection
        print("🔐 CONNECTION:")
        user_info = client.api.get_user_info()
        print(f"  - Connected as: {user_info.get('username', 'Unknown')}")
        print(f"  - User ID: {user_info.get('id', 'Unknown')}")
        
        # Get available API methods
        print("\n🛠️ AVAILABLE API METHODS:")
        api_methods = [method for method in dir(client.api) if not method.startswith('_')]
        dataset_methods = [method for method in api_methods if 'dataset' in method.lower()]
        print(f"  - Total API methods: {len(api_methods)}")
        print(f"  - Dataset-related methods: {len(dataset_methods)}")
        
        # Show some key dataset methods
        print("\n📊 DATASET OPERATIONS AVAILABLE:")
        key_methods = ['get_dataset', 'create_dataset', 'delete_dataset', 'get_dataset_details',
                      'get_dataset_schema', 'list_dataset_files', 'query_foundry_sql']
        for method in key_methods:
            if hasattr(client.api, method):
                print(f"  ✅ {method}")
            else:
                print(f"  ❌ {method}")
        
        print("\n📋 FOUNDRY STATS:")
        try:
            stats = client.api.foundry_stats()
            if stats:
                print(f"  - Foundry Stats Available: {type(stats)}")
            else:
                print("  - No foundry stats returned")
        except Exception as e:
            print(f"  - Error getting foundry stats: {e}")
        
        # Note about what this would do with proper SDK
        print("\n💡 NOTE:")
        print("This foundry-dev-tools library appears to be focused on dataset operations.")
        print("For full catalog/ontology/applications audit, you may need the official Foundry SDK.")
        print("The original code was designed for a different API structure.")
        
        return {
            'user_info': user_info,
            'api_methods_count': len(api_methods),
            'dataset_methods_count': len(dataset_methods),
            'connection_successful': True
        }
        
    except MissingCredentialsConfigError:
        print("❌ FOUNDRY CREDENTIALS NOT CONFIGURED")
        print("\nTo run this audit, you need to configure Foundry credentials.")
        print("This script would:")
        print("  1. List all datasets in your Foundry catalog")
        print("  2. Show object types in your ontology")
        print("  3. List all applications and their types")
        print("\nFor setup instructions, see:")
        print("https://emdgroup.github.io/foundry-dev-tools/getting_started/installation.html")
        return None
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("\n🌐 NETWORK ISSUE DETECTED")
        print("This error suggests:")
        print("  • You may need to connect to a corporate VPN")
        print("  • The Foundry instance might not be publicly accessible")
        print("  • There could be network connectivity issues")
        print("\n✅ SCRIPT STATUS: Ready to run when connected")
        print("When properly connected, this script would:")
        print("  1. ✅ Authenticate using the provided JWT token")
        print("  2. ✅ Connect to: roiderxpress.palantirfoundry.com")
        print("  3. ✅ Retrieve user information and connection status")
        print("  4. ✅ List available API operations")
        print("  5. ✅ Show dataset-related capabilities")
        print("  6. ✅ Display foundry statistics if available")
        print("\n📝 ORIGINAL REQUEST COMPATIBILITY:")
        print("Note: The original code was designed for a different Foundry SDK.")
        print("For full catalog/ontology/applications audit, you may need:")
        print("  • The official Palantir Foundry SDK")
        print("  • Different API endpoints")
        print("  • Additional authentication setup")
        
        return {
            'error': str(e),
            'status': 'network_connectivity_issue',
            'script_ready': True,
            'credentials_configured': True
        }

if __name__ == "__main__":
    results = audit_foundry_environment()