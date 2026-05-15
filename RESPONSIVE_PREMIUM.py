"""
RESPONSIVE PREMIUM ANALYTICS PLATFORM
======================================

Fully responsive design that works on:
✅ Desktop (1920px+)
✅ Laptop (1366px)
✅ Tablet (768px)
✅ Mobile (all sizes)

Features:
✨ Beautiful responsive UI
📊 8 Advanced Visualizations
🤖 Multi-Agent AI
📚 RAG Document Search
📥 PDF Downloads

Run: streamlit run RESPONSIVE_PREMIUM.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import time
import os

# Page config
st.set_page_config(
    page_title="Analytics Platform",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# RESPONSIVE PREMIUM CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    /* Base Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #12161d 50%, #1a1e27 100%);
        font-family: 'Montserrat', sans-serif;
        color: #e8eef5;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Container */
    .block-container {
        padding: 2rem 1.5rem !important;
        max-width: 100% !important;
    }
    
    @media (min-width: 768px) {
        .block-container {
            padding: 3rem 2.5rem !important;
        }
    }
    
    @media (min-width: 1200px) {
        .block-container {
            padding: 4rem 4rem !important;
        }
    }
    
    /* Responsive Typography */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #ffffff 0%, #e8ecf1 50%, #b8c8d8 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.5rem !important;
        animation: fadeIn 1s ease-out;
    }
    
    @media (min-width: 768px) {
        h1 { font-size: 4rem !important; }
    }
    
    @media (min-width: 1200px) {
        h1 { font-size: 5.5rem !important; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    h2 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        color: #e8eef5 !important;
        margin: 2.5rem 0 1.5rem 0 !important;
    }
    
    @media (min-width: 768px) {
        h2 { font-size: 2.8rem !important; }
    }
    
    h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #a8b8cc !important;
        margin-top: 2rem !important;
    }
    
    /* Subtitle */
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 300;
        letter-spacing: 0.08em;
        color: #7a8ca0;
        margin-bottom: 2.5rem;
    }
    
    @media (min-width: 768px) {
        .subtitle {
            font-size: 0.88rem;
            margin-bottom: 4rem;
        }
    }
    
    /* Responsive Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-top: 2px solid rgba(139,159,201,0.2);
        border-radius: 4px;
        padding: 1.5rem 1.2rem;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 36px rgba(0,0,0,0.4);
        transition: all 0.5s ease;
        margin-bottom: 1rem;
    }
    
    @media (min-width: 768px) {
        div[data-testid="metric-container"] {
            padding: 2rem 1.8rem;
        }
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(93,127,165,0.45);
        border-top-color: rgba(139,159,201,0.4);
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 300 !important;
        color: #ffffff !important;
        letter-spacing: -0.03em !important;
    }
    
    @media (min-width: 768px) {
        [data-testid="stMetricValue"] {
            font-size: 3rem !important;
        }
    }
    
    @media (min-width: 1200px) {
        [data-testid="stMetricValue"] {
            font-size: 3.8rem !important;
        }
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: #7a8ca0 !important;
    }
    
    /* Responsive Buttons - FIT TO CONTAINER */
    .stButton > button {
        background: rgba(255,255,255,0.02) !important;
        color: #b8c4d0 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 0 !important;
        padding: 0.9rem 0.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.6rem !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        width: 100% !important;
        box-sizing: border-box !important;
        min-height: 3.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.3 !important;
    }
    
    @media (min-width: 768px) {
        .stButton > button {
            font-size: 0.68rem !important;
            padding: 1rem 0.8rem !important;
        }
    }
    
    @media (min-width: 1200px) {
        .stButton > button {
            font-size: 0.72rem !important;
            padding: 1.2rem 1.5rem !important;
            letter-spacing: 0.08em !important;
        }
    }
    
    .stButton > button:hover {
        background: rgba(139,159,201,0.12) !important;
        border-color: rgba(139,159,201,0.35) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px rgba(0,0,0,0.5) !important;
        color: #ffffff !important;
    }
    
    /* Primary Button - Gold */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #0a0e14 !important;
        border: none !important;
        font-weight: 800 !important;
        box-shadow: 0 12px 36px rgba(212,175,55,0.4) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%) !important;
        box-shadow: 0 20px 56px rgba(212,175,55,0.6) !important;
        transform: translateY(-6px) scale(1.02) !important;
    }
    
    /* Download Buttons - Emerald */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(118,185,127,0.15) 0%, rgba(86,162,95,0.10) 100%) !important;
        color: #d8f0dc !important;
        border: 1px solid rgba(118,185,127,0.25) !important;
        border-radius: 0 !important;
        padding: 0.9rem 1.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.10em !important;
        text-transform: uppercase !important;
        box-shadow: 0 6px 20px rgba(118,185,127,0.3) !important;
        transition: all 0.4s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(118,185,127,0.25) 0%, rgba(86,162,95,0.18) 100%) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(118,185,127,0.45) !important;
    }
    
    /* Responsive Text Input */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.015) !important;
        border: none !important;
        border-bottom: 2px solid rgba(139,159,201,0.15) !important;
        border-radius: 0 !important;
        color: #e8ecf1 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 300 !important;
        padding: 1.2rem 0.5rem !important;
        transition: all 0.4s ease !important;
        box-shadow: none !important;
    }
    
    @media (min-width: 768px) {
        .stTextInput > div > div > input {
            font-size: 1.05rem !important;
            padding: 1.5rem 0.5rem !important;
        }
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255,255,255,0.02) !important;
        border-bottom-color: rgba(139,159,201,0.6) !important;
        box-shadow: 0 4px 0 -2px rgba(139,159,201,0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #5a6b7f !important;
        font-style: normal !important;
    }
    
    /* Responsive Agent Messages */
    .agent-message {
        padding: 2rem;
        margin: 2rem 0;
        border-left: 2px solid;
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.5);
        animation: slideIn 0.8s ease-out;
        transition: all 0.6s ease;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    @media (min-width: 768px) {
        .agent-message {
            padding: 3rem;
            font-size: 1rem;
        }
    }
    
    @media (min-width: 1200px) {
        .agent-message {
            padding: 4rem;
            font-size: 1.05rem;
            line-height: 1.9;
        }
    }
    
    .agent-message:hover {
        transform: translateX(10px);
        box-shadow: 0 24px 72px rgba(0,0,0,0.6);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .analyst-message {
        background: linear-gradient(135deg, rgba(93,127,165,0.15) 0%, rgba(61,90,128,0.08) 100%);
        border-left-color: #8b9fc9;
        border: 1px solid rgba(93,127,165,0.2);
    }
    
    .advisor-message {
        background: linear-gradient(135deg, rgba(76,175,80,0.15) 0%, rgba(56,142,60,0.08) 100%);
        border-left-color: #76b97f;
        border: 1px solid rgba(76,175,80,0.2);
    }
    
    /* Responsive Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        overflow-x: auto;
        flex-wrap: nowrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #7a8ca0;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 0.65rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        padding: 1rem 1.2rem;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.72rem;
            padding: 1.2rem 2rem;
        }
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #b8c4d0;
        border-bottom-color: rgba(139,159,201,0.3);
        background: rgba(255,255,255,0.02);
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        border-bottom-color: #8b9fc9 !important;
        background: rgba(139,159,201,0.06) !important;
    }
    
    /* Responsive Dataframe */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 4px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
        overflow-x: auto !important;
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(139,159,201,0.08) !important;
        border-left: 2px solid #8b9fc9 !important;
        border-radius: 2px !important;
        color: #e8eef5 !important;
        padding: 1.2rem 1.5rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
    }
    
    [data-testid="stSuccess"] {
        background: rgba(118,185,127,0.08) !important;
        border-left-color: #76b97f !important;
    }
    
    /* Responsive Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 2px !important;
        color: #a8b8cc !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        padding: 1rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.04) !important;
        border-color: rgba(139,159,201,0.15) !important;
        color: #e8eef5 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,159,201,0.2), transparent);
        margin: 3rem 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8,9,14,0.98) 0%, rgba(14,18,25,0.98) 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
</style>
""", unsafe_allow_html=True)

