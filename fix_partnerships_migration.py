#!/usr/bin/env python
"""Fix partnerships migration by handling ID field conversion"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection

print("Fixing partnerships table ID field...")

with connection.cursor() as cursor:
    # Check if partnerships_partnership table exists and its current ID type
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'partnerships_partnership'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        # Check current ID column type
        cursor.execute("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'partnerships_partnership' 
            AND column_name = 'id';
        """)
        result = cursor.fetchone()
        if result:
            current_type = result[0]
            print(f"Current ID type: {current_type}")
            
            if current_type == 'bigint':
                print("Table exists with bigint ID. Dropping table to recreate with UUID...")
                # Drop foreign key constraints first
                cursor.execute("""
                    SELECT conname, conrelid::regclass 
                    FROM pg_constraint 
                    WHERE confrelid = 'partnerships_partnership'::regclass;
                """)
                constraints = cursor.fetchall()
                
                # Drop the table (cascade will handle foreign keys)
                cursor.execute("DROP TABLE IF EXISTS partnerships_partnership CASCADE;")
                print("Dropped partnerships_partnership table.")
            else:
                print(f"ID type is already {current_type}, no change needed.")
    else:
        print("partnerships_partnership table does not exist.")

print("\nApplying remaining migrations...")
from django.core.management import call_command
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("\nAll migrations applied successfully!")
except Exception as e:
    print(f"Error: {e}")
