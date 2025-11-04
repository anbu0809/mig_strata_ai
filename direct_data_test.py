import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_active_session, get_connection_by_id
from backend.routes.migrate import connect_to_database

def test_data_migration():
    print("Testing data migration directly...")
    
    try:
        # Get session info
        session = get_active_session()
        source_db = session.get("source")
        target_db = session.get("target")
        print(f"Session: source={source_db}, target={target_db}")
        
        if not source_db or not target_db:
            print("ERROR: Source or target database not selected")
            return
        
        # Get full connection details
        source_connection_info = get_connection_by_id(source_db["id"])
        target_connection_info = get_connection_by_id(target_db["id"])
        print(f"Source connection info: {source_connection_info}")
        print(f"Target connection info: {target_connection_info}")
        
        # Connect to databases
        print("Connecting to databases...")
        source_connection = connect_to_database(source_connection_info)
        target_connection = connect_to_database(target_connection_info)
        source_cursor = source_connection.cursor()
        target_cursor = target_connection.cursor()
        print("Successfully connected to databases")
        
        # Drop existing tables to avoid conflicts
        print("Dropping existing tables...")
        tables_to_drop = ["order_items", "orders", "products", "employees", "customers"]  # Reverse order for foreign key constraints
        for table in tables_to_drop:
            try:
                target_cursor.execute(f"DROP TABLE IF EXISTS \"{table}\" CASCADE")
                print(f"Dropped table {table}")
            except Exception as e:
                print(f"Warning: Could not drop table {table}: {e}")
        target_connection.commit()
        print("Existing tables dropped")
        
        # Hardcoded table list for known database structure
        tables_to_migrate = ["customers", "employees", "orders", "order_items", "products"]
        print(f"Tables to migrate: {tables_to_migrate}")
        
        # Migrate data
        rows_migrated = 0
        for i, table in enumerate(tables_to_migrate):
            print(f"Starting migration of table {table} ({i+1}/{len(tables_to_migrate)})")
            # Get row count for this table
            source_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            result = source_cursor.fetchone()
            table_row_count = result[0] if result else 0
            print(f"Table {table} has {table_row_count} rows")
            
            # Copy data from source to target
            source_cursor.execute(f"SELECT * FROM {table}")
            rows = source_cursor.fetchall()
            print(f"Fetched {len(rows)} rows from {table}")
            
            if rows:
                # Get column names
                column_names = [desc[0] for desc in source_cursor.description]
                placeholders = ", ".join(["%s"] * len(column_names))
                columns = ", ".join([f"\"{name}\"" for name in column_names])
                
                # Insert data into target table
                insert_query = f"INSERT INTO \"{table}\" ({columns}) VALUES ({placeholders})"
                print(f"Executing insert query for {len(rows)} rows")
                target_cursor.executemany(insert_query, rows)
                target_connection.commit()
                print(f"Committed {len(rows)} rows to {table}")
            
            rows_migrated += table_row_count
            print(f"Migrated {table_row_count} rows from {table}, total: {rows_migrated}")
        
        print(f"Data migration completed. Total rows migrated: {rows_migrated}")
        
        # Close connections
        source_connection.close()
        target_connection.close()
        print("Connections closed")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_migration()