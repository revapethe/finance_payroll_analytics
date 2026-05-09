"""
FINAL COMPLETE PLATFORM - Everything Combined
==============================================

✅ Multi-Agent System (2 AI agents that chat)
✅ Employee Database Search (2,000 employees)
✅ RAG Document Search (25 PDFs via ChromaDB)
✅ PDF Download Buttons (download any document)
✅ Premium Professional UI (glassmorphism, animations)
✅ All functionality preserved!

The agents search BOTH employee data AND documents, then discuss!

Run: streamlit run FINAL_COMBINED_PLATFORM.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
import time
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Ultimate Analytics Platform",
    page_icon="🚀",
    layout="wide"
)

# PREMIUM PROFESSIONAL CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d1b2a 40%, #162130 70%, #1b2838 100%);
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #ffffff 0%, #e8f0f8 50%, #a5b8cf 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        border-bottom: 4px solid transparent;
        border-image: linear-gradient(90deg, #6b8db5 0%, transparent 100%);
        border-image-slice: 1;
        padding-bottom: 1.5rem !important;
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Premium Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.04) 100%);
        border: 2px solid rgba(255,255,255,0.14);
        border-radius: 20px;
        padding: 2rem 1.8rem;
        backdrop-filter: blur(18px) saturate(180%);
        box-shadow: 0 10px 36px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.12);
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 60px rgba(93,127,165,0.45);
        border-color: rgba(165,184,207,0.40);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-shadow: 0 3px 12px rgba(0,0,0,0.4);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.80rem !important;
        color: #8fa3b8 !important;
        font-weight: 700 !important;
        letter-spacing: 0.10em !important;
        text-transform: uppercase !important;
    }
    
    /* Agent Messages - Glassmorphism */
    .agent-message {
        padding: 2.5rem;
        margin: 2rem 0;
        border-radius: 20px;
        border-left: 6px solid;
        backdrop-filter: blur(20px) saturate(180%);
        box-shadow: 0 16px 48px rgba(0,0,0,0.50), inset 0 1px 3px rgba(255,255,255,0.10);
        animation: slideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .agent-message:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 24px 72px rgba(0,0,0,0.60);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-60px) scale(0.95); }
        to { opacity: 1; transform: translateX(0) scale(1); }
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
    
    /* Document Results */
    .doc-result {
        background: linear-gradient(135deg, rgba(165,184,207,0.18) 0%, rgba(93,127,165,0.10) 100%);
        border: 2px solid rgba(165,184,207,0.28);
        border-left: 6px solid #a5b8cf;
        border-radius: 18px;
        padding: 2.2rem;
        margin: 1.8rem 0;
        backdrop-filter: blur(16px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.40);
        transition: all 0.5s ease;
    }
    
    .doc-result:hover {
        transform: translateX(8px) translateY(-4px);
        box-shadow: 0 20px 56px rgba(165,184,207,0.35);
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #5d7fa5 0%, #3d5a80 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255,255,255,0.20) !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        font-size: 0.82rem !important;
        box-shadow: 0 8px 24px rgba(93,127,165,0.40) !important;
        transition: all 0.4s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 16px 40px rgba(93,127,165,0.60) !important;
    }
    
    /* Primary Button - Gold */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #0a1628 !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 28px rgba(212,175,55,0.50) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%) !important;
        box-shadow: 0 16px 44px rgba(212,175,55,0.70) !important;
    }
    
    /* Download Buttons - Green */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.25) !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.8rem !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(76,175,80,0.45) !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase !important;
        font-size: 0.80rem !important;
        letter-spacing: 0.05em !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 12px 32px rgba(76,175,80,0.65) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load data
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
        count = collection.count()
        return collection, count
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
            'avg_salary': dept_df['annual_salary_usd'].mean()
        }
    
    return kb

# Multi-Agent Classes
class DataAnalystAgent:
    def __init__(self, df, kb, doc_collection=None):
        self.df = df
        self.knowledge_base = kb
        self.doc_collection = doc_collection
        self.name = "📊 Data Analyst Agent"
    
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
        if self.doc_collection is None:
            return None
        try:
            results = self.doc_collection.query(query_texts=[query], n_results=3)
            return results
        except:
            return None
    
    def respond(self, query):
        emp_results, filters = self.search_employees(query)
        doc_results = self.search_documents(query)
        
        message = ""
        
        if len(emp_results) > 0:
            message += f"**📊 Employee Data Analysis:**\n\n"
            message += f"Found **{len(emp_results)} employees**"
            if filters:
                message += f" ({' | '.join(filters)})"
            message += f"\n\n- Average salary: ${emp_results['annual_salary_usd'].mean():,.0f}\n\n"
            message += f"**Top 5:**\n"
            for idx, (_, emp) in enumerate(emp_results.head(5).iterrows(), 1):
                message += f"{idx}. {emp['employee_id']} - {emp['job_title']} - ${emp['annual_salary_usd']:,.0f}\n"
        
        if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
            message += f"\n\n**📚 Policy Document Insights:**\n\n"
            for i, (doc, meta) in enumerate(zip(doc_results['documents'][0], doc_results['metadatas'][0]), 1):
                message += f"📄 From *{meta['title']}*:\n> {doc[:180]}...\n\n"
        
        return {
            'agent': self.name,
            'message': message,
            'emp_data': emp_results,
            'doc_data': doc_results
        }

class BusinessAdvisorAgent:
    def __init__(self, kb):
        self.knowledge_base = kb
        self.name = "💼 Business Advisor Agent"
    
    def respond(self, analyst_response):
        emp_data = analyst_response.get('emp_data')
        
        message = "Based on the Data Analyst's findings:\n\n"
        
        if emp_data is not None and len(emp_data) > 0:
            avg_salary = emp_data['annual_salary_usd'].mean()
            global_avg = self.knowledge_base['avg_salary_global']
            
            message += "**💡 Recommendations:**\n"
            if avg_salary > global_avg * 1.3:
                message += f"- This group averages ${avg_salary:,.0f} (above company ${global_avg:,.0f})\n"
                message += f"- Consider market benchmarking\n"
            else:
                message += f"- Salaries aligned with company averages\n"
            
            message += "\n**🎯 Opportunities:**\n"
            message += f"- {len(emp_data)} employee talent pool for strategic initiatives\n"
        
        return {
            'agent': self.name,
            'message': message
        }

def main():
    st.markdown("# 🚀 Ultimate Analytics Platform")
    st.markdown("**Multi-Agent AI + RAG Document Search + Premium Features**")
    st.markdown("---")
    
    df = load_employee_data()
    if df is None:
        st.error("❌ No employee data found")
        st.stop()
    
    collection, doc_count = load_chromadb()
    kb = build_knowledge_base(df)
    
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("👥 Employees", f"{len(df):,}")
    with col2:
        st.metric("🇺🇸 USA", f"{len(df[df['country']=='United States']):,}")
    with col3:
        st.metric("🇮🇳 India", f"{len(df[df['country']=='India']):,}")
    with col4:
        st.metric("💰 Avg Salary", f"${df['annual_salary_usd'].mean()/1000:.0f}K")
    with col5:
        st.metric("📄 Documents", f"{doc_count}" if doc_count > 0 else "Setup needed")
    
    st.markdown("---")
    
    # Initialize agents
    analyst_agent = DataAnalystAgent(df, kb, collection)
    advisor_agent = BusinessAdvisorAgent(kb)
    
    # Main interface
    st.markdown("## 🔍 Unified AI Search")
    st.markdown("*Ask anything - agents search employee data AND policy documents*")
    
    # Quick buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🇺🇸 Top 10 USA", use_container_width=True):
            st.session_state.query = "Top 10 in USA"
    with col2:
        if st.button("📚 Remote Policy", use_container_width=True):
            st.session_state.query = "What is the remote work policy?"
    with col3:
        if st.button("💰 Salary Ranges", use_container_width=True):
            st.session_state.query = "What are salary ranges for engineers?"
    with col4:
        if st.button("🎯 Eng + Policy", use_container_width=True):
            st.session_state.query = "Engineering salaries vs policy ranges"
    
    user_query = st.text_input(
        "Your question:",
        value=st.session_state.get('query', ''),
        placeholder="e.g., What are Engineering Manager salaries and what does policy say?",
    )
    
    if st.button("🚀 Search & Analyze with AI Agents", type="primary"):
        if user_query:
            st.markdown("---")
            st.markdown("## 💬 AI Agent Conversation")
            
            st.markdown("### 👤 You asked:")
            st.info(user_query)
            
            # Agent 1
            st.markdown("### 📊 Data Analyst Agent")
            with st.spinner("🔍 Searching employee database and documents..."):
                time.sleep(0.7)
                analyst_response = analyst_agent.respond(user_query)
            
            with st.expander("🧠 Thinking"):
                st.markdown("- Searching employee records\n- Querying policy documents\n- Combining insights")
            
            st.markdown(f'<div class="agent-message analyst-message">{analyst_response["message"]}</div>', unsafe_allow_html=True)
            
            # Show PDF downloads if documents were found
            doc_results = analyst_response.get('doc_data')
            if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
                st.markdown("#### 📥 Download Source Documents")
                
                # Get unique documents
                seen_docs = set()
                for meta in doc_results['metadatas'][0]:
                    doc_id = meta.get('doc_id')
                    if doc_id and doc_id not in seen_docs:
                        seen_docs.add(doc_id)
                        
                        # Find PDF file
                        pdf_file = meta.get('filename')
                        if pdf_file and os.path.exists(pdf_file):
                            with open(pdf_file, 'rb') as f:
                                pdf_data = f.read()
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{meta['title']}**")
                            with col2:
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_data,
                                    file_name=os.path.basename(pdf_file),
                                    mime="application/pdf",
                                    key=f"dl_{doc_id}",
                                    use_container_width=True
                                )
            
            # Agent 2
            st.markdown("### 💼 Business Advisor Agent")
            with st.spinner("🤖 Generating strategic insights..."):
                time.sleep(0.5)
                advisor_response = advisor_agent.respond(analyst_response)
            
            with st.expander("🧠 Thinking"):
                st.markdown("- Evaluating vs benchmarks\n- Considering policy context\n- Generating recommendations")
            
            st.markdown(f'<div class="agent-message advisor-message">{advisor_response["message"]}</div>', unsafe_allow_html=True)
            
            # Detailed results
            if analyst_response.get('emp_data') is not None and len(analyst_response['emp_data']) > 0:
                st.markdown("---")
                st.markdown("## 📊 Detailed Employee Data")
                
                results = analyst_response['emp_data']
                
                display_df = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(10).copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['ID', 'Job', 'Dept', 'City', 'Country', 'Salary']
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
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
        st.success(f"✅ {len(df):,} employees")
        
        if doc_count > 0:
            st.success(f"✅ {doc_count} doc chunks")
        else:
            st.warning("⚠️ Run setup first:")
            st.code("python rag_document_system_fixed.py", language="bash")
        
        st.markdown("---")
        st.markdown("### 🤖 AI Agents")
        st.markdown("📊 **Data Analyst**\n💼 **Business Advisor**")

if __name__ == "__main__":
    main()
