import psycopg2

# Azure PostgreSQL connection parameters
host = "mypostgresdummy.postgres.database.azure.com"
port = 5432
database = "newdb"  # This was the issue - you mentioned db name=newdb
username = "mydbadmin"
password = "decisionminds@123"
ssl_mode = "require"

print("Attempting to connect to PostgreSQL...")
print(f"Host: {host}")
print(f"Username: {username}")
print(f"Database: {database}")
print(f"Port: {port}")
print(f"SSL Mode: {ssl_mode}")

# Try different authentication approaches
approaches = [
    # Approach 1: Standard username (without @hostname)
    {"user": username},
    # Approach 2: Username with @hostname
    {"user": f"{username}@{host.split('.')[0]}"},
]

for i, approach in enumerate(approaches, 1):
    try:
        # Configure connection parameters
        connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'password': password,
            'sslmode': ssl_mode,
            **approach
        }
        
        print(f"\nTrying approach {i}: {approach}")
        
        # Create connection
        connection = psycopg2.connect(**connection_params)
        
        # Get server version
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        
        print(f"✓ Successfully connected to PostgreSQL using approach {i}!")
        print(f"Server version: {version}")
        break
        
    except Exception as e:
        print(f"✗ Approach {i} failed: {e}")
else:
    print("\n✗ All approaches failed to connect to PostgreSQL")