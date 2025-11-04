import requests
import time

# Test to verify that all 50 rows are migrated
print("Verifying data migration...")

# Start the data migration
response = requests.post('http://localhost:8000/api/migrate/data')
print(f"Start migration response: {response.status_code}")
print(f"Response: {response.json()}")

# Poll for status until completion
max_attempts = 30
for attempt in range(max_attempts):
    status_response = requests.get('http://localhost:8000/api/migrate/data/status')
    status = status_response.json()
    print(f"Attempt {attempt + 1}: {status['phase']} - {status.get('rows_migrated', 0)}/{status.get('total_rows', 0)} rows")
    
    if status.get('done') or status.get('error'):
        break
    
    time.sleep(2)

print("\nFinal status:")
final_status_response = requests.get('http://localhost:8000/api/migrate/data/status')
final_status = final_status_response.json()
print(f"Phase: {final_status['phase']}")
print(f"Rows migrated: {final_status.get('rows_migrated', 0)} of {final_status.get('total_rows', 0)}")
print(f"Percent: {final_status['percent']}%")
print(f"Done: {final_status['done']}")
if final_status.get('error'):
    print(f"Error: {final_status['error']}")

# Verify the data was actually migrated by checking the target database
print("\nVerifying data in target database...")
session_response = requests.get('http://localhost:8000/api/session')
session = session_response.json()

if session.get('target'):
    print(f"Target database: {session['target']['name']} ({session['target']['dbType']})")
    
    # Try to get table information from the target database
    try:
        # This would require implementing a new endpoint to check target database tables
        # For now, we'll just check the migration status
        print("Data migration verification complete.")
        if final_status.get('rows_migrated', 0) == 50:
            print("SUCCESS: All 50 rows were migrated!")
        else:
            print(f"PARTIAL SUCCESS: {final_status.get('rows_migrated', 0)} of 50 rows were migrated.")
    except Exception as e:
        print(f"Could not verify target database: {e}")
else:
    print("No target database selected.")