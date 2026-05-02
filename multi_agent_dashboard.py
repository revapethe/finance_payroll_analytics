"""
MULTI-AGENT EMPLOYEE ANALYTICS SYSTEM
======================================

Two AI Agents that chat with each other:
1. DATA ANALYST AGENT - Searches and analyzes data
2. BUSINESS ADVISOR AGENT - Provides insights and recommendations

They collaborate using:
- RAG (Retrieval-Augmented Generation)
- Agentic AI (autonomous decision making)
- Multi-agent conversation

Run: streamlit run multi_agent_dashboard.py

Author: Analytics Team
Date: January 2026
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
    page_title="Multi-Agent Analytics",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }
    
    h1 {
        color: #ffffff !important;
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 0.5rem;
    }
    
    /* Agent chat bubbles */
    .agent-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    .analyst-message {
        background: #1f2a3a;
        border-left-color: #4a90e2;
    }
    
    .advisor-message {
        background: #1f3a1f;
        border-left-color: #4caf50;
    }
    
    .agent-name {
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .thinking {
        color: #b0b0b0;
        font-style: italic;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = {}

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

def build_knowledge_base(df):
    """RAG: Create searchable knowledge base from data"""
    
    kb = {
        'total_employees': len(df),
        'countries': df['country'].value_counts().to_dict(),
        'departments': df['department'].value_counts().to_dict(),
        'avg_salary_global': df['annual_salary_usd'].mean(),
        'salary_range': {
            'min': df['annual_salary_usd'].min(),
            'max': df['annual_salary_usd'].max()
        },
        'top_earners': df.nlargest(10, 'annual_salary_usd')[['employee_id', 'job_title', 'annual_salary_usd']].to_dict('records'),
        'by_country': {},
        'by_department': {}
    }
    
    # Country-specific knowledge
    for country in df['country'].unique():
        country_df = df[df['country'] == country]
        kb['by_country'][country] = {
            'count': len(country_df),
            'avg_salary': country_df['annual_salary_usd'].mean(),
            'top_jobs': country_df['job_title'].value_counts().head(5).to_dict()
        }
    
    # Department-specific knowledge
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        kb['by_department'][dept] = {
            'count': len(dept_df),
            'avg_salary': dept_df['annual_salary_usd'].mean(),
            'salary_range': {
                'min': dept_df['annual_salary_usd'].min(),
                'max': dept_df['annual_salary_usd'].max()
            }
        }
    
    return kb

class DataAnalystAgent:
    """Agent 1: Searches and retrieves data"""
    
    def __init__(self, df, kb):
        self.df = df
        self.knowledge_base = kb
        self.name = "📊 Data Analyst Agent"
        self.color = "#4a90e2"
    
    def think(self, query):
        """Agent's reasoning process"""
        thoughts = []
        
        if 'top' in query.lower():
            thoughts.append("I need to find top performers by salary")
        if 'compare' in query.lower():
            thoughts.append("This requires comparative analysis")
        if 'why' in query.lower():
            thoughts.append("I should analyze underlying factors")
        
        return thoughts
    
    def search_and_analyze(self, query):
        """RAG: Retrieve relevant data and analyze"""
        
        q = query.lower()
        filtered = self.df.copy()
        filters = []
        
        # Extract filters (same as before)
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
        
        # Salary filters
        over_match = re.search(r'over\s+(\d+)k?', q)
        if over_match:
            amount = int(over_match.group(1)) * 1000
            filtered = filtered[filtered['annual_salary_usd'] > amount]
            filters.append(f'>${amount:,}')
        
        # Sort and limit
        filtered = filtered.sort_values('annual_salary_usd', ascending=False)
        
        top_match = re.search(r'top\s+(\d+)', q)
        if top_match:
            n = int(top_match.group(1))
            filtered = filtered.head(n)
        elif 'top' in q:
            filtered = filtered.head(10)
        
        # Create analysis
        analysis = {
            'results': filtered,
            'count': len(filtered),
            'avg_salary': filtered['annual_salary_usd'].mean() if len(filtered) > 0 else 0,
            'filters': filters,
            'insights': self.generate_insights(filtered)
        }
        
        return analysis
    
    def generate_insights(self, data):
        """Generate data insights"""
        if len(data) == 0:
            return []
        
        insights = []
        
        # Salary insights
        avg = data['annual_salary_usd'].mean()
        median = data['annual_salary_usd'].median()
        
        if avg > median * 1.2:
            insights.append("Salary distribution is right-skewed (few high earners pulling average up)")
        
        # Department insights
        if 'department' in data.columns:
            dept_counts = data['department'].value_counts()
            if len(dept_counts) > 0:
                top_dept = dept_counts.index[0]
                insights.append(f"Majority are in {top_dept} department")
        
        # Country insights
        if 'country' in data.columns and len(data['country'].unique()) > 1:
            usa_avg = data[data['country'] == 'United States']['annual_salary_usd'].mean()
            india_avg = data[data['country'] == 'India']['annual_salary_usd'].mean()
            if usa_avg > india_avg * 2:
                ratio = usa_avg / india_avg
                insights.append(f"USA salaries are {ratio:.1f}x higher than India")
        
        return insights
    
    def respond(self, query):
        """Generate response"""
        thoughts = self.think(query)
        analysis = self.search_and_analyze(query)
        
        response = {
            'agent': self.name,
            'thoughts': thoughts,
            'data': analysis,
            'message': self.format_message(analysis)
        }
        
        return response
    
    def format_message(self, analysis):
        """Format message for conversation"""
        if analysis['count'] == 0:
            return "I searched the database but found no employees matching those criteria."
        
        msg = f"I found **{analysis['count']} employees** matching the criteria.\n\n"
        
        if analysis['filters']:
            msg += f"**Filters applied:** {' | '.join(analysis['filters'])}\n\n"
        
        msg += f"**Statistics:**\n"
        msg += f"- Average salary: ${analysis['avg_salary']:,.0f}\n"
        
        if len(analysis['results']) > 0:
            msg += f"\n**Top 5:**\n"
            for idx, (_, emp) in enumerate(analysis['results'].head(5).iterrows(), 1):
                msg += f"{idx}. {emp['employee_id']} - {emp['job_title']} - ${emp['annual_salary_usd']:,.0f}\n"
        
        if analysis['insights']:
            msg += f"\n**Data Insights:**\n"
            for insight in analysis['insights']:
                msg += f"- {insight}\n"
        
        return msg

