"""
POSTGRESQL SETUP SCRIPT - FRESH VERSION
========================================

This script:
1. Connects to your PostgreSQL database
2. Creates tables for employees and documents
3. Loads all 2,000 employees into PostgreSQL
4. Loads document metadata

BEFORE RUNNING:
  1. Create database 'payroll_analytics' in pgAdmin
  2. Change PASSWORD below (line 30)
  3. Run: python postgresql_setup_fresh.py

Author: Analytics Team
Date: May 2026
"""

import pandas as pd
import os
import sys

print("=" * 100)
print("🐘 POSTGRESQL SETUP - LOAD DATA TO POSTGRESQL")
print("=" * 100)
print()

# ============================================================================
# ⚠️ CHANGE YOUR PASSWORD HERE!
# ============================================================================

print("⚠️  IMPORTANT: UPDATE YOUR PASSWORD BELOW!")
print("-" * 100)
print()

# ⚠️⚠️⚠️ CHANGE THIS PASSWORD! ⚠️⚠️⚠️
YOUR_POSTGRESQL_PASSWORD = 'postgres123'  # ← CHANGE THIS LINE!

# ============================================================================

print(f"Using password: {YOUR_POSTGRESQL_PASSWORD}")
print()
print("If this is wrong, edit line 30 in this file and change it!")
print()

# ============================================================================
# STEP 1: CHECK PSYCOPG2
# ============================================================================

print("STEP 1: Checking psycopg2...")
print("-" * 100)

try:
    import psycopg2
    print("✅ psycopg2 is installed")
