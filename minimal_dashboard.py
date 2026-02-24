"""
MINIMAL PROFESSIONAL DASHBOARD - BLACK THEME
=============================================

Clean, simple, professional design.
- Pure black theme
- Square corners (no rounded edges)
- No animations or effects
- Simple, readable text
- Focus on data and functionality

Run: streamlit run minimal_dashboard.py

Author: Analytics Team
Date: January 2026
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime
import os
import re

st.set_page_config(
    page_title="Employee Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal Black Theme CSS
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #000000;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .main .block-container {
        padding: 2rem;
        max-width: 1600px;
    }
    
    /* All text white */
    .stApp, .stMarkdown, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Headers - Simple and clean */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 400 !important;
        font-family: Arial, sans-serif !important;
    }
    
    h1 {
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.2rem !important;
    }
    
    /* Metric Cards - Black with white border, square */
    div[data-testid="metric-container"] {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        padding: 1rem !important;
        box-shadow: none !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #ffffff !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        text-transform: none !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 400 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }
    
    /* Input Fields - Square, simple */
    .stTextInput input {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus {
        border: 2px solid #ffffff !important;
        box-shadow: none !important;
    }
    
    .stTextInput input::placeholder {
        color: #999999 !important;
    }
    
    /* Buttons - Square, simple */
    .stButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        text-transform: none !important;
        box-shadow: none !important;
    }
    
    .stButton button:hover {
        background-color: #cccccc !important;
        color: #000000 !important;
    }
    
    /* Tabs - Square */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #000000;
        border-bottom: 1px solid #ffffff;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #000000;
        border: none;
        border-radius: 0px;
        color: #999999;
        padding: 0.75rem 1.5rem;
        font-weight: 400;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #000000;
        color: #ffffff;
        border-bottom: 2px solid #ffffff;
    }
    
    /* Expander - Square */
    .streamlit-expanderHeader {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        color: #ffffff !important;
    }
    
    .streamlit-expanderContent {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-top: none !important;
        border-radius: 0px !important;
    }
    
    /* DataFrame */
    .stDataFrame {
        background-color: #000000;
        border: 1px solid #ffffff;
        border-radius: 0px;
    }
    
    .stDataFrame table {
        color: #ffffff !important;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        color: #ffffff !important;
        border-radius: 0px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 400 !important;
    }
    
    .stDownloadButton button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #000000;
        border: 1px solid #ffffff;
        border-radius: 0px;
        color: #ffffff;
    }
    
    /* Success/Info/Warning - Simple */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        color: #ffffff !important;
    }
    
    /* Divider */
    hr {
        border-color: #ffffff;
        margin: 2rem 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

@st.cache_data
def load_data():
    """Load employee data"""
    
    for db in ['employees.db', 'employees_complete.db', 'employee_database.db', 'employees_full_database.db']:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                df = pd.read_sql_query("SELECT * FROM employees", conn)
                conn.close()
                return df
            except:
                continue
    
    if os.path.exists('employee_data.csv'):
        return pd.read_csv('employee_data.csv')
    
    return None

def search_employees(df, query):
    """Search function with filters"""
    
    q = query.lower()
    filtered = df.copy()
    filters = []
    
    # Country
    if 'usa' in q or 'united states' in q:
        filtered = filtered[filtered['country'] == 'United States']
        filters.append('USA')
    elif 'india' in q:
        filtered = filtered[filtered['country'] == 'India']
        filters.append('India')
    
    # Department
    for dept in ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance', 'Product']:
        if dept.lower() in q:
            filtered = filtered[filtered['department'] == dept]
            filters.append(dept)
            break
    
    # Job title
    if 'manager' in q:
        filtered = filtered[filtered['job_title'].str.contains('Manager', case=False, na=False)]
        filters.append('Manager')
    if 'engineer' in q:
        filtered = filtered[filtered['job_title'].str.contains('Engineer', case=False, na=False)]
        filters.append('Engineer')
    if 'director' in q:
        filtered = filtered[filtered['job_title'].str.contains('Director', case=False, na=False)]
        filters.append('Director')
    if 'senior' in q:
        filtered = filtered[filtered['job_title'].str.contains('Senior', case=False, na=False)]
        filters.append('Senior')
    
    # Salary
    over_match = re.search(r'over\s+(\d+)k?', q)
    if over_match:
        amount = int(over_match.group(1)) * 1000
        filtered = filtered[filtered['annual_salary_usd'] > amount]
        filters.append(f'>${amount:,}')
    
    under_match = re.search(r'under\s+(\d+)k?', q)
    if under_match:
        amount = int(under_match.group(1)) * 1000
        filtered = filtered[filtered['annual_salary_usd'] < amount]
        filters.append(f'<${amount:,}')
    
    between_match = re.search(r'between\s+(\d+)k?\s+and\s+(\d+)k?', q)
    if between_match:
        min_amt = int(between_match.group(1)) * 1000
        max_amt = int(between_match.group(2)) * 1000
        filtered = filtered[(filtered['annual_salary_usd'] >= min_amt) & (filtered['annual_salary_usd'] <= max_amt)]
        filters.append(f'${min_amt:,}-${max_amt:,}')
    
    # Cities
    cities = {'san francisco': 'San Francisco', 'bangalore': 'Bangalore', 'new york': 'New York',
              'mumbai': 'Mumbai', 'seattle': 'Seattle', 'hyderabad': 'Hyderabad'}
    for key, city in cities.items():
        if key in q:
            filtered = filtered[filtered['city'] == city]
            filters.append(city)
            break
    
    # Sort
    filtered = filtered.sort_values('annual_salary_usd', ascending=False)
    
    # Limit
    top_match = re.search(r'top\s+(\d+)', q)
    if top_match:
        n = int(top_match.group(1))
        filtered = filtered.head(n)
        filters.append(f'Top {n}')
    elif 'top' in q:
        filtered = filtered.head(10)
        filters.append('Top 10')
    elif len(filtered) > 50:
        filtered = filtered.head(50)
    
    return filtered, filters

def main():
    # Load data
    df = load_data()
    
    if df is None:
        st.error("No employee data found. Please ensure employee_data.csv exists.")
        st.stop()
    
    # Header
    st.markdown("# Employee Analytics Platform")
    st.markdown("AI-Powered Employee Search and Intelligence")
    st.markdown("---")
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    usa_df = df[df['country'] == 'United States']
    india_df = df[df['country'] == 'India']
    
    with col1:
        st.metric("Total Employees", f"{len(df):,}")
    with col2:
        st.metric("USA Employees", f"{len(usa_df):,}")
    with col3:
        st.metric("India Employees", f"{len(india_df):,}")
    with col4:
        st.metric("Average Salary", f"${df['annual_salary_usd'].mean():,.0f}")
    with col5:
        st.metric("Total Payroll", f"${df['annual_salary_usd'].sum()/1e6:.1f}M")
    
    st.markdown("---")
    
    # Search Section
    st.markdown("## Search Employees")
    
    # Quick filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("USA Top 10", use_container_width=True):
            st.session_state.search_query = "Top 10 in USA"
    with col2:
        if st.button("India Top 10", use_container_width=True):
            st.session_state.search_query = "Top 10 in India"
    with col3:
        if st.button("Managers", use_container_width=True):
            st.session_state.search_query = "All managers"
    with col4:
        if st.button("Engineers", use_container_width=True):
            st.session_state.search_query = "All engineers"
    with col5:
        if st.button("Over 150K", use_container_width=True):
            st.session_state.search_query = "Over 150k"
    with col6:
        if st.button("Engineering", use_container_width=True):
            st.session_state.search_query = "Engineering department"
    
    st.markdown("")
    
    # Search input
    search_query = st.text_input(
        "Enter search query",
        value=st.session_state.get('search_query', ''),
        placeholder="Example: Engineering Managers in USA earning over 180k"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_button = st.button("Search", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.search_query = ''
            st.rerun()
    
    st.markdown("---")
    
    # Perform search
    if search_button and search_query:
        
        results, filters = search_employees(df, search_query)
        
        st.session_state.search_history.append({
            'query': search_query,
            'count': len(results),
            'time': datetime.now()
        })
        
        if len(results) > 0:
            
            # Results header
            st.markdown(f"## Search Results: {len(results):,} employees found")
            
            if filters:
                st.markdown(f"**Filters Applied:** {' | '.join(filters)}")
            
            st.markdown("")
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Results", "Statistics", "Charts", "Export"])
            
            with tab1:
                # Results table
                st.markdown("### Employee List")
                
                # Show as expandable rows
                for idx, (_, emp) in enumerate(results.head(30).iterrows(), 1):
                    with st.expander(f"{idx}. {emp.get('employee_id', 'N/A')} - {emp.get('job_title', 'N/A')} - ${emp.get('annual_salary_usd', 0):,.0f}"):
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Employee Information**")
                            st.write(f"ID: {emp.get('employee_id', 'N/A')}")
                            st.write(f"Name: {emp.get('first_name', emp.get('name', 'N/A'))} {emp.get('last_name', '')}")
                            st.write(f"Email: {emp.get('email', 'N/A')}")
                        
                        with col2:
                            st.markdown("**Job Details**")
                            st.write(f"Title: {emp.get('job_title', 'N/A')}")
                            st.write(f"Department: {emp.get('department', 'N/A')}")
                            st.write(f"Performance: {emp.get('performance', emp.get('performance_rating', 'N/A'))}")
                        
                        with col3:
                            st.markdown("**Location & Compensation**")
                            st.write(f"City: {emp.get('city', 'N/A')}")
                            st.write(f"Country: {emp.get('country', 'N/A')}")
                            st.write(f"Salary: ${emp.get('annual_salary_usd', 0):,.2f}")
                            st.write(f"Work Mode: {emp.get('remote_status', 'N/A')}")
                
                if len(results) > 30:
                    st.info(f"Showing first 30 of {len(results):,} results. Use Export tab for all data.")
            
            with tab2:
                # Statistics
                st.markdown("### Summary Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Count", f"{len(results):,}")
                with col2:
                    st.metric("Average", f"${results['annual_salary_usd'].mean():,.0f}")
                with col3:
                    st.metric("Median", f"${results['annual_salary_usd'].median():,.0f}")
                with col4:
                    st.metric("Total", f"${results['annual_salary_usd'].sum()/1e6:.2f}M")
                
                st.markdown("")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Minimum", f"${results['annual_salary_usd'].min():,.0f}")
                with col2:
                    st.metric("Maximum", f"${results['annual_salary_usd'].max():,.0f}")
                with col3:
                    st.metric("Range", f"${results['annual_salary_usd'].max() - results['annual_salary_usd'].min():,.0f}")
                with col4:
                    st.metric("Std Dev", f"${results['annual_salary_usd'].std():,.0f}")
                
                st.markdown("---")
                
                # Breakdowns
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'country' in results.columns and len(results['country'].unique()) > 1:
                        st.markdown("**By Country**")
                        country_stats = results.groupby('country').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).round(0)
                        country_stats.columns = ['Count', 'Avg Salary']
                        st.dataframe(country_stats, use_container_width=True)
                
                with col2:
                    if 'department' in results.columns:
                        st.markdown("**By Department**")
                        dept_stats = results.groupby('department').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).round(0).sort_values('Avg Salary', ascending=False)
                        dept_stats.columns = ['Count', 'Avg Salary']
                        st.dataframe(dept_stats, use_container_width=True)
            
            with tab3:
                # Charts
                st.markdown("### Data Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top 10 bar chart - simple black theme
                    top_10 = results.nlargest(10, 'annual_salary_usd')
                    
                    fig1 = go.Figure(data=[
                        go.Bar(
                            y=top_10['employee_id'],
                            x=top_10['annual_salary_usd'],
                            orientation='h',
                            marker=dict(color='#ffffff', line=dict(color='#000000', width=0)),
                            text=top_10['annual_salary_usd'].apply(lambda x: f'${x:,.0f}'),
                            textposition='outside'
                        )
                    ])
                    
                    fig1.update_layout(
                        title="Top 10 by Salary",
                        plot_bgcolor='#000000',
                        paper_bgcolor='#000000',
                        font=dict(color='#ffffff', family='Arial'),
                        height=450,
                        xaxis=dict(
                            showgrid=True,
                            gridcolor='#333333',
                            color='#ffffff'
                        ),
                        yaxis=dict(
                            showgrid=False,
                            color='#ffffff'
                        ),
                        margin=dict(l=100, r=100, t=40, b=40)
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Salary distribution box plot
                    fig2 = go.Figure()
                    
                    for country in results['country'].unique():
                        country_data = results[results['country'] == country]
                        fig2.add_trace(go.Box(
                            y=country_data['annual_salary_usd'],
                            name=country,
                            marker=dict(color='#ffffff'),
                            line=dict(color='#ffffff')
                        ))
                    
                    fig2.update_layout(
                        title="Salary Distribution by Country",
                        plot_bgcolor='#000000',
                        paper_bgcolor='#000000',
                        font=dict(color='#ffffff', family='Arial'),
                        height=450,
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='#333333',
                            color='#ffffff'
                        ),
                        xaxis=dict(color='#ffffff'),
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Department distribution
                if 'department' in results.columns and len(results['department'].unique()) > 1:
                    dept_counts = results['department'].value_counts()
                    
                    fig3 = go.Figure(data=[
                        go.Bar(
                            x=dept_counts.index,
                            y=dept_counts.values,
                            marker=dict(color='#ffffff', line=dict(color='#000000', width=0)),
                            text=dept_counts.values,
                            textposition='outside'
                        )
                    ])
                    
                    fig3.update_layout(
                        title="Employee Count by Department",
                        plot_bgcolor='#000000',
                        paper_bgcolor='#000000',
                        font=dict(color='#ffffff', family='Arial'),
                        height=400,
                        xaxis=dict(
                            showgrid=False,
                            color='#ffffff'
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='#333333',
                            color='#ffffff'
                        ),
                        margin=dict(l=40, r=40, t=40, b=80)
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True)
            
            with tab4:
                # Export
                st.markdown("### Export Data")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Excel Export**")
                    st.markdown("Multi-sheet workbook with results and summary")
                    
                    from io import BytesIO
                    buffer = BytesIO()
                    
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        results.to_excel(writer, sheet_name='Results', index=False)
                        
                        summary = pd.DataFrame({
                            'Metric': ['Query', 'Results', 'Avg Salary', 'Total Payroll', 'Date'],
                            'Value': [
                                search_query,
                                len(results),
                                f"${results['annual_salary_usd'].mean():,.2f}",
                                f"${results['annual_salary_usd'].sum():,.2f}",
                                datetime.now().strftime('%Y-%m-%d %H:%M')
                            ]
                        })
                        summary.to_excel(writer, sheet_name='Summary', index=False)
                    
                    st.download_button(
                        label="Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with col2:
                    st.markdown("**CSV Export**")
                    st.markdown("Raw data for analysis")
                    
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col3:
                    st.markdown("**Full Dataset**")
                    st.markdown("All employees")
                    
                    full_csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download All",
                        data=full_csv,
                        file_name=f"all_employees_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        else:
            st.warning("No results found. Try a different search.")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Data Source:** employee_data.csv")
    with col2:
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    with col3:
        if st.session_state.search_history:
            st.markdown(f"**Searches:** {len(st.session_state.search_history)}")

if __name__ == "__main__":
    main()