class BusinessAdvisorAgent:
    """Agent 2: Provides business insights and recommendations"""
    
    def __init__(self, kb):
        self.knowledge_base = kb
        self.name = "💼 Business Advisor Agent"
        self.color = "#4caf50"
    
    def think(self, analyst_data):
        """Agent's reasoning about the data"""
        thoughts = []
        
        if analyst_data['count'] > 0:
            thoughts.append("Analyzing business implications")
            
            avg = analyst_data['avg_salary']
            if avg > 150000:
                thoughts.append("High salary range - analyzing compensation strategy")
            
            if analyst_data['count'] < 10:
                thoughts.append("Small sample - considering statistical significance")
        
        return thoughts
    
    def analyze_business_context(self, analyst_data):
        """Provide business recommendations"""
        
        if analyst_data['count'] == 0:
            return {
                'recommendations': ["Consider expanding search criteria", "No actionable insights from empty dataset"],
                'concerns': [],
                'opportunities': []
            }
        
        recommendations = []
        concerns = []
        opportunities = []
        
        avg_salary = analyst_data['avg_salary']
        count = analyst_data['count']
        
        # Salary analysis
        if avg_salary > self.knowledge_base['avg_salary_global'] * 1.3:
            concerns.append(f"This group's average (${avg_salary:,.0f}) is 30%+ above company average (${self.knowledge_base['avg_salary_global']:,.0f})")
            recommendations.append("Review compensation equity across departments")
        
        # Headcount analysis
        if 'Engineering' in str(analyst_data.get('filters', [])):
            eng_pct = (count / self.knowledge_base['by_department'].get('Engineering', {}).get('count', 1)) * 100
            if eng_pct > 20:
                opportunities.append(f"You're looking at {eng_pct:.0f}% of Engineering - significant talent pool")
        
        # Growth opportunities
        if avg_salary < 100000 and count > 20:
            opportunities.append("Large pool of mid-level talent - good for succession planning")
        
        if not recommendations:
            recommendations.append("Salary levels appear aligned with company averages")
        
        return {
            'recommendations': recommendations,
            'concerns': concerns,
            'opportunities': opportunities
        }
    
    def respond(self, analyst_response):
        """Generate business advisor response"""
        
        thoughts = self.think(analyst_response['data'])
        business_analysis = self.analyze_business_context(analyst_response['data'])
        
        response = {
            'agent': self.name,
            'thoughts': thoughts,
            'analysis': business_analysis,
            'message': self.format_message(analyst_response, business_analysis)
        }
        
        return response
    
    def format_message(self, analyst_response, business_analysis):
        """Format business advisor message"""
        
        msg = f"Based on the {analyst_response['data']['count']} employees found:\n\n"
        
        if business_analysis['recommendations']:
            msg += "**💡 Recommendations:**\n"
            for rec in business_analysis['recommendations']:
                msg += f"- {rec}\n"
            msg += "\n"
        
        if business_analysis['concerns']:
            msg += "**⚠️ Concerns:**\n"
            for concern in business_analysis['concerns']:
                msg += f"- {concern}\n"
            msg += "\n"
        
        if business_analysis['opportunities']:
            msg += "**🎯 Opportunities:**\n"
            for opp in business_analysis['opportunities']:
                msg += f"- {opp}\n"
        
        return msg

