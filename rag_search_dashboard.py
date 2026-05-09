"""
RAG DOCUMENT SEARCH DASHBOARD
==============================

Beautiful web interface to search through 25 employee PDFs
using ChromaDB and RAG pipeline.

Run: streamlit run rag_search_dashboard.py

Author: Analytics Team
Date: May 2026
"""

import streamlit as st
import chromadb
import os
import sqlite3
import json
import pandas as pd

# Page config
st.set_page_config(
    page_title="Document Search - RAG",
    page_icon="📚",
    layout="wide"
)

# Beautiful CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d1b2a 50%, #1b2838 100%);
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        background: linear-gradient(135deg, #f0f4f8 0%, #a5b8cf 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.5rem !important;
    }
    
    .doc-result {
        background: linear-gradient(135deg, rgba(93,127,165,0.12) 0%, rgba(61,90,128,0.06) 100%);
        border: 1px solid rgba(93,127,165,0.2);
        border-left: 4px solid #5d7fa5;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .doc-result:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 32px rgba(93,127,165,0.2);
        border-color: rgba(93,127,165,0.4);
    }
    
    .doc-title {
        color: #a5b8cf;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .doc-content {
        color: #e8f0f8;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .relevance-score {
        color: #4caf50;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load ChromaDB
@st.cache_resource
def load_chromadb():
    """Load ChromaDB collection"""
    try:
        # NEW ChromaDB configuration
        client = chromadb.PersistentClient(path="./chroma_db")
        
        collection = client.get_or_create_collection(name="employee_documents")
        
        # Verify collection has data
        count = collection.count()
        if count == 0:
            return None, "ChromaDB collection is empty. Run 'python rag_document_system_fixed.py' first!"
        
        return collection, None
    except Exception as e:
        return None, str(e)

# Main app
def main():
    # Header
    st.markdown("# 📚 Document Search")
    st.markdown("**Search 25 employee documents using AI-powered RAG**")
    st.markdown("---")
    
    # Load ChromaDB
    collection, error = load_chromadb()
    
    if error:
        st.error(f"❌ ChromaDB Error: {error}")
        st.info("Run `python rag_document_system.py` first to set up the system!")
        st.stop()
    
    # Load config
    config = None
    if os.path.exists('rag_config.json'):
        with open('rag_config.json', 'r') as f:
            config = json.load(f)
    elif os.path.exists('rag_system_config.json'):
        with open('rag_system_config.json', 'r') as f:
            config = json.load(f)
    
    if config:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Documents", config.get('total_documents', 25))
        with col2:
            st.metric("🧩 Chunks", f"{config.get('total_chunks', 0):,}")
        with col3:
            db_type = config.get('database_type', 'ChromaDB')
            st.metric("💾 Database", db_type)
    
    st.markdown("---")
    
    # Example questions
    st.markdown("### 💡 Try These Questions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Remote Work Policy", use_container_width=True):
            st.session_state.query = "What is the remote work policy?"
    with col2:
        if st.button("Salary Ranges", use_container_width=True):
            st.session_state.query = "What are the salary ranges for engineers?"
    with col3:
        if st.button("Vacation Days", use_container_width=True):
            st.session_state.query = "How many vacation days do employees get?"
    with col4:
        if st.button("Performance Reviews", use_container_width=True):
            st.session_state.query = "How does the performance review process work?"
    
    # Search input
    query = st.text_input(
        "Ask a question about employee policies:",
        value=st.session_state.get('query', ''),
        placeholder="e.g., What is the bonus structure? When are performance reviews?",
        key="search_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Perform search
    if search_btn and query:
        st.markdown("---")
        
        with st.spinner("🔍 Searching through documents..."):
            # Query ChromaDB
            results = collection.query(
                query_texts=[query],
                n_results=5
            )
        
        if results['documents'] and len(results['documents'][0]) > 0:
            st.success(f"✅ Found {len(results['documents'][0])} relevant results")
            
            # Display results
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0], 
                results['metadatas'][0],
                results['distances'][0]
            ), 1):
                
                # Calculate relevance percentage
                relevance = max(0, (1 - distance) * 100)
                
                with st.container():
                    st.markdown(f"""
                    <div class="doc-result">
                        <div class="doc-title">
                            📄 {i}. {metadata['title']} 
                            <span class="relevance-score">({relevance:.0f}% relevant)</span>
                        </div>
                        <div class="doc-content">
                            {doc}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show full document option
                    with st.expander(f"📖 View full document: {metadata['title']}"):
                        # Load from database
                        if os.path.exists('employee_documents.db'):
                            conn = sqlite3.connect('employee_documents.db')
                            cursor = conn.cursor()
                            cursor.execute("SELECT content FROM documents WHERE doc_id = ?", (metadata['doc_id'],))
                            full_doc = cursor.fetchone()
                            if full_doc:
                                st.text(full_doc[0])
                            conn.close()
                        
                        st.markdown(f"**File:** {metadata['filename']}")
            
            # Show generated answer
            st.markdown("---")
            st.markdown("### 🤖 AI-Generated Answer")
            
            # Combine top results to create answer
            combined_context = "\n\n".join(results['documents'][0][:3])
            
            answer = f"""
Based on the documents, here's what I found about "{query}":

{combined_context[:1000]}

*This answer is compiled from {len(results['documents'][0])} relevant document sections.*
            """
            
            st.info(answer)
            
        else:
            st.warning("No relevant documents found. Try a different question!")
    
    # Document list
    with st.expander("📚 View All Available Documents"):
        if os.path.exists('employee_documents.db'):
            conn = sqlite3.connect('employee_documents.db')
            docs_df = pd.read_sql_query("SELECT doc_id, title, page_count FROM documents ORDER BY title", conn)
            st.dataframe(docs_df, use_container_width=True)
            conn.close()

if __name__ == "__main__":
    main()
