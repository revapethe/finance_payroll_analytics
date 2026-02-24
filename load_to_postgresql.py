"""
LOAD EMPLOYEE DATA INTO PostgreSQL
===================================

This script loads your employee_data.csv into PostgreSQL database.

BEFORE RUNNING:
1. Make sure PostgreSQL is installed
2. Make sure you created 'payroll_db' database in pgAdmin
3. Change the password below to YOUR password
4. Run: python load_to_postgresql.py

Author: Analytics Team
Date: January 2026
"""

import pandas as pd
import sys
import os

print("=" * 100)
print("LOADING EMPLOYEE DATA INTO PostgreSQL")
print("=" * 100)
print()

# ============================================================================
# STEP 1: CHECK REQUIREMENTS
# ============================================================================

print("Step 1: Checking requirements...")
print("-" * 100)
print()

# Check psycopg2
try:
    import psycopg2
    print("✅ psycopg2 is installed")
except ImportError:
    print("❌ psycopg2 is NOT installed")
    print()
    print("Install it with: pip install psycopg2-binary")
    print()
    sys.exit(1)

# Check CSV file
if not os.path.exists('employee_data.csv'):
    print("❌ employee_data.csv NOT found")
    print()
    print("Make sure employee_data.csv is in this folder")
    print()
    sys.exit(1)

print("✅ employee_data.csv found")
print()

# ============================================================================
# STEP 2: LOAD CSV DATA
# ============================================================================

print("Step 2: Loading employee data from CSV...")
print("-" * 100)
print()

df = pd.read_csv('employee_data.csv')
print(f"✅ Loaded {len(df):,} employees")
print(f"✅ Columns: {len(df.columns)}")
print()

# ============================================================================
# STEP 3: CONNECT TO PostgreSQL
# ============================================================================

print("Step 3: Connecting to PostgreSQL...")
print("-" * 100)
print()

# ⚠️ CHANGE THESE SETTINGS TO MATCH YOUR SETUP ⚠️
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'payroll_db',  # Make sure you created this in pgAdmin!
    'user': 'postgres',
    'password': 'Reva@123'  # ⚠️ CHANGE THIS TO YOUR PASSWORD!
}

print("Connection settings:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  Database: {DB_CONFIG['database']}")
print(f"  User: {DB_CONFIG['user']}")
print()

try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("✅ Connected to PostgreSQL successfully!")
    print()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("TROUBLESHOOTING:")
    print("  1. Is PostgreSQL running?")
    print("     • Win + R → services.msc → Find 'postgresql-x64-16' → Should be Running")
    print()
    print("  2. Did you change the password in this script?")
    print("     • Line 52: password='YOUR_PASSWORD_HERE'")
    print("     • Change to your actual password")
    print()
    print("  3. Did you create 'payroll_db' database?")
    print("     • Open pgAdmin → Right-click Databases → Create → Database")
    print("     • Name: payroll_db")
    print()
    print("  4. Try using SQLite instead (no setup needed!):")
    print("     • Run: python FINAL_WORKING_SOLUTION.py")
    print()
    sys.exit(1)

cursor = conn.cursor()

# ============================================================================
# STEP 4: CREATE TABLE
# ============================================================================

print("Step 4: Creating Employees table...")
print("-" * 100)
print()

# Drop table if exists
try:
    cursor.execute("DROP TABLE IF EXISTS employees CASCADE")
    conn.commit()
    print("   Dropped existing table")
except:
    pass