def multi_agent_conversation(user_query, analyst_agent, advisor_agent):
    """Orchestrate conversation between two agents"""
    
    conversation = []
    
    # User query
    conversation.append({
        'role': 'user',
        'message': user_query,
        'timestamp': datetime.now()
    })
    
    # Agent 1: Data Analyst responds
    with st.spinner('🤖 Data Analyst Agent is searching...'):
        time.sleep(0.5)  # Simulate thinking
        analyst_response = analyst_agent.respond(user_query)
        conversation.append({
            'role': 'analyst',
            'agent': analyst_agent.name,
            'thoughts': analyst_response['thoughts'],
            'message': analyst_response['message'],
            'data': analyst_response['data'],
            'timestamp': datetime.now()
        })
    
    # Agent 2: Business Advisor responds to Agent 1
    with st.spinner('🤖 Business Advisor Agent is analyzing...'):
        time.sleep(0.5)  # Simulate thinking
        advisor_response = advisor_agent.respond(analyst_response)
        conversation.append({
            'role': 'advisor',
            'agent': advisor_agent.name,
            'thoughts': advisor_response['thoughts'],
            'message': advisor_response['message'],
            'timestamp': datetime.now()
        })
    
    # Agent 1 might respond back to Agent 2
    if len(analyst_response['data']['results']) > 0:
        with st.spinner('🤖 Agents are collaborating...'):
            time.sleep(0.3)
            
            # Analyst provides additional context based on advisor's concerns
            followup = f"To address the business concerns, here are additional details:\n\n"
            
            results = analyst_response['data']['results']
            if len(results) > 0:
                # Performance distribution
                if 'performance' in results.columns:
                    perf_dist = results['performance'].value_counts()
                    followup += f"**Performance Distribution:**\n"
                    for perf, count in perf_dist.items():
                        followup += f"- {perf}: {count} employees\n"
                
                # Remote status
                if 'remote_status' in results.columns:
                    remote_dist = results['remote_status'].value_counts()
                    followup += f"\n**Work Arrangements:**\n"
                    for status, count in remote_dist.items():
                        followup += f"- {status}: {count} employees\n"
            
            conversation.append({
                'role': 'analyst',
                'agent': analyst_agent.name,
                'message': followup,
                'timestamp': datetime.now()
            })
    
    return conversation, analyst_response['data']['results']