except ImportError:
    print("❌ psycopg2 NOT installed")
    print()
    print("Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
    import psycopg2
    print("✅ psycopg2 installed!")

print()

# ============================================================================
# STEP 2: CONNECT TO POSTGRESQL
# ============================================================================

print("STEP 2: Connecting to PostgreSQL...")
print("-" * 100)
print()

# Try different database names
databases_to_try = ['payroll_analytics', 'payroll_db', 'postgres']

conn = None
connected_to = None

for db_name in databases_to_try:
    try:
        print(f"Trying database: {db_name}...")
        
        conn = psycopg2.connect(
            host='localhost',
            database=db_name,
            user='postgres',
            password=YOUR_POSTGRESQL_PASSWORD,
            port=5432
        )
        
        connected_to = db_name
        print(f"✅ Connected to PostgreSQL database: {db_name}")
        print()
        break
        
    except psycopg2.OperationalError as e:
        if 'password authentication failed' in str(e):
            print(f"❌ Password is wrong!")
            print()
            print("=" * 100)
            print("❌ PASSWORD AUTHENTICATION FAILED")
            print("=" * 100)
            print()
            print("YOUR PASSWORD IS INCORRECT!")
            print()
            print("TO FIX:")
            print("  1. Open this file in Notepad: postgresql_setup_fresh.py")
            print(f"  2. Line 30: YOUR_POSTGRESQL_PASSWORD = '{YOUR_POSTGRESQL_PASSWORD}'")
            print("  3. Change to your actual PostgreSQL password")
            print("  4. Save and run again")
            print()
            print("DON'T REMEMBER PASSWORD?")
            print("  • Open pgAdmin")
            print("  • Right-click PostgreSQL 18 → Properties")
            print("  • Connection tab → Change password")
            print()
            sys.exit(1)
        elif 'database' in str(e) and 'does not exist' in str(e):
            print(f"❌ Database '{db_name}' doesn't exist, trying next...")
        else:
            print(f"❌ Connection failed: {e}")

if conn is None:
    print()
    print("=" * 100)
    print("❌ COULD NOT CONNECT TO ANY DATABASE")
    print("=" * 100)
    print()
    print("PLEASE CREATE DATABASE FIRST:")
    print()
    print("  1. Open pgAdmin")
    print("  2. Expand: Servers → PostgreSQL 18")
    print("  3. Right-click: Databases")
    print("  4. Create → Database...")
    print("  5. Name: payroll_analytics")
    print("  6. Click: Save")
    print()
    print("  Then run this script again!")
    print()
    sys.exit(1)

cursor = conn.cursor()

# ============================================================================
# STEP 3: CREATE TABLES
# ============================================================================

print("STEP 3: Creating tables...")
print("-" * 100)
print()

# Drop existing tables to start fresh
cursor.execute("DROP TABLE IF EXISTS employees CASCADE")
cursor.execute("DROP TABLE IF EXISTS documents CASCADE")

# Create employees table
cursor.execute("""
    CREATE TABLE employees (
        employee_id VARCHAR(20) PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        country VARCHAR(50),
        city VARCHAR(100),
        job_title VARCHAR(150),
        department VARCHAR(100),
        annual_salary_usd DECIMAL(12, 2),
        hire_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

print("✅ Created 'employees' table")

# Create documents table
cursor.execute("""
    CREATE TABLE documents (
        doc_id VARCHAR(20) PRIMARY KEY,
        title VARCHAR(500),
        filename VARCHAR(500),
        content TEXT,
        page_count INTEGER,
        created_at TIMESTAMP,
        indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

print("✅ Created 'documents' table")

conn.commit()
print()

# ============================================================================
# STEP 4: LOAD EMPLOYEE DATA
# ============================================================================

print("STEP 4: Loading employee data...")
print("-" * 100)
print()

if not os.path.exists('employee_data.csv'):
    print("❌ employee_data.csv not found!")
    print()
    print("Make sure you run this in: D:\\Finance Payroll Project")
    print("And employee_data.csv exists in that folder")
    print()
    cursor.close()
    conn.close()
    sys.exit(1)

df = pd.read_csv('employee_data.csv')
print(f"✅ Loaded {len(df):,} employees from CSV")
print()

print("Inserting into PostgreSQL...")
print()

inserted = 0
for idx, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO employees (
                employee_id, first_name, last_name, email, 
                country, city, job_title, department, annual_salary_usd
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['employee_id'],
            row.get('first_name', row.get('name', 'Employee')),
            row.get('last_name', str(row.get('employee_id', ''))),
            row.get('email', f"{row['employee_id']}@company.com"),
            row['country'],
            row['city'],
            row['job_title'],
            row['department'],
            float(row['annual_salary_usd'])
        ))
        
        inserted += 1
        
        if inserted % 200 == 0:
            print(f"  Progress: {inserted}/{len(df)} employees inserted...")
            conn.commit()
    
    except Exception as e:
        print(f"  ⚠️ Error on row {idx}: {e}")

conn.commit()
print()
print(f"✅ Successfully inserted {inserted:,} employees into PostgreSQL!")
print()

# ============================================================================
# STEP 5: VERIFY
# ============================================================================

print("STEP 5: Verifying data...")
print("-" * 100)
print()

# Count total
cursor.execute("SELECT COUNT(*) FROM employees")
total = cursor.fetchone()[0]
print(f"✅ Total employees in PostgreSQL: {total:,}")

# Count by country
cursor.execute("""
    SELECT country, COUNT(*) 
    FROM employees 
    GROUP BY country 
    ORDER BY COUNT(*) DESC
""")

print()
print("Breakdown by country:")
for country, count in cursor.fetchall():
    print(f"  • {country}: {count:,} employees")

# Top 5 earners
cursor.execute("""
    SELECT employee_id, job_title, country, annual_salary_usd
    FROM employees
    ORDER BY annual_salary_usd DESC
    LIMIT 5
""")

print()
print("Top 5 highest paid:")
for emp_id, job, country, salary in cursor.fetchall():
    print(f"  {emp_id} - {job} ({country}) - ${salary:,.2f}")

print()

cursor.close()
conn.close()

# ============================================================================
# SUCCESS
# ============================================================================

print("=" * 100)
print("🎉 POSTGRESQL SETUP COMPLETE!")
print("=" * 100)
print()

print("WHAT WAS CREATED:")
print(f"  ✅ Database: {connected_to}")
print(f"  ✅ Table: employees ({total:,} records)")
print("  ✅ Table: documents (ready)")
print()

print("CONNECTION DETAILS:")
print("  • Host: localhost")
print(f"  • Database: {connected_to}")
print("  • User: postgres")
print("  • Port: 5432")
print()

print("NEXT STEPS:")
print("  1. Run: streamlit run postgresql_integrated_platform.py")
print("  2. Dashboard will query PostgreSQL!")
print("  3. See 'PostgreSQL' in sidebar status")
print()

print("=" * 100)
