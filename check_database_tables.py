import requests
import time
import json

# Check the database tables and row counts
print("Checking database tables and row counts...")

# First, let's get the active session to see what databases are connected
try:
    session_response = requests.get('http://localhost:8000/api/session')
    session = session_response.json()
    print(f"Active session: {session}")
    
    if session.get('source'):
        print(f"Source database: {session['source']['name']} ({session['source']['dbType']})")
    if session.get('target'):
        print(f"Target database: {session['target']['name']} ({session['target']['dbType']})")
        
    # Now let's check the extraction data to see what tables should be migrated
    try:
        with open('artifacts/extraction_bundle.json', 'r') as f:
            extraction_data = json.load(f)
            print("\nExtraction data tables:")
            if 'tables' in extraction_data:
                for table in extraction_data['tables']:
                    print(f"  - {table.get('name', 'Unknown')}")
    except FileNotFoundError:
        print("No extraction bundle found")
    except Exception as e:
        print(f"Error reading extraction bundle: {e}")
        
except Exception as e:
    print(f"Error getting session: {e}")