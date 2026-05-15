"""
POSTGRESQL-INTEGRATED ANALYTICS PLATFORM
=========================================

Complete platform that uses PostgreSQL for data storage:
✅ Queries PostgreSQL for employee data
✅ Multi-agent AI system
✅ RAG document search with ChromaDB
✅ PDF downloads
✅ Beautiful UI

Run: streamlit run postgres_platform.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
import time
import os

# Page config
st.set_page_config(page_title="PostgreSQL Analytics", page_icon="🐘", layout="wide")

# Beautiful CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d1b2a 40%, #1b2838 100%);
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #fff 0%, #a5b8cf 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        border-bottom: 4px solid transparent;
        border-image: linear-gradient(90deg, #6b8db5 0%, transparent 100%);
        border-image-slice: 1;
        padding-bottom: 1.5rem !important;
    }
    
    .agent-message {
        padding: 2.5rem;
        margin: 2rem 0;
        border-radius: 20px;
        border-left: 6px solid;
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.50);
        transition: all 0.6s ease;
    }
    
    .agent-message:hover {
        transform: translateX(10px);
        box-shadow: 0 24px 72px rgba(0,0,0,0.60);
    }
    
    .analyst-message {
        background: linear-gradient(135deg, rgba(93,127,165,0.22) 0%, rgba(61,90,128,0.14) 100%);
        border-left-color: #6b8db5;
        border: 2px solid rgba(93,127,165,0.30);
    }
    
    .advisor-message {
        background: linear-gradient(135deg, rgba(76,175,80,0.22) 0%, rgba(56,142,60,0.14) 100%);
        border-left-color: #66bb6a;
        border: 2px solid rgba(76,175,80,0.30);
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.04) 100%);
        border: 2px solid rgba(255,255,255,0.14);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 36px rgba(0,0,0,0.4);
        transition: all 0.5s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 60px rgba(93,127,165,0.45);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #5d7fa5 0%, #3d5a80 100%) !important;
        color: #fff !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        box-shadow: 0 8px 24px rgba(93,127,165,0.4) !important;
        transition: all 0.4s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 16px 40px rgba(93,127,165,0.6) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #0a1628 !important;
        font-weight: 800 !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING WITH POSTGRESQL
# ============================================================================

@st.cache_resource
def get_postgres_connection():
    """Connect to PostgreSQL"""
    try:
        import psycopg2
        
        # Connection parameters
        conn = psycopg2.connect(
            host='localhost',
            database='payroll_analytics',  # or payroll_db
            user='postgres',
            password='postgres123',  # The password you just set!
            port=5432
        )
        
        return conn, None, "payroll_analytics"
    
    except Exception as e:
        return None, str(e), None

@st.cache_data
def load_employee_data(_conn):
    """Load employees from PostgreSQL or CSV fallback"""
    
    if _conn is not None:
        try:
            df = pd.read_sql_query("SELECT * FROM employees", _conn)
            return df, "PostgreSQL ✅"
        except Exception as e:
            st.warning(f"PostgreSQL query failed: {e}")
    
    # Fallback to CSV
    if os.path.exists('employee_data.csv'):
        return pd.read_csv('employee_data.csv'), "CSV (fallback)"
    
    return None, None

@st.cache_resource
def load_chromadb():
    """Load ChromaDB"""
    try:
        import chromadb
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="employee_documents")
        return collection, collection.count()
    except:
        return None, 0

def build_kb(df):
    """Build knowledge base"""
    return {
        'total_employees': len(df),
        'avg_salary_global': df['annual_salary_usd'].mean(),
        'by_department': {
            dept: {
                'count': len(df[df['department'] == dept]),
                'avg_salary': df[df['department'] == dept]['annual_salary_usd'].mean()
            }
            for dept in df['department'].unique()
        }
    }

# ============================================================================
# AGENT CLASSES
# ============================================================================

class DataAnalystAgent:
    def __init__(self, df, kb, doc_collection, pg_conn=None):
        self.df = df
        self.kb = kb
        self.doc_collection = doc_collection
        self.pg_conn = pg_conn
        self.name = "📊 Data Analyst Agent"
    
    def search_employees(self, query):
        """Search employees - uses PostgreSQL if available"""
        q = query.lower()
        
        # If PostgreSQL is available, use SQL
        if self.pg_conn is not None:
            try:
                sql = "SELECT * FROM employees WHERE 1=1"
                params = []
                
                if 'usa' in q:
                    sql += " AND country = %s"
                    params.append('United States')
                elif 'india' in q:
                    sql += " AND country = %s"
                    params.append('India')
                
                for dept in ['Engineering', 'HR', 'Sales', 'Marketing']:
                    if dept.lower() in q:
                        sql += " AND department = %s"
                        params.append(dept)
                        break
                
                if 'manager' in q:
                    sql += " AND job_title ILIKE %s"
                    params.append('%Manager%')
                
                over_match = re.search(r'over\s+(\d+)k?', q)
                if over_match:
                    sql += " AND annual_salary_usd > %s"
                    params.append(int(over_match.group(1)) * 1000)
                
                sql += " ORDER BY annual_salary_usd DESC"
                
                if 'top' in q:
                    top_match = re.search(r'top\s+(\d+)', q)
                    limit = int(top_match.group(1)) if top_match else 10
                    sql += f" LIMIT {limit}"
                
                results = pd.read_sql_query(sql, self.pg_conn, params=params if params else None)
                return results, ['PostgreSQL Query']
            
            except Exception as e:
                st.warning(f"PostgreSQL query failed: {e}, using pandas")
        
        # Fallback to pandas filtering
        filtered = self.df.copy()
        filters = []
        
        if 'usa' in q:
            filtered = filtered[filtered['country'] == 'United States']
            filters.append('USA')
        elif 'india' in q:
            filtered = filtered[filtered['country'] == 'India']
            filters.append('India')
        
        for dept in ['Engineering', 'HR', 'Sales']:
            if dept.lower() in q:
                filtered = filtered[filtered['department'] == dept]
                filters.append(dept)
                break
        
        if 'manager' in q:
            filtered = filtered[filtered['job_title'].str.contains('Manager', case=False, na=False)]
            filters.append('Manager')
        
        filtered = filtered.sort_values('annual_salary_usd', ascending=False)
        
        if 'top' in q:
            filtered = filtered.head(10)
        
        return filtered, filters
    
    def search_documents(self, query):
        """Search documents via ChromaDB"""
        if not self.doc_collection:
            return None
        try:
            return self.doc_collection.query(query_texts=[query], n_results=3)
        except:
            return None
    
    def respond(self, query):
        """Generate response"""
        emp_results, filters = self.search_employees(query)
        doc_results = self.search_documents(query)
        
        msg = ""
        
        if len(emp_results) > 0:
            msg += f"**📊 Employee Data:**\n\nFound **{len(emp_results)} employees**"
            if filters:
                msg += f" ({' | '.join(filters)})"
            msg += f"\n\n- Average: ${emp_results['annual_salary_usd'].mean():,.0f}\n\n**Top 5:**\n"
            for i, (_, e) in enumerate(emp_results.head(5).iterrows(), 1):
                msg += f"{i}. {e['employee_id']} - {e['job_title']} - ${e['annual_salary_usd']:,.0f}\n"
        
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            msg += f"\n\n**📚 Policy Documents:**\n\n"
            for i, (doc, meta) in enumerate(zip(doc_results['documents'][0], doc_results['metadatas'][0]), 1):
                msg += f"📄 *{meta['title']}*: {doc[:150]}...\n\n"
        
        return {
            'agent': self.name,
            'message': msg,
            'emp_data': emp_results,
            'doc_data': doc_results
        }

class BusinessAdvisorAgent:
    def __init__(self, kb):
        self.kb = kb
        self.name = "💼 Business Advisor Agent"
    
    def respond(self, analyst_response):
        emp = analyst_response.get('emp_data')
        msg = "Based on findings:\n\n**💡 Recommendations:**\n"
        
        if emp is not None and len(emp) > 0:
            avg = emp['annual_salary_usd'].mean()
            global_avg = self.kb['avg_salary_global']
            
            if avg > global_avg * 1.3:
                msg += f"- Above company average (${avg:,.0f} vs ${global_avg:,.0f})\n"
            else:
                msg += f"- Aligned with company averages\n"
            
            msg += f"\n**🎯 Opportunities:**\n- {len(emp)} employee talent pool\n"
        
        return {'agent': self.name, 'message': msg}

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.markdown("# 🐘 PostgreSQL Analytics Platform")
    st.markdown("**Multi-Agent AI + PostgreSQL + ChromaDB RAG**")
    st.markdown("---")
    
    # Connect to PostgreSQL
    pg_conn, pg_error, db_name = get_postgres_connection()
    
    # Load data
    df, data_source = load_employee_data(pg_conn)
    
    if df is None:
        st.error("❌ No employee data found")
        st.stop()
    
    collection, doc_count = load_chromadb()
    kb = build_kb(df)
    
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("👥 Employees", f"{len(df):,}")
    with col2:
        st.metric("🇺🇸 USA", f"{len(df[df['country']=='United States']):,}")
    with col3:
        st.metric("🇮🇳 India", f"{len(df[df['country']=='India']):,}")
    with col4:
        st.metric("💰 Avg", f"${df['annual_salary_usd'].mean()/1000:.0f}K")
    with col5:
        st.metric("📄 Docs", f"{doc_count}" if doc_count > 0 else "0")
    
    st.markdown("---")
    
    # Initialize agents
    analyst = DataAnalystAgent(df, kb, collection, pg_conn)
    advisor = BusinessAdvisorAgent(kb)
    
    st.markdown("## 🔍 Ask the AI Agents")
    
    # Quick buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🇺🇸 Top 10 USA", use_container_width=True):
            st.session_state.q = "Top 10 in USA"
    with col2:
        if st.button("📚 Remote Policy", use_container_width=True):
            st.session_state.q = "What is the remote work policy?"
    with col3:
        if st.button("💰 Salaries", use_container_width=True):
            st.session_state.q = "Engineering salary ranges"
    with col4:
        if st.button("🎯 Combined", use_container_width=True):
            st.session_state.q = "Engineering salaries vs policy"
    
    query = st.text_input(
        "Your question:",
        value=st.session_state.get('q', ''),
        placeholder="e.g., What are Engineering Manager salaries and what does policy say?",
    )
    
    if st.button("🚀 Search & Analyze", type="primary"):
        if query:
            st.markdown("---")
            st.markdown("## 💬 AI Agent Conversation")
            
            st.info(f"**You asked:** {query}")
            
            # Agent 1
            st.markdown("### 📊 Data Analyst Agent")
            with st.spinner("🔍 Searching PostgreSQL and documents..."):
                time.sleep(0.7)
                a1 = analyst.respond(query)
            
            st.markdown(f'<div class="agent-message analyst-message">{a1["message"]}</div>', unsafe_allow_html=True)
            
            # PDF Downloads
            if a1.get('doc_data') and a1['doc_data']['documents'] and len(a1['doc_data']['documents'][0]) > 0:
                st.markdown("#### 📥 Download Source Documents")
                
                seen = set()
                for meta in a1['doc_data']['metadatas'][0]:
                    doc_id = meta.get('doc_id')
                    if doc_id and doc_id not in seen:
                        seen.add(doc_id)
                        
                        pdf_file = meta.get('filename')
                        if pdf_file and os.path.exists(pdf_file):
                            with open(pdf_file, 'rb') as f:
                                pdf_data = f.read()
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**📄 {meta['title']}**")
                            with col2:
                                st.download_button(
                                    label="📥 Download",
                                    data=pdf_data,
                                    file_name=os.path.basename(pdf_file),
                                    mime="application/pdf",
                                    key=f"dl_{doc_id}",
                                    use_container_width=True
                                )
            
            # Agent 2
            st.markdown("### 💼 Business Advisor Agent")
            with st.spinner("🤖 Analyzing..."):
                time.sleep(0.5)
                a2 = advisor.respond(a1)
            
            st.markdown(f'<div class="agent-message advisor-message">{a2["message"]}</div>', unsafe_allow_html=True)
            
            # Data table
            if a1.get('emp_data') is not None and len(a1['emp_data']) > 0:
                st.markdown("---")
                st.markdown("## 📊 Employee Details")
                
                results = a1['emp_data']
                display = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(10).copy()
                display['annual_salary_usd'] = display['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display.columns = ['ID', 'Job', 'Dept', 'City', 'Country', 'Salary']
                st.dataframe(display, use_container_width=True, height=400)
                
                # Chart
                if len(results) >= 5:
                    top10 = results.nlargest(10, 'annual_salary_usd')
                    
                    fig = go.Figure(data=[go.Bar(
                        y=top10['employee_id'].head(10),
                        x=top10['annual_salary_usd'].head(10),
                        orientation='h',
                        marker=dict(color='#5d7fa5'),
                        text=top10['annual_salary_usd'].head(10).apply(lambda x: f'${x:,.0f}'),
                        textposition='outside'
                    )])
                    
                    fig.update_layout(
                        title="Top 10 by Salary",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#fff'),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 System Status")
        
        st.markdown("**Employee Data:**")
        st.success(f"✅ {len(df):,} employees")
        st.info(f"**Source:** {data_source}")
        
        if pg_conn:
            st.success(f"**🐘 PostgreSQL:** {db_name}")
        else:
            st.warning("**🐘 PostgreSQL:** Not connected")
            if pg_error:
                with st.expander("Error details"):
                    st.code(pg_error)
        
        st.markdown("**Document Search:**")
        if doc_count > 0:
            st.success(f"✅ {doc_count} chunks")
        else:
            st.warning("⚠️ No documents")

if __name__ == "__main__":
    main()
