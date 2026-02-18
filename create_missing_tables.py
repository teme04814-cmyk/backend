#!/usr/bin/env python
"""Create missing tables using Django's schema editor"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.db import connection
from partnerships.models import Company, Partnership, PartnershipDocument, PartnershipApprovalLog
from payments.models import Payment
from systemsettings.models import SystemSetting
from contact.models import ContactMessage

print("Creating missing tables...")

with connection.schema_editor() as schema_editor:
    # Create partnerships tables
    try:
        print("Creating partnerships_company table...")
        schema_editor.create_model(Company)
        print("  ✓ Created partnerships_company")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    try:
        print("Creating partnerships_partnership table...")
        schema_editor.create_model(Partnership)
        print("  ✓ Created partnerships_partnership")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    try:
        print("Creating partnerships_partnershipdocument table...")
        schema_editor.create_model(PartnershipDocument)
        print("  ✓ Created partnerships_partnershipdocument")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    try:
        print("Creating partnerships_partnershipapprovallog table...")
        schema_editor.create_model(PartnershipApprovalLog)
        print("  ✓ Created partnerships_partnershipapprovallog")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Create other missing tables
    try:
        print("Creating payments_payment table...")
        schema_editor.create_model(Payment)
        print("  ✓ Created payments_payment")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    try:
        print("Creating systemsettings_systemsetting table...")
        schema_editor.create_model(SystemSetting)
        print("  ✓ Created systemsettings_systemsetting")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    try:
        print("Creating contact_contactmessage table...")
        schema_editor.create_model(ContactMessage)
        print("  ✓ Created contact_contactmessage")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\nVerifying tables...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    print(f"Total tables: {len(tables)}")
    partnerships_tables = [t for t in tables if 'partnership' in t[0].lower()]
    if partnerships_tables:
        print("Partnerships tables:")
        for table in partnerships_tables:
            print(f"  - {table[0]}")
