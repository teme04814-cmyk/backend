#!/usr/bin/env python
"""Create tables from SQL file"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection

sql_file = 'create_partnerships_tables.sql'

print(f"Reading SQL from {sql_file}...")
with open(sql_file, 'r') as f:
    sql = f.read()

print("Executing SQL...")
with connection.cursor() as cursor:
    # Split by semicolons and execute each statement
    statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
    
    for i, statement in enumerate(statements, 1):
        try:
            cursor.execute(statement)
            print(f"  ✓ Executed statement {i}")
        except Exception as e:
            # Ignore "already exists" errors
            if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                print(f"  - Statement {i} skipped (already exists)")
            else:
                print(f"  ✗ Error in statement {i}: {e}")

connection.commit()
print("\nTables created successfully!")

# Verify tables
print("\nVerifying tables...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'partnerships_%'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    print(f"Found {len(tables)} partnerships tables:")
    for table in tables:
        print(f"  - {table[0]}")
