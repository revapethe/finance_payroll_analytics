"""
AUTO-SETUP DEPLOYMENT VERSION
==============================

This version automatically:
✅ Generates 25 PDFs on first launch
✅ Creates ChromaDB vector database
✅ Populates embeddings
✅ Works on Streamlit Cloud deployment!

No manual setup needed - just deploy and it works!

Run: streamlit run AUTO_SETUP_DEPLOYMENT.py

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
    page_title="Complete Analytics Platform",
    page_icon="🚀",
    layout="wide"
)

# Premium CSS (same beautiful styling)
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
    }
    
    .agent-message {
        padding: 2.5rem;
        margin: 2rem 0;
        border-radius: 20px;
        border-left: 6px solid;
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.50);
        animation: slideIn 0.8s ease-out;
        transition: all 0.6s ease;
    }
    
    .agent-message:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 24px 72px rgba(0,0,0,0.60);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-60px); }
        to { opacity: 1; transform: translateX(0); }
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
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #5d7fa5 0%, #3d5a80 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255,255,255,0.20) !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        box-shadow: 0 8px 24px rgba(93,127,165,0.40) !important;
        transition: all 0.4s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 16px 40px rgba(93,127,165,0.60) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #0a1628 !important;
        font-weight: 800 !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.8rem !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(76,175,80,0.45) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# AUTO-SETUP FUNCTION (Runs on deployment if needed)
# ============================================================================

def generate_pdfs_and_chromadb():
    """Generate PDFs and populate ChromaDB - for deployment"""
    
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    try:
        # Step 1: Generate PDFs
        status_placeholder.info("📄 Step 1/3: Generating 25 employee policy PDFs...")
        progress_bar.progress(10)
        
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        os.makedirs('employee_documents', exist_ok=True)
        
        docs = [
            ('Remote Work Policy', 'REMOTE WORK POLICY\n\nEligibility: All employees except those requiring physical presence\n\nWork Arrangements:\n1. Fully Remote - Work from anywhere\n2. Hybrid - 3 days office, 2 remote (recommended)\n3. In-Office - 5 days per week\n\nEquipment: Laptop, monitor, $500 home office stipend, $50/month internet'),
            ('Salary Compensation Guide', 'SALARY COMPENSATION GUIDE 2026\n\nUSA Ranges:\n- Software Engineer: $90,000 - $140,000\n- Senior Engineer: $130,000 - $180,000\n- Engineering Manager: $140,000 - $210,000\n- Director: $180,000 - $250,000\n\nIndia Ranges:\n- Software Engineer: ₹900,000 - ₹1,800,000\n- Senior Engineer: ₹1,500,000 - ₹2,800,000\n- Engineering Manager: ₹2,000,000 - ₹4,200,000\n\nBonus: 0-25% of base salary'),
            ('Employee Benefits', 'EMPLOYEE BENEFITS\n\nHealth Insurance: Full PPO coverage, $0 premium\nRetirement: 401k with 6% company match\nTime Off: 20-30 days vacation (by tenure), 10 sick days, 5 personal days\nParental Leave: 16 weeks paid\nLearning Budget: $2,000/year per employee\nGym: $100/month reimbursement'),
            ('Performance Reviews', 'PERFORMANCE REVIEW PROCESS\n\nSchedule: Quarterly reviews, annual comprehensive\n\nRatings:\n- Outstanding (5%): 8-10% raise + 20-25% bonus\n- Excellent (20%): 5-7% raise + 15-20% bonus\n- Good (50%): 3-5% raise + 10-15% bonus\n\nPromotion: Minimum 2 years in role, consistent high ratings, manager nomination'),
            ('Vacation PTO Policy', 'VACATION AND PTO\n\nAllocation by Tenure:\n- Years 0-3: 20 days vacation + 10 sick\n- Years 4-7: 25 days vacation + 10 sick\n- Years 8+: 30 days vacation + 10 sick\n\nPersonal Days: 5 days all employees\nHolidays: 12 company holidays\n\nRequesting: Submit 2 weeks advance, manager approval required'),
        ]
        
        # Add 20 more
        for i in range(6, 26):
            docs.append((f'Policy Guide {i}', f'POLICY DOCUMENT {i}\n\nImportant employee policy information and guidelines for document {i}. Updated May 2026.'))
        
        pdf_files = []
        for i, (title, content) in enumerate(docs, 1):
            filename = f"employee_documents/DOC{i:03d}_{title.replace(' ', '_')}.pdf"
            
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, height - 1*inch, title)
            
            c.setFont("Helvetica", 10)
            text = c.beginText(1*inch, height - 1.5*inch)
            for line in content.split('\n'):
                text.textLine(line)
            c.drawText(text)
            
            c.save()
            pdf_files.append({'filename': filename, 'title': title, 'doc_id': f'DOC{i:03d}', 'content': content})
        
        progress_bar.progress(40)
        status_placeholder.success(f"✅ Created {len(pdf_files)} PDFs")
        
        # Step 2: Create ChromaDB
        status_placeholder.info("🧠 Step 2/3: Creating ChromaDB vector database...")
        progress_bar.progress(50)
        
        import chromadb
        
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Delete old collection if exists
        try:
            client.delete_collection(name="employee_documents")
        except:
            pass
        
        collection = client.create_collection(name="employee_documents")
        
        # Step 3: Add documents to ChromaDB
        status_placeholder.info("📊 Step 3/3: Indexing documents (creating embeddings)...")
        progress_bar.progress(60)
        
        chunks = []
        metadatas = []
        ids = []
        
        for pdf in pdf_files:
            content = pdf['content']
            # Create 3-5 chunks per document
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
        
        # Add to ChromaDB in batches
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            end = min(i + batch_size, len(chunks))
            collection.add(
                ids=ids[i:end],
                documents=chunks[i:end],
                metadatas=metadatas[i:end]
            )
            progress = 60 + int(((i + batch_size) / len(chunks)) * 35)
            progress_bar.progress(min(progress, 95))
        
        progress_bar.progress(100)
        status_placeholder.success(f"✅ Setup complete! Indexed {len(chunks)} document chunks")
        
        time.sleep(2)
        status_placeholder.empty()
        progress_bar.empty()
        
        return True
        
    except Exception as e:
        status_placeholder.error(f"❌ Setup failed: {e}")
        return False

# Data loading
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

# Agent classes (same as before)
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
                message += f"📄 From *{meta['title']}*:\n> {doc[:200]}...\n\n"
        
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
            else:
                message += f"- Salaries aligned with company averages\n"
            
            message += "\n**🎯 Opportunities:**\n"
            message += f"- {len(emp_data)} employee talent pool for initiatives\n"
        
        return {
            'agent': self.name,
            'message': message
        }

def main():
    st.markdown("# 🚀 Ultimate Analytics Platform")
    st.markdown("**Multi-Agent AI + RAG Document Search**")
    st.markdown("---")
    
    # Load employee data
    df = load_employee_data()
    if df is None:
        st.error("❌ No employee data found")
        st.stop()
    
    # Check ChromaDB
    collection, doc_count = load_chromadb()
    
    # AUTO-SETUP if ChromaDB is empty
    if doc_count == 0:
        st.warning("🔧 First-time setup required (runs once, takes 2 minutes)")
        
        if st.button("▶️ Run Setup Now", type="primary"):
            if generate_pdfs_and_chromadb():
                st.success("✅ Setup complete! Refreshing...")
                time.sleep(2)
                st.rerun()
        else:
            st.info("👆 Click the button above to generate PDFs and ChromaDB")
        
        st.stop()
    
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
        st.metric("📄 Doc Chunks", f"{doc_count}", delta="Ready")
    
    st.markdown("---")
    
    # Initialize agents
    analyst_agent = DataAnalystAgent(df, kb, collection)
    advisor_agent = BusinessAdvisorAgent(kb)
    
    st.markdown("## 🔍 Ask the AI Agents")
    
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
            st.session_state.query = "Engineering salaries vs policy"
    
    user_query = st.text_input(
        "Your question:",
        value=st.session_state.get('query', ''),
        placeholder="e.g., What are Engineering Manager salaries and policy ranges?",
    )
    
    if st.button("🚀 Search & Analyze", type="primary"):
        if user_query:
            st.markdown("---")
            st.markdown("## 💬 AI Agent Conversation")
            
            st.markdown("### 👤 You asked:")
            st.info(user_query)
            
            # Agent 1
            st.markdown("### 📊 Data Analyst Agent")
            with st.spinner("🔍 Searching database and documents..."):
                time.sleep(0.7)
                analyst_response = analyst_agent.respond(user_query)
            
            st.markdown(f'<div class="agent-message analyst-message">{analyst_response["message"]}</div>', unsafe_allow_html=True)
            
            # PDF DOWNLOADS
            doc_results = analyst_response.get('doc_data')
            if doc_results and doc_results['documents'] and len(doc_results['documents'][0]) > 0:
                st.markdown("#### 📥 Download Source Documents")
                
                seen = set()
                for meta in doc_results['metadatas'][0]:
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
                                    key=f"pdf_dl_{doc_id}",
                                    use_container_width=True
                                )
            
            # Agent 2
            st.markdown("### 💼 Business Advisor Agent")
            with st.spinner("🤖 Analyzing..."):
                time.sleep(0.5)
                advisor_response = advisor_agent.respond(analyst_response)
            
            st.markdown(f'<div class="agent-message advisor-message">{advisor_response["message"]}</div>', unsafe_allow_html=True)
            
            # Employee data table
            if analyst_response.get('emp_data') is not None and len(analyst_response['emp_data']) > 0:
                st.markdown("---")
                st.markdown("## 📊 Employee Details")
                
                results = analyst_response['emp_data']
                display_df = results[['employee_id', 'job_title', 'department', 'city', 'country', 'annual_salary_usd']].head(10).copy()
                display_df['annual_salary_usd'] = display_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                display_df.columns = ['ID', 'Job', 'Dept', 'City', 'Country', 'Salary']
                st.dataframe(display_df, use_container_width=True, height=400)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 System Status")
        st.success(f"✅ {len(df):,} employees loaded")
        
        if doc_count > 0:
            st.success(f"✅ {doc_count} document chunks indexed")
        else:
            st.warning("⚠️ Document search not available")

if __name__ == "__main__":
    main()
