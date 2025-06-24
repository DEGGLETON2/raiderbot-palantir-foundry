# Foundry Environment Audit - Debug Version
# Copy this exactly into Foundry and run it

def audit_foundry_environment():
    print("=== FOUNDRY ENVIRONMENT AUDIT - DEBUG MODE ===\n")
    
    # First, let's see what's available in the global scope
    print("🔍 CHECKING GLOBAL ENVIRONMENT:")
    
    # Check if 'client' exists
    try:
        print(f"  - 'client' variable exists: {type(client)}")
        print(f"  - client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
        client_available = True
    except NameError:
        print("  - 'client' variable NOT found in global scope")
        client_available = False
    
    # Check what's available in globals()
    print(f"\n📋 GLOBAL VARIABLES:")
    foundry_related = []
    for name, obj in globals().items():
        if not name.startswith('_'):
            if any(keyword in name.lower() for keyword in ['foundry', 'client', 'catalog', 'ontology', 'dataset']):
                foundry_related.append(f"  - {name}: {type(obj)}")
    
    if foundry_related:
        print("Foundry-related globals found:")
        for item in foundry_related:
            print(item)
    else:
        print("  - No obvious Foundry-related variables found")
    
    # Check available imports
    print(f"\n📦 CHECKING COMMON FOUNDRY IMPORTS:")
    common_imports = [
        'foundry',
        'foundry_platform_sdk', 
        'palantir',
        'foundry_client',
        'transforms',
        'datasets'
    ]
    
    for imp in common_imports:
        try:
            exec(f"import {imp}")
            print(f"  ✅ {imp} - available")
        except ImportError:
            print(f"  ❌ {imp} - not available")
    
    if not client_available:
        print("\n❌ Cannot proceed with audit - 'client' not available")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure you're running this in a Foundry Code Repository")
        print("2. Check if you need to initialize a client first")
        print("3. Verify you have the right permissions")
        print("4. Try running in a Foundry notebook instead")
        return {'error': 'client_not_available'}
    
    # If client is available, proceed with original audit
    print("\n✅ CLIENT FOUND - PROCEEDING WITH AUDIT")
    print("\n" + "="*50)
    
    try:
        # Dataset audit (original code)
        print("\n📊 DATASETS:")
        datasets = client.catalog.list_datasets()
        for dataset in datasets:
            print(f"  - Dataset: {dataset.name} - RID: {dataset.rid}")
    except Exception as e:
        print(f"  ❌ Dataset audit failed: {e}")
    
    try:
        # Ontology audit (original code)
        print("\n🏗️ ONTOLOGY:")
        ontology = client.ontology.get_ontology()
        print(f"  - Object Types: {list(ontology.object_types.keys())}")
    except Exception as e:
        print(f"  ❌ Ontology audit failed: {e}")
    
    try:
        # Applications audit (original code)
        print("\n📱 APPLICATIONS:")
        apps = client.applications.list_applications()
        for app in apps:
            print(f"  - App: {app.name} - Type: {app.type}")
    except Exception as e:
        print(f"  ❌ Applications audit failed: {e}")
    
    print("\n✅ AUDIT COMPLETE")
    
    return {
        'client_available': client_available,
        'audit_attempted': True
    }

# Run the audit
results = audit_foundry_environment()