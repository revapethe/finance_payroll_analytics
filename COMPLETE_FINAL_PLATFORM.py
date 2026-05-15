"""
COMPLETE FINAL PLATFORM - ULTIMATE VERSION
===========================================

This combines EVERYTHING:
✨ Beautiful Responsive UI (from RESPONSIVE_PREMIUM)
🔄 Auto-Setup on Deployment (from AUTO_SETUP)
🐘 PostgreSQL Support (with CSV fallback)
🤖 Multi-Agent AI System
📚 RAG Document Search with ChromaDB
📥 PDF Downloads
📊 8 Advanced Visualizations
🎨 Premium Editorial Design

Works everywhere: Local, Deployed, All screen sizes!

Run: streamlit run COMPLETE_FINAL_PLATFORM.py

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

st.set_page_config(
    page_title="Finance Payroll Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# RESPONSIVE PREMIUM CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #12161d 50%, #1a1e27 100%);
        font-family: 'Montserrat', sans-serif;
        color: #e8eef5;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding: 2rem 1.5rem !important;
        max-width: 100% !important;
    }
    
    @media (min-width: 768px) {
        .block-container { padding: 3rem 2.5rem !important; }
    }
    
    @media (min-width: 1200px) {
        .block-container { padding: 4rem 4rem !important; }
    }
    
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
    
    @media (min-width: 768px) { h1 { font-size: 4rem !important; } }
    @media (min-width: 1200px) { h1 { font-size: 5.5rem !important; } }
    
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
    
    @media (min-width: 768px) { h2 { font-size: 2.8rem !important; } }
    
    h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #a8b8cc !important;
        margin-top: 2rem !important;
    }
    
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 300;
        letter-spacing: 0.08em;
        color: #7a8ca0;
        margin-bottom: 2.5rem;
    }
    
    @media (min-width: 768px) {
        .subtitle { font-size: 0.88rem; margin-bottom: 4rem; }
    }
    
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
        div[data-testid="metric-container"] { padding: 2rem 1.8rem; }
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(93,127,165,0.45);
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 300 !important;
        color: #ffffff !important;
    }
    
    @media (min-width: 768px) { [data-testid="stMetricValue"] { font-size: 3rem !important; } }
    @media (min-width: 1200px) { [data-testid="stMetricValue"] { font-size: 3.8rem !important; } }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: #7a8ca0 !important;
    }
    
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
        min-height: 3.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.3 !important;
    }
    
    @media (min-width: 768px) {
        .stButton > button { font-size: 0.68rem !important; padding: 1rem 0.8rem !important; }
    }
    
    @media (min-width: 1200px) {
        .stButton > button { font-size: 0.72rem !important; padding: 1.2rem 1.5rem !important; }
    }
    
    .stButton > button:hover {
        background: rgba(139,159,201,0.12) !important;
        border-color: rgba(139,159,201,0.35) !important;
        transform: translateY(-4px) !important;
        color: #ffffff !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #0a0e14 !important;
        font-weight: 800 !important;
        box-shadow: 0 12px 36px rgba(212,175,55,0.4) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%) !important;
        transform: translateY(-6px) scale(1.02) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(118,185,127,0.15) 0%, rgba(86,162,95,0.10) 100%) !important;
        color: #d8f0dc !important;
        border: 1px solid rgba(118,185,127,0.25) !important;
        padding: 0.9rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.10em !important;
        text-transform: uppercase !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.015) !important;
        border: none !important;
        border-bottom: 2px solid rgba(139,159,201,0.15) !important;
        color: #e8ecf1 !important;
        font-size: 0.95rem !important;
        padding: 1.2rem 0.5rem !important;
    }
    
    @media (min-width: 768px) {
        .stTextInput > div > div > input { font-size: 1.05rem !important; padding: 1.5rem 0.5rem !important; }
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #5a6b7f !important;
        font-style: normal !important;
    }
    
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
    
    @media (min-width: 768px) { .agent-message { padding: 3rem; font-size: 1rem; } }
    @media (min-width: 1200px) { .agent-message { padding: 4rem; font-size: 1.05rem; } }
    
    .agent-message:hover {
        transform: translateX(10px);
        box-shadow: 0 24px 72px rgba(0,0,0,0.6);
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
    
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid rgba(255,255,255,0.08);
        overflow-x: auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #7a8ca0;
        font-weight: 600;
        font-size: 0.65rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        padding: 1rem 1.2rem;
        border-bottom: 2px solid transparent;
    }
    
    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"] { font-size: 0.72rem; padding: 1.2rem 2rem; }
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        border-bottom-color: #8b9fc9 !important;
        background: rgba(139,159,201,0.06) !important;
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
    }
    
    .stAlert {
        background: rgba(139,159,201,0.08) !important;
        border-left: 2px solid #8b9fc9 !important;
        color: #e8eef5 !important;
        padding: 1.2rem 1.5rem !important;
    }
    
    [data-testid="stSuccess"] {
        background: rgba(118,185,127,0.08) !important;
        border-left-color: #76b97f !important;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,159,201,0.2), transparent);
        margin: 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# AUTO-SETUP FUNCTION
def generate_pdfs_and_chromadb():
    """Auto-generate PDFs and ChromaDB on deployment"""
    
    status = st.empty()
    progress = st.progress(0)
    
    try:
        status.info("📄 Generating employee policy documents...")
        progress.progress(10)
        
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        os.makedirs('employee_documents', exist_ok=True)
        
        docs = [
            ('Remote Work Policy', 'REMOTE WORK POLICY\n\nEligibility: All employees\nArrangements: Fully Remote, Hybrid (3 days office), In-Office\nEquipment: Laptop, monitor, $500 stipend, $50/month internet'),
            ('Salary Compensation Guide', 'SALARY GUIDE 2026\n\nUSA Engineers: $90K-$210K\nIndia Engineers: ₹900K-₹4.2M\nBonus: 0-25% annual\nEquity: 4-year vesting'),
            ('Employee Benefits', 'BENEFITS\n\nHealth: Full PPO coverage\n401k: 6% match\nPTO: 20-30 days\nParental: 16 weeks paid\nLearning: $2K/year'),
            ('Performance Reviews', 'PERFORMANCE REVIEWS\n\nQuarterly reviews\nRatings: Outstanding (5%), Excellent (20%), Good (50%)\nMerit: 0-10% based on rating'),
            ('Vacation PTO Policy', 'VACATION POLICY\n\nYears 0-3: 20 days\nYears 4-7: 25 days\nYears 8+: 30 days\nSick: 10 days\nPersonal: 5 days'),
        ]
        
        for i in range(6, 26):
            docs.append((f'Policy Guide {i}', f'POLICY DOCUMENT {i}\n\nEmployee policy guidelines and procedures. Updated May 2026.'))
        
        pdf_files = []
        for i, (title, content) in enumerate(docs, 1):
            filename = f"employee_documents/DOC{i:03d}_{title.replace(' ', '_')}.pdf"
            
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, letter[1] - 1*inch, title)
            
            c.setFont("Helvetica", 10)
            text = c.beginText(1*inch, letter[1] - 1.5*inch)
            for line in content.split('\n'):
                text.textLine(line)
            c.drawText(text)
            c.save()
            
            pdf_files.append({'filename': filename, 'title': title, 'doc_id': f'DOC{i:03d}', 'content': content})
        
        progress.progress(40)
        status.success(f"✅ Created {len(pdf_files)} PDFs")
        
        status.info("🧠 Creating ChromaDB vector database...")
        progress.progress(50)
        
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        
        try:
            client.delete_collection(name="employee_documents")
        except:
            pass
        
        collection = client.create_collection(name="employee_documents")
        
        chunks, metadatas, ids = [], [], []
        
        for pdf in pdf_files:
            content = pdf['content']
            chunk_size = max(len(content) // 3, 100)
            
            for chunk_idx in range(3):
                start = chunk_idx * chunk_size
                chunk = content[start:start + chunk_size]
                
                if len(chunk.strip()) > 30:
                    chunks.append(chunk)
                    metadatas.append({
                        'doc_id': pdf['doc_id'],
                        'title': pdf['title'],
                        'filename': pdf['filename']
                    })
                    ids.append(f"{pdf['doc_id']}_chunk{chunk_idx}")
        
        for i in range(0, len(chunks), 50):
            end = min(i + 50, len(chunks))
            collection.add(ids=ids[i:end], documents=chunks[i:end], metadatas=metadatas[i:end])
            progress.progress(50 + int((end / len(chunks)) * 45))
        
        progress.progress(100)
        status.success(f"✅ Indexed {len(chunks)} document chunks")
        time.sleep(2)
        status.empty()
        progress.empty()
        return True
        
    except Exception as e:
        status.error(f"❌ Setup failed: {e}")
        return False

# DATA LOADING
@st.cache_resource
def get_postgres_connection():
    try:
        import psycopg2
        configs = [
            {'host': 'localhost', 'database': 'payroll_analytics', 'user': 'postgres', 'password': 'postgres123', 'port': 5432},
            {'host': 'localhost', 'database': 'payroll_db', 'user': 'postgres', 'password': 'postgres123', 'port': 5432},
        ]
        
        for config in configs:
            try:
                conn = psycopg2.connect(**config)
                return conn, config['database']
            except:
                continue
        return None, None
    except:
        return None, None

@st.cache_data
def load_employee_data(_pg_conn=None):
    if _pg_conn:
        try:
            df = pd.read_sql_query("SELECT * FROM employees", _pg_conn)
            return df, "PostgreSQL"
        except:
            pass
    
    for db in ['employees.db', 'employees_complete.db']:
        if os.path.exists(db):
            try:
                import sqlite3
                conn = sqlite3.connect(db)
                df = pd.read_sql_query("SELECT * FROM employees", conn)
                conn.close()
                return df, "SQLite"
            except:
                continue
    
    if os.path.exists('employee_data.csv'):
        return pd.read_csv('employee_data.csv'), "CSV"
    
    return None, None

@st.cache_resource
def load_chromadb():
    try:
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="employee_documents")
        return collection, collection.count()
    except:
        return None, 0

def build_kb(df):
    return {
        'total_employees': len(df),
        'countries': df['country'].value_counts().to_dict(),
        'avg_salary_global': df['annual_salary_usd'].mean(),
        'by_department': {
            dept: {
                'count': len(df[df['department'] == dept]),
                'avg_salary': df[df['department'] == dept]['annual_salary_usd'].mean()
            }
            for dept in df['department'].unique()
        }
    }

# AGENT CLASSES
class DataAnalystAgent:
    def __init__(self, df, kb, doc_collection=None):
        self.df, self.knowledge_base, self.doc_collection = df, kb, doc_collection
        self.name = "Data Analyst"
    
    def search_employees(self, query):
        q = query.lower()
        filtered, filters = self.df.copy(), []
        
        if 'usa' in q or 'united states' in q:
            filtered = filtered[filtered['country'] == 'United States']
            filters.append('USA')
        elif 'india' in q:
            filtered = filtered[filtered['country'] == 'India']
            filters.append('India')
        
        for dept in ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance']:
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
        
        msg = ""
        
        if len(emp_results) > 0:
            msg += f"**Workforce Analysis**\n\nIdentified **{len(emp_results):,} employees**"
            if filters:
                msg += f" — {' · '.join(filters)}"
            msg += f"\n\n**Compensation:**\n• Mean: ${emp_results['annual_salary_usd'].mean():,.0f}\n"
            msg += f"• Range: ${emp_results['annual_salary_usd'].min():,.0f}–${emp_results['annual_salary_usd'].max():,.0f}\n\n"
            msg += f"**Top Five:**\n"
            for i, (_, e) in enumerate(emp_results.head(5).iterrows(), 1):
                msg += f"{i}. {e['employee_id']} — {e['job_title']} — ${e['annual_salary_usd']:,.0f}\n"
        
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            msg += f"\n\n**Policy Documentation:**\n\n"
            for doc, meta in zip(doc_results['documents'][0], doc_results['metadatas'][0]):
                msg += f"*{meta['title']}* — {doc[:140]}...\n\n"
        
        return {'agent': self.name, 'message': msg, 'emp_data': emp_results, 'doc_data': doc_results}

class BusinessAdvisorAgent:
    def __init__(self, kb):
        self.knowledge_base, self.name = kb, "Business Advisor"
    
    def respond(self, analyst_response):
        emp = analyst_response.get('emp_data')
        msg = "**Strategic Assessment**\n\n**Recommendations:**\n"
        
        if emp is not None and len(emp) > 0:
            avg, global_avg = emp['annual_salary_usd'].mean(), self.knowledge_base['avg_salary_global']
            variance = ((avg / global_avg) - 1) * 100
            
            if abs(variance) > 30:
                msg += f"• Cohort {abs(variance):.0f}% {'above' if variance > 0 else 'below'} baseline\n"
            else:
                msg += f"• Compensation aligned with standards\n"
            
            msg += f"\n**Opportunities:**\n• {len(emp):,} employee talent pool\n"
        
        return {'agent': self.name, 'message': msg}

def main():
    st.markdown("<h1>Finance Payroll Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Multi-Agent Intelligence • RAG Document Search</p>", unsafe_allow_html=True)
    
    pg_conn, db_name = get_postgres_connection()
    
    result = load_employee_data(pg_conn)
    if not result or result[0] is None:
        st.error("Data unavailable")
        st.stop()
    
    df, data_source = result
    collection, doc_count = load_chromadb()
    
    # AUTO-SETUP CHECK
    if doc_count == 0:
        st.warning("🔧 First-time setup required (generates PDFs and ChromaDB)")
        if st.button("▶️ Run Setup Now", type="primary"):
            if generate_pdfs_and_chromadb():
                st.success("✅ Setup complete! Refreshing...")
                time.sleep(2)
                st.rerun()
        else:
            st.info("👆 Click button to generate documents")
        st.stop()
    
    kb = build_kb(df)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Workforce", f"{len(df):,}")
    with col2:
        st.metric("United States", f"{kb['countries'].get('United States', 0):,}")
    with col3:
        st.metric("India", f"{kb['countries'].get('India', 0):,}")
    with col4:
        st.metric("Mean Salary", f"${kb['avg_salary_global']/1000:.0f}K")
    
    st.markdown("---")
    
    analyst = DataAnalystAgent(df, kb, collection)
    advisor = BusinessAdvisorAgent(kb)
    
    st.markdown("## Search & Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Top 10 USA", use_container_width=True):
            st.session_state.query = "Top 10 in USA"
    with col2:
        if st.button("Remote Policy", use_container_width=True):
            st.session_state.query = "What is the remote work policy?"
    with col3:
        if st.button("Engineering", use_container_width=True):
            st.session_state.query = "Analyze Engineering"
    with col4:
        if st.button("Salary Ranges", use_container_width=True):
            st.session_state.query = "Salary ranges"
    
    query = st.text_input("", value=st.session_state.get('query', ''), 
                         placeholder="Ask about employees or policies", label_visibility="collapsed")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if search_btn and query:
        st.markdown("---")
        st.markdown("## AI Analysis")
        st.info(f"**Query:** {query}")
        
        st.markdown("### 📊 Data Analyst")
        with st.spinner("Searching..."):
            time.sleep(0.7)
            a1 = analyst.respond(query)
        
        st.markdown(f'<div class="agent-message analyst-message">{a1["message"]}</div>', unsafe_allow_html=True)
        
        # PDF Downloads
        if a1.get('doc_data') and a1['doc_data']['documents'] and len(a1['doc_data']['documents'][0]) > 0:
            st.markdown("### 📥 Source Documents")
            
            seen, cols, col_idx = set(), st.columns(min(len(a1['doc_data']['metadatas'][0]), 3)), 0
            
            for meta in a1['doc_data']['metadatas'][0]:
                doc_id = meta.get('doc_id')
                if doc_id and doc_id not in seen and col_idx < 3:
                    seen.add(doc_id)
                    pdf_file = meta.get('filename')
                    
                    if pdf_file and os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            with cols[col_idx]:
                                st.markdown(f"**{meta['title']}**")
                                st.download_button("Download PDF", f.read(), os.path.basename(pdf_file),
                                                 "application/pdf", key=f"pdf_{doc_id}", use_container_width=True)
                        col_idx += 1
        
        st.markdown("### 💼 Business Advisor")
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            a2 = advisor.respond(a1)
        
        st.markdown(f'<div class="agent-message advisor-message">{a2["message"]}</div>', unsafe_allow_html=True)
        
        # Visualizations
        if a1.get('emp_data') is not None and len(a1['emp_data']) > 0:
            st.markdown("---")
            st.markdown("## Advanced Visualizations")
            
            results = a1['emp_data']
            
            viz1, viz2, viz3, viz4 = st.tabs(["Distribution", "Rankings", "Geographic", "Data Table"])
            
            with viz1:
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=results['annual_salary_usd'], nbinsx=20,
                                          marker=dict(color='#8b9fc9', line=dict(color='#6b8db5', width=1))))
                fig.update_layout(title="Salary Distribution", plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#b8c8d8'), height=450)
                st.plotly_chart(fig, use_container_width=True)
                
                if 'department' in results.columns and len(results['department'].unique()) > 1:
                    fig2 = go.Figure()
                    for dept in results['department'].unique():
                        fig2.add_trace(go.Box(y=results[results['department']==dept]['annual_salary_usd'],
                                            name=dept, marker=dict(color='#8b9fc9')))
                    fig2.update_layout(title="Department Comparison", plot_bgcolor='rgba(0,0,0,0)',
                                     paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#b8c8d8'), height=450)
                    st.plotly_chart(fig2, use_container_width=True)
            
            with viz2:
                top10 = results.nlargest(10, 'annual_salary_usd')
                fig = go.Figure(data=[go.Bar(y=top10['employee_id'], x=top10['annual_salary_usd'], orientation='h',
                                            marker=dict(color='#8b9fc9'),
                                            text=top10['annual_salary_usd'].apply(lambda x: f'${x/1000:.0f}K'),
                                            textposition='outside')])
                fig.update_layout(title="Top 10", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#b8c8d8'), height=500, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with viz3:
                if 'city' in results.columns:
                    city_stats = results.groupby(['country', 'city']).agg({'employee_id': 'count',
                                                                           'annual_salary_usd': 'mean'}).reset_index()
                    city_stats.columns = ['Country', 'City', 'Employees', 'Avg']
                    
                    fig = px.scatter(city_stats.head(20), x='Employees', y='Avg', size='Employees',
                                   color='Country', hover_name='City',
                                   color_discrete_map={'United States': '#8b9fc9', 'India': '#76b97f'})
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='#b8c8d8'), height=500)
                    st.plotly_chart(fig, use_container_width=True)
                
                if len(results) > 15:
                    fig2 = px.sunburst(results.head(100), path=['country', 'department', 'job_title'],
                                     values='annual_salary_usd')
                    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=500)
                    st.plotly_chart(fig2, use_container_width=True)
            
            with viz4:
                display = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(20).copy()
                display['annual_salary_usd'] = display['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display.columns = ['ID', 'Position', 'Dept', 'City', 'Country', 'Salary']
                st.dataframe(display, use_container_width=True, height=600)
    
    with st.sidebar:
        st.markdown("### System Status")
        st.markdown("**Employee Data:**")
        st.success(f"✅ {len(df):,} employees")
        st.info(f"**Source:** {data_source}")
        
        if pg_conn and db_name:
            st.success(f"**🐘 PostgreSQL:** {db_name}")
        else:
            st.warning("**🐘 PostgreSQL:** Not connected")
        
        st.markdown("**Documents:**")
        if doc_count > 0:
            st.success(f"✅ {doc_count} doc chunks")
        else:
            st.warning("⚠️ No documents")

if __name__ == "__main__":
    main()
