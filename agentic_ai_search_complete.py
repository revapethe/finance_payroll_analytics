"""
COMPLETE AGENTIC AI SEARCH SYSTEM
==================================

Advanced AI-powered search for employee dataset with:
- Natural language understanding
- Multiple search modes
- Intelligent filtering
- Auto-export capabilities
- Web interface option

Run: python agentic_ai_search_complete.py

Author: Analytics Team
Date: January 2026
"""

import pandas as pd
import sqlite3
import re
from datetime import datetime
import os
import sys

class AdvancedAgenticSearch:
    """
    Advanced Agentic AI Search System
    Can search anything in your employee dataset using natural language
    """
    
    def __init__(self):
        self.conn = None
        self.df = None
        self.data_source = None
        self.search_history = []
        self.total_employees = 0
        
        print("=" * 100)
        print("🤖 INITIALIZING AGENTIC AI SEARCH SYSTEM")
        print("=" * 100)
        print()
        
        self._load_data()
    
    def _load_data(self):
        """Load data from database or CSV"""
        
        print("Loading employee data...")
        
        # Option 1: Try SQLite database
        for db_file in ['employees.db', 'employees_complete.db', 'employees_full_database.db', 'employee_database.db']:
            if os.path.exists(db_file):
                try:
                    self.conn = sqlite3.connect(db_file)
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM employees")
                    self.total_employees = cursor.fetchone()[0]
                    print(f"✅ Connected to: {db_file}")
                    print(f"✅ Total employees: {self.total_employees:,}")
                    self.data_source = 'sqlite'
                    self.db_name = db_file
                    return
                except Exception as e:
                    continue
        
        # Option 2: Load from CSV
        if os.path.exists('employee_data.csv'):
            print("Loading from CSV...")
            self.df = pd.read_csv('employee_data.csv')
            self.total_employees = len(self.df)
            print(f"✅ Loaded CSV: {self.total_employees:,} employees")
            
            # Create temporary database for faster queries
            print("Creating temporary database for faster search...")
            self.conn = sqlite3.connect(':memory:')  # In-memory database
            self.df.to_sql('employees', self.conn, if_exists='replace', index=False)
            self.data_source = 'sqlite'
            self.db_name = 'In-Memory Database'
            print("✅ Temporary database created")
            return
        
        # No data found
        print("❌ NO DATA FOUND!")
        print()
        print("Please ensure you have:")
        print("  • employee_data.csv")
        print("  • OR run: python BEGINNER_COMPLETE_GUIDE.py")
        print()
        self.data_source = None
    
    def parse_query(self, query):
        """
        Advanced query parser - extracts intent and parameters
        """
        
        q = query.lower()
        filters = []
        params = {}
        
        # 1. EXTRACT COUNTRY
        if any(word in q for word in ['usa', 'united states', 'america', 'us ']):
            filters.append("country = 'United States'")
            params['country'] = 'USA'
        elif 'india' in q:
            filters.append("country = 'India'")
            params['country'] = 'India'
        
        # 2. EXTRACT DEPARTMENT
        departments = {
            'engineering': 'Engineering',
            'hr': 'HR',
            'human resources': 'HR',
            'sales': 'Sales',
            'marketing': 'Marketing',
            'finance': 'Finance',
            'product': 'Product',
            'operations': 'Operations'
        }
        for keyword, dept in departments.items():
            if keyword in q:
                filters.append(f"department = '{dept}'")
                params['department'] = dept
                break
        
        # 3. EXTRACT JOB TITLE KEYWORDS
        job_keywords = ['manager', 'engineer', 'director', 'analyst', 'developer', 
                       'senior', 'junior', 'lead', 'principal', 'staff']
        for keyword in job_keywords:
            if keyword in q:
                filters.append(f"job_title LIKE '%{keyword.title()}%'")
                params['job_keyword'] = keyword
                break
        
        # 4. EXTRACT CITY
        cities = {
            'san francisco': 'San Francisco', 'sf': 'San Francisco',
            'new york': 'New York', 'nyc': 'New York', 'ny': 'New York',
            'seattle': 'Seattle',
            'austin': 'Austin',
            'boston': 'Boston',
            'chicago': 'Chicago',
            'los angeles': 'Los Angeles', 'la': 'Los Angeles',
            'bangalore': 'Bangalore', 'bengaluru': 'Bangalore',
            'mumbai': 'Mumbai', 'bombay': 'Mumbai',
            'hyderabad': 'Hyderabad',
            'pune': 'Pune',
            'delhi': 'Delhi',
            'chennai': 'Chennai', 'madras': 'Chennai',
            'gurgaon': 'Gurgaon', 'gurugram': 'Gurgaon'
        }
        for keyword, city_name in cities.items():
            if keyword in q:
                filters.append(f"city = '{city_name}'")
                params['city'] = city_name
                break
        
        # 5. EXTRACT SALARY FILTERS
        # "over 150k", "above 150000", "more than 150k"
        over_patterns = [
            r'over\\s+(\\d+)k',
            r'above\\s+(\\d+)k',
            r'more than\\s+(\\d+)k',
            r'>\\s*(\\d+)k',
            r'greater than\\s+(\\d+)k'
        ]
        for pattern in over_patterns:
            match = re.search(pattern, q)
            if match:
                amount = int(match.group(1)) * 1000
                filters.append(f"annual_salary_usd > {amount}")
                params['salary_min'] = amount
                break
        
        # "under 100k", "below 100000", "less than 100k"
        under_patterns = [
            r'under\\s+(\\d+)k',
            r'below\\s+(\\d+)k',
            r'less than\\s+(\\d+)k',
            r'<\\s*(\\d+)k'
        ]
        for pattern in under_patterns:
            match = re.search(pattern, q)
            if match:
                amount = int(match.group(1)) * 1000
                filters.append(f"annual_salary_usd < {amount}")
                params['salary_max'] = amount
                break
        
        # "between 100k and 200k"
        between_match = re.search(r'between\\s+(\\d+)k?\\s+and\\s+(\\d+)k?', q)
        if between_match:
            min_amt = int(between_match.group(1)) * 1000
            max_amt = int(between_match.group(2)) * 1000
            filters.append(f"annual_salary_usd BETWEEN {min_amt} AND {max_amt}")
            params['salary_range'] = (min_amt, max_amt)
        
        # 6. EXTRACT PERFORMANCE
        if any(word in q for word in ['excellent', 'outstanding', 'top performer']):
            filters.append("(performance LIKE '%Excellent%' OR performance LIKE '%Outstanding%' OR performance_rating LIKE '%Excellent%' OR performance_rating LIKE '%Outstanding%')")
            params['performance'] = 'High'
        elif any(word in q for word in ['poor', 'needs improvement', 'low performer']):
            filters.append("(performance LIKE '%Needs Improvement%' OR performance_rating LIKE '%Needs Improvement%')")
            params['performance'] = 'Low'
        elif 'good' in q:
            filters.append("(performance = 'Good' OR performance_rating = 'Good')")
            params['performance'] = 'Good'
        
        # 7. EXTRACT REMOTE STATUS
        if 'remote' in q:
            if 'fully remote' in q:
                filters.append("remote_status = 'Fully Remote'")
                params['remote'] = 'Fully Remote'
            elif 'hybrid' in q:
                filters.append("remote_status = 'Hybrid'")
                params['remote'] = 'Hybrid'
            elif 'office' in q or 'on-site' in q:
                filters.append("remote_status = 'In-Office'")
                params['remote'] = 'In-Office'
        
        # 8. EXTRACT LIMIT (TOP N)
        limit = None
        top_patterns = [r'top\\s+(\\d+)', r'first\\s+(\\d+)', r'show\\s+(\\d+)']
        for pattern in top_patterns:
            match = re.search(pattern, q)
            if match:
                limit = int(match.group(1))
                params['limit'] = limit
                break
        
        if limit is None and 'top' in q:
            limit = 10
            params['limit'] = 10
        
        # 9. EXTRACT SORT ORDER
        order_by = "annual_salary_usd DESC"  # Default: highest salary first
        
        if any(word in q for word in ['lowest', 'cheapest', 'minimum']):
            order_by = "annual_salary_usd ASC"
        elif any(word in q for word in ['alphabetical', 'by name']):
            order_by = "employee_id ASC"
        elif 'recent' in q or 'newest' in q:
            order_by = "hire_date DESC"
        elif 'oldest' in q or 'longest' in q:
            order_by = "years_of_service DESC"
        
        return filters, params, limit, order_by
    
    def search(self, query):
        """
        Main search function - the AI brain!
        """
        
        if self.data_source is None:
            print("No data loaded. Cannot search.")
            return pd.DataFrame()
        
        # Parse the natural language query
        filters, params, limit, order_by = self.parse_query(query)
        
        # Build SQL query
        where_clause = " AND ".join(filters) if filters else "1=1"
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        sql_query = f"""
            SELECT * FROM employees
            WHERE {where_clause}
            ORDER BY {order_by}
            {limit_clause}
        """
        
        print(f"\\n{'='*100}")
        print(f"🔍 SEARCHING: '{query}'")
        print(f"{'='*100}\\n")
        
        # Show what the AI understood
        if params:
            print("🧠 AI UNDERSTOOD:")
            print("-" * 100)
            for key, value in params.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
            print()
        
        # Execute query
        try:
            results = pd.read_sql_query(sql_query, self.conn)
            
            # Record in history
            self.search_history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'query': query,
                'filters': params,
                'results_count': len(results),
                'sql': sql_query
            })
            
            # Display results
            self._display_results(results, query, params)
            
            return results
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print(f"\\nSQL Query: {sql_query}")
            print()
            return pd.DataFrame()
    
    def _display_results(self, results, query, params):
        """Display search results beautifully"""
        
        if len(results) == 0:
            print("❌ NO RESULTS FOUND")
            print()
            print("💡 SUGGESTIONS:")
            print("  • Try broader search terms")
            print("  • Check spelling")
            print("  • Remove some filters")
            print("  • Type 'help' for examples")
            return
        
        print(f"✅ FOUND {len(results):,} EMPLOYEES")
        print("=" * 100)
        print()
        
        # Determine how many to display
        display_count = min(len(results), 15)
        
        # Display results
        print("SEARCH RESULTS:")
        print("-" * 100)
        
        for i, (_, emp) in enumerate(results.head(display_count).iterrows(), 1):
            # Get employee data
            emp_id = str(emp.get('employee_id', 'N/A'))
            first_name = str(emp.get('first_name', emp.get('name', 'Unknown')))
            last_name = str(emp.get('last_name', ''))
            email = str(emp.get('email', 'N/A'))
            job_title = str(emp.get('job_title', 'N/A'))
            department = str(emp.get('department', 'N/A'))
            country = str(emp.get('country', 'N/A'))
            city = str(emp.get('city', 'N/A'))
            salary_usd = float(emp.get('annual_salary_usd', 0))
            performance = str(emp.get('performance', emp.get('performance_rating', 'N/A')))
            remote = str(emp.get('remote_status', 'N/A'))
            years = emp.get('years_of_service', 'N/A')
            
            # Format display
            full_name = f"{first_name} {last_name}".strip()
            
            print(f"{i:3d}. 🆔 {emp_id} - {full_name}")
            print(f"     💼 Job: {job_title}")
            print(f"     🏢 Department: {department}")
            print(f"     📍 Location: {city}, {country}")
            print(f"     💰 Salary: ${salary_usd:,.2f}")
            print(f"     ⭐ Performance: {performance} | 🏠 {remote}")
            if years != 'N/A':
                print(f"     📅 Years of Service: {years}")
            print(f"     📧 Email: {email}")
            print()
        
        if len(results) > display_count:
            print(f"{'='*100}")
            print(f"... and {len(results) - display_count:,} more employees")
            print(f"{'='*100}")
            print()
        
        # Summary Statistics
        print("=" * 100)
        print("📊 SUMMARY STATISTICS")
        print("=" * 100)
        print()
        
        print(f"Total Results: {len(results):,}")
        print(f"Average Salary: ${results['annual_salary_usd'].mean():,.2f}")
        print(f"Median Salary: ${results['annual_salary_usd'].median():,.2f}")
        print(f"Salary Range: ${results['annual_salary_usd'].min():,.2f} - ${results['annual_salary_usd'].max():,.2f}")
        print(f"Total Payroll: ${results['annual_salary_usd'].sum():,.2f}")
        print()
        
        # Breakdown by country
        if 'country' in results.columns and len(results['country'].unique()) > 1:
            print("By Country:")
            for country, count in results['country'].value_counts().items():
                avg_sal = results[results['country']==country]['annual_salary_usd'].mean()
                print(f"  {country}: {count} employees (avg ${avg_sal:,.2f})")
            print()
        
        # Breakdown by department
        if 'department' in results.columns and len(results['department'].unique()) > 1:
            print("By Department:")
            for dept, count in results['department'].value_counts().head(5).items():
                print(f"  {dept}: {count} employees")
            print()
        
        print("=" * 100)
        print()
        
        # Export option
        self._offer_export(results, query)
    
    def _offer_export(self, results, query):
        """Offer to export results"""
        
        print("💾 EXPORT OPTIONS:")
        print("-" * 100)
        print("  1. Export to Excel")
        print("  2. Export to CSV")
        print("  3. No export (continue searching)")
        print()
        
        choice = input("Choose (1/2/3): ").strip()
        
        if choice == '1':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"search_results_{timestamp}.xlsx"
            
            try:
                # Create comprehensive Excel with multiple sheets
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    # Sheet 1: All results
                    results.to_excel(writer, sheet_name='Search Results', index=False)
                    
                    # Sheet 2: Summary
                    summary_data = {
                        'Metric': [
                            'Search Query',
                            'Total Results',
                            'Average Salary',
                            'Median Salary',
                            'Min Salary',
                            'Max Salary',
                            'Total Payroll',
                            'Search Date'
                        ],
                        'Value': [
                            query,
                            len(results),
                            f"${results['annual_salary_usd'].mean():,.2f}",
                            f"${results['annual_salary_usd'].median():,.2f}",
                            f"${results['annual_salary_usd'].min():,.2f}",
                            f"${results['annual_salary_usd'].max():,.2f}",
                            f"${results['annual_salary_usd'].sum():,.2f}",
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                print(f"✅ Exported to: {filename}")
                print()
            except Exception as e:
                print(f"⚠️ Excel export failed: {e}")
                # Fallback to CSV
                csv_name = f"search_results_{timestamp}.csv"
                results.to_csv(csv_name, index=False)
                print(f"✅ Exported to CSV: {csv_name}")
                print()
        
        elif choice == '2':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"search_results_{timestamp}.csv"
            results.to_csv(filename, index=False)
            print(f"✅ Exported to: {filename}")
            print()
    
    def show_help(self):
        """Show help and examples"""
        
        print()
        print("=" * 100)
        print("📚 AGENTIC AI SEARCH - EXAMPLES & HELP")
        print("=" * 100)
        print()
        
        examples = {
            "BASIC SEARCHES": [
                "Find all employees",
                "Show me everyone in USA",
                "All India employees",
                "Engineering department",
                "HR team"
            ],
            "JOB TITLE SEARCHES": [
                "All managers",
                "Find engineers",
                "Show me directors",
                "Senior positions",
                "Junior developers",
                "Engineering Managers"
            ],
            "SALARY SEARCHES": [
                "Employees earning over 150k",
                "Show me salaries under 100k",
                "Between 100k and 200k",
                "Highest paid employees",
                "Lowest salaries"
            ],
            "LOCATION SEARCHES": [
                "All employees in San Francisco",
                "Bangalore team",
                "New York workers",
                "Everyone in Seattle"
            ],
            "COMBINED SEARCHES": [
                "Engineering Managers in USA earning over 180k",
                "Top 10 engineers in India",
                "HR employees in San Francisco over 100k",
                "Senior developers in Bangalore",
                "All remote workers in Engineering",
                "Excellent performers in Sales"
            ],
            "TOP N SEARCHES": [
                "Top 10 employees",
                "Top 5 in USA",
                "First 20 results",
                "Show me top 3 in each department"
            ],
            "SPECIAL SEARCHES": [
                "Remote workers",
                "Excellent performers",
                "Hybrid workers in Engineering",
                "All managers earning over 150k"
            ]
        }
        
        for category, queries in examples.items():
            print(f"{category}:")
            print("-" * 100)
            for q in queries:
                print(f"  • {q}")
            print()
    
    def show_history(self):
        """Show search history"""
        
        if not self.search_history:
            print("\\nNo search history yet.\\n")
            return
        
        print()
        print("=" * 100)
        print("📜 SEARCH HISTORY")
        print("=" * 100)
        print()
        
        for i, search in enumerate(self.search_history, 1):
            print(f"{i:2d}. [{search['timestamp']}] '{search['query']}'")
            print(f"    Results: {search['results_count']:,} employees")
            if search['filters']:
                print(f"    Filters: {', '.join(f'{k}={v}' for k,v in search['filters'].items())}")
            print()

def main():
    """Main program - Interactive search interface"""
    
    print("=" * 100)
    print("🤖 AGENTIC AI EMPLOYEE SEARCH SYSTEM")
    print("=" * 100)
    print()
    print("Search your employee dataset using NATURAL LANGUAGE!")
    print("No SQL required - just ask what you want to find.")
    print()
    
    # Initialize AI agent
    agent = AdvancedAgenticSearch()
    
    if agent.data_source is None:
        print("\\nPlease create employee data first:")
        print("  Run: python BEGINNER_COMPLETE_GUIDE.py")
        return
    
    print()
    print("=" * 100)
    print("🚀 SEARCH SYSTEM READY!")
    print("=" * 100)
    print()
    print("QUICK START EXAMPLES:")
    print("  • 'Top 10 in USA'")
    print("  • 'All Engineering Managers'")
    print("  • 'Employees over 150k'")
    print("  • 'Engineers in San Francisco'")
    print()
    print("COMMANDS:")
    print("  • Type 'help' - See all examples")
    print("  • Type 'history' - View search history")
    print("  • Type 'quit' - Exit")
    print()
    print("=" * 100)
    print()
    
    # Interactive search loop
    while True:
        try:
            query = input("🔍 SEARCH: ").strip()
            
            if not query:
                continue
            
            # Handle special commands
            if query.lower() in ['quit', 'exit', 'q']:
                print()
                print("=" * 100)
                print(f"✅ SESSION COMPLETE!")
                print(f"Total searches performed: {len(agent.search_history)}")
                print("=" * 100)
                break
            
            elif query.lower() in ['help', 'h', '?']:
                agent.show_help()
                continue
            
            elif query.lower() == 'history':
                agent.show_history()
                continue
            
            elif query.lower() == 'stats':
                print(f"\\nTotal employees in database: {agent.total_employees:,}")
                print(f"Searches performed: {len(agent.search_history)}")
                print(f"Database: {agent.db_name}\\n")
                continue
            
            # Execute search
            agent.search(query)
            
        except KeyboardInterrupt:
            print("\\n\\nExiting...\\n")
            break
        except Exception as e:
            print(f"\\nError: {e}\\n")

if __name__ == "__main__":
    main()
