from palantir_foundry_sdk import FoundryRestClient
from palantir_foundry_sdk.datasets import Dataset
from palantir_foundry_sdk.ontology import OntologyClient
from palantir_foundry_sdk.catalog import CatalogClient
from palantir_foundry_sdk.applications import ApplicationsClient

class RaiderExpressFoundryAudit:
    def __init__(self, foundry_url: str, auth_token: str):
        """Initialize Foundry client with RaiderExpress credentials"""
        self.client = FoundryRestClient(
            hostname=foundry_url.replace('https://', ''),  # Remove protocol if present
            auth_token=auth_token
        )
        
        # Initialize service clients
        self.catalog = CatalogClient(self.client)
        self.ontology = OntologyClient(self.client) 
        self.applications = ApplicationsClient(self.client)
    
    def audit_foundry_environment(self):
        """Complete Foundry environment audit"""
        print("=== RAIDER EXPRESS FOUNDRY ENVIRONMENT AUDIT ===\n")
        
        results = {
            'datasets': [],
            'ontology': {},
            'applications': []
        }
        
        # Dataset audit
        try:
            print("📊 DATASETS:")
            datasets = self.catalog.list_datasets()
            for dataset in datasets:
                dataset_info = {
                    'name': dataset.name,
                    'rid': dataset.rid,
                    'path': getattr(dataset, 'path', 'N/A')
                }
                results['datasets'].append(dataset_info)
                print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
            
            print(f"\nTotal datasets found: {len(results['datasets'])}")
            
        except Exception as e:
            print(f"  ❌ Error listing datasets: {e}")
        
        # Ontology audit  
        try:
            print("\n🏗️ ONTOLOGY:")
            ontology = self.ontology.get_ontology()
            object_types = list(ontology.object_types.keys())
            results['ontology'] = {
                'object_types': object_types,
                'total_count': len(object_types)
            }
            
            print(f"  - Total Object Types: {len(object_types)}")
            
            # Show first 10 object types
            for obj_type in object_types[:10]:
                print(f"  - {obj_type}")
            
            if len(object_types) > 10:
                print(f"  ... and {len(object_types) - 10} more object types")
                
        except Exception as e:
            print(f"  ❌ Error accessing ontology: {e}")
        
        # Applications audit
        try:
            print("\n📱 APPLICATIONS:")
            apps = self.applications.list_applications()
            for app in apps:
                app_info = {
                    'name': app.name,
                    'type': app.type,
                    'rid': getattr(app, 'rid', 'N/A')
                }
                results['applications'].append(app_info)
                print(f"  - App: {app.name} - Type: {app.type}")
            
            print(f"\nTotal applications found: {len(results['applications'])}")
            
        except Exception as e:
            print(f"  ❌ Error listing applications: {e}")
        
        # Additional environment info
        try:
            print("\n🔍 ENVIRONMENT INFO:")
            print(f"  - Foundry URL: {self.client.hostname}")
            print(f"  - Client authenticated: {'✅' if self.client.auth_token else '❌'}")
            print(f"  - SDK Version: {getattr(self.client, 'version', 'Unknown')}")
            
        except Exception as e:
            print(f"  ❌ Error getting environment info: {e}")
        
        print("\n✅ AUDIT COMPLETE")
        return results

def audit_foundry_environment():
    """Main audit function - matches your original code signature"""
    
    # RaiderExpress Foundry credentials
    foundry_url = "https://roiderxpress.palantirfoundry.com"
    auth_token = "eyJwbG50IjlmImoalR4SFVGTWdPUExtWEpyUThwWVE9PSIsImF5Zy16IjkVTMjUzInQ.eyJzdWIiOjJRQ0tFcGQp2dJVMkMONHI0c2NqODhnPT0iLCJqdGkiOjUncIVEOWZkeFNCeVpGYTA5MERzL2QlBPT0lBCJvcmciOiJOZklkZlVOTFRFT3RSM1ZaQXNQQXFBPT0ifQ.HlVOHCUs_jM5TRl3awa3TvtfVrv73GoY8WYPrudTl7SqYiLe4TxjlSnWLRr"
    
    # Initialize and run audit
    audit_client = RaiderExpressFoundryAudit(foundry_url, auth_token)
    return audit_client.audit_foundry_environment()

# Execute the audit (matches your original pattern)
if __name__ == "__main__":
    results = audit_foundry_environment()
else:
    # For interactive use
    results = audit_foundry_environment()