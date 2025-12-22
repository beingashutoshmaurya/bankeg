"""
Migration script to add AI-related columns to the KYC table.
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
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(kyc)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'ai_validation_status' not in columns:
        print("Adding ai_validation_status column...")
        cursor.execute("ALTER TABLE kyc ADD COLUMN ai_validation_status VARCHAR(50)")
        print("✓ Added ai_validation_status column")
    else:
        print("✓ ai_validation_status column already exists")
    
    if 'ai_remarks' not in columns:
        print("Adding ai_remarks column...")
        cursor.execute("ALTER TABLE kyc ADD COLUMN ai_remarks VARCHAR(500)")
        print("✓ Added ai_remarks column")
    else:
        print("✓ ai_remarks column already exists")
    
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