def main():
    # Header
    st.markdown("# 🤖 Multi-Agent Employee Analytics")
    st.markdown("**Two AI Agents collaborating using RAG and Agentic AI**")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ No employee data found. Please ensure employee_data.csv exists.")
        st.stop()
    
    # Build knowledge base (RAG)
    kb = build_knowledge_base(df)
    st.session_state.knowledge_base = kb
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Employees", f"{kb['total_employees']:,}")
    with col2:
        usa_count = kb['countries'].get('United States', 0)
        st.metric("USA", f"{usa_count:,}")
    with col3:
        india_count = kb['countries'].get('India', 0)
        st.metric("India", f"{india_count:,}")
    with col4:
        st.metric("Avg Salary", f"${kb['avg_salary_global']/1000:.0f}K")
    
    st.markdown("---")
    
    # Agent information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Data Analyst Agent
        **Role:** Search and retrieve employee data
        - Executes database queries
        - Calculates statistics
        - Finds patterns in data
        - Uses RAG to access knowledge base
        """)
    
    with col2:
        st.markdown("""
        ### 💼 Business Advisor Agent
        **Role:** Provide strategic insights
        - Analyzes business implications
        - Identifies concerns and opportunities
        - Makes recommendations
        - Considers company context
        """)
    
    st.markdown("---")
    
    # Initialize agents
    analyst_agent = DataAnalystAgent(df, kb)
    advisor_agent = BusinessAdvisorAgent(kb)
    
    # Query input
    st.markdown("## Ask a Question - Watch Agents Collaborate")
    
    # Quick examples
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Top 10 USA", use_container_width=True):
            st.session_state.query = "Top 10 highest paid in USA"
    with col2:
        if st.button("Compare Countries", use_container_width=True):
            st.session_state.query = "Compare USA vs India salaries"
    with col3:
        if st.button("Engineering Analysis", use_container_width=True):
            st.session_state.query = "Analyze Engineering department"
    with col4:
        if st.button("High Earners", use_container_width=True):
            st.session_state.query = "Employees over 180k"
    
    user_query = st.text_input(
        "Your question:",
        value=st.session_state.get('query', ''),
        placeholder="e.g., What are the salary trends in Engineering?"
    )
    
    if st.button("🚀 Start Agent Conversation", type="primary"):
        if user_query:
            # Run multi-agent conversation
            conversation, results = multi_agent_conversation(user_query, analyst_agent, advisor_agent)
            st.session_state.conversation = conversation
            st.session_state.last_results = results
    
    # Display conversation
    if st.session_state.conversation:
        st.markdown("---")
        st.markdown("## 💬 Agent Conversation")
        
        for msg in st.session_state.conversation:
            if msg['role'] == 'user':
                st.markdown(f"### 👤 You asked:")
                st.info(msg['message'])
            
            elif msg['role'] == 'analyst':
                st.markdown(f"### 📊 Data Analyst Agent")
                
                if 'thoughts' in msg:
                    with st.expander("🧠 Agent's Thinking Process", expanded=False):
                        for thought in msg['thoughts']:
                            st.markdown(f"- *{thought}*")
                
                st.markdown(f'<div class="agent-message analyst-message">{msg["message"]}</div>', 
                           unsafe_allow_html=True)
            
            elif msg['role'] == 'advisor':
                st.markdown(f"### 💼 Business Advisor Agent")
                
                if 'thoughts' in msg:
                    with st.expander("🧠 Agent's Thinking Process", expanded=False):
                        for thought in msg['thoughts']:
                            st.markdown(f"- *{thought}*")
                
                st.markdown(f'<div class="agent-message advisor-message">{msg["message"]}</div>', 
                           unsafe_allow_html=True)
        
        # Show results if available
        if 'last_results' in st.session_state and len(st.session_state.last_results) > 0:
            st.markdown("---")
            st.markdown("## 📊 Detailed Data")
            
            tab1, tab2 = st.tabs(["📋 Employee List", "📈 Visualization"])
            
            with tab1:
                results_df = st.session_state.last_results[['employee_id', 'job_title', 'department', 
                                                             'city', 'country', 'annual_salary_usd']].head(20)
                results_df['annual_salary_usd'] = results_df['annual_salary_usd'].apply(lambda x: f"${x:,.0f}")
                results_df.columns = ['ID', 'Job', 'Dept', 'City', 'Country', 'Salary']
                st.dataframe(results_df, use_container_width=True, height=400)
            
            with tab2:
                top10 = st.session_state.last_results.nlargest(10, 'annual_salary_usd')
                
                fig = go.Figure(data=[
                    go.Bar(
                        y=top10['employee_id'],
                        x=top10['annual_salary_usd'],
                        orientation='h',
                        marker=dict(color='#4a90e2'),
                        text=top10['annual_salary_usd'].apply(lambda x: f'${x:,.0f}'),
                        textposition='outside'
                    )
                ])
                
                fig.update_layout(
                    title="Top 10 by Salary",
                    plot_bgcolor='#1a1a1a',
                    paper_bgcolor='#1a1a1a',
                    font=dict(color='#fff'),
                    height=400,
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor='#333', color='#fff'),
                    yaxis=dict(showgrid=False, color='#fff')
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # Knowledge base viewer
    with st.expander("🧠 View RAG Knowledge Base"):
        st.markdown("**Global Statistics:**")
        st.json({
            'total_employees': kb['total_employees'],
            'average_salary': f"${kb['avg_salary_global']:,.0f}",
            'salary_range': f"${kb['salary_range']['min']:,.0f} - ${kb['salary_range']['max']:,.0f}",
            'countries': kb['countries']
        })

if __name__ == "__main__":
    main()
