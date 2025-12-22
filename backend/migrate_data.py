"""
Migration script to copy data from final_project/backend_project/instance/banking.db
to backend/instance/banking.db
"""
import sqlite3
import os
from pathlib import Path

# Database paths
source_db = Path(__file__).parent.parent / 'final_project' / 'backend_project' / 'instance' / 'banking.db'
dest_db = Path(__file__).parent / 'instance' / 'banking.db'

print(f"Source database: {source_db}")
print(f"Destination database: {dest_db}")

if not source_db.exists():
    print(f"Error: Source database not found at {source_db}")
    exit(1)

if not dest_db.exists():
    print(f"Error: Destination database not found at {dest_db}")
    exit(1)

try:
    # Connect to both databases
    source_conn = sqlite3.connect(str(source_db))
    dest_conn = sqlite3.connect(str(dest_db))
    
    source_cursor = source_conn.cursor()
    dest_cursor = dest_conn.cursor()
    
    # Get list of tables from source
    source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in source_cursor.fetchall()]
    
    print(f"\nFound {len(tables)} tables in source database:")
    for table in tables:
        print(f"  - {table}")
    
    # Tables to migrate (in order to respect foreign key constraints)
    # Order matters: migrate parent tables before child tables
    migration_order = [
        'bank_manager',
        'bank_employee', 
        'customers',
        'accounts',
        'kyc',
        'otp_verification',
        'beneficiaries',
        'transactions',
        'bill_payments',
        'virtual_cards',
        'spending_categories',
        'notifications',
        'issue',
        'task'
    ]
    
    # Only migrate tables that exist in source
    tables_to_migrate = [t for t in migration_order if t in tables]
    
    print(f"\nMigrating {len(tables_to_migrate)} tables...")
    
    for table in tables_to_migrate:
        try:
            # Get table structure from source
            source_cursor.execute(f"PRAGMA table_info({table})")
            source_columns = [row[1] for row in source_cursor.fetchall()]
            
            # Get table structure from destination
            dest_cursor.execute(f"PRAGMA table_info({table})")
            dest_columns = [row[1] for row in dest_cursor.fetchall()]
            
            # Find common columns
            common_columns = [col for col in source_columns if col in dest_columns]
            
            if not common_columns:
                print(f"  ⚠ Skipping {table}: No common columns")
                continue
            
            # Check if table has data in destination
            dest_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            existing_count = dest_cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"  ⚠ {table}: {existing_count} rows already exist. Appending new data...")
                # Get max ID from destination to avoid conflicts
                dest_cursor.execute(f"SELECT MAX(id) FROM {table}")
                max_id_result = dest_cursor.fetchone()
                max_id = max_id_result[0] if max_id_result[0] else 0
            else:
                max_id = 0
            
            # Fetch all data from source
            columns_str = ', '.join(common_columns)
            source_cursor.execute(f"SELECT {columns_str} FROM {table}")
            rows = source_cursor.fetchall()
            
            if not rows:
                print(f"  ✓ {table}: No data to migrate")
                continue
            
            # Prepare insert statement
            placeholders = ', '.join(['?' for _ in common_columns])
            insert_sql = f"INSERT OR IGNORE INTO {table} ({columns_str}) VALUES ({placeholders})"
            
            # Adjust IDs if needed to avoid conflicts
            migrated_count = 0
            for row in rows:
                row_dict = dict(zip(common_columns, row))
                
                # If 'id' is in common columns and we have existing data, adjust the ID
                if 'id' in common_columns and existing_count > 0:
                    original_id = row_dict['id']
                    if original_id <= max_id:
                        # Skip rows with IDs that would conflict
                        continue
                
                # Insert row
                values = tuple(row_dict[col] for col in common_columns)
                try:
                    dest_cursor.execute(insert_sql, values)
                    migrated_count += 1
                except sqlite3.IntegrityError as e:
                    # Skip duplicate entries
                    pass
            
            dest_conn.commit()
            print(f"  ✓ {table}: Migrated {migrated_count} rows")
            
        except Exception as e:
            print(f"  ✗ {table}: Error - {e}")
            dest_conn.rollback()
            continue
    
    print("\n✓ Migration completed!")
    
    # Show summary
    print("\nSummary:")
    for table in tables_to_migrate:
        dest_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = dest_cursor.fetchone()[0]
        print(f"  {table}: {count} rows")
    
except sqlite3.Error as e:
    print(f"\n✗ Database error: {e}")
    if 'dest_conn' in locals():
        dest_conn.rollback()
except Exception as e:
    print(f"\n✗ Error: {e}")
finally:
    if 'source_conn' in locals():
        source_conn.close()
    if 'dest_conn' in locals():
        dest_conn.close()
    print("\nDatabase connections closed.")

