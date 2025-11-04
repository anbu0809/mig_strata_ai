import requests
import time
import json

# Detailed test of data migration with more logging
print("Starting detailed data migration test...")

# Start the data migration
response = requests.post('http://localhost:8000/api/migrate/data')
print(f"Start migration response: {response.status_code}")
print(f"Response: {response.json()}")

# Poll for status with more frequent updates
statuses = []
for i in range(30):  # Check for 30 iterations
    status_response = requests.get('http://localhost:8000/api/migrate/data/status')
    status = status_response.json()
    statuses.append(status)
    print(f"Status {i+1}: {status}")
    
    if status.get('done') or status.get('error'):
        break
    
    time.sleep(1)

print("\nData migration completed!")
final_status = statuses[-1]
if final_status.get('error'):
    print(f"Error: {final_status['error']}")
else:
    print("Data migration Success!")
    print(f"Rows migrated: {final_status.get('rows_migrated', 0)} of {final_status.get('total_rows', 0)}")
    
    # Show all status updates to see the progression
    print("\nFull migration progression:")
    for i, status in enumerate(statuses):
        print(f"  {i+1}. {status['phase']} - {status.get('rows_migrated', 0)}/{status.get('total_rows', 0)} rows")