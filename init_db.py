"""
Script to initialize the Strata database
"""
from backend.database import init_db

if __name__ == "__main__":
    print("Initializing Strata database...")
    init_db()
    print("Database initialized successfully!")