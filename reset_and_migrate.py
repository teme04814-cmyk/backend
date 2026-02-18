#!/usr/bin/env python
"""Reset migration state and apply migrations"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

print("Step 1: Checking database state...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'django_migrations'
        );
    """)
    migrations_exists = cursor.fetchone()[0]
    
    if migrations_exists:
        print("django_migrations table exists. Dropping it to reset state...")
        cursor.execute("DROP TABLE IF EXISTS django_migrations CASCADE;")
        print("Dropped django_migrations table.")
    else:
        print("django_migrations table does not exist.")

print("\nStep 2: Applying all migrations...")
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("\nMigrations applied successfully!")
except Exception as e:
    print(f"Error applying migrations: {e}")

print("\nStep 3: Verifying tables...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    print(f"Found {len(tables)} tables:")
    for table in tables[:10]:  # Show first 10
        print(f"  - {table[0]}")
    if len(tables) > 10:
        print(f"  ... and {len(tables) - 10} more tables")
