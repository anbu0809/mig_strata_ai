#!/usr/bin/env python3
"""
Deployment script for Strata Backend Engine
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlite3
        from cryptography.fernet import Fernet
        print("✓ All required dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def initialize_database():
    """Initialize the database if it doesn't exist"""
    if os.path.exists("strata.db"):
        print("✓ Database already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "init_db.py"], check=True)
        print("✓ Database initialized successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to initialize database")
        return False

def install_requirements():
    """Install requirements from requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("⚠ No requirements.txt found")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False

def start_server(host="0.0.0.0", port=8000):
    """Start the FastAPI server"""
    try:
        print(f"Starting server on {host}:{port}")
        subprocess.run([sys.executable, "-m", "uvicorn", "backend.main:app", 
                       "--host", host, "--port", str(port), "--reload"], check=True)
    except subprocess.CalledProcessError:
        print("✗ Failed to start server")
        return False
    return True

def main():
    """Main deployment function"""
    print("🚀 Strata Backend Engine Deployment")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("requirements.txt"):
        print("✗ Please run this script from the strata-backend-engine directory")
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("Installing requirements...")
        if not install_requirements():
            return False
    
    # Initialize database
    if not initialize_database():
        return False
    
    # Start server
    print("\n🚀 Starting Strata Backend Engine...")
    print("The API will be available at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    return start_server()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)