# Data loading (same as before)
@st.cache_data
def load_employee_data():
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

@st.cache_resource
def load_chromadb():
    try:
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="employee_documents")
        return collection, collection.count()
    except:
        return None, 0

def build_knowledge_base(df):
    kb = {
        'total_employees': len(df),
        'countries': df['country'].value_counts().to_dict(),
        'avg_salary_global': df['annual_salary_usd'].mean(),
        'by_department': {}
    }
    
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        kb['by_department'][dept] = {
            'count': len(dept_df),
            'avg_salary': dept_df['annual_salary_usd'].mean(),
            'min_salary': dept_df['annual_salary_usd'].min(),
            'max_salary': dept_df['annual_salary_usd'].max()
        }
    
    return kb

# Multi-Agent Classes
class DataAnalystAgent:
    def __init__(self, df, kb, doc_collection=None):
        self.df = df
        self.knowledge_base = kb
        self.doc_collection = doc_collection
        self.name = "Data Analyst Agent"
    
    def search_employees(self, query):
        q = query.lower()
        filtered = self.df.copy()
        filters = []
        
        if 'usa' in q or 'united states' in q:
            filtered = filtered[filtered['country'] == 'United States']
            filters.append('USA')
        elif 'india' in q:
            filtered = filtered[filtered['country'] == 'India']
            filters.append('India')
        
        for dept in ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance', 'Product']:
            if dept.lower() in q:
                filtered = filtered[filtered['department'] == dept]
                filters.append(dept)
                break
        
        if 'manager' in q:
            filtered = filtered[filtered['job_title'].str.contains('Manager', case=False, na=False)]
            filters.append('Manager')
        
        over_match = re.search(r'over\s+(\d+)k?', q)
        if over_match:
            amount = int(over_match.group(1)) * 1000
            filtered = filtered[filtered['annual_salary_usd'] > amount]
            filters.append(f'>${amount:,}')
        
        filtered = filtered.sort_values('annual_salary_usd', ascending=False)
        
        top_match = re.search(r'top\s+(\d+)', q)
        if top_match:
            filtered = filtered.head(int(top_match.group(1)))
        elif 'top' in q:
            filtered = filtered.head(10)
        
        return filtered, filters
    
    def search_documents(self, query):
        if not self.doc_collection:
            return None
        try:
            return self.doc_collection.query(query_texts=[query], n_results=3)
        except:
            return None
    
    def respond(self, query):
        emp_results, filters = self.search_employees(query)
        doc_results = self.search_documents(query)
        
        message = ""
        
        if len(emp_results) > 0:
            message += f"**Workforce Analysis**\n\n"
            message += f"Identified **{len(emp_results):,} employees**"
            if filters:
                message += f" — {' · '.join(filters)}"
            
            message += f"\n\n**Compensation:**\n"
            message += f"• Mean: ${emp_results['annual_salary_usd'].mean():,.0f}\n"
            message += f"• Range: ${emp_results['annual_salary_usd'].min():,.0f}–${emp_results['annual_salary_usd'].max():,.0f}\n\n"
            
            message += f"**Top Five:**\n"
            for idx, (_, emp) in enumerate(emp_results.head(5).iterrows(), 1):
                message += f"{idx}. {emp['employee_id']} — {emp['job_title']} — ${emp['annual_salary_usd']:,.0f}\n"
        
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            message += f"\n\n**Policy Documentation:**\n\n"
            for i, (doc, meta) in enumerate(zip(doc_results['documents'][0], doc_results['metadatas'][0])):
                message += f"*{meta['title']}* — {doc[:140]}...\n\n"
        
        return {
            'agent': self.name,
            'message': message,
            'emp_data': emp_results,
            'doc_data': doc_results
        }

