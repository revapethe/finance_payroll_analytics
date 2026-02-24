"""
CLEAN PROFESSIONAL DASHBOARD - FIXED VERSION
=============================================

Simple, attractive, professional design.
Fixed: Removed expander arrow_down text issue
Clean dark theme with blue accents.

Run: streamlit run clean_professional_dashboard.py

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

# Clean Professional CSS
st.markdown("""
<style>
    /* Dark Professional Background */
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
    
    /* Text */
    .stApp, .stMarkdown, p, span, div, label {
        color: #e8e8e8 !important;
    }
    
    /* Headers */
    h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 500 !important;
        border-bottom: 2px solid #4a90e2 !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 500 !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #e8e8e8 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #242424 !important;
        border-left: 3px solid #4a90e2 !important;
        padding: 1.2rem !important;
        border-radius: 4px !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #b0b0b0 !important;
        font-size: 0.85rem !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 500 !important;
    }
    
    /* Input Fields */
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
    
    /* Buttons */
    .stButton button {
        background-color: #4a90e2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .stButton button:hover {
        background-color: #357abd !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid #404040;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        color: #b0b0b0;
        padding: 0.7rem 1.2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4a90e2;
        color: #ffffff;
    }
    
    /* Expander - FIXED */
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
    
    /* Hide the arrow icon text */
    .streamlit-expanderHeader svg {
        fill: #4a90e2 !important;
    }
    
    /* DataFrame */
    .stDataFrame {
        background-color: #242424;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    
    /* Download Buttons */
    .stDownloadButton button {
        background-color: #2a2a2a !important;
        border: 1px solid #4a90e2 !important;
        color: #ffffff !important;
        border-radius: 4px !important;
    }
    
    .stDownloadButton button:hover {
        background-color: #4a90e2 !important;
    }
    
    /* Messages */
    .stSuccess {
        background-color: #1f3a1f !important;
        border-left: 3px solid #4caf50 !important;
        border-radius: 4px !important;
    }
    
    .stInfo {
        background-color: #1f2a3a !important;
        border-left: 3px solid #4a90e2 !important;
        border-radius: 4px !important;
    }
    
    .stWarning {
        background-color: #3a301f !important;
        border-left: 3px solid #ff9800 !important;
        border-radius: 4px !important;
    }
    
    /* Divider */
    hr {
        border-color: #404040 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Filter badges */
    .filter-badge {
        display: inline-block;
        background-color: #2a2a2a;
        color: #4a90e2;
        padding: 0.4rem 0.9rem;
        border-radius: 3px;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid #404040;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

@st.cache_data
def load_data():
    """Load employee data"""
    
    for db in ['employees.db', 'employees_complete.db', 'employee_database.db']:
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
    """AI search function"""
    
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
    
    # Job
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
    
    # Sort and limit
    filtered = filtered.sort_values('annual_salary_usd', ascending=False)
    
    top_match = re.search(r'top\s+(\d+)', q)
    if top_match:
        n = int(top_match.group(1))
        filtered = filtered.head(n)
        filters.append(f'Top {n}')
    elif 'top' in q:
        filtered = filtered.head(10)
        filters.append('Top 10')
    
    return filtered, filters

def main():
    # Load data
    df = load_data()
    
    if df is None:
        st.error("No employee data found. Please ensure employee_data.csv exists.")
        st.stop()
    
    # Header
    st.markdown("# Employee Analytics Dashboard")
    st.markdown("AI-powered employee search and intelligence")
    
    st.markdown("---")
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    usa_df = df[df['country'] == 'United States']
    india_df = df[df['country'] == 'India']
    
    with col1:
        st.metric("Total Employees", f"{len(df):,}", "Global workforce")
    with col2:
        st.metric("USA", f"{len(usa_df):,}", f"${usa_df['annual_salary_usd'].mean()/1000:.0f}K avg")
    with col3:
        st.metric("India", f"{len(india_df):,}", f"${india_df['annual_salary_usd'].mean()/1000:.0f}K avg")
    with col4:
        st.metric("Avg Salary", f"${df['annual_salary_usd'].mean()/1000:.0f}K", "All employees")
    with col5:
        st.metric("Total Payroll", f"${df['annual_salary_usd'].sum()/1e6:.1f}M", "Annual")
    
    st.markdown("")
    
    # Search section
    st.markdown("## Search")
    
    # Quick filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("Top 10 USA", use_container_width=True):
            st.session_state.sq = "Top 10 in USA"
    with col2:
        if st.button("Top 10 India", use_container_width=True):
            st.session_state.sq = "Top 10 in India"
    with col3:
        if st.button("Managers", use_container_width=True):
            st.session_state.sq = "All managers"
    with col4:
        if st.button("Engineers", use_container_width=True):
            st.session_state.sq = "All engineers"
    with col5:
        if st.button("Over 150K", use_container_width=True):
            st.session_state.sq = "Over 150k"
    with col6:
        if st.button("Engineering", use_container_width=True):
            st.session_state.sq = "Engineering department"
    
    st.markdown("")
    
    # Search input
    search_query = st.text_input(
        "Enter search query",
        value=st.session_state.get('sq', ''),
        placeholder="e.g., Engineering Managers in USA earning over 180k"
    )
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        search_btn = st.button("Search", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.sq = ''
            st.rerun()
    
    st.markdown("---")
    
    # Perform search
    if search_btn and search_query:
        
        results, filters = search_employees(df, search_query)
        
        st.session_state.search_history.append({
            'query': search_query,
            'count': len(results)
        })
        
        if len(results) > 0:
            
            # Show filters
            if filters:
                st.markdown("**Filters:** " + " · ".join([f'<span class="filter-badge">{f}</span>' for f in filters]), 
                           unsafe_allow_html=True)
            
            st.success(f"Found {len(results):,} employees")
            
            st.markdown("")
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Results", "📊 Stats", "📈 Charts", "💾 Export"])
            
            with tab1:
                st.markdown(f"### Results ({len(results):,} employees)")
                
                # Show results in a clean table format first
                display_df = results.head(20)[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['ID', 'Job Title', 'Department', 'City', 'Country', 'Salary']
                
                st.dataframe(display_df, use_container_width=True, height=600)
                
                if len(results) > 20:
                    st.info(f"Showing first 20 of {len(results):,} results. Export tab has all data.")
                
                st.markdown("")
                
                # Detailed view - simple markdown instead of expanders
                st.markdown("### Top 10 Detailed View")
                
                for idx, (_, emp) in enumerate(results.head(10).iterrows(), 1):
                    st.markdown(f"""
**{idx}. {emp.get('employee_id', 'N/A')} - {emp.get('job_title', 'N/A')}**
- **Name:** {emp.get('first_name', emp.get('name', 'N/A'))} {emp.get('last_name', '')}
- **Department:** {emp.get('department', 'N/A')} | **Location:** {emp.get('city', 'N/A')}, {emp.get('country', 'N/A')}
- **Salary:** ${emp.get('annual_salary_usd', 0):,.2f} | **Performance:** {emp.get('performance', emp.get('performance_rating', 'N/A'))}
                    """)
                    st.markdown("---")
            
            with tab2:
                st.markdown("### Statistics")
                
                # Summary stats
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
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Min Salary", f"${results['annual_salary_usd'].min():,.0f}")
                with col2:
                    st.metric("Max Salary", f"${results['annual_salary_usd'].max():,.0f}")
                with col3:
                    st.metric("Range", f"${results['annual_salary_usd'].max() - results['annual_salary_usd'].min():,.0f}")
                
                st.markdown("---")
                
                # Breakdowns
                col1, col2 = st.columns(2)
                
                with col1:
                    if len(results['country'].unique()) > 1:
                        st.markdown("**By Country**")
                        country_stats = results.groupby('country').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).round(0)
                        country_stats.columns = ['Employees', 'Avg Salary']
                        st.dataframe(country_stats, use_container_width=True)
                
                with col2:
                    st.markdown("**By Department**")
                    dept_stats = results.groupby('department').agg({
                        'employee_id': 'count',
                        'annual_salary_usd': 'mean'
                    }).round(0)
                    dept_stats.columns = ['Employees', 'Avg Salary']
                    st.dataframe(dept_stats, use_container_width=True)
            
            with tab3:
                st.markdown("### Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Bar chart
                    top_10 = results.nlargest(10, 'annual_salary_usd')
                    
                    fig1 = go.Figure(data=[
                        go.Bar(
                            y=top_10['employee_id'],
                            x=top_10['annual_salary_usd'],
                            orientation='h',
                            marker=dict(color='#4a90e2'),
                            text=top_10['annual_salary_usd'].apply(lambda x: f'${x:,.0f}'),
                            textposition='outside'
                        )
                    ])
                    
                    fig1.update_layout(
                        title="Top 10 by Salary",
                        plot_bgcolor='#1a1a1a',
                        paper_bgcolor='#1a1a1a',
                        font=dict(color='#ffffff'),
                        height=400,
                        showlegend=False,
                        xaxis=dict(showgrid=True, gridcolor='#333333', color='#ffffff'),
                        yaxis=dict(showgrid=False, color='#ffffff')
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Box plot
                    fig2 = go.Figure()
                    
                    for country in results['country'].unique():
                        data = results[results['country'] == country]
                        fig2.add_trace(go.Box(
                            y=data['annual_salary_usd'],
                            name=country,
                            marker=dict(color='#4a90e2')
                        ))
                    
                    fig2.update_layout(
                        title="Salary Distribution",
                        plot_bgcolor='#1a1a1a',
                        paper_bgcolor='#1a1a1a',
                        font=dict(color='#ffffff'),
                        height=400,
                        yaxis=dict(showgrid=True, gridcolor='#333333', color='#ffffff'),
                        xaxis=dict(color='#ffffff')
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
            
            with tab4:
                st.markdown("### Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Excel Export (with summary)**")
                    
                    from io import BytesIO
                    buffer = BytesIO()
                    
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        results.to_excel(writer, sheet_name='Results', index=False)
                        
                        summary = pd.DataFrame({
                            'Metric': ['Query', 'Results', 'Avg Salary', 'Total', 'Date'],
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
                    st.markdown("**CSV Export (raw data)**")
                    
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.markdown("")
                st.info(f"Search: '{search_query}' | {len(results):,} employees | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        else:
            st.warning("No results found. Try a different search.")
    
    # Footer
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Total Employees:** {len(df):,}")
    with col2:
        if st.session_state.search_history:
            st.markdown(f"**Searches Performed:** {len(st.session_state.search_history)}")

if __name__ == "__main__":
    main()
