"""
BEGINNER'S COMPLETE GUIDE - INDIA & USA EMPLOYEE DATA
======================================================

WHAT THIS SCRIPT DOES:
1. Generates 2,000 employee records (1,000 USA + 1,000 India)
2. Creates Top 10 reports for both countries
3. Builds visualizations
4. Exports to Excel files

HOW TO RUN:
Simply run: python BEGINNER_COMPLETE_GUIDE.py

NO CODING REQUIRED - JUST RUN IT!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

print("=" * 100)
print("🚀 INDIA & USA EMPLOYEE DATA GENERATOR")
print("=" * 100)
print()

# USA Jobs and Salaries (in USD)
USA_JOBS = {
    'Software Engineer': (90000, 140000),
    'Senior Software Engineer': (130000, 190000),
    'Data Scientist': (95000, 145000),
    'Product Manager': (110000, 160000),
    'Engineering Manager': (140000, 210000),
    'Sales Manager': (70000, 120000)
}

# India Jobs and Salaries (in INR)
INDIA_JOBS = {
    'Software Engineer': (900000, 1800000),
    'Senior Software Engineer': (1800000, 3200000),
    'Data Scientist': (1000000, 2400000),
    'Product Manager': (1300000, 2800000),
    'Engineering Manager': (2000000, 4200000),
    'Sales Manager': (700000, 1500000)
}

USA_CITIES = ['San Francisco', 'New York', 'Seattle', 'Austin', 'Boston']
INDIA_CITIES = ['Bangalore', 'Mumbai', 'Hyderabad', 'Pune', 'Delhi']
DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'HR', 'Finance']

print("📍 Generating USA employees...")
usa_employees = []
for i in range(1, 1001):
    job = random.choice(list(USA_JOBS.keys()))
    salary = random.randint(USA_JOBS[job][0], USA_JOBS[job][1])
    hire_date = datetime.now() - timedelta(days=random.randint(0, 3650))
    
    usa_employees.append({
        'employee_id': f'USA{i:04d}',
        'first_name': f'USAEmp{i}',
        'last_name': f'Last{i}',
        'email': f'usa{i}@company.com',
        'country': 'United States',
        'city': random.choice(USA_CITIES),
        'job_title': job,
        'department': random.choice(DEPARTMENTS),
        'currency': 'USD',
        'annual_salary_local': salary,
        'annual_salary_usd': salary,
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'years_of_service': round((datetime.now() - hire_date).days / 365.25, 1),
        'performance': random.choice(['Outstanding', 'Excellent', 'Good', 'Satisfactory']),
        'remote_status': random.choice(['Remote', 'Hybrid', 'On-Site'])
    })

print(f"   ✅ Generated {len(usa_employees)} USA employees")

print("📍 Generating India employees...")
india_employees = []
for i in range(1, 1001):
    job = random.choice(list(INDIA_JOBS.keys()))
    salary_inr = random.randint(INDIA_JOBS[job][0], INDIA_JOBS[job][1])
    salary_usd = round(salary_inr * 0.012, 2)
    hire_date = datetime.now() - timedelta(days=random.randint(0, 3650))
    
    india_employees.append({
        'employee_id': f'IND{i:04d}',
        'first_name': f'IndEmp{i}',
        'last_name': f'Last{i+1000}',
        'email': f'ind{i}@company.com',
        'country': 'India',
        'city': random.choice(INDIA_CITIES),
        'job_title': job,
        'department': random.choice(DEPARTMENTS),
        'currency': 'INR',
        'annual_salary_local': salary_inr,
        'annual_salary_usd': salary_usd,
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'years_of_service': round((datetime.now() - hire_date).days / 365.25, 1),
        'performance': random.choice(['Outstanding', 'Excellent', 'Good', 'Satisfactory']),
        'remote_status': random.choice(['Remote', 'Hybrid', 'On-Site'])
    })

print(f"   ✅ Generated {len(india_employees)} India employees")
print()

# Combine and save
df = pd.DataFrame(usa_employees + india_employees)
df.to_csv('employee_data.csv', index=False)
print("✅ Saved to: employee_data.csv")
print()

# Statistics
usa_df = df[df['country'] == 'United States']
india_df = df[df['country'] == 'India']

print("=" * 100)
print("📊 SUMMARY STATISTICS")
print("=" * 100)
print(f"\nTotal Employees: {len(df):,}")
print(f"\nUSA: {len(usa_df):,} employees | Avg: ${usa_df['annual_salary_usd'].mean():,.2f}")
print(f"India: {len(india_df):,} employees | Avg: ₹{india_df['annual_salary_local'].mean():,.2f} (${india_df['annual_salary_usd'].mean():,.2f} USD)")
print()

# Top 10 USA
print("=" * 100)
print("🏆 TOP 10 USA EMPLOYEES")
print("=" * 100)
top_10_usa = usa_df.nlargest(10, 'annual_salary_usd')
for rank, (_, emp) in enumerate(top_10_usa.iterrows(), 1):
    print(f"{rank:2d}. {emp['employee_id']} - {emp['job_title']:30} ${emp['annual_salary_usd']:>10,.0f}")

top_10_usa.to_excel('USA_Top10.xlsx', index=False)
print("\n✅ Saved to: USA_Top10.xlsx")
print()

# Top 10 India
print("=" * 100)
print("🏆 TOP 10 INDIA EMPLOYEES")
print("=" * 100)
top_10_india = india_df.nlargest(10, 'annual_salary_local')
for rank, (_, emp) in enumerate(top_10_india.iterrows(), 1):
    print(f"{rank:2d}. {emp['employee_id']} - {emp['job_title']:30} ₹{emp['annual_salary_local']:>12,.0f}")

top_10_india.to_excel('India_Top10.xlsx', index=False)
print("\n✅ Saved to: India_Top10.xlsx")
print()

# Create visualization
print("📈 Creating charts...")
plt.figure(figsize=(10, 6))
top_usa_sorted = top_10_usa.sort_values('annual_salary_usd')
plt.barh(range(len(top_usa_sorted)), top_usa_sorted['annual_salary_usd'], color='steelblue')
plt.yticks(range(len(top_usa_sorted)), [f"{r['employee_id']}" for _, r in top_usa_sorted.iterrows()])
plt.xlabel('Annual Salary (USD)', fontsize=12, fontweight='bold')
plt.title('USA - Top 10 Employees by Salary', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('USA_Top10_Chart.png', dpi=300)
print("   ✅ Chart saved: USA_Top10_Chart.png")
print()

# Final report
with pd.ExcelWriter('FINAL_REPORT.xlsx') as writer:
    df.to_excel(writer, sheet_name='All Data', index=False)
    top_10_usa.to_excel(writer, sheet_name='USA Top 10', index=False)
    top_10_india.to_excel(writer, sheet_name='India Top 10', index=False)

print("=" * 100)
print("✅ ALL DONE! FILES CREATED:")
print("=" * 100)
print("\n   1. employee_data.csv - All 2,000 employees")
print("   2. USA_Top10.xlsx - Top 10 USA employees")
print("   3. India_Top10.xlsx - Top 10 India employees")
print("   4. USA_Top10_Chart.png - Visualization")
print("   5. FINAL_REPORT.xlsx - Complete report")
print()
print("🎉 Open the Excel files to see your data!")
print()
