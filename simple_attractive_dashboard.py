"""
SIMPLE & ATTRACTIVE PROFESSIONAL DASHBOARD
===========================================

Clean, simple design with subtle professional touches:
- Dark charcoal theme (not pure black)
- Subtle accent colors
- Clean typography
- Minimal but intentional design
- Professional without being boring

Run: streamlit run simple_attractive_dashboard.py

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

# Simple but Attractive CSS
st.markdown("""
<style>
    /* Clean dark background */
    .stApp {
        background-color: #1a1a1a;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Container */
    .main .block-container {
        padding: 2rem;
        max-width: 1600px;
    }
    
    /* Text - Clean and readable */
    .stApp, .stMarkdown, p, span, div, label {
        color: #e8e8e8 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Headers - Simple with subtle accent */
    h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.3rem !important;
        border-bottom: 2px solid #4a90e2 !important;
        padding-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 500 !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #e8e8e8 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
    
    /* Metric Cards - Clean with subtle accent */
    div[data-testid="metric-container"] {
        background-color: #242424 !important;
        border-left: 3px solid #4a90e2 !important;
        padding: 1.2rem !important;
        border-radius: 4px !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #b0b0b0 !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #4a90e2 !important;
        font-size: 0.85rem !important;
    }
    
    /* Input - Clean design */
    .stTextInput input {
        background-color: #242424 !important;
        border: 1px solid #404040 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput input:focus {
        border: 1px solid #4a90e2 !important;
        box-shadow: 0 0 0 1px #4a90e2 !important;
    }
    
    .stTextInput input::placeholder {
        color: #808080 !important;
    }
    
    /* Buttons - Simple with accent color */
    .stButton button {
        background-color: #4a90e2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    .stButton button:hover {
        background-color: #357abd !important;
    }
    
    .stButton button[kind="secondary"] {
        background-color: #333333 !important;
        border: 1px solid #555555 !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background-color: #404040 !important;
    }
    
    /* Tabs - Clean */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
        border-bottom: 1px solid #404040;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-radius: 4px 4px 0 0;
        color: #b0b0b0;
        padding: 0.7rem 1.2rem;
        font-weight: 400;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2a2a2a;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4a90e2;
        color: #ffffff;
        font-weight: 500;
    }
    
    /* Expander - Clean */
    .streamlit-expanderHeader {
        background-color: #242424 !important;
        border: 1px solid #404040 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
        padding: 0.8rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #2a2a2a !important;
        border-color: #4a90e2 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1f1f1f !important;
        border: 1px solid #404040 !important;
        border-top: none !important;
        border-radius: 0 0 4px 4px !important;
        padding: 1rem !important;
    }
    
    /* DataFrame - Clean */
    .stDataFrame {
        background-color: #242424;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        color: #ffffff !important;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background-color: #2a2a2a !important;
        border: 1px solid #4a90e2 !important;
        color: #ffffff !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.5rem !important;
    }
    
    .stDownloadButton button:hover {
        background-color: #4a90e2 !important;
        border-color: #4a90e2 !important;
    }
    
    /* Messages - Clean */
    .stSuccess {
        background-color: #1f3a1f !important;
        border-left: 3px solid #4caf50 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: #1f2a3a !important;
        border-left: 3px solid #4a90e2 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: #3a301f !important;
        border-left: 3px solid #ff9800 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: #3a1f1f !important;
        border-left: 3px solid #f44336 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }
    
    /* Divider */
    hr {
        border-color: #404040 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Subtle highlight for important elements */
    .highlight-box {
        background-color: #242424;
        border: 1px solid #4a90e2;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Info badge */
    .info-badge {
        display: inline-block;
        background-color: #333333;
        color: #4a90e2;
        padding: 0.3rem 0.8rem;
        border-radius: 3px;
        font-size: 0.85rem;
        margin: 0.2rem;
        border: 1px solid #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

@st.cache_data
def load_data():
    """Load employee data from database or CSV"""
    
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
    """AI-powered search"""
    
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
    
    # Job keywords
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
        filters.append(f'Over ${amount:,}')
    
    under_match = re.search(r'under\s+(\d+)k?', q)
    if under_match:
        amount = int(under_match.group(1)) * 1000
        filtered = filtered[filtered['annual_salary_usd'] < amount]
        filters.append(f'Under ${amount:,}')
    
    between_match = re.search(r'between\s+(\d+)k?\s+and\s+(\d+)k?', q)
    if between_match:
        min_amt = int(between_match.group(1)) * 1000
        max_amt = int(between_match.group(2)) * 1000
        filtered = filtered[(filtered['annual_salary_usd'] >= min_amt) & (filtered['annual_salary_usd'] <= max_amt)]
        filters.append(f'${min_amt:,} - ${max_amt:,}')
    
    # Cities
    cities = {'san francisco': 'San Francisco', 'bangalore': 'Bangalore', 'new york': 'New York',
              'mumbai': 'Mumbai', 'seattle': 'Seattle'}
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
        st.error("No employee data found. Please ensure employee_data.csv exists in this folder.")
        st.stop()
    
    # Header - Simple with subtle accent
    st.markdown("# Employee Analytics Dashboard")
    st.markdown("Search and analyze employee data using AI")
    
    st.markdown("---")
    
    # Top metrics - Clean layout
    col1, col2, col3, col4, col5 = st.columns(5)
    
    usa_df = df[df['country'] == 'United States']
    india_df = df[df['country'] == 'India']
    
    with col1:
        st.metric("Total Employees", f"{len(df):,}")
    with col2:
        st.metric("USA", f"{len(usa_df):,}")
    with col3:
        st.metric("India", f"{len(india_df):,}")
    with col4:
        st.metric("Average Salary", f"${df['annual_salary_usd'].mean()/1000:.0f}K")
    with col5:
        st.metric("Total Payroll", f"${df['annual_salary_usd'].sum()/1e6:.1f}M")
    
    st.markdown("")
    
    # Search section
    st.markdown("## Search Employees")
    
    # Quick search buttons - One row, clean
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("Top 10 USA", use_container_width=True):
            st.session_state.search_query = "Top 10 in USA"
    with col2:
        if st.button("Top 10 India", use_container_width=True):
            st.session_state.search_query = "Top 10 in India"
    with col3:
        if st.button("All Managers", use_container_width=True):
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
    
    # Search input - Clean and simple
    search_query = st.text_input(
        "Enter your search",
        value=st.session_state.get('search_query', ''),
        placeholder="Example: Engineering Managers in USA earning over 180k"
    )
    
    # Search controls
    col1, col2 = st.columns([5, 1])
    
    with col1:
        search_clicked = st.button("Search", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.search_query = ''
            st.rerun()
    
    # Example searches
    with st.expander("Show example searches"):
        st.markdown("""
        **Basic Searches:**
        - Top 10 in USA
        - All Engineering Managers
        - Employees over 150k
        
        **Location Searches:**
        - Engineers in San Francisco
        - Bangalore employees
        - All in New York
        
        **Combined Searches:**
        - Engineering Managers in USA over 180k
        - Senior developers in India
        - HR employees earning between 80k and 120k
        """)
    
    st.markdown("---")
    
    # Perform search
    if search_clicked and search_query:
        
        results, filters = search_employees(df, search_query)
        
        st.session_state.search_history.append({
            'query': search_query,
            'count': len(results),
            'time': datetime.now()
        })
        
        if len(results) > 0:
            
            # Show what AI found
            if filters:
                filter_text = " | ".join([f'<span class="info-badge">{f}</span>' for f in filters])
                st.markdown(f"**Filters Applied:** {filter_text}", unsafe_allow_html=True)
            
            st.success(f"Found {len(results):,} employees")
            
            st.markdown("")
            
            # Results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Results", "Statistics", "Charts", "Export"])
            
            with tab1:
                st.markdown(f"### Search Results ({len(results):,} employees)")
                
                # Display results
                for idx, (_, emp) in enumerate(results.head(25).iterrows(), 1):
                    with st.expander(f"{idx}. {emp.get('employee_id', 'N/A')} - {emp.get('job_title', 'N/A')} - ${emp.get('annual_salary_usd', 0):,.0f}"):
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Personal Info**")
                            st.write(f"Name: {emp.get('first_name', emp.get('name', 'N/A'))} {emp.get('last_name', '')}")
                            st.write(f"ID: {emp.get('employee_id', 'N/A')}")
                            st.write(f"Email: {emp.get('email', 'N/A')}")
                        
                        with col2:
                            st.markdown("**Job Details**")
                            st.write(f"Title: {emp.get('job_title', 'N/A')}")
                            st.write(f"Department: {emp.get('department', 'N/A')}")
                            st.write(f"Performance: {emp.get('performance', emp.get('performance_rating', 'N/A'))}")
                        
                        with col3:
                            st.markdown("**Location & Pay**")
                            st.write(f"City: {emp.get('city', 'N/A')}")
                            st.write(f"Country: {emp.get('country', 'N/A')}")
                            st.write(f"Salary: ${emp.get('annual_salary_usd', 0):,.2f}")
                
                if len(results) > 25:
                    st.info(f"Showing first 25 of {len(results):,} results. See Export tab for all data.")
            
            with tab2:
                st.markdown("### Summary Statistics")
                
                # Main stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Results", f"{len(results):,}")
                with col2:
                    st.metric("Average Salary", f"${results['annual_salary_usd'].mean():,.0f}")
                with col3:
                    st.metric("Median Salary", f"${results['annual_salary_usd'].median():,.0f}")
                with col4:
                    st.metric("Total Payroll", f"${results['annual_salary_usd'].sum()/1e6:.2f}M")
                
                st.markdown("")
                
                # Salary range
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Minimum", f"${results['annual_salary_usd'].min():,.0f}")
                with col2:
                    st.metric("Maximum", f"${results['annual_salary_usd'].max():,.0f}")
                with col3:
                    st.metric("Range", f"${results['annual_salary_usd'].max() - results['annual_salary_usd'].min():,.0f}")
                
                st.markdown("---")
                
                # Breakdowns
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'country' in results.columns and len(results['country'].unique()) > 1:
                        st.markdown("**Breakdown by Country**")
                        country_summary = results.groupby('country').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).round(0)
                        country_summary.columns = ['Count', 'Average Salary']
                        st.dataframe(country_summary, use_container_width=True)
                
                with col2:
                    if 'department' in results.columns:
                        st.markdown("**Breakdown by Department**")
                        dept_summary = results.groupby('department').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).round(0).sort_values('Average Salary', ascending=False)
                        dept_summary.columns = ['Count', 'Average Salary']
                        st.dataframe(dept_summary, use_container_width=True)
            
            with tab3:
                st.markdown("### Data Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Simple bar chart
                    top_15 = results.nlargest(15, 'annual_salary_usd')
                    
                    fig1 = go.Figure(data=[
                        go.Bar(
                            y=top_15['employee_id'],
                            x=top_15['annual_salary_usd'],
                            orientation='h',
                            marker=dict(color='#4a90e2'),
                            text=top_15['annual_salary_usd'].apply(lambda x: f'${x:,.0f}'),
                            textposition='outside'
                        )
                    ])
                    
                    fig1.update_layout(
                        title="Top 15 Employees by Salary",
                        plot_bgcolor='#1a1a1a',
                        paper_bgcolor='#1a1a1a',
                        font=dict(color='#ffffff', size=12),
                        height=500,
                        showlegend=False,
                        xaxis=dict(showgrid=True, gridcolor='#333333', color='#ffffff'),
                        yaxis=dict(showgrid=False, color='#ffffff')
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Simple box plot
                    fig2 = go.Figure()
                    
                    for country in results['country'].unique():
                        country_data = results[results['country'] == country]
                        fig2.add_trace(go.Box(
                            y=country_data['annual_salary_usd'],
                            name=country,
                            marker=dict(color='#4a90e2'),
                            line=dict(color='#4a90e2')
                        ))
                    
                    fig2.update_layout(
                        title="Salary Distribution by Country",
                        plot_bgcolor='#1a1a1a',
                        paper_bgcolor='#1a1a1a',
                        font=dict(color='#ffffff', size=12),
                        height=500,
                        yaxis=dict(showgrid=True, gridcolor='#333333', color='#ffffff'),
                        xaxis=dict(color='#ffffff')
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Department chart if applicable
                if 'department' in results.columns and len(results['department'].unique()) > 1:
                    dept_counts = results['department'].value_counts()
                    
                    fig3 = go.Figure(data=[
                        go.Bar(
                            x=dept_counts.index,
                            y=dept_counts.values,
                            marker=dict(color='#4a90e2'),
                            text=dept_counts.values,
                            textposition='outside'
                        )
                    ])
                    
                    fig3.update_layout(
                        title="Employees by Department",
                        plot_bgcolor='#1a1a1a',
                        paper_bgcolor='#1a1a1a',
                        font=dict(color='#ffffff', size=12),
                        height=400,
                        showlegend=False,
                        xaxis=dict(showgrid=False, color='#ffffff'),
                        yaxis=dict(showgrid=True, gridcolor='#333333', color='#ffffff')
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True)
            
            with tab4:
                st.markdown("### Export Data")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Excel Report**")
                    
                    from io import BytesIO
                    buffer = BytesIO()
                    
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        results.to_excel(writer, sheet_name='Results', index=False)
                        
                        summary = pd.DataFrame({
                            'Metric': ['Search Query', 'Total Results', 'Average Salary', 'Median Salary', 
                                      'Min Salary', 'Max Salary', 'Total Payroll', 'Search Date'],
                            'Value': [
                                search_query,
                                len(results),
                                f"${results['annual_salary_usd'].mean():,.2f}",
                                f"${results['annual_salary_usd'].median():,.2f}",
                                f"${results['annual_salary_usd'].min():,.2f}",
                                f"${results['annual_salary_usd'].max():,.2f}",
                                f"${results['annual_salary_usd'].sum():,.2f}",
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            ]
                        })
                        summary.to_excel(writer, sheet_name='Summary', index=False)
                    
                    st.download_button(
                        label="Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with col2:
                    st.markdown("**CSV Export**")
                    
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
                    
                    full_csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download All Data",
                        data=full_csv,
                        file_name=f"all_employees_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.markdown("")
                st.info(f"Search: '{search_query}' | {len(results):,} employees | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        else:
            st.warning("No results found. Try adjusting your search.")
    
    # Footer - Clean
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Agentic AI Search**")
    with col2:
        st.markdown(f"**Total Employees: {len(df):,}**")
    with col3:
        if st.session_state.search_history:
            st.markdown(f"**Searches: {len(st.session_state.search_history)}**")

if __name__ == "__main__":
    main()
