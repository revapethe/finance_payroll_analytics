"""
HOW TO PUT GENERATED DATA INTO SQL SERVER - COMPLETE GUIDE
===========================================================

This script will:
1. Check your connection
2. Create database
3. Create table
4. Load ALL your employee data into SQL Server
5. Verify it worked

Just run: python load_data_to_sqlserver.py

Author: Analytics Team
Date: January 2026
"""

import pandas as pd
import sys

print("=" * 100)
print("LOADING EMPLOYEE DATA INTO SQL SERVER")
print("=" * 100)
print()

# ============================================================================
# STEP 1: CHECK REQUIREMENTS
# ============================================================================

print("STEP 1: Checking requirements...")
print("-" * 100)
print()

# Check for pyodbc
try:
    import pyodbc
    print("✅ pyodbc is installed")
except ImportError:
    print("❌ pyodbc is NOT installed")
    print()
    print("Please run: pip install pyodbc")
    print()
    sys.exit(1)

# Check for CSV file
import os
if os.path.exists('employee_data.csv'):
    print("✅ employee_data.csv found")
else:
    print("❌ employee_data.csv NOT found")
    print()
    print("Please run BEGINNER_COMPLETE_GUIDE.py first to generate data")
    print()
    sys.exit(1)

print()

# ============================================================================
# STEP 2: LOAD YOUR CSV DATA
# ============================================================================

print("STEP 2: Loading your employee data from CSV...")
print("-" * 100)
print()

df = pd.read_csv('employee_data.csv')

print(f"✅ Loaded {len(df):,} employees")
print(f"✅ Columns: {len(df.columns)}")
print()

print("Sample data:")
print(df.head(3).to_string())
print()

# ============================================================================
# STEP 3: TRY MULTIPLE CONNECTION METHODS
# ============================================================================

print("STEP 3: Finding SQL Server connection...")
print("-" * 100)
print()