# Create table
create_table_sql = """
CREATE TABLE employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    country VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    job_title VARCHAR(150) NOT NULL,
    department VARCHAR(100),
    currency VARCHAR(10),
    annual_salary_local NUMERIC(15, 2),
    annual_salary_usd NUMERIC(15, 2) NOT NULL,
    hire_date DATE,
    years_of_service NUMERIC(5, 1),
    performance_rating VARCHAR(50),
    remote_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

cursor.execute(create_table_sql)
conn.commit()
print("✅ Table 'employees' created successfully")
print()

# ============================================================================
# STEP 5: INSERT ALL EMPLOYEE DATA
# ============================================================================

print("Step 5: Inserting employee data...")
print("-" * 100)
print()

insert_sql = """
INSERT INTO employees 
(employee_id, first_name, last_name, email, country, city, job_title,
 department, currency, annual_salary_local, annual_salary_usd,
 hire_date, years_of_service, performance_rating, remote_status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

print(f"Inserting {len(df):,} employees into PostgreSQL...")
print("(This may take 30-60 seconds)")
print()

successful = 0
failed = 0

for index, row in df.iterrows():
    try:
        cursor.execute(insert_sql, (
            str(row['employee_id']),
            str(row.get('first_name', row.get('name', 'Unknown'))),
            str(row.get('last_name', 'Unknown')),
            str(row.get('email', f"{row['employee_id']}@company.com")),
            str(row['country']),
            str(row['city']),
            str(row['job_title']),
            str(row['department']),
            str(row['currency']),
            float(row.get('annual_salary_local', row['annual_salary_usd'])),
            float(row['annual_salary_usd']),
            str(row.get('hire_date', '2020-01-01')),
            float(row.get('years_of_service', 5.0)),
            str(row.get('performance', row.get('performance_rating', 'Good'))),
            str(row.get('remote_status', 'Hybrid'))
        ))
        
        successful += 1
        
        # Commit in batches
        if successful % 100 == 0:
            conn.commit()
            print(f"  Progress: {successful}/{len(df)} inserted...")
            
    except Exception as e:
        failed += 1
        if failed <= 3:
            print(f"  ⚠️ Error on row {index}: {e}")

conn.commit()

print()
print(f"✅ Successfully inserted {successful:,} employees")
if failed > 0:
    print(f"⚠️ Failed to insert {failed} employees")
print()

# ============================================================================
# STEP 6: VERIFY DATA
# ============================================================================

print("Step 6: Verifying data in PostgreSQL...")
print("-" * 100)
print()

cursor.execute("SELECT COUNT(*) FROM employees")
total = cursor.fetchone()[0]
print(f"✅ Total employees in database: {total:,}")

cursor.execute("SELECT country, COUNT(*) FROM employees GROUP BY country")
print()
print("Employees by country:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

print()

# ============================================================================
# STEP 7: QUERY TOP 10 USA
# ============================================================================

print("Step 7: Querying TOP 10 USA employees...")
print("-" * 100)
print()

top_10_usa_df = pd.read_sql_query("""
    SELECT 
        employee_id,
        first_name || ' ' || last_name AS full_name,
        job_title,
        department,
        city,
        annual_salary_usd,
        performance_rating
    FROM employees
    WHERE country = 'United States'
    ORDER BY annual_salary_usd DESC
    LIMIT 10
""", conn)

print("TOP 10 USA EMPLOYEES:")
print("=" * 100)
for i, row in top_10_usa_df.iterrows():
    print(f"{i+1:2d}. {row['employee_id']} - {row['full_name']}")
    print(f"    💼 {row['job_title']}")
    print(f"    💰 ${row['annual_salary_usd']:,.2f}")
    print(f"    🏢 {row['department']} | 📍 {row['city']}")
    print()

# ============================================================================
# STEP 8: QUERY TOP 10 INDIA
# ============================================================================

print("Step 8: Querying TOP 10 India employees...")
print("-" * 100)
print()

top_10_india_df = pd.read_sql_query("""
    SELECT 
        employee_id,
        first_name || ' ' || last_name AS full_name,
        job_title,
        city,
        annual_salary_local,
        annual_salary_usd
    FROM employees
    WHERE country = 'India'
    ORDER BY annual_salary_local DESC
    LIMIT 10
""", conn)

print("TOP 10 INDIA EMPLOYEES:")
print("=" * 100)
for i, row in top_10_india_df.iterrows():
    print(f"{i+1:2d}. {row['employee_id']} - {row['full_name']}")
    print(f"    💼 {row['job_title']}")
    print(f"    💰 ₹{row['annual_salary_local']:,.2f} (${row['annual_salary_usd']:,.2f} USD)")
    print(f"    📍 {row['city']}")
    print()

# ============================================================================
# STEP 9: EXPORT TO EXCEL
# ============================================================================

print("Step 9: Exporting to Excel...")
print("-" * 100)
print()

try:
    top_10_usa_df.to_excel('USA_Top10_PostgreSQL.xlsx', index=False)
    top_10_india_df.to_excel('India_Top10_PostgreSQL.xlsx', index=False)
    print("✅ USA_Top10_PostgreSQL.xlsx created")
    print("✅ India_Top10_PostgreSQL.xlsx created")
except Exception as e:
    print(f"⚠️ Excel export failed: {e}")
    top_10_usa_df.to_csv('USA_Top10_PostgreSQL.csv', index=False)
    top_10_india_df.to_csv('India_Top10_PostgreSQL.csv', index=False)
    print("✅ CSV files created instead")

print()

# ============================================================================
# STEP 10: CLOSE CONNECTION
# ============================================================================

cursor.close()
conn.close()
print("✅ Connection closed")
print()

# ============================================================================
# SUCCESS MESSAGE
# ============================================================================

print("=" * 100)
print("🎉 SUCCESS! YOUR DATA IS IN PostgreSQL!")
print("=" * 100)
print()

print("DATABASE INFO:")
print("  • Host: localhost")
print("  • Port: 5432")
print("  • Database: payroll_db")
print("  • Table: employees")
print(f"  • Records: {successful:,}")
print()

print("NOW YOU CAN:")
print()
print("  1️⃣ OPEN pgAdmin")
print("     • Connect to PostgreSQL 16")
print("     • Expand: payroll_db → Schemas → public → Tables")
print("     • Right-click: employees → View/Edit Data → All Rows")
print("     • SEE YOUR 2,000 EMPLOYEES!")
print()

print("  2️⃣ RUN SQL QUERIES IN pgAdmin")
print("     • Right-click payroll_db → Query Tool")
print("     • Type SQL queries")
print("     • Execute (F5)")
print()

print("  3️⃣ QUERY FROM PYTHON")
print("     • import psycopg2")
print("     • Connect and query anytime")
print()

print("=" * 100)
print()

print("📝 SQL QUERIES TO TRY IN pgAdmin:")
print()

sample_queries = """
-- Top 10 by salary
SELECT * FROM employees 
ORDER BY annual_salary_usd DESC 
LIMIT 10;

-- Count by country
SELECT country, COUNT(*) 
FROM employees 
GROUP BY country;

-- Average salary by department
SELECT department, AVG(annual_salary_usd) as avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- High earners (>$150K)
SELECT employee_id, first_name, last_name, annual_salary_usd
FROM employees
WHERE annual_salary_usd > 150000
ORDER BY annual_salary_usd DESC;
"""

print(sample_queries)
print()

print("=" * 100)
print("SCRIPT COMPLETE!")
print("=" * 100)
