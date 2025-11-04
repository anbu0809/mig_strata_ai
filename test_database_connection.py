import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_active_session, get_connection_by_id
from backend.routes.migrate import connect_to_database

def test_database_connection():
    print("Testing database connection...")
    
    try:
        # Get session info
        session = get_active_session()
        print(f"Active session: {session}")
        
        source_db = session.get("source")
        target_db = session.get("target")
        
        if not source_db or not target_db:
            print("Source or target database not selected")
            return
            
        print(f"Source database: {source_db}")
        print(f"Target database: {target_db}")
        
        # Get full connection details
        source_connection_info = get_connection_by_id(source_db["id"])
        target_connection_info = get_connection_by_id(target_db["id"])
        
        print(f"Source connection info: {source_connection_info}")
        print(f"Target connection info: {target_connection_info}")
        
        # Try to connect to databases
        source_connection = connect_to_database(source_connection_info)
        target_connection = connect_to_database(target_connection_info)
        
        print("Successfully connected to both databases")
        
        # Try to query tables
        source_cursor = source_connection.cursor()
        target_cursor = target_connection.cursor()
        
        # List tables in source database
        source_cursor.execute("SHOW TABLES")
        tables = source_cursor.fetchall()
        print(f"Source database tables: {tables}")
        
        # Check row counts for each table
        for table_row in tables:
            if table_row and len(table_row) > 0:
                table_name = table_row[0]
                source_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                result = source_cursor.fetchone()
                if result and len(result) > 0:
                    count = result[0]
                    print(f"Table {table_name}: {count} rows")
            
        source_cursor.close()
        target_cursor.close()
        source_connection.close()
        target_connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()