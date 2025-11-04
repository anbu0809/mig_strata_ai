"""
End-to-end test script for Strata application
"""
import requests
import time
import json

def test_end_to_end():
    base_url = "http://localhost:8000"
    
    print("Starting Strata end-to-end test...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "online"
        print("✓ Health check passed")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test 2: Test connection endpoint
    print("\n2. Testing connection endpoints...")
    try:
        # Test listing connections (should return empty list)
        response = requests.get(f"{base_url}/api/connections")
        assert response.status_code == 200
        print("✓ Connection listing passed")
    except Exception as e:
        print(f"✗ Connection endpoints test failed: {e}")
        return False
    
    # Test 3: Test session endpoints
    print("\n3. Testing session endpoints...")
    try:
        # Test getting session (should return empty session)
        response = requests.get(f"{base_url}/api/session")
        assert response.status_code == 200
        print("✓ Session retrieval passed")
    except Exception as e:
        print(f"✗ Session endpoints test failed: {e}")
        return False
    
    print("\nAll end-to-end tests passed!")
    return True

if __name__ == "__main__":
    success = test_end_to_end()
    if success:
        print("\n🎉 Strata application is working correctly!")
    else:
        print("\n❌ Strata application has issues!")