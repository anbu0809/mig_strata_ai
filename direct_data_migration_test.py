import sys
import os
import asyncio
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.routes.migrate import run_data_migration_task

async def test_data_migration():
    print("Running data migration directly...")
    try:
        await run_data_migration_task()
        print("Data migration completed")
    except Exception as e:
        print(f"Error in data migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_data_migration())