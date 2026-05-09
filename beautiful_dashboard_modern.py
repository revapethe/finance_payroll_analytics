"""
BEAUTIFUL MODERN EMPLOYEE ANALYTICS DASHBOARD
==============================================

Stunning UI with:
- Distinctive typography (Playfair Display + Inter)
- Refined dark emerald theme
- Smooth animations
- Professional data visualizations
- Multi-agent AI integration

Run: streamlit run beautiful_dashboard_modern.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Employee Analytics",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stunning Custom CSS with refined aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Base Styles */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d1b2a 50%, #1b2838 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 100% !important;
    }
    
    /* Header Styling */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #f0f4f8 0%, #a5b8cf 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    h2 {
        font-family: 'Playfair Display', serif !important;
        color: #e8f0f8 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        color: #c5d3e3 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    /* Subtitle with animation */
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #8fa3b8;
        font-weight: 300;
        letter-spacing: 0.05em;
        margin-bottom: 3rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Metric Cards - Glassmorphism Effect */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #f0f4f8 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #8fa3b8 !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(100,150,200,0.2);
        border-color: rgba(165,184,207,0.3);
    }
    
    /* Search Section */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #f0f4f8 !important;
        font-size: 1rem !important;
        padding: 0.9rem 1.2rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(165,184,207,0.5) !important;
        box-shadow: 0 0 0 3px rgba(165,184,207,0.1) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b7f95 !important;
    }
    
    /* Buttons - Refined Style */
    .stButton > button {
        background: linear-gradient(135deg, #3d5a80 0%, #2c4259 100%) !important;
        color: #f0f4f8 !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(61,90,128,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4a6fa5 0%, #3d5a80 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(61,90,128,0.5) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5a7fa5 0%, #3d5a80 100%) !important;
        font-weight: 600 !important;
    }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.03);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8fa3b8;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.05);
        color: #c5d3e3;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(93,127,165,0.3) 0%, rgba(61,90,128,0.3) 100%) !important;
        color: #f0f4f8 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(93,127,165,0.1) !important;
        border-left: 4px solid #5d7fa5 !important;
        border-radius: 8px !important;
        color: #e8f0f8 !important;
    }
    
    /* Success boxes */
    [data-testid="stSuccess"] {
        background: rgba(76,175,80,0.1) !important;
        border-left: 4px solid #4caf50 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 8px !important;
        color: #c5d3e3 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.06) !important;
    }
    
    /* Accent line decoration */
    .accent-line {
        height: 3px;
        background: linear-gradient(90deg, #5d7fa5 0%, transparent 100%);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Custom card styling */
    .custom-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        border-color: rgba(165,184,207,0.3);
        box-shadow: 0 8px 32px rgba(93,127,165,0.2);
    }
    
    /* Agent message styling */
    .agent-message {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        border-left: 4px solid;
        background: rgba(255,255,255,0.03);
        font-family: 'Inter', sans-serif;
        animation: slideIn 0.4s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .analyst-message {
        border-left-color: #5d7fa5;
        background: linear-gradient(135deg, rgba(93,127,165,0.08) 0%, rgba(93,127,165,0.02) 100%);
    }
    
    .advisor-message {
        border-left-color: #4caf50;
        background: linear-gradient(135deg, rgba(76,175,80,0.08) 0%, rgba(76,175,80,0.02) 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth scroll */
    html {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load employee data"""
    for db in ['employees.db', 'employees_complete.db']:
        if os.path.exists(db):
            try:
                import sqlite3
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
    """Intelligent search function"""
    q = query.lower()
    filtered = df.copy()
    filters = []
    
    # Country filter
    if 'usa' in q or 'united states' in q:
        filtered = filtered[filtered['country'] == 'United States']
        filters.append('USA')
    elif 'india' in q:
        filtered = filtered[filtered['country'] == 'India']
        filters.append('India')
    
    # Department filter
    for dept in ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance', 'Product']:
        if dept.lower() in q:
            filtered = filtered[filtered['department'] == dept]
            filters.append(dept)
            break
    
    # Job title filter
    if 'manager' in q:
        filtered = filtered[filtered['job_title'].str.contains('Manager', case=False, na=False)]
        filters.append('Manager')
    if 'engineer' in q:
        filtered = filtered[filtered['job_title'].str.contains('Engineer', case=False, na=False)]
        filters.append('Engineer')
    if 'senior' in q:
        filtered = filtered[filtered['job_title'].str.contains('Senior', case=False, na=False)]
        filters.append('Senior')
    
    # Salary filters
    over_match = re.search(r'over\s+(\d+)k?', q)
    if over_match:
        amount = int(over_match.group(1)) * 1000
        filtered = filtered[filtered['annual_salary_usd'] > amount]
        filters.append(f'>${amount:,}')
    
    # Sort by salary
    filtered = filtered.sort_values('annual_salary_usd', ascending=False)
    
    # Limit results
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
    # Header with animation
    st.markdown("<h1>Employee Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-Powered Workforce Intelligence Platform</p>", unsafe_allow_html=True)
    
    # Decorative line
    st.markdown("<div class='accent-line'></div>", unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ No employee data found. Please ensure employee_data.csv exists.")
        st.stop()
    
    # Top metrics with glassmorphism
    col1, col2, col3, col4 = st.columns(4)
    
    usa_count = len(df[df['country'] == 'United States'])
    india_count = len(df[df['country'] == 'India'])
    avg_salary = df['annual_salary_usd'].mean()
    
    with col1:
        st.metric("Total Employees", f"{len(df):,}")
    with col2:
        st.metric("USA", f"{usa_count:,}")
    with col3:
        st.metric("India", f"{india_count:,}")
    with col4:
        st.metric("Average Salary", f"${avg_salary/1000:.0f}K")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Search section with refined design
    st.markdown("## Search Employees")
    
    # Quick action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🇺🇸 Top 10 USA", use_container_width=True):
            st.session_state.search_query = "Top 10 in USA"
    with col2:
        if st.button("🇮🇳 Top 10 India", use_container_width=True):
            st.session_state.search_query = "Top 10 in India"
    with col3:
        if st.button("👔 All Managers", use_container_width=True):
            st.session_state.search_query = "All managers"
    with col4:
        if st.button("💻 Engineers", use_container_width=True):
            st.session_state.search_query = "All engineers"
    with col5:
        if st.button("💰 Over 150K", use_container_width=True):
            st.session_state.search_query = "Over 150k"
    
    # Search input
    query = st.text_input(
        "Ask anything about employees:",
        value=st.session_state.get('search_query', ''),
        placeholder="e.g., Engineering Managers in USA earning over $180K",
        key="main_search"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.search_query = ""
            st.rerun()
    
    # Perform search
    if search_btn and query:
        st.markdown("<div class='accent-line'></div>", unsafe_allow_html=True)
        
        results, filters = search_employees(df, query)
        
        # Results header
        st.success(f"✨ Found {len(results)} employees")
        
        if filters:
            filter_text = " | ".join(filters)
            st.info(f"**Filters:** {filter_text}")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Results", "📊 Statistics", "📈 Charts", "💾 Export"])
        
        with tab1:
            if len(results) > 0:
                # Show table
                display_cols = ['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']
                display_df = results[display_cols].head(20).copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['ID', 'Job Title', 'Department', 'City', 'Country', 'Salary']
                
                st.dataframe(display_df, use_container_width=True, height=500)
                
                # Top 10 details
                st.markdown("### Top 10 Details")
                for idx, (_, emp) in enumerate(results.head(10).iterrows(), 1):
                    with st.expander(f"#{idx} - {emp['employee_id']} - {emp['job_title']} - ${emp['annual_salary_usd']:,.0f}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                            **Employee:** {emp.get('first_name', emp.get('name', 'N/A'))} {emp.get('last_name', '')}  
                            **Job:** {emp['job_title']}  
                            **Department:** {emp['department']}  
                            """)
                        with col2:
                            st.markdown(f"""
                            **Location:** {emp['city']}, {emp['country']}  
                            **Salary:** ${emp['annual_salary_usd']:,.2f}  
                            **Email:** {emp.get('email', 'N/A')}  
                            """)
            else:
                st.warning("No employees found matching your criteria.")
        
        with tab2:
            if len(results) > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Count", f"{len(results):,}")
                    st.metric("Average Salary", f"${results['annual_salary_usd'].mean():,.0f}")
                
                with col2:
                    st.metric("Median Salary", f"${results['annual_salary_usd'].median():,.0f}")
                    st.metric("Total Payroll", f"${results['annual_salary_usd'].sum()/1e6:.1f}M")
                
                with col3:
                    st.metric("Min Salary", f"${results['annual_salary_usd'].min():,.0f}")
                    st.metric("Max Salary", f"${results['annual_salary_usd'].max():,.0f}")
                
                # Breakdown by country
                if 'country' in results.columns and len(results['country'].unique()) > 1:
                    st.markdown("### Country Breakdown")
                    country_stats = results.groupby('country').agg({
                        'employee_id': 'count',
                        'annual_salary_usd': ['mean', 'sum']
                    }).round(0)
                    st.dataframe(country_stats, use_container_width=True)
        
        with tab3:
            if len(results) > 0:
                # Top 10 bar chart
                top10 = results.nlargest(10, 'annual_salary_usd')
                
                fig = go.Figure(data=[
                    go.Bar(
                        y=top10['employee_id'],
                        x=top10['annual_salary_usd'],
                        orientation='h',
                        marker=dict(
                            color=top10['annual_salary_usd'],
                            colorscale='Blues',
                            line=dict(color='rgba(165,184,207,0.3)', width=1)
                        ),
                        text=top10['annual_salary_usd'].apply(lambda x: f'${x:,.0f}'),
                        textposition='outside',
                        hovertemplate='<b>%{y}</b><br>Salary: $%{x:,.0f}<extra></extra>'
                    )
                ])
                
                fig.update_layout(
                    title=dict(
                        text="Top 10 by Salary",
                        font=dict(family='Playfair Display', size=24, color='#e8f0f8')
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#c5d3e3', family='Inter'),
                    height=500,
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.05)',
                        color='#8fa3b8',
                        title="Annual Salary (USD)"
                    ),
                    yaxis=dict(
                        showgrid=False,
                        color='#c5d3e3'
                    ),
                    margin=dict(l=20, r=100, t=60, b=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Department distribution if applicable
                if 'department' in results.columns:
                    dept_counts = results['department'].value_counts()
                    
                    fig2 = go.Figure(data=[
                        go.Pie(
                            labels=dept_counts.index,
                            values=dept_counts.values,
                            hole=0.4,
                            marker=dict(
                                colors=['#5d7fa5', '#4a6fa5', '#3d5a80', '#2c4259', '#1b2838', '#0d1b2a'],
                                line=dict(color='rgba(255,255,255,0.2)', width=2)
                            ),
                            textfont=dict(size=14, color='#f0f4f8'),
                            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
                        )
                    ])
                    
                    fig2.update_layout(
                        title=dict(
                            text="Distribution by Department",
                            font=dict(family='Playfair Display', size=24, color='#e8f0f8')
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#c5d3e3', family='Inter'),
                        height=400,
                        showlegend=True,
                        legend=dict(
                            font=dict(size=12),
                            bgcolor='rgba(255,255,255,0.05)',
                            bordercolor='rgba(255,255,255,0.1)',
                            borderwidth=1
                        )
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
        
        with tab4:
            st.markdown("### Download Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Excel export
                if st.button("📥 Download Excel", use_container_width=True):
                    from io import BytesIO
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        results.to_excel(writer, index=False, sheet_name='Results')
                        
                        # Summary sheet
                        summary_df = pd.DataFrame({
                            'Metric': ['Total Employees', 'Average Salary', 'Median Salary', 'Min Salary', 'Max Salary'],
                            'Value': [
                                len(results),
                                f"${results['annual_salary_usd'].mean():,.0f}",
                                f"${results['annual_salary_usd'].median():,.0f}",
                                f"${results['annual_salary_usd'].min():,.0f}",
                                f"${results['annual_salary_usd'].max():,.0f}"
                            ]
                        })
                        summary_df.to_excel(writer, index=False, sheet_name='Summary')
                    
                    st.download_button(
                        label="💾 Save Excel File",
                        data=output.getvalue(),
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            with col2:
                # CSV export
                csv = results.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    # Sidebar with search history
    with st.sidebar:
        st.markdown("### 📜 Recent Searches")
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        
        if query and search_btn:
            if query not in st.session_state.search_history:
                st.session_state.search_history.insert(0, query)
                st.session_state.search_history = st.session_state.search_history[:10]
        
        for hist_query in st.session_state.search_history:
            if st.button(f"🔍 {hist_query}", key=f"hist_{hist_query}", use_container_width=True):
                st.session_state.search_query = hist_query
                st.rerun()

if __name__ == "__main__":
    main()
