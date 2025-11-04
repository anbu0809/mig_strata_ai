import requests
import time
import json

# Test the structure migration endpoint
print("Testing structure migration...")

# Start the structure migration
response = requests.post('http://localhost:8000/api/migrate/structure')
print(f"Start migration response: {response.status_code}")
print(f"Response: {response.json()}")

# Poll for status
while True:
    status_response = requests.get('http://localhost:8000/api/migrate/structure/status')
    status = status_response.json()
    print(f"Status: {status}")
    
    if status.get('done') or status.get('error'):
        break
    
    time.sleep(2)

print("Migration completed!")
if status.get('error'):
    print(f"Error: {status['error']}")
else:
    print("Success!")
    
    # Get the AI-generated queries
    queries_response = requests.get('http://localhost:8000/api/migrate/structure/queries')
    queries = queries_response.json()
    print(f"AI Queries: {queries}")