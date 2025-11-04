"""
Application status checker for Strata
"""
import requests
import psutil
import os

def check_backend_status():
    """Check if the backend is running"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "online":
            return True, "Running"
        else:
            return False, f"Unexpected response: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Not running"
    except Exception as e:
        return False, f"Error: {e}"

def check_frontend_status():
    """Check if the frontend development server is running"""
    # Check for processes running on port 3000
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if the process is using port 3000
            if proc.info['cmdline'] and 'vite' in ' '.join(proc.info['cmdline']):
                return True, "Running"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Try to connect to the frontend
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code in [200, 304]:
            return True, "Running"
        else:
            return False, f"Unexpected response: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Not running"
    except Exception as e:
        return False, f"Error: {e}"

def check_database_status():
    """Check if the database file exists"""
    if os.path.exists("strata.db"):
        return True, "Database file exists"
    else:
        return False, "Database file not found"

def main():
    print("Strata Application Status")
    print("=" * 30)
    
    # Check backend
    backend_running, backend_status = check_backend_status()
    print(f"Backend:     {'✓' if backend_running else '✗'} {backend_status}")
    
    # Check frontend
    frontend_running, frontend_status = check_frontend_status()
    print(f"Frontend:    {'✓' if frontend_running else '✗'} {frontend_status}")
    
    # Check database
    db_exists, db_status = check_database_status()
    print(f"Database:    {'✓' if db_exists else '✗'} {db_status}")
    
    print("\n" + "=" * 30)
    if backend_running and frontend_running and db_exists:
        print("🎉 All systems operational!")
    else:
        print("⚠️  Some components need attention")

if __name__ == "__main__":
    main()