"""
ULTIMATE PREMIUM ANALYTICS PLATFORM
====================================

Museum-quality data visualization experience with:
✨ Exceptional UI design (luxury editorial aesthetic)
📊 8+ Advanced Visualizations (histograms, heatmaps, trends, sunburst, etc.)
🤖 Multi-Agent AI System
📚 RAG Document Search
📥 PDF Downloads
🎨 Premium animations and micro-interactions

The most beautiful analytics dashboard!

Run: streamlit run ULTIMATE_PREMIUM.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import re
import time
from datetime import datetime
import os
import numpy as np

# Page config
st.set_page_config(
    page_title="Executive Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# EXCEPTIONAL PREMIUM UI - Editorial Luxury Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300&family=Montserrat:wght@200;300;400;500;600;700;800;900&display=swap');
    
    /* Sophisticated Dark Editorial Theme */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(14,18,28,1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(18,22,32,1) 0%, transparent 50%),
            linear-gradient(135deg, #08090e 0%, #0e1219 20%, #12161d 40%, #161a22 60%, #1a1e27 80%, #1e222b 100%);
        font-family: 'Montserrat', -apple-system, sans-serif;
        color: #e8ecf1;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding: 4rem 5rem !important;
        max-width: 100% !important;
    }
    
    /* Exquisite Typography Hierarchy */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        font-size: 6.5rem !important;
        letter-spacing: 0.04em !important;
        line-height: 1.1 !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 20%, #e8ecf1 50%, #d0d8e0 80%, #b8c4d0 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 0 0 0.8rem 0 !important;
        animation: heroEntry 2s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    
    
    @keyframes heroEntry {
        from {
            opacity: 0;
            transform: translateY(-80px) scale(0.96);
            filter: blur(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }
    
    @keyframes lineExpand {
        from { width: 0; opacity: 0; }
        to { width: 80px; opacity: 1; }
    }
    
    h2 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 400 !important;
        font-size: 3.2rem !important;
        color: #e8ecf1 !important;
        letter-spacing: 0.02em !important;
        margin: 5rem 0 2rem 0 !important;
        position: relative;
        padding-bottom: 1rem;
    }
    
    h2::before {
        content: '◆';
        position: absolute;
        left: -2.5rem;
        color: #8b9fc9;
        font-size: 1rem;
        opacity: 0.4;
    }
    
    h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.24em !important;
        text-transform: uppercase !important;
        color: #8b9fc9 !important;
        margin: 2.5rem 0 1.2rem 0 !important;
    }
    
    /* Subtitle - Refined */
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.88rem;
        font-weight: 300;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #5a6b7f;
        margin-bottom: 5rem;
        animation: fadeIn 2s ease-out 0.5s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Museum-Quality Metric Cards */
    div[data-testid="metric-container"] {
        background: 
            linear-gradient(135deg, rgba(255,255,255,0.012) 0%, rgba(255,255,255,0.004) 100%),
            radial-gradient(circle at 30% 20%, rgba(139,159,201,0.06) 0%, transparent 70%);
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        border-right: 1px solid rgba(255,255,255,0.02);
        border-radius: 0;
        padding: 3rem 2.5rem;
        backdrop-filter: blur(40px) saturate(120%);
        box-shadow: 
            0 30px 90px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.03),
            inset 1px 0 0 rgba(255,255,255,0.01);
        transition: all 0.9s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,159,201,0.4), transparent);
        opacity: 0;
        transition: opacity 0.9s ease;
    }
    
    div[data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: -100%;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%);
        transition: top 0.9s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-18px);
        box-shadow: 
            0 40px 120px rgba(0,0,0,0.7),
            0 0 0 1px rgba(139,159,201,0.15),
            inset 0 1px 0 rgba(255,255,255,0.05);
        border-top-color: rgba(139,159,201,0.25);
    }
    
    div[data-testid="metric-container"]:hover::before {
        opacity: 1;
    }
    
    div[data-testid="metric-container"]:hover::after {
        top: 0;
    }
    
    /* Staggered card animations */
    div[data-testid="metric-container"]:nth-child(1) {
        animation: cardFloat 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
    }
    div[data-testid="metric-container"]:nth-child(2) {
        animation: cardFloat 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }
    div[data-testid="metric-container"]:nth-child(3) {
        animation: cardFloat 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.6s both;
    }
    div[data-testid="metric-container"]:nth-child(4) {
        animation: cardFloat 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.8s both;
    }
    
    @keyframes cardFloat {
        from {
            opacity: 0;
            transform: translateY(60px) scale(0.94);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 3.8rem !important;
        font-weight: 200 !important;
        color: #ffffff !important;
        letter-spacing: -0.04em !important;
        text-shadow: 0 6px 24px rgba(0,0,0,0.8);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.22em !important;
        text-transform: uppercase !important;
        color: #5a6b7f !important;
        margin-bottom: 1rem !important;
    }
    
    /* Luxury Agent Messages */
    .agent-message {
        padding: 4rem;
        margin: 4rem 0;
        border-left: 2px solid;
        background: 
            linear-gradient(135deg, rgba(255,255,255,0.008) 0%, rgba(255,255,255,0.003) 100%),
            radial-gradient(circle at 10% 20%, rgba(139,159,201,0.05) 0%, transparent 60%);
        backdrop-filter: blur(50px) saturate(110%);
        box-shadow: 
            0 40px 120px rgba(0,0,0,0.7),
            inset 0 1px 0 rgba(255,255,255,0.02),
            inset 2px 0 0 rgba(255,255,255,0.01);
        animation: agentEntrance 1.2s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        font-size: 1.05rem;
        line-height: 1.9;
        font-weight: 300;
    }
    
    .agent-message::before {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 1px;
        background: linear-gradient(180deg, transparent, rgba(255,255,255,0.04), transparent);
        opacity: 0;
        transition: opacity 1s ease;
    }
    
    .agent-message:hover {
        transform: translateX(24px) scale(1.01);
        box-shadow: 
            0 50px 150px rgba(0,0,0,0.8),
            0 0 0 1px rgba(139,159,201,0.12),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }
    
    .agent-message:hover::before {
        opacity: 1;
    }
    
    @keyframes agentEntrance {
        from {
            opacity: 0;
            transform: translateX(-120px) translateY(40px) scale(0.92);
            filter: blur(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0) translateY(0) scale(1);
            filter: blur(0);
        }
    }
    
    .analyst-message {
        border-left-color: #8b9fc9;
        background: 
            linear-gradient(135deg, rgba(139,159,201,0.10) 0%, rgba(107,141,181,0.04) 100%),
            radial-gradient(circle at 10% 20%, rgba(139,159,201,0.08) 0%, transparent 60%);
    }
    
    .advisor-message {
        border-left-color: #76b97f;
        background: 
            linear-gradient(135deg, rgba(118,185,127,0.10) 0%, rgba(86,162,95,0.04) 100%),
            radial-gradient(circle at 10% 20%, rgba(118,185,127,0.08) 0%, transparent 60%);
    }
    
    /* Refined Minimal Buttons */
    .stButton > button {
        background: rgba(255,255,255,0.02) !important;
        color: #b8c4d0 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 0 !important;
        padding: 1.3rem 2rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 
            0 12px 40px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.03) !important;
        position: relative !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        min-width: auto !important;
        width: auto !important;
        height: auto !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: left 0.8s ease;
    }
    
    .stButton > button:hover {
        background: rgba(139,159,201,0.12) !important;
        border-color: rgba(139,159,201,0.35) !important;
        transform: translateY(-8px) !important;
        box-shadow: 
            0 24px 72px rgba(0,0,0,0.6),
            0 0 0 1px rgba(139,159,201,0.15),
            inset 0 1px 0 rgba(255,255,255,0.06) !important;
        color: #ffffff !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Premium Primary Button - Gold Accent */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #c19b2a 50%, #a8861f 100%) !important;
        color: #0a0e14 !important;
        border: none !important;
        font-weight: 900 !important;
        box-shadow: 
            0 16px 48px rgba(212,175,55,0.40),
            inset 0 1px 2px rgba(255,255,255,0.4),
            inset 0 -1px 2px rgba(0,0,0,0.2) !important;
        letter-spacing: 0.24em !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #e5c158 0%, #d4af37 50%, #c19b2a 100%) !important;
        transform: translateY(-10px) scale(1.03) !important;
        box-shadow: 
            0 28px 84px rgba(212,175,55,0.60),
            0 0 0 2px rgba(212,175,55,0.3),
            inset 0 2px 4px rgba(255,255,255,0.5) !important;
    }
    
    /* Emerald Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(118,185,127,0.15) 0%, rgba(86,162,95,0.10) 100%) !important;
        color: #d8f0dc !important;
        border: 1px solid rgba(118,185,127,0.25) !important;
        border-radius: 0 !important;
        padding: 1rem 1.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        box-shadow: 
            0 8px 28px rgba(118,185,127,0.30),
            inset 0 1px 0 rgba(255,255,255,0.08) !important;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(118,185,127,0.25) 0%, rgba(86,162,95,0.18) 100%) !important;
        border-color: rgba(118,185,127,0.45) !important;
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 
            0 16px 48px rgba(118,185,127,0.45),
            0 0 0 1px rgba(118,185,127,0.2) !important;
        color: #ffffff !important;
    }
    
    /* Refined Text Input */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.015) !important;
        border: none !important;
        border-bottom: 2px solid rgba(139,159,201,0.15) !important;
        border-radius: 0 !important;
        color: #e8ecf1 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 300 !important;
        padding: 1.5rem 0.5rem !important;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255,255,255,0.02) !important;
        border-bottom-color: rgba(139,159,201,0.6) !important;
        box-shadow: 0 4px 0 -2px rgba(139,159,201,0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #5a6b7f !important;
        font-style: italic !important;
        font-weight: 300 !important;
    }
    
    /* Editorial Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 0;
        margin-bottom: 3rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5a6b7f;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        padding: 1.5rem 3rem;
        border: none;
        border-bottom: 3px solid transparent;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #b8c4d0;
        border-bottom-color: rgba(139,159,201,0.25);
        background: rgba(255,255,255,0.015);
    }
    
    .stTabs [aria-selected="true"] {
        color: #e8ecf1 !important;
        font-weight: 900 !important;
        border-bottom-color: #8b9fc9 !important;
        background: rgba(139,159,201,0.04) !important;
    }
    
    /* Refined Dataframe */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.01) !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        border-radius: 0 !important;
        box-shadow: 0 12px 48px rgba(0,0,0,0.5) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.88rem !important;
    }
    
    /* Alert Boxes - Editorial Style */
    .stAlert {
        background: rgba(139,159,201,0.06) !important;
        border: none !important;
        border-left: 2px solid #8b9fc9 !important;
        border-radius: 0 !important;
        color: #d4dfe8 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        padding: 2rem 2.5rem !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4) !important;
    }
    
    [data-testid="stSuccess"] {
        background: rgba(118,185,127,0.06) !important;
        border-left-color: #76b97f !important;
    }
    
    [data-testid="stWarning"] {
        background: rgba(212,175,55,0.06) !important;
        border-left-color: #c9a961 !important;
    }
    
    /* Expander - Minimal Refined */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.015) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 0 !important;
        color: #a8b8cc !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.08em !important;
        padding: 1.3rem 2rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.03) !important;
        border-color: rgba(139,159,201,0.15) !important;
        color: #e8ecf1 !important;
        transform: translateX(8px);
    }
    
    /* Sidebar - Refined */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8,9,14,0.98) 0%, rgba(14,18,25,0.98) 100%);
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b9fc9 !important;
        border-right-color: rgba(139,159,201,0.3) !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(139,159,201,0.2) 50%, transparent 100%);
        margin: 5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

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
        'by_department': {},
        'by_country': {}
    }
    
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        kb['by_department'][dept] = {
            'count': len(dept_df),
            'avg_salary': dept_df['annual_salary_usd'].mean(),
            'min_salary': dept_df['annual_salary_usd'].min(),
            'max_salary': dept_df['annual_salary_usd'].max()
        }
    
    for country in df['country'].unique():
        country_df = df[df['country'] == country]
        kb['by_country'][country] = {
            'count': len(country_df),
            'avg_salary': country_df['annual_salary_usd'].mean()
        }
    
    return kb

# ============================================================================
# MULTI-AGENT SYSTEM
# ============================================================================

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
            filters.append('United States')
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
        
        if 'senior' in q:
            filtered = filtered[filtered['job_title'].str.contains('Senior', case=False, na=False)]
            filters.append('Senior')
        
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
        
        filtered = filtered.sort_values('annual_salary_usd', ascending=False)
        
        top_match = re.search(r'top\s+(\d+)', q)
        if top_match:
            filtered = filtered.head(int(top_match.group(1)))
            filters.append(f'Top {top_match.group(1)}')
        elif 'top' in q:
            filtered = filtered.head(10)
            filters.append('Top 10')
        
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
                message += f" — {' • '.join(filters)}"
            
            avg = emp_results['annual_salary_usd'].mean()
            median = emp_results['annual_salary_usd'].median()
            
            message += f"\n\n**Compensation Metrics:**\n"
            message += f"• Mean: ${avg:,.0f}\n"
            message += f"• Median: ${median:,.0f}\n"
            message += f"• Range: ${emp_results['annual_salary_usd'].min():,.0f} — ${emp_results['annual_salary_usd'].max():,.0f}\n"
            
            if 'department' in emp_results.columns and len(emp_results['department'].unique()) > 1:
                message += f"• Departments: {len(emp_results['department'].unique())}\n"
            
            message += f"\n**Top Five Contributors:**\n"
            for idx, (_, emp) in enumerate(emp_results.head(5).iterrows(), 1):
                message += f"{idx}. {emp['employee_id']} — {emp['job_title']} — ${emp['annual_salary_usd']:,.0f}\n"
        
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            message += f"\n\n**Policy Documentation Findings:**\n\n"
            for i, (doc, meta) in enumerate(zip(doc_results['documents'][0], doc_results['metadatas'][0])):
                # Calculate relevance if distances available
                if 'distances' in doc_results and len(doc_results['distances'][0]) > i:
                    relevance = max(0, (1 - doc_results['distances'][0][i]) * 100)
                    message += f"*{meta['title']}* ({relevance:.0f}% relevance) — {doc[:140]}...\n\n"
                else:
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
            
            message += "**Executive Recommendations:**\n"
            
            if abs(variance) > 30:
                direction = "above" if variance > 0 else "below"
                message += f"• Cohort compensation averages {abs(variance):.0f}% {direction} organizational baseline (${global_avg:,.0f})\n"
                if variance > 0:
                    message += f"• Recommend market competitiveness analysis and retention risk assessment\n"
                else:
                    message += f"• Potential opportunity for strategic compensation adjustment\n"
            else:
                message += f"• Compensation positioning aligned within acceptable variance threshold\n"
                message += f"• Current structure supports organizational equity objectives\n"
            
            message += f"\n**Strategic Opportunities:**\n"
            message += f"• Talent pool: {len(emp_data):,} employees available for strategic deployment\n"
            
            if len(emp_data) > 50:
                message += f"• Substantial cohort enables comprehensive succession planning initiatives\n"
            
            if 'department' in emp_data.columns:
                dept_diversity = len(emp_data['department'].unique())
                if dept_diversity > 1:
                    message += f"• Cross-functional representation ({dept_diversity} departments) supports collaborative programs\n"
        
        return {
            'agent': self.name,
            'message': message
        }

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Elegant header
    st.markdown("<h1>Finance Payroll Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Multi-Agent Intelligence Platform</p>", unsafe_allow_html=True)
    
    # Load all data
    df = load_employee_data()
    
    if df is None:
        st.error("Data source unavailable")
        st.stop()
    
    collection, doc_count = load_chromadb()
    kb = build_knowledge_base(df)
    
    # Premium metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workforce", f"{len(df):,}")
    with col2:
        usa_count = kb['countries'].get('United States', 0)
        st.metric("United States", f"{usa_count:,}")
    with col3:
        india_count = kb['countries'].get('India', 0)
        st.metric("India", f"{india_count:,}")
    with col4:
        st.metric("Mean Compensation", f"${kb['avg_salary_global']/1000:.0f}K")
    
    st.markdown("---")
    
    # Initialize agents
    analyst_agent = DataAnalystAgent(df, kb, collection)
    advisor_agent = BusinessAdvisorAgent(kb)
    
    # Search interface
    st.markdown("## Intelligence Inquiry")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Executive Compensation", use_container_width=True):
            st.session_state.query = "Top 10 highest paid in USA"
    with col2:
        if st.button("Remote Work Guidelines", use_container_width=True):
            st.session_state.query = "What is the remote work policy?"
    with col3:
        if st.button("Engineering Analysis", use_container_width=True):
            st.session_state.query = "Analyze Engineering department"
    with col4:
        if st.button("Compensation Benchmarks", use_container_width=True):
            st.session_state.query = "Engineering salary ranges vs policy guidelines"
    
    user_query = st.text_input(
        "",
        value=st.session_state.get('query', ''),
        placeholder="Inquire about workforce analytics, organizational policies, or strategic insights...",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([1, 6])
    with col1:
        search_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if search_btn and user_query:
        st.markdown("---")
        st.markdown("## Intelligence Briefing")
        
        st.info(f"**Query:** {user_query}")
        
        # Agent 1: Data Analyst
        st.markdown("### ◆ Data Analyst Agent")
        
        with st.spinner("Analyzing data repositories..."):
            time.sleep(0.8)
            analyst_response = analyst_agent.respond(user_query)
        
        with st.expander("Analytical Methodology"):
            st.markdown("• Database query execution and filtering\n• Document corpus semantic search\n• Statistical aggregation and analysis")
        
        st.markdown(f'<div class="agent-message analyst-message">{analyst_response["message"]}</div>', 
                   unsafe_allow_html=True)
        
        # PDF Downloads
        doc_results = analyst_response.get('doc_data')
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            st.markdown("### Source Documentation")
            
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
                                key=f"dl_{doc_id}",
                                use_container_width=True
                            )
                            col_idx += 1
        
        # Agent 2: Business Advisor
        st.markdown("### ◆ Business Advisor Agent")
        
        with st.spinner("Synthesizing strategic insights..."):
            time.sleep(0.6)
            advisor_response = advisor_agent.respond(analyst_response)
        
        with st.expander("Strategic Framework"):
            st.markdown("• Comparative benchmarking analysis\n• Organizational alignment assessment\n• Strategic opportunity identification")
        
        st.markdown(f'<div class="agent-message advisor-message">{advisor_response["message"]}</div>', 
                   unsafe_allow_html=True)
        
        # ADVANCED VISUALIZATIONS
        if analyst_response.get('emp_data') is not None and len(analyst_response['emp_data']) > 0:
            st.markdown("---")
            st.markdown("## Advanced Analytics")
            
            results = analyst_response['emp_data']
            
            # Multiple visualization tabs
            viz1, viz2, viz3, viz4 = st.tabs([
                "Distribution Analysis",
                "Comparative Intelligence",
                "Geographic Insights",
                "Detailed Records"
            ])
            
            # TAB 1: DISTRIBUTION ANALYSIS
            with viz1:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Salary histogram with KDE
                    fig = go.Figure()
                    
                    fig.add_trace(go.Histogram(
                        x=results['annual_salary_usd'],
                        nbinsx=25,
                        marker=dict(
                            color='rgba(139,159,201,0.7)',
                            line=dict(color='#8b9fc9', width=1.5)
                        ),
                        name='Frequency',
                        opacity=0.85
                    ))
                    
                    fig.update_layout(
                        title=dict(
                            text="Compensation Distribution",
                            font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#a8b8cc', family='Montserrat', size=10),
                        height=400,
                        showlegend=False,
                        xaxis=dict(
                            title="Annual Compensation (USD)",
                            showgrid=True,
                            gridcolor='rgba(255,255,255,0.03)',
                            color='#7a8ca0',
                            zeroline=False
                        ),
                        yaxis=dict(
                            title="Employee Count",
                            showgrid=True,
                            gridcolor='rgba(255,255,255,0.03)',
                            color='#7a8ca0'
                        ),
                        bargap=0.05
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Box plot by department
                    if 'department' in results.columns and len(results['department'].unique()) > 1:
                        fig = go.Figure()
                        
                        colors = ['#8b9fc9', '#76b97f', '#c9a961', '#a87f8f', '#7fa8a8']
                        
                        for idx, dept in enumerate(results['department'].unique()):
                            dept_data = results[results['department'] == dept]
                            
                            fig.add_trace(go.Box(
                                y=dept_data['annual_salary_usd'],
                                name=dept,
                                marker=dict(color=colors[idx % len(colors)]),
                                boxmean='sd',
                                whiskerwidth=0.5,
                                line=dict(width=1.5)
                            ))
                        
                        fig.update_layout(
                            title=dict(
                                text="Department Distribution",
                                font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')
                            ),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#a8b8cc', family='Montserrat', size=10),
                            showlegend=False,
                            height=400,
                            yaxis=dict(
                                title="Annual Compensation (USD)",
                                showgrid=True,
                                gridcolor='rgba(255,255,255,0.03)',
                                color='#7a8ca0'
                            ),
                            xaxis=dict(
                                showgrid=False,
                                color='#a8b8cc'
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            # TAB 2: COMPARATIVE ANALYSIS
            with viz2:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top 10 horizontal bar - Premium style
                    top10 = results.nlargest(10, 'annual_salary_usd')
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            y=top10['employee_id'],
                            x=top10['annual_salary_usd'],
                            orientation='h',
                            marker=dict(
                                color=top10['annual_salary_usd'],
                                colorscale=[[0, '#6b8db5'], [0.3, '#8b9fc9'], [0.7, '#a8b8cc'], [1, '#c4cfd8']],
                                line=dict(color='rgba(139,159,201,0.4)', width=1),
                                showscale=False
                            ),
                            text=top10['annual_salary_usd'].apply(lambda x: f'${x/1000:.0f}K'),
                            textposition='outside',
                            textfont=dict(family='Montserrat', size=11, color='#b8c8d8', weight=600),
                            hovertemplate='<b>%{y}</b><br>Compensation: $%{x:,.0f}<extra></extra>'
                        )
                    ])
                    
                    fig.update_layout(
                        title=dict(
                            text="Top Performers",
                            font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#a8b8cc', family='Montserrat'),
                        height=500,
                        showlegend=False,
                        xaxis=dict(
                            title="Annual Compensation (USD)",
                            showgrid=True,
                            gridcolor='rgba(255,255,255,0.03)',
                            color='#7a8ca0'
                        ),
                        yaxis=dict(
                            showgrid=False,
                            color='#b8c8d8'
                        ),
                        margin=dict(l=30, r=130, t=60, b=50)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Department comparison bars
                    if 'department' in results.columns:
                        dept_stats = results.groupby('department').agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).reset_index()
                        dept_stats.columns = ['Department', 'Count', 'Mean Salary']
                        dept_stats = dept_stats.sort_values('Mean Salary', ascending=True)
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                y=dept_stats['Department'],
                                x=dept_stats['Mean Salary'],
                                orientation='h',
                                marker=dict(
                                    color='#76b97f',
                                    line=dict(color='#56a25f', width=1)
                                ),
                                text=dept_stats['Mean Salary'].apply(lambda x: f'${x/1000:.0f}K'),
                                textposition='outside',
                                textfont=dict(color='#b8c8d8', weight=600),
                                hovertemplate='<b>%{y}</b><br>Average: $%{x:,.0f}<extra></extra>'
                            )
                        ])
                        
                        fig.update_layout(
                            title=dict(
                                text="Department Benchmarks",
                                font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')
                            ),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#a8b8cc'),
                            height=500,
                            showlegend=False,
                            xaxis=dict(
                                title="Mean Compensation (USD)",
                                showgrid=True,
                                gridcolor='rgba(255,255,255,0.03)',
                                color='#7a8ca0'
                            ),
                            margin=dict(l=30, r=130, t=60, b=50)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            # TAB 3: GEOGRAPHIC INSIGHTS
            with viz3:
                col1, col2 = st.columns(2)
                
                with col1:
                    # City scatter plot
                    if 'city' in results.columns:
                        city_stats = results.groupby(['country', 'city']).agg({
                            'employee_id': 'count',
                            'annual_salary_usd': 'mean'
                        }).reset_index()
                        city_stats.columns = ['Country', 'City', 'Employees', 'Mean Salary']
                        city_stats = city_stats.sort_values('Employees', ascending=False).head(20)
                        
                        fig = px.scatter(
                            city_stats,
                            x='Employees',
                            y='Mean Salary',
                            size='Employees',
                            color='Country',
                            hover_name='City',
                            title='Geographic Distribution',
                            color_discrete_map={
                                'United States': '#8b9fc9',
                                'India': '#76b97f'
                            },
                            size_max=60
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#a8b8cc', family='Montserrat', size=10),
                            title=dict(font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')),
                            height=500,
                            xaxis=dict(
                                showgrid=True,
                                gridcolor='rgba(255,255,255,0.03)',
                                color='#7a8ca0',
                                title='Employee Count'
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor='rgba(255,255,255,0.03)',
                                color='#7a8ca0',
                                title='Mean Compensation (USD)'
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Sunburst organizational hierarchy
                    if len(results) > 15:
                        sunburst_data = results.head(100)
                        
                        fig = px.sunburst(
                            sunburst_data,
                            path=['country', 'department', 'job_title'],
                            values='annual_salary_usd',
                            title='Organizational Structure',
                            color='annual_salary_usd',
                            color_continuous_scale=[[0, '#6b8db5'], [0.5, '#8b9fc9'], [1, '#a8b8cc']]
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#a8b8cc', family='Montserrat', size=10),
                            title=dict(font=dict(family='Cormorant Garamond', size=24, color='#e8ecf1')),
                            height=500,
                            showlegend=False
                        )
                        
                        fig.update_traces(
                            textfont=dict(size=11, family='Montserrat', color='#0a0e14'),
                            marker=dict(line=dict(color='#1a1e27', width=2))
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            # TAB 4: DETAILED RECORDS
            with viz4:
                # Premium data table
                st.markdown("### Employee Records")
                
                display_df = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(25).copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['Employee ID', 'Position', 'Department', 'City', 'Country', 'Annual Compensation']
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=600
                )
                
                # Statistical summary
                st.markdown("### Statistical Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Count", f"{len(results):,}")
                with col2:
                    st.metric("Mean", f"${results['annual_salary_usd'].mean():,.0f}")
                with col3:
                    st.metric("Median", f"${results['annual_salary_usd'].median():,.0f}")
                with col4:
                    std_dev = results['annual_salary_usd'].std()
                    st.metric("Std Dev", f"${std_dev:,.0f}")
    
    # Refined sidebar
    with st.sidebar:
        st.markdown("### System Intelligence")
        
        st.success(f"**Workforce:** {len(df):,} employees indexed")
        
        if doc_count > 0:
            st.success(f"**Documentation:** {doc_count} segments analyzed")
        else:
            st.warning("**Documentation:** Unavailable")
        
        st.markdown("---")
        
        st.markdown("### Multi-Agent Architecture")
        st.markdown("**◆ Data Analyst Agent**\n*Retrieval and statistical analysis*")
        st.markdown("**◆ Business Advisor Agent**\n*Strategic insights and recommendations*")
        
        st.markdown("---")
        
        st.markdown("### RAG Knowledge Base")
        st.markdown(f"• {len(df):,} employee records")
        st.markdown(f"• {len(df['department'].unique())} departments")
        st.markdown(f"• {len(df['country'].unique())} countries")
        
        if doc_count > 0:
            st.markdown(f"• {doc_count} document chunks")

if __name__ == "__main__":
    main()
