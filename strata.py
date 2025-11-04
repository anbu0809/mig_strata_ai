#!/usr/bin/env python3
"""
Strata CLI - Command Line Interface for Strata Application
"""
import argparse
import sys
import os
import subprocess

def setup_command(args):
    """Setup the Strata application"""
    print("Setting up Strata application...")
    # Import and run setup
    from dev_utils import setup_environment
    setup_environment()

def start_command(args):
    """Start the Strata application"""
    print("Starting Strata application...")
    # Import and run start
    from dev_utils import start_backend, start_frontend
    import time
    
    if args.component == "all":
        start_backend()
        time.sleep(3)  # Give backend time to start
        start_frontend()
    elif args.component == "backend":
        start_backend()
    elif args.component == "frontend":
        start_frontend()

def status_command(args):
    """Check the status of the Strata application"""
    print("Checking Strata application status...")
    # Import and run status check
    from status import main
    main()

def test_command(args):
    """Run tests for the Strata application"""
    print("Running Strata tests...")
    if args.type == "all" or args.type == "e2e":
        # Run end-to-end tests
        from e2e_test import test_end_to_end
        success = test_end_to_end()
        if not success:
            sys.exit(1)
    
    if args.type == "all" or args.type == "backend":
        # Run backend tests (placeholder)
        print("Running backend tests...")
        # In a real application, you would run actual backend tests here
    
    if args.type == "all" or args.type == "frontend":
        # Run frontend tests (placeholder)
        print("Running frontend tests...")
        # In a real application, you would run actual frontend tests here

def deploy_command(args):
    """Deploy the Strata application"""
    print("Deploying Strata application...")
    # Import and run deployment
    from deploy import main
    success = main()
    if not success:
        sys.exit(1)

def reset_command(args):
    """Reset the Strata application"""
    print("Resetting Strata application...")
    
    # Remove database file
    if os.path.exists("strata.db"):
        os.remove("strata.db")
        print("✓ Database file removed")
    
    # Remove artifacts directory
    if os.path.exists("artifacts"):
        import shutil
        shutil.rmtree("artifacts")
        print("✓ Artifacts directory removed")
    
    # Remove encryption key
    if os.path.exists("fernet.key"):
        os.remove("fernet.key")
        print("✓ Encryption key removed")
    
    print("Strata application reset successfully!")

def main():
    parser = argparse.ArgumentParser(description="Strata - Enterprise AI Translation Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup the Strata application")
    setup_parser.set_defaults(func=setup_command)
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the Strata application")
    start_parser.add_argument("component", choices=["all", "backend", "frontend"], 
                             default="all", help="Component to start")
    start_parser.set_defaults(func=start_command)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check the status of the Strata application")
    status_parser.set_defaults(func=status_command)
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests for the Strata application")
    test_parser.add_argument("type", choices=["all", "e2e", "backend", "frontend"], 
                            default="all", help="Type of tests to run")
    test_parser.set_defaults(func=test_command)
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy the Strata application")
    deploy_parser.set_defaults(func=deploy_command)
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset the Strata application")
    reset_parser.set_defaults(func=reset_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute the command
    args.func(args)

if __name__ == "__main__":
    main()