# Different connection strings to try
connection_options = [
    ('localhost\\SQLEXPRESS', 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;Trusted_Connection=yes;'),
    ('.\\SQLEXPRESS', 'DRIVER={SQL Server};SERVER=.\\SQLEXPRESS;Trusted_Connection=yes;'),
    ('REVADELL\\SQLEXPRESS', 'DRIVER={SQL Server};SERVER=REVADELL\\SQLEXPRESS;Trusted_Connection=yes;'),
    ('(localdb)\\MSSQLLocalDB', 'DRIVER={SQL Server};SERVER=(localdb)\\MSSQLLocalDB;Trusted_Connection=yes;'),
    ('localhost', 'DRIVER={SQL Server};SERVER=localhost;Trusted_Connection=yes;'),
    ('.', 'DRIVER={SQL Server};SERVER=.;Trusted_Connection=yes;')
]

conn = None
server_name = None

print("Trying different connection methods...")
print()

for server, conn_string in connection_options:
    print(f"  Trying: {server}...", end=" ")
    try:
        conn = pyodbc.connect(conn_string, timeout=3)
        print("✅ SUCCESS!")
        server_name = server
        break
    except Exception as e:
        print(f"❌ Failed")

print()

if conn is None:
    print("=" * 100)
    print("❌ COULD NOT CONNECT TO SQL SERVER")
    print("=" * 100)
    print()
    print("POSSIBLE REASONS:")
    print("  1. SQL Server is not installed")
    print("  2. SQL Server service is not running")
    print("  3. Different instance name")
    print()
    print("TO FIX:")
    print()
    print("  OPTION A: Start SQL Server Service")
    print("    1. Press Win + R")
    print("    2. Type: services.msc")
    print("    3. Find: SQL Server (SQLEXPRESS)")
    print("    4. Right-click → Start")
    print("    5. Run this script again")
    print()
    print("  OPTION B: Use SQLite Instead (Easier!)")
    print("    Run: python use_sqlite_instead.py")
    print()
    sys.exit(1)

print("✅ Connected to SQL Server!")
print(f"✅ Server: {server_name}")
print()

cursor = conn.cursor()

# ============================================================================
# STEP 4: CREATE DATABASE
# ============================================================================

print("STEP 4: Creating database...")
print("-" * 100)
print()

try:
    # Try to create database
    conn.autocommit = True
    cursor.execute("CREATE DATABASE PayrollDB")
    print("✅ Database 'PayrollDB' created")
except Exception as e:
    if "already exists" in str(e):
        print("⚠️  Database 'PayrollDB' already exists (OK, will use existing)")
    else:
        print(f"⚠️  Warning: {e}")

print()

# Reconnect to the specific database
conn.close()

# Reconnect to PayrollDB
db_conn_string = connection_options[[s for s, _ in connection_options].index(server_name)][1].replace('Trusted_Connection=yes;', 'DATABASE=PayrollDB;Trusted_Connection=yes;')

try:
    conn = pyodbc.connect(db_conn_string)
    conn.autocommit = False
    cursor = conn.cursor()
    print("✅ Connected to PayrollDB database")
except Exception as e:
    print(f"❌ Could not connect to PayrollDB: {e}")
    sys.exit(1)

print()

# ============================================================================
# STEP 5: CREATE TABLE
# ============================================================================

print("STEP 5: Creating Employees table...")
print("-" * 100)
print()

# Drop table if exists
try:
    cursor.execute("DROP TABLE IF EXISTS Employees")
    conn.commit()
except:
    pass

# Create table
create_table_sql = """
CREATE TABLE Employees (
    EmployeeID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Country VARCHAR(50) NOT NULL,
    City VARCHAR(100),
    JobTitle VARCHAR(100),
    Department VARCHAR(50),
    Currency VARCHAR(10),
    AnnualSalaryLocal DECIMAL(15, 2),
    AnnualSalaryUSD DECIMAL(15, 2),
    MonthlySalaryUSD DECIMAL(15, 2),
    HireDate DATE,
    YearsOfService DECIMAL(5, 1),
    PerformanceRating VARCHAR(50),
    RemoteStatus VARCHAR(50),
    Education VARCHAR(50),
    CreatedDate DATETIME DEFAULT GETDATE()
)
"""

try:
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Table 'Employees' created successfully")
except Exception as e:
    print(f"❌ Error creating table: {e}")
    sys.exit(1)

print()

# ============================================================================
# STEP 6: INSERT ALL EMPLOYEE DATA
# ============================================================================

print("STEP 6: Inserting employee data into SQL Server...")
print("-" * 100)
print()

insert_sql = """
INSERT INTO Employees 
(EmployeeID, FirstName, LastName, Email, Country, City, JobTitle, 
 Department, Currency, AnnualSalaryLocal, AnnualSalaryUSD, MonthlySalaryUSD,
 HireDate, YearsOfService, PerformanceRating, RemoteStatus, Education)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

successful_inserts = 0
failed_inserts = 0

print(f"Inserting {len(df)} employees...")
print()

for index, row in df.iterrows():
    try:
        # Prepare data
        employee_id = str(row.get('employee_id', f'EMP{index:04d}'))
        
        # Handle different possible column names
        first_name = str(row.get('first_name', row.get('name', 'Unknown')))
        last_name = str(row.get('last_name', row.get('last', 'Unknown')))
        email = str(row.get('email', f"{employee_id}@company.com"))
        country = str(row['country'])
        city = str(row.get('city', 'Unknown'))
        job_title = str(row['job_title'])
        department = str(row['department'])
        currency = str(row['currency'])
        
        annual_salary_local = float(row.get('annual_salary_local', row.get('annual_salary_usd', 0)))
        annual_salary_usd = float(row['annual_salary_usd'])
        monthly_salary_usd = float(row.get('monthly_salary_usd', annual_salary_usd / 12))
        
        hire_date = str(row.get('hire_date', '2020-01-01'))
        years_of_service = float(row.get('years_of_service', row.get('years', 5.0)))
        performance = str(row.get('performance_rating', row.get('performance', 'Good')))
        remote_status = str(row.get('remote_status', 'Hybrid'))
        education = str(row.get('education', 'Bachelor'))
        
        # Insert
        cursor.execute(insert_sql, (
            employee_id,
            first_name,
            last_name,
            email,
            country,
            city,
            job_title,
            department,
            currency,
            annual_salary_local,
            annual_salary_usd,
            monthly_salary_usd,
            hire_date,
            years_of_service,
            performance,
            remote_status,
            education
        ))
        
        successful_inserts += 1
        
        # Show progress
        if (index + 1) % 200 == 0:
            print(f"  Progress: {index + 1}/{len(df)} employees inserted...")
            conn.commit()  # Commit in batches
            
    except Exception as e:
        failed_inserts += 1
        if failed_inserts <= 3:  # Only show first 3 errors
            print(f"  ⚠️  Error inserting row {index}: {e}")

# Final commit
conn.commit()

print()
print(f"✅ Successfully inserted: {successful_inserts:,} employees")
if failed_inserts > 0:
    print(f"⚠️  Failed to insert: {failed_inserts} employees")
print()

# ============================================================================
# STEP 7: VERIFY DATA IN SQL SERVER
# ============================================================================

print("STEP 7: Verifying data in SQL Server...")
print("-" * 100)
print()

# Count total employees
cursor.execute("SELECT COUNT(*) FROM Employees")
total_count = cursor.fetchone()[0]
print(f"✅ Total employees in database: {total_count:,}")

# Count by country
cursor.execute("""
    SELECT Country, COUNT(*) as Count
    FROM Employees
    GROUP BY Country
""")

print()
print("Employees by Country:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

print()

# ============================================================================
# STEP 8: QUERY TOP 10 USA
# ============================================================================

print("STEP 8: Querying TOP 10 USA employees from SQL Server...")
print("-" * 100)
print()

top_10_usa_query = """
SELECT TOP 10
    EmployeeID,
    FirstName,
    LastName,
    JobTitle,
    Department,
    City,
    AnnualSalaryUSD,
    PerformanceRating
FROM Employees
WHERE Country = 'United States'
ORDER BY AnnualSalaryUSD DESC
"""

top_10_usa = pd.read_sql(top_10_usa_query, conn)

print("TOP 10 USA EMPLOYEES (FROM SQL SERVER):")
print("=" * 100)
print()

for idx, row in top_10_usa.iterrows():
    print(f"{idx+1:2d}. {row['EmployeeID']} - {row['FirstName']} {row['LastName']}")
    print(f"    💼 {row['JobTitle']}")
    print(f"    💰 ${row['AnnualSalaryUSD']:,.2f}")
    print(f"    🏢 {row['Department']} | 📍 {row['City']}")
    print()

# ============================================================================
# STEP 9: QUERY TOP 10 INDIA
# ============================================================================

print("STEP 9: Querying TOP 10 India employees from SQL Server...")
print("-" * 100)
print()

top_10_india_query = """
SELECT TOP 10
    EmployeeID,
    FirstName,
    LastName,
    JobTitle,
    Department,
    City,
    AnnualSalaryLocal,
    AnnualSalaryUSD
FROM Employees
WHERE Country = 'India'
ORDER BY AnnualSalaryLocal DESC
"""

top_10_india = pd.read_sql(top_10_india_query, conn)

print("TOP 10 INDIA EMPLOYEES (FROM SQL SERVER):")
print("=" * 100)
print()

for idx, row in top_10_india.iterrows():
    print(f"{idx+1:2d}. {row['EmployeeID']} - {row['FirstName']} {row['LastName']}")
    print(f"    💼 {row['JobTitle']}")
    print(f"    💰 ₹{row['AnnualSalaryLocal']:,.2f} (${row['AnnualSalaryUSD']:,.2f} USD)")
    print(f"    🏢 {row['Department']} | 📍 {row['City']}")
    print()

# ============================================================================
# STEP 10: EXPORT TO EXCEL
# ============================================================================

print("STEP 10: Exporting results to Excel...")
print("-" * 100)
print()

try:
    # Create comprehensive Excel report
    with pd.ExcelWriter('SQL_Server_Employee_Report.xlsx', engine='openpyxl') as writer:
        top_10_usa.to_excel(writer, sheet_name='USA Top 10', index=False)
        top_10_india.to_excel(writer, sheet_name='India Top 10', index=False)
    
    print("✅ Excel report created: SQL_Server_Employee_Report.xlsx")
except Exception as e:
    print(f"⚠️  Could not create Excel: {e}")
    print("   Saving as CSV instead...")
    top_10_usa.to_csv('USA_Top10_from_SQLServer.csv', index=False)
    top_10_india.to_csv('India_Top10_from_SQLServer.csv', index=False)
    print("✅ CSV files created")

print()

# ============================================================================
# STEP 11: RUN ADDITIONAL QUERIES
# ============================================================================

print("STEP 11: Running additional analysis queries...")
print("-" * 100)
print()

# Department summary
dept_query = """
SELECT 
    Country,
    Department,
    COUNT(*) AS EmployeeCount,
    AVG(AnnualSalaryUSD) AS AvgSalaryUSD,
    SUM(AnnualSalaryUSD) AS TotalPayrollUSD
FROM Employees
GROUP BY Country, Department
ORDER BY TotalPayrollUSD DESC
"""

dept_summary = pd.read_sql(dept_query, conn)

print("DEPARTMENT SUMMARY:")
print(dept_summary.to_string(index=False))
print()

# ============================================================================
# STEP 12: CLOSE CONNECTION
# ============================================================================

cursor.close()
conn.close()

print()
print("=" * 100)
print("🎉 SUCCESS! YOUR DATA IS NOW IN SQL SERVER!")
print("=" * 100)
print()

print("WHAT WAS CREATED:")
print()
print("  IN SQL SERVER:")
print("    • Database: PayrollDB")
print("    • Table: Employees")
print("    • Rows: {:,} employee records".format(successful_inserts))
print()

print("  ON YOUR COMPUTER:")
print("    • SQL_Server_Employee_Report.xlsx (Top 10 reports)")
print()

print("=" * 100)
print()

print("NOW YOU CAN:")
print()
print("  1️⃣  OPEN SSMS")
print("     • Connect to: " + server_name)
print("     • Expand: Databases → PayrollDB → Tables → dbo.Employees")
print("     • Right-click table → Select Top 1000 Rows")
print("     • SEE YOUR DATA!")
print()

print("  2️⃣  RUN SQL QUERIES IN SSMS")
print("     • Click 'New Query'")
print("     • Type SQL (see examples below)")
print("     • Press F5 to execute")
print()

print("  3️⃣  QUERY FROM PYTHON ANYTIME")
print("     • Use the connection method that worked")
print("     • Run any SQL query")
print("     • Export to Excel")
print()

print("=" * 100)
print()

print("📝 SQL QUERIES TO TRY IN SSMS:")
print()

sample_queries = """
-- Make sure you're using the right database
USE PayrollDB;
GO

-- Query 1: View all employees
SELECT * FROM Employees;

-- Query 2: Count by country
SELECT Country, COUNT(*) as Total
FROM Employees
GROUP BY Country;

-- Query 3: Top 10 USA
SELECT TOP 10 *
FROM Employees
WHERE Country = 'United States'
ORDER BY AnnualSalaryUSD DESC;

-- Query 4: Top 10 India (by INR)
SELECT TOP 10 
    EmployeeID,
    FirstName + ' ' + LastName AS FullName,
    JobTitle,
    AnnualSalaryLocal AS SalaryINR,
    AnnualSalaryUSD
FROM Employees
WHERE Country = 'India'
ORDER BY AnnualSalaryLocal DESC;

-- Query 5: Average salary by department
SELECT 
    Department,
    COUNT(*) AS Employees,
    AVG(AnnualSalaryUSD) AS AvgSalary
FROM Employees
GROUP BY Department
ORDER BY AvgSalary DESC;

-- Query 6: Employees in specific city
SELECT *
FROM Employees
WHERE City = 'San Francisco'
ORDER BY AnnualSalaryUSD DESC;

-- Query 7: High performers
SELECT *
FROM Employees
WHERE PerformanceRating IN ('Excellent', 'Outstanding')
ORDER BY AnnualSalaryUSD DESC;

-- Query 8: Remote workers
SELECT Country, RemoteStatus, COUNT(*) as Count
FROM Employees
GROUP BY Country, RemoteStatus
ORDER BY Country, Count DESC;
"""

print(sample_queries)
print()

print("=" * 100)
print()

print("✅ COPY THESE QUERIES INTO SSMS AND RUN THEM (F5)")
print()

print("=" * 100)
print("SCRIPT COMPLETE!")
print("=" * 100)
