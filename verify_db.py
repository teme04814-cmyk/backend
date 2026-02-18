#!/usr/bin/env python
"""Verify database connection and check django_migrations table"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection
from django.conf import settings

print(f"Database Configuration:")
print(f"  ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"  NAME: {settings.DATABASES['default']['NAME']}")
print(f"  HOST: {settings.DATABASES['default']['HOST']}")
print(f"  PORT: {settings.DATABASES['default']['PORT']}")
print(f"  USER: {settings.DATABASES['default']['USER']}")
print()

try:
    with connection.cursor() as cursor:
        # Check if django_migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            );
        """)
        migrations_table_exists = cursor.fetchone()[0]
        
        if migrations_table_exists:
            print("django_migrations table exists!")
            cursor.execute("SELECT COUNT(*) FROM django_migrations;")
            count = cursor.fetchone()[0]
            print(f"Found {count} migration records")
        else:
            print("django_migrations table does NOT exist - migrations haven't been applied!")
            
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nTotal tables in database: {len(tables)}")
        if tables:
            print("Tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
except Exception as e:
    print(f"Error: {e}")
