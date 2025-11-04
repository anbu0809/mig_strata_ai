"""
Simple test script to verify the backend is working
"""
import requests
import time

def test_backend():
    # Test if the backend is running
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("Backend is running successfully!")
            print("Response:", response.json())
            return True
        else:
            print(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Backend is not running. Please start the backend server.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    print("Testing Strata backend...")
    success = test_backend()
    if success:
        print("All tests passed!")
    else:
        print("Tests failed!")