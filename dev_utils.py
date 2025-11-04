"""
Development utilities for Strata application
"""
import os
import sys
import subprocess
import time

def setup_environment():
    """Set up the development environment"""
    print("Setting up Strata development environment...")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Activate virtual environment and install dependencies
    print("Installing backend dependencies...")
    if os.name == 'nt':  # Windows
        subprocess.run(["venv\\Scripts\\pip", "install", "-r", "requirements.txt"])
    else:  # Unix/Linux/Mac
        subprocess.run(["venv/bin/pip", "install", "-r", "requirements.txt"])
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    os.chdir("frontend")
    subprocess.run(["npm", "install"])
    os.chdir("..")
    
    print("Development environment setup complete!")

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    if os.name == 'nt':  # Windows
        subprocess.Popen(["venv\\Scripts\\python", "main.py"])
    else:  # Unix/Linux/Mac
        subprocess.Popen(["venv/bin/python", "main.py"])
    print("Backend server started!")

def start_frontend():
    """Start the frontend development server"""
    print("Starting frontend development server...")
    os.chdir("frontend")
    subprocess.Popen(["npm", "run", "dev"])
    os.chdir("..")
    print("Frontend development server started!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python dev_utils.py [setup|start-backend|start-frontend|start-all]")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_environment()
    elif command == "start-backend":
        start_backend()
    elif command == "start-frontend":
        start_frontend()
    elif command == "start-all":
        start_backend()
        time.sleep(3)  # Give backend time to start
        start_frontend()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python dev_utils.py [setup|start-backend|start-frontend|start-all]")

if __name__ == "__main__":
    main()