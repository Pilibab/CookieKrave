from app.config import configs 

import psycopg2
# import os
from pathlib import Path

from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

def run_sql_initialization():
    DB_URI = configs.DIRECT_URL.get_secret_value()
    sql_dir = Path(__file__).parent

    # Join it with your filename
    sql_file = sql_dir / "sample_data.sql"

    # Initialize variables with type hints
    conn: Connection | None = None
    cur: Cursor | None = None

    try:
        print(f"Connecting to Supabase...")
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()

        with open(sql_file, 'r') as f:
            sql_content = f.read()
            if sql_content.strip():
                try:
                    # This sends the whole block to the DB
                    cur.execute(sql_content) 
                    # CRITICAL: If you don't commit, the inserts won't save!
                    conn.commit() 
                    print(f"Successfully executed {sql_file}")
                except Exception as e:
                    conn.rollback() # Undo everything if one insert fails
                    print(f"Error seeding database: {e}") 
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