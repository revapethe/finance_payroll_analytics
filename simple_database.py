import pandas as pd
import sqlite3

print("=" * 80)
print("SIMPLE DATABASE SOLUTION - LOADING YOUR DATA")
print("=" * 80)
print()

# Load CSV
try:
    df = pd.read_csv('employee_data.csv')
    print(f"✅ Loaded {len(df):,} employees")
except:
    print("❌ employee_data.csv not found")
    print()
    print("First run: python BEGINNER_COMPLETE_GUIDE.py")
    exit()

# Create SQLite database
conn = sqlite3.connect('employees.db')
print("✅ Created database: employees.db")

# Insert data
df.to_sql('employees', conn, if_exists='replace', index=False)
print(f"✅ Inserted {len(df):,} employees into database")
print()

# Query top 10 USA
top_usa = pd.read_sql_query("""
    SELECT * FROM employees
    WHERE country = 'United States'
    ORDER BY annual_salary_usd DESC
    LIMIT 10
""", conn)

print("TOP 10 USA:")
print("=" * 80)
for i, r in top_usa.iterrows():
    print(f"{i+1}. {r['employee_id']} - ${r['annual_salary_usd']:,.0f}")

print()

# Query top 10 India
top_india = pd.read_sql_query("""
    SELECT * FROM employees
    WHERE country = 'India'
    ORDER BY annual_salary_usd DESC
    LIMIT 10
""", conn)

print("TOP 10 INDIA:")
print("=" * 80)
for i, r in top_india.iterrows():
    print(f"{i+1}. {r['employee_id']} - ${r['annual_salary_usd']:,.0f}")

print()

# Export
top_usa.to_excel('USA_Top10.xlsx', index=False)
top_india.to_excel('India_Top10.xlsx', index=False)

print("✅ USA_Top10.xlsx created")
print("✅ India_Top10.xlsx created")
print("✅ employees.db created")
print()
print("=" * 80)
print("✅ DONE! Your data is in a database now!")
print("=" * 80)

conn.close()
