"""
FIXED RAG DOCUMENT SYSTEM - WITH VERIFICATION
==============================================

Fixed version that ensures documents are properly stored
and searchable in ChromaDB.

Run: python rag_document_system_fixed.py

Author: Analytics Team
Date: May 2026
"""

import os
import sys
from datetime import datetime
import json

print("=" * 100)
print("🚀 RAG DOCUMENT SYSTEM - FIXED VERSION")
print("=" * 100)
print()

# ============================================================================
# STEP 1: CHECK AND INSTALL REQUIREMENTS
# ============================================================================

print("STEP 1: CHECKING REQUIREMENTS")
print("-" * 100)
print()

def check_and_install():
    """Check if required libraries are installed"""
    required = {
        'chromadb': 'chromadb',
        'reportlab': 'reportlab',
    }
    
    missing = []
    for package, pip_name in required.items():
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} NOT installed")
            missing.append(pip_name)
    
    if missing:
        print()
        print("⚠️  Installing missing libraries...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ Installation complete!")
    
    print()

check_and_install()

# ============================================================================
# STEP 2: GENERATE SAMPLE PDFS
# ============================================================================

print("=" * 100)
print("STEP 2: GENERATING 25 EMPLOYEE POLICY PDFs")
print("=" * 100)
print()

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Create directory
os.makedirs('employee_documents', exist_ok=True)

documents_data = [
    {
        'title': 'Remote Work Policy',
        'content': '''REMOTE WORK POLICY

Eligibility: All employees except those in roles requiring physical presence

Work Arrangements:
1. Fully Remote - Work from anywhere, quarterly in-person meetings required
2. Hybrid - 3 days office, 2 days remote (recommended model)
3. In-Office - 5 days per week for certain roles

Equipment Provided:
- Laptop (MacBook Pro or ThinkPad)
- External monitor, keyboard, mouse
- Home office stipend: $500 one-time
- Monthly internet reimbursement: $50

Requirements:
- Reliable high-speed internet connection
- Dedicated home workspace
- Available during core hours: 10 AM - 3 PM local time
- Daily team check-ins required

Communication Expectations:
- Response time: Within 4 hours during business hours
- Camera on for team meetings
- Slack/Teams for daily communication'''
    },
    {
        'title': 'Salary Compensation Guide',
        'content': '''COMPENSATION GUIDELINES 2026

USA Salary Ranges by Role:
- Software Engineer: $90,000 - $140,000
- Senior Software Engineer: $130,000 - $180,000  
- Engineering Manager: $140,000 - $210,000
- Director of Engineering: $180,000 - $250,000
- VP Engineering: $220,000 - $300,000

India Salary Ranges by Role:
- Software Engineer: ₹900,000 - ₹1,800,000 ($10.8K - $21.6K USD)
- Senior Software Engineer: ₹1,500,000 - ₹2,800,000 ($18K - $33.7K USD)
- Engineering Manager: ₹2,000,000 - ₹4,200,000 ($24K - $50.4K USD)
- Director: ₹3,500,000 - ₹6,500,000 ($42K - $78K USD)

Equity Compensation:
- Stock options granted to all employees
- Vesting schedule: 4 years with 1-year cliff
- Annual refresh grants for top performers
- Exercise window: 10 years

Bonus Structure:
- Individual performance component: 0-15% of base
- Company performance component: 0-10% of base
- Total potential bonus: 0-25% annually
- Paid quarterly based on achievement'''
    },
    {
        'title': 'Employee Benefits Overview',
        'content': '''EMPLOYEE BENEFITS PACKAGE

Health Insurance:
- Medical: Full PPO coverage, $0 employee premium
- Dental: Preventive and major coverage included
- Vision: Eye exams and prescription coverage
- Mental health: Unlimited therapy sessions

Retirement Benefits:
- 401(k) plan with 6% company match
- Immediate vesting of company contributions
- Financial planning services included

Time Off:
- Vacation: 20 days annually (increases with tenure)
- Sick leave: 10 days annually  
- Personal days: 5 days annually
- Parental leave: 16 weeks paid (primary caregiver)
- Holidays: 12 company holidays

Additional Perks:
- Learning budget: $2,000 per year
- Gym membership reimbursement: $100/month
- Commuter benefits: Pre-tax transit/parking
- Life insurance: 2x annual salary
- Disability insurance: Short and long-term coverage'''
    },
    {
        'title': 'Performance Review Process',
        'content': '''PERFORMANCE REVIEW SYSTEM

Review Schedule:
- Quarterly reviews for all employees
- Annual comprehensive review in December
- Mid-year calibration in June

Rating Scale:
1. Outstanding (Top 5%) - Exceptional, transformative impact
2. Excellent (20%) - Consistently exceeds expectations
3. Good (50%) - Meets all expectations, solid performer
4. Satisfactory (20%) - Meets minimum requirements
5. Needs Improvement (5%) - Performance gaps identified

Evaluation Criteria:
- Technical execution and quality (40%)
- Communication and collaboration (25%)
- Initiative and innovation (20%)
- Leadership and mentorship (15%)

Compensation Impact:
- Outstanding: 8-10% merit increase + 20-25% bonus
- Excellent: 5-7% merit increase + 15-20% bonus
- Good: 3-5% merit increase + 10-15% bonus
- Satisfactory: 0-2% merit increase + 5-10% bonus
- Needs Improvement: 0% increase, performance improvement plan

Promotion Requirements:
- Minimum 2 years in current role
- Consistent Excellent or Outstanding ratings
- Demonstrated next-level capabilities
- Manager nomination and peer endorsement
- Panel review and approval'''
    },
    {
        'title': 'Vacation and PTO Policy',
        'content': '''VACATION AND PAID TIME OFF

Annual PTO Allocation:
- Years 0-3: 20 days vacation + 10 sick days
- Years 4-7: 25 days vacation + 10 sick days  
- Years 8+: 30 days vacation + 10 sick days
- Personal days: 5 days (all employees)

Accrual:
- Vacation accrues monthly (1.67 days/month for 20 days/year)
- Sick days: Full allocation on January 1st
- Unused sick days: Do not carry over
- Unused vacation: Up to 10 days carry over to next year

Requesting Time Off:
- Submit requests in HR system minimum 2 weeks advance
- Manager approval required
- Blackout periods: End of quarter (last 2 weeks)
- Minimum notice for sick leave: Same day notification

Holiday Schedule:
- New Year's Day, MLK Day, Presidents Day
- Memorial Day, Independence Day, Labor Day
- Thanksgiving (2 days), Christmas (2 days)
- Floating holidays: 2 days (employee choice)'''
    }
]

