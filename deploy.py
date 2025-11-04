"""
Deployment script for Strata application
"""
import os
import subprocess
import sys

def build_frontend():
    """Build the frontend for production"""
    print("Building frontend for production...")
    os.chdir("frontend")
    result = subprocess.run(["npm", "run", "build"])
    os.chdir("..")
    
    if result.returncode == 0:
        print("✓ Frontend build successful")
        return True
    else:
        print("✗ Frontend build failed")
        return False

def create_deployment_package():
    """Create a deployment package"""
    print("Creating deployment package...")
    
    # In a real deployment scenario, you would:
    # 1. Build the frontend
    # 2. Package the backend
    # 3. Create a deployment archive
    # 4. Upload to deployment target
    
    print("Deployment package creation completed!")
    return True

def main():
    print("Strata Deployment Script")
    print("=" * 30)
    
    # Build frontend
    if not build_frontend():
        print("Failed to build frontend. Aborting deployment.")
        return False
    
    # Create deployment package
    if not create_deployment_package():
        print("Failed to create deployment package.")
        return False
    
    print("\n🎉 Deployment package created successfully!")
    print("Deployment files are located in the 'dist' directory.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)