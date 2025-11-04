import requests
import time
import json

# Test the data migration endpoint
print("Testing data migration...")

# Start the data migration
response = requests.post('http://localhost:8000/api/migrate/data')
print(f"Start migration response: {response.status_code}")
print(f"Response: {response.json()}")

# Poll for status
while True:
    status_response = requests.get('http://localhost:8000/api/migrate/data/status')
    status = status_response.json()
    print(f"Status: {status}")
    
    if status.get('done') or status.get('error'):
        break
    
    time.sleep(2)

print("Data migration completed!")
if status.get('error'):
    print(f"Error: {status['error']}")
else:
    print("Data migration Success!")
    print(f"Rows migrated: {status.get('rows_migrated', 0)} of {status.get('total_rows', 0)}")