# Add 20 more document templates
additional_docs = [
    ('Onboarding Guide', 'First week schedule, orientation sessions, IT setup, badge access, team introductions, training modules, 30-60-90 day goals'),
    ('Code of Conduct', 'Professional behavior standards, ethics policy, confidentiality, conflicts of interest, compliance requirements'),
    ('IT Security Policy', 'Password requirements (12+ chars, MFA required), data encryption, device security, incident reporting, acceptable use'),
    ('Travel Policy', 'Flight booking (economy for <5hrs, business for 5+hrs), hotel ($200/night limit), meals ($75/day), rental cars, expense submission'),
    ('Equipment Policy', 'Laptop refresh cycle (3 years), software licenses, monitors and peripherals, shipping for remote employees'),
    ('Learning and Development', 'Annual learning budget $2,000, conference attendance, certification reimbursement, internal training programs'),
    ('Diversity and Inclusion', 'DEI commitments, employee resource groups, inclusive hiring, bias training, reporting mechanisms'),
    ('Health and Safety', 'Office ergonomics, emergency procedures, first aid locations, reporting injuries, COVID-19 protocols'),
    ('Career Development', 'Growth paths (IC track and management track), mentorship program, internal mobility, promotion timeline'),
    ('Meeting Guidelines', 'Default to 25/50 min meetings, required agenda, action items, recording policy, meeting-free Fridays'),
    ('Expense Reimbursement', 'Submission deadline (30 days), approved expenses, corporate card policy, receipt requirements'),
    ('Stock Options Guide', 'Grant amounts by level, exercise process, tax implications, vesting schedule, RSU vs options'),
    ('Employee Referral Program', '$5,000 bonus for hired referrals, eligibility after 90 days, payout schedule, eligible positions'),
    ('Work-Life Balance', 'No emails after 6 PM policy, mental health days, wellness programs, flexible scheduling'),
    ('Communication Tools', 'Slack for daily communication, Zoom for meetings, email for formal communication, response time expectations'),
    ('Data Privacy Policy', 'GDPR compliance, data handling procedures, employee data access rights, consent management'),
    ('Office Facilities', 'Parking validation, cafeteria hours, gym access, phone booths, collaboration spaces, quiet zones'),
    ('Emergency Contacts', 'IT helpdesk: x2000, HR: x3000, Facilities: x4000, Security: x5000, Emergency: 911'),
    ('Professional Development', 'Skill advancement, technical certifications, leadership training, tuition reimbursement up to $10K/year'),
    ('Engineering Standards', 'Code review process, testing requirements, deployment procedures, on-call rotation, documentation standards')
]

for title, content in additional_docs:
    documents_data.append({
        'title': title,
        'content': f'''{title.upper()}

{content}

Last Updated: May 2026
Version: 1.0
Contact: hr@company.com for questions'''
    })

# Generate PDFs
pdf_files = []

print(f"Creating {len(documents_data)} PDF documents...")
print()

for i, doc in enumerate(documents_data, 1):
    filename = f"employee_documents/DOC{i:03d}_{doc['title'].replace(' ', '_').replace('/', '_')}.pdf"
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, height - 1*inch, doc['title'])
    
    # Content
    c.setFont("Helvetica", 10)
    text_object = c.beginText(1*inch, height - 1.5*inch)
    
    for line in doc['content'].split('\n'):
        text_object.textLine(line)
    
    c.drawText(text_object)
    
    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.5*inch, f"DOC{i:03d} | {datetime.now().strftime('%Y-%m-%d')}")
    
    c.save()
    
    pdf_files.append({
        'filename': filename,
        'title': doc['title'],
        'content': doc['content'],
        'doc_id': f'DOC{i:03d}'
    })
    
    print(f"  ✅ {i}/25: {doc['title']}")