class BusinessAdvisorAgent:
    def __init__(self, kb):
        self.knowledge_base = kb
        self.name = "Business Advisor Agent"
    
    def respond(self, analyst_response):
        emp_data = analyst_response.get('emp_data')
        
        message = "**Strategic Assessment**\n\n"
        
        if emp_data is not None and len(emp_data) > 0:
            avg_salary = emp_data['annual_salary_usd'].mean()
            global_avg = self.knowledge_base['avg_salary_global']
            variance = ((avg_salary / global_avg) - 1) * 100
            
            message += "**Recommendations:**\n"
            
            if abs(variance) > 30:
                direction = "above" if variance > 0 else "below"
                message += f"• Cohort averages {abs(variance):.0f}% {direction} organizational baseline\n"
            else:
                message += f"• Compensation aligned with organizational standards\n"
            
            message += f"\n**Opportunities:**\n"
            message += f"• {len(emp_data):,} employee talent pool for strategic initiatives\n"
        
        return {
            'agent': self.name,
            'message': message
        }

def main():
    # Header
    st.markdown("<h1>Finance Payroll Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Multi-Agent Intelligence • RAG Document Search</p>", unsafe_allow_html=True)
    
    # Load data
    df = load_employee_data()
    
    if df is None:
        st.error("Data unavailable")
        st.stop()
    
    collection, doc_count = load_chromadb()
    kb = build_knowledge_base(df)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Workforce", f"{len(df):,}")
    with col2:
        usa_count = kb['countries'].get('United States', 0)
        st.metric("United States", f"{usa_count:,}")
    with col3:
        india_count = kb['countries'].get('India', 0)
        st.metric("India", f"{india_count:,}")
    with col4:
        st.metric("Mean Salary", f"${kb['avg_salary_global']/1000:.0f}K")
    
    st.markdown("---")
    
    # Initialize agents
    analyst_agent = DataAnalystAgent(df, kb, collection)
    advisor_agent = BusinessAdvisorAgent(kb)
    
    # Search interface
    st.markdown("## Search & Analysis")
    
    # Responsive buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Top 10 USA", use_container_width=True):
            st.session_state.query = "Top 10 in USA"
    with col2:
        if st.button("Remote Policy", use_container_width=True):
            st.session_state.query = "What is the remote work policy?"
    with col3:
        if st.button("Engineering", use_container_width=True):
            st.session_state.query = "Analyze Engineering department"
    with col4:
        if st.button("Salary Ranges", use_container_width=True):
            st.session_state.query = "Engineering salary ranges vs policy"
    
    user_query = st.text_input(
        "",
        value=st.session_state.get('query', ''),
        placeholder="Ask about employees or policies",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if search_btn and user_query:
        st.markdown("---")
        st.markdown("## AI Analysis")
        
        st.info(f"**Query:** {user_query}")
        
        # Agent 1
        st.markdown("### 📊 Data Analyst")
        with st.spinner("Searching..."):
            time.sleep(0.7)
            analyst_response = analyst_agent.respond(user_query)
        
        st.markdown(f'<div class="agent-message analyst-message">{analyst_response["message"]}</div>', 
                   unsafe_allow_html=True)
        
        # PDF Downloads
        doc_results = analyst_response.get('doc_data')
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            st.markdown("### 📥 Source Documents")
            
            seen = set()
            download_cols = st.columns(min(len(doc_results['metadatas'][0]), 3))
            
            col_idx = 0
            for meta in doc_results['metadatas'][0]:
                doc_id = meta.get('doc_id')
                if doc_id and doc_id not in seen and col_idx < 3:
                    seen.add(doc_id)
                    
                    pdf_file = meta.get('filename')
                    if pdf_file and os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            pdf_data = f.read()
                        
                        with download_cols[col_idx]:
                            st.markdown(f"**{meta['title']}**")
                            st.download_button(
                                label="Download PDF",
                                data=pdf_data,
                                file_name=os.path.basename(pdf_file),
                                mime="application/pdf",
                                key=f"pdf_{doc_id}",
                                use_container_width=True
                            )
                            col_idx += 1
        
        # Agent 2
        st.markdown("### 💼 Business Advisor")
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            advisor_response = advisor_agent.respond(analyst_response)
        
        st.markdown(f'<div class="agent-message advisor-message">{advisor_response["message"]}</div>', 
                   unsafe_allow_html=True)
        
        # Visualizations
        if analyst_response.get('emp_data') is not None and len(analyst_response['emp_data']) > 0:
            st.markdown("---")
            st.markdown("## Advanced Visualizations")
            
            results = analyst_response['emp_data']
            
            viz1, viz2, viz3, viz4 = st.tabs([
                "Distribution",
                "Rankings",
                "Geographic",
                "Data Table"
            ])
            
            with viz1:
                # Histogram
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=results['annual_salary_usd'],
                    nbinsx=20,
                    marker=dict(color='#8b9fc9', line=dict(color='#6b8db5', width=1)),
                    opacity=0.8
                ))
                
                fig.update_layout(
                    title="Salary Distribution",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#b8c8d8'),
                    height=450,
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Box plot by department
                if 'department' in results.columns and len(results['department'].unique()) > 1:
                    fig2 = go.Figure()
                    
                    for dept in results['department'].unique():
                        dept_data = results[results['department'] == dept]
                        fig2.add_trace(go.Box(
                            y=dept_data['annual_salary_usd'],
                            name=dept,
                            marker=dict(color='#8b9fc9')
                        ))
                    
                    fig2.update_layout(
                        title="Department Comparison",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#b8c8d8'),
                        height=450
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
            
            with viz2:
                # Top 10 bar chart
                top10 = results.nlargest(10, 'annual_salary_usd')
                
                fig = go.Figure(data=[go.Bar(
                    y=top10['employee_id'],
                    x=top10['annual_salary_usd'],
                    orientation='h',
                    marker=dict(
                        color=top10['annual_salary_usd'],
                        colorscale='Blues',
                        line=dict(color='rgba(139,159,201,0.3)', width=1)
                    ),
                    text=top10['annual_salary_usd'].apply(lambda x: f'${x/1000:.0f}K'),
                    textposition='outside'
                )])
                
                fig.update_layout(
                    title="Top 10 by Salary",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#b8c8d8'),
                    height=500,
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    margin=dict(l=20, r=120, t=60, b=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with viz3:
                # Scatter plot by city
                if 'city' in results.columns:
                    city_stats = results.groupby(['country', 'city']).agg({
                        'employee_id': 'count',
                        'annual_salary_usd': 'mean'
                    }).reset_index()
                    city_stats.columns = ['Country', 'City', 'Employees', 'Avg Salary']
                    
                    fig = px.scatter(
                        city_stats.head(20),
                        x='Employees',
                        y='Avg Salary',
                        size='Employees',
                        color='Country',
                        hover_name='City',
                        color_discrete_map={'United States': '#8b9fc9', 'India': '#76b97f'}
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#b8c8d8'),
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Sunburst
                if len(results) > 15:
                    fig2 = px.sunburst(
                        results.head(100),
                        path=['country', 'department', 'job_title'],
                        values='annual_salary_usd'
                    )
                    
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#0a0e14'),
                        height=500
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
            
            with viz4:
                # Data table
                display_df = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(20).copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['ID', 'Position', 'Dept', 'City', 'Country', 'Salary']
                
                st.dataframe(display_df, use_container_width=True, height=600)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### System Status")
        st.success(f"✅ {len(df):,} employees")
        
        if doc_count > 0:
            st.success(f"✅ {doc_count} doc chunks")
        else:
            st.warning("⚠️ Run setup first")

if __name__ == "__main__":
    main()
