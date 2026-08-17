import sqlite3
import os

db_path = 'app.db'
if not os.path.exists(db_path):
    print("Database file not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_table_info(table_name):
    print(f"\n=== Table: {table_name} ===")
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f" - {col[1]} ({col[2]})")
            
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Total Rows: {count}")
    except Exception as e:
        print(f"Error: {e}")

print_table_info('users')
print_table_info('equipment')
print_table_info('buildings')
print_table_info('floors')
print_table_info('rooms')

conn.close()