print()
print(f"✅ Created {len(pdf_files)} PDF documents")
print()

# ============================================================================
# STEP 3: CREATE CHROMADB AND STORE DOCUMENTS
# ============================================================================

print("=" * 100)
print("STEP 3: CREATING CHROMADB VECTOR DATABASE")
print("=" * 100)
print()

import chromadb

# Initialize with new API
print("Initializing ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collection if it exists (start fresh)
try:
    client.delete_collection(name="employee_documents")
    print("  ✅ Deleted old collection")
except:
    pass

# Create new collection
collection = client.create_collection(
    name="employee_documents",
    metadata={"description": "Employee policies and handbooks"}
)

print("  ✅ ChromaDB collection created")
print()

# Prepare documents for embedding
print("Preparing documents for ChromaDB...")
print()

doc_ids = []
doc_contents = []
doc_metadatas = []

for pdf in pdf_files:
    # Split content into chunks
    content = pdf['content']
    chunk_size = 400
    
    # Create chunks with overlap
    chunks = []
    for i in range(0, len(content), chunk_size // 2):
        chunk = content[i:i + chunk_size]
        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())
    
    # Add each chunk to ChromaDB
    for chunk_idx, chunk in enumerate(chunks):
        doc_ids.append(f"{pdf['doc_id']}_chunk{chunk_idx}")
        doc_contents.append(chunk)
        doc_metadatas.append({
            'doc_id': pdf['doc_id'],
            'title': pdf['title'],
            'filename': pdf['filename'],
            'chunk_index': chunk_idx
        })

print(f"  ✅ Created {len(doc_contents)} searchable chunks")
print()

# Add to ChromaDB
print("Adding documents to ChromaDB...")
print("⏳ This may take 30-60 seconds for embeddings...")
print()

# Add in batches
batch_size = 50
for i in range(0, len(doc_contents), batch_size):
    end = min(i + batch_size, len(doc_contents))
    
    collection.add(
        ids=doc_ids[i:end],
        documents=doc_contents[i:end],
        metadatas=doc_metadatas[i:end]
    )
    
    print(f"  ✅ Added chunks {i+1}-{end}/{len(doc_contents)}")

print()
print(f"✅ ChromaDB populated with {len(doc_contents)} embedded chunks")
print()

# Verify it worked
print("Verifying ChromaDB...")
count = collection.count()
print(f"  ✅ ChromaDB contains {count} documents")
print()

if count == 0:
    print("❌ ERROR: ChromaDB is empty!")
    sys.exit(1)

# ============================================================================
# STEP 4: TEST SEARCH
# ============================================================================

print("=" * 100)
print("STEP 4: TESTING SEARCH FUNCTIONALITY")
print("=" * 100)
print()

test_queries = [
    "What is the remote work policy?",
    "What are the salary ranges?",
    "How many vacation days?"
]

for query in test_queries:
    print(f"🔍 Testing: \"{query}\"")
    
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    if results['documents'] and len(results['documents'][0]) > 0:
        print(f"  ✅ Found {len(results['documents'][0])} results")
        print(f"  📄 Top result from: {results['metadatas'][0][0]['title']}")
        print(f"     {results['documents'][0][0][:100]}...")
    else:
        print(f"  ❌ No results found!")
    
    print()

# ============================================================================
# STEP 5: SAVE CONFIGURATION
# ============================================================================

print("=" * 100)
print("STEP 5: SAVING CONFIGURATION")
print("=" * 100)
print()

config = {
    'total_documents': len(pdf_files),
    'total_chunks': len(doc_contents),
    'chromadb_location': './chroma_db',
    'collection_name': 'employee_documents',
    'documents_in_chromadb': count,
    'setup_completed': datetime.now().isoformat()
}

with open('rag_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuration saved: rag_config.json")
print()

# ============================================================================
# SUCCESS MESSAGE
# ============================================================================

print("=" * 100)
print("🎉 SETUP COMPLETE!")
print("=" * 100)
print()

print("WHAT WAS CREATED:")
print(f"  ✅ 25 PDF documents in 'employee_documents/' folder")
print(f"  ✅ ChromaDB vector database in 'chroma_db/' folder")
print(f"  ✅ {count} searchable document chunks")
print(f"  ✅ Configuration file: rag_config.json")
print()

print("NEXT STEPS:")
print("  1. Run: streamlit run rag_search_dashboard.py")
print("  2. Search documents in your browser")
print("  3. Get instant answers from PDFs!")
print()

print("SAMPLE SEARCHES TO TRY:")
print('  • "What is the remote work policy?"')
print('  • "What are the salary ranges for engineers?"')
print('  • "How many vacation days do employees get?"')
print('  • "What is the bonus structure?"')
print()

print("=" * 100)
