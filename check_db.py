#!/usr/bin/env python
"""Quick script to verify PostgreSQL database connection and list tables"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection

# Check database connection
with connection.cursor() as cursor:
    # Get list of tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    print("Successfully connected to PostgreSQL database!")
    print(f"Found {len(tables)} tables:\n")
    
    for table in tables:
        # Get row count for each table
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} rows")
