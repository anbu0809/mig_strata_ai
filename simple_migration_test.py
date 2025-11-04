import requests
import time

# Simple test to trigger data migration and see what happens
print("Testing data migration...")

# First, check the current session
session_response = requests.get('http://localhost:8000/api/session')
print(f"Current session: {session_response.json()}")

# Check if we have source and target databases
session = session_response.json()
if not session.get('source') or not session.get('target'):
    print("ERROR: Source or target database not selected")
    exit(1)

# Start the data migration
response = requests.post('http://localhost:8000/api/migrate/data')
print(f"Start migration response: {response.status_code}")
print(f"Response: {response.json()}")

# Wait a bit and check status
time.sleep(5)

status_response = requests.get('http://localhost:8000/api/migrate/data/status')
status = status_response.json()
print(f"Status after 5 seconds: {status}")

# Wait a bit more and check status again
time.sleep(5)

status_response = requests.get('http://localhost:8000/api/migrate/data/status')
status = status_response.json()
print(f"Status after 10 seconds: {status}")