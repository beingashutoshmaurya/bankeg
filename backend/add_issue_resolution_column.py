"""
Migration script to add resolution_summary column to the issue table.
Run this once to update the database schema.
"""
import sqlite3
import os

# Path to the database
db_path = os.path.join('instance', 'banking.db')

# If instance folder doesn't exist, try root
if not os.path.exists(db_path):
    db_path = 'banking.db'

if not os.path.exists(db_path):
    print(f"Error: Database file not found at {db_path}")
    exit(1)

print(f"Connecting to database: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(issue)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'resolution_summary' not in columns:
        print("Adding resolution_summary column...")
        cursor.execute("ALTER TABLE issue ADD COLUMN resolution_summary VARCHAR(500)")
        print("✓ Added resolution_summary column")
    else:
        print("✓ resolution_summary column already exists")
    
    conn.commit()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    conn.rollback()
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
        print("Database connection closed.")

