import sqlite3
import os
from typing import List, Dict, Any, Optional
from cryptography.fernet import Fernet
import base64
import json

# Database setup
DB_PATH = "strata.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create connections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            db_type TEXT NOT NULL,
            credentials BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create active session table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_session (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            source_id INTEGER,
            target_id INTEGER,
            FOREIGN KEY (source_id) REFERENCES connections (id),
            FOREIGN KEY (target_id) REFERENCES connections (id)
        )
    ''')
    
    # Insert default session row if not exists
    cursor.execute('''
        INSERT OR IGNORE INTO active_session (id, source_id, target_id) VALUES (1, NULL, NULL)
    ''')
    
    conn.commit()
    conn.close()

def get_fernet_key():
    key_file = "fernet.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    return key

def encrypt_credentials(credentials: Dict[str, Any]) -> bytes:
    key = get_fernet_key()
    fernet = Fernet(key)
    credentials_str = json.dumps(credentials)
    return fernet.encrypt(credentials_str.encode())

def decrypt_credentials(encrypted_credentials: bytes) -> Dict[str, Any]:
    key = get_fernet_key()
    fernet = Fernet(key)
    decrypted_str = fernet.decrypt(encrypted_credentials).decode()
    return json.loads(decrypted_str)

def save_connection(name: str, db_type: str, credentials: Dict[str, Any]) -> int:
    encrypted_creds = encrypt_credentials(credentials)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO connections (name, db_type, credentials)
        VALUES (?, ?, ?)
    ''', (name, db_type, encrypted_creds))
    
    conn.commit()
    connection_id = cursor.lastrowid
    conn.close()
    
    return connection_id if connection_id is not None else 0

def update_connection(connection_id: int, name: str, db_type: str, credentials: Dict[str, Any]) -> bool:
    try:
        encrypted_creds = encrypt_credentials(credentials)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE connections 
            SET name = ?, db_type = ?, credentials = ?
            WHERE id = ?
        ''', (name, db_type, encrypted_creds, connection_id))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    except Exception:
        return False

def get_all_connections() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, db_type FROM connections')
    rows = cursor.fetchall()
    
    conn.close()
    
    return [{"id": row[0], "name": row[1], "dbType": row[2]} for row in rows]

def get_connection_by_id(connection_id: int) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, db_type, credentials FROM connections WHERE id = ?', (connection_id,))
    row = cursor.fetchone()
    
    if not row:
        return None
    
    conn.close()
    
    return {
        "id": row[0],
        "name": row[1],
        "dbType": row[2],
        "credentials": decrypt_credentials(row[3])
    }

def delete_connection_by_id(connection_id: int) -> bool:
    """Delete a connection by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
        conn.commit()
        conn.close()
        
        return True
    except Exception:
        return False

def set_source_target(source_id: int, target_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE active_session 
        SET source_id = ?, target_id = ? 
        WHERE id = 1
    ''', (source_id, target_id))
    
    conn.commit()
    conn.close()

def get_active_session() -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.source_id, s.target_id,
               c1.id as source_id, c1.name as source_name, c1.db_type as source_db_type,
               c2.id as target_id, c2.name as target_name, c2.db_type as target_db_type
        FROM active_session s
        LEFT JOIN connections c1 ON s.source_id = c1.id
        LEFT JOIN connections c2 ON s.target_id = c2.id
        WHERE s.id = 1
    ''')
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"source": None, "target": None}
    
    source = {
        "id": row[2],
        "name": row[3],
        "dbType": row[4]
    } if row[2] else None
    
    target = {
        "id": row[5],
        "name": row[6],
        "dbType": row[7]
    } if row[5] else None
    
    return {"source": source, "target": target}

def reset_session():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE active_session 
        SET source_id = NULL, target_id = NULL 
        WHERE id = 1
    ''')
    
    conn.commit()
    conn.close()