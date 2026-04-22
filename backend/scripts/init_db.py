from app.config import configs 

import psycopg2
import os
from pathlib import Path

from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
# Update these with your Supabase Connection String 
# Found in: Project Settings > Database > Connection string > URI
DB_URI = configs.DIRECT_URL.get_secret_value()

def run_sql_initialization():
    # Path to your SQL files
    sql_dir = Path(__file__).parent.parent / "app" / "db"
    
    # Get all .sql files and sort them (01_..., 02_...)
    sql_files = sorted([f for f in os.listdir(sql_dir) if f.endswith('.sql')])

    # Initialize variables with type hints
    conn: Connection | None = None
    cur: Cursor | None = None
    try:
        print(f"Connecting to Supabase...")
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()

        for filename in sql_files:
            file_path = sql_dir / filename
            print(f"Executing {filename}...")
            
            with open(file_path, 'r') as f:
                sql_content = f.read()
                if sql_content.strip():
                    cur.execute(sql_content)
        
        conn.commit()
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error during initialization: {e}")
        if 'conn' in locals():
            if conn is not None:
                conn.rollback()
    finally:
        if cur is not None: 
            cur.close()
        if conn is not None: 
            conn.close()

if __name__ == "__main__":
    run_sql_initialization()