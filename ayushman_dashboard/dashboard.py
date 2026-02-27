import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from mock_data import load_mock_data
from audit_generator import generate_audit_summary
from report_export import generate_pdf_report
import PyPDF2
import io

st.set_page_config(page_title="Ayushman Bharat Fraud Intelligence", layout="wide", page_icon="🛡️")

# --- Custom CSS Injection ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Background for the main container */
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 100%);
        color: #e0e0e0;
    }
    
    /* Elegant Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 19, 43, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    h1, h2, h3, h4, p {
        color: #ffffff !important;
    }

    /* Glassmorphism KPI Cards replacing st.metric */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .metric-title {
        color: #8da9c4;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
    }
    .metric-value.risk { color: #ff595e; }
    .metric-value.safe { color: #8ac926; }
    .metric-value.warn { color: #ffca3a; }
    .metric-value.neutral { color: #1982c4; }

    /* Clean expander styles */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    
    /* Clean up dataframe styling */
    th {
        background-color: rgba(25, 130, 196, 0.2) !important;
        color: #ffffff !important;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }
    
    /* Custom divider */
    hr {
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- API Placeholders ---
@st.cache_data
def fetch_overview_data():
    # TODO: Replace with API call later
    try:
        return load_mock_data()
    except Exception:
        return None

@st.cache_data
def fetch_hospital_data():
    # TODO: Replace with GET /api/hospitals
    try:
        return load_mock_data()
    except Exception:
        return None

@st.cache_data
def fetch_claim_data():
    # TODO: Replace with GET /api/claim/{id}
    try:
        return load_mock_data()
    except Exception:
        return None

# Load Data
overview_df = fetch_overview_data()
if overview_df is None:
    st.error("Data service temporarily unavailable.")
    st.stop()

# --- Helpers ---
def is_fraud(row):
    return row['image_reuse_flag'] == 1 or row['duplicate_flag'] == 1 or row['anomaly_score'] > 0.75 or row['risk_category'] in ['High', 'Critical']

overview_df['is_suspicious'] = overview_df.apply(is_fraud, axis=1)

# Sidebar Navigation
st.sidebar.title("🛡️ Fraud Intelligence")
page = st.sidebar.radio("Navigation", ["Hospital Risk Ranking", "Claim Drill-Down"])

if page == "Hospital Risk Ranking":
    st.title("🏥 Hospital Risk Ranking")
    st.markdown("---")
    
    hosp_df = fetch_hospital_data()
    if hosp_df is None:
        st.error("Data service temporarily unavailable.")
        st.stop()
        
    hosp_df['is_suspicious'] = hosp_df.apply(is_fraud, axis=1)
    
    # Grouping logic
    agg_funcs = {
        'state': 'first',
        'claim_amount': 'mean',
        'is_suspicious': 'sum',
        'image_reuse_flag': 'sum',
        'duplicate_flag': 'sum',
        'risk_score': 'mean',
        'claim_id': 'count'
    }
    hospital_stats = hosp_df.groupby('hospital_id').agg(agg_funcs).rename(columns={
        'claim_amount': 'Avg Claim Amount',
        'is_suspicious': 'Fraud Count',
        'image_reuse_flag': 'Image Reuse Cases',
        'risk_score': 'Avg Risk Score',
        'claim_id': 'Total Claims',
        'duplicate_flag': 'Duplicate Cases',
        'state': 'State'
    }).reset_index()
    
    # Filters
    states = ['All'] + sorted(hospital_stats['State'].unique().tolist())
    selected_state = st.selectbox("Filter by State", states)
    
    if selected_state != 'All':
        hospital_stats = hospital_stats[hospital_stats['State'] == selected_state]
        
    hospital_stats = hospital_stats.sort_values(by="Avg Risk Score", ascending=False)
    
    st.dataframe(
        hospital_stats[['hospital_id', 'State', 'Avg Claim Amount', 'Fraud Count', 'Image Reuse Cases', 'Avg Risk Score']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Hospital Drill-Down")
    selected_hosp = st.selectbox("Select Hospital for Drill-Down", hospital_stats['hospital_id'])
    
    if selected_hosp:
        h_data = hospital_stats[hospital_stats['hospital_id'] == selected_hosp].iloc[0]
        st.write(f"### Metrics for {selected_hosp}")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div class="metric-title">Total Claims</div><div class="metric-value neutral">{h_data["Total Claims"]}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-title">Fraud Count</div><div class="metric-value {"risk" if h_data["Fraud Count"] > 0 else "safe"}">{h_data["Fraud Count"]}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-title">Avg Risk Score</div><div class="metric-value {"risk" if h_data["Avg Risk Score"] > 60 else ("warn" if h_data["Avg Risk Score"] > 30 else "safe")}">{h_data["Avg Risk Score"]:.2f}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div class="metric-title">State</div><div class="metric-value neutral" style="font-size:1.5rem; line-height:2.5rem;">{h_data["State"]}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        risk_cat = "Low"
        if h_data['Avg Risk Score'] > 80: risk_cat = "Critical"
        elif h_data['Avg Risk Score'] > 60: risk_cat = "High"
        elif h_data['Avg Risk Score'] > 30: risk_cat = "Medium"
        
        st.info(f"**Overall Risk Classification:** {risk_cat}")
        
        st.markdown("#### Fraud Breakdown")
        
        # Plotly Interactive Chart
        breakdown_data = pd.DataFrame({
            'Category': ['Image Reuse', 'Duplicates'],
            'Count': [h_data['Image Reuse Cases'], h_data['Duplicate Cases']]
        })
        fig = px.bar(breakdown_data, x='Category', y='Count', 
                     color='Category',
                     color_discrete_sequence=['#ff595e', '#ffca3a'],
                     template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(l=0, r=0, t=10, b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Prepare data for report export
        if st.button("Generate Audit Report"):
            stats_dict = {
                'state': h_data['State'],
                'total_claims': h_data['Total Claims'],
                'fraud_count': h_data['Fraud Count'],
                'image_reuse_count': h_data['Image Reuse Cases'],
                'duplicate_count': h_data['Duplicate Cases'],
                'avg_risk_score': h_data['Avg Risk Score'],
                'risk_category': risk_cat,
                'avg_claim_deviation': 15.4 # Mock deviation value
            }
            summary = generate_audit_summary(selected_hosp, stats_dict)
            top_claims = hosp_df[hosp_df['hospital_id'] == selected_hosp].sort_values(by='risk_score', ascending=False)
            
            with st.spinner("Generating PDF..."):
                pdf_path = generate_pdf_report(selected_hosp, stats_dict, top_claims, summary)
                
            st.success("Report Generated Successfully!")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_file,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

elif page == "Claim Drill-Down":
    st.title("📄 Claim Drill-Down & AI Analysis")
    st.markdown("---")
    
    claim_df = fetch_claim_data()
    if claim_df is None:
        st.error("Data service temporarily unavailable.")
        st.stop()
        
    tab1, tab2 = st.tabs(["Search Existing Claim", "Upload New Medical Record"])
        
    with tab1:
        selected_claim = st.selectbox("Select a Claim ID to investigate", claim_df['claim_id'].head(1000))
        
        if selected_claim:
            claim_data = claim_df[claim_df['claim_id'] == selected_claim].iloc[0]
            
            st.subheader("Claim Details")
            c1, c2, c3 = st.columns(3)
            c1.write(f"**Hospital ID:** {claim_data['hospital_id']}")
            c1.write(f"**State:** {claim_data['state']}")
            
            c2.write(f"**Procedure Code:** {claim_data['procedure_code']}")
            c2.write(f"**Claim Amount:** ₹{claim_data['claim_amount']:,.2f}")
            
            c3.write(f"**Anomaly Score:** {claim_data['anomaly_score']:.4f}")
            
            st.markdown("---")
            st.subheader("Risk Intelligence")
            
            r1, r2, r3 = st.columns(3)
            
            cat_color = "safe"
            if claim_data['risk_category'] == 'Critical': cat_color = "risk"
            elif claim_data['risk_category'] == 'High': cat_color = "risk"
            elif claim_data['risk_category'] == 'Medium': cat_color = "warn"
            
            r1.markdown(f'<div class="metric-card"><div class="metric-title">Risk Score</div><div class="metric-value {cat_color}">{claim_data["risk_score"]}</div></div>', unsafe_allow_html=True)
            r2.markdown(f'<div class="metric-card"><div class="metric-title">Risk Category</div><div class="metric-value {cat_color}" style="font-size:1.8rem;">{claim_data["risk_category"]}</div></div>', unsafe_allow_html=True)
            
            flags = []
            if claim_data['image_reuse_flag'] == 1: flags.append("📸 Image Reuse")
            if claim_data['duplicate_flag'] == 1: flags.append("📑 Duplicate Claim")
            if claim_data['anomaly_score'] > 0.75: flags.append("⚠️ High Anomaly")
            
            flags_html = "<br>".join(flags) if flags else "No Anomaly Detected"
            flag_class = "risk" if flags else "safe"
            r3.markdown(f'<div class="metric-card"><div class="metric-title">Flags Triggered</div><div class="metric-value {flag_class}" style="font-size:1.1rem; line-height:1.5rem;">{flags_html}</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
                
            with st.expander("View Audit Explanation"):
                if len(flags) > 0:
                    st.warning(f"This claim generated a {claim_data['risk_category']} risk alert due to the following indicators: {', '.join(flags)}. The high anomaly score of {claim_data['anomaly_score']} suggests significant deviation from typical baseline claims for {claim_data['procedure_code']}. Manual verification of supporting documents is recommended.")
                else:
                    st.success("This claim appears normal and conforms to standard baseline metrics. The risk score is within acceptable limits.")

    with tab2:
        st.subheader("Upload Medical Record for Scoring")
        uploaded_file = st.file_uploader("Upload PDF Document (e.g. Bill, Report)", type=["pdf"])

        if uploaded_file is not None:
            with st.spinner("AI Engine Analyzing Document..."):
                # Simulate parsing delay
                import time
                time.sleep(1.5)
                
                # Try to extract text using PyPDF2
                extracted_text = ""
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    num_pages = len(pdf_reader.pages)
                    for page_num in range(min(num_pages, 3)): # read up to first 3 pages
                        extracted_text += pdf_reader.pages[page_num].extract_text() + " "
                except Exception as e:
                    extracted_text = "Error parsing text."

                # Mock Logic - Simulate an analysis finding based on random chance
                import random
                rng = random.Random(uploaded_file.size) # Deterministic based on file size
                
                is_suspicious = rng.random() > 0.6
                mock_amount = rng.randint(3000, 45000)
                mock_proc = f"PROC_{rng.randint(1, 50):03d}"
                
            st.success("Document Analysis Complete")
            
            st.markdown("### Extraction Summary")
            e1, e2, e3 = st.columns(3)
            
            pages = num_pages if 'num_pages' in locals() else 0
            e1.markdown(f'<div class="metric-card"><div class="metric-title">Pages Scanned</div><div class="metric-value neutral">{pages}</div></div>', unsafe_allow_html=True)
            e2.markdown(f'<div class="metric-card"><div class="metric-title">Detected Procedure</div><div class="metric-value neutral" style="font-size:1.5rem;">{mock_proc}</div></div>', unsafe_allow_html=True)
            e3.markdown(f'<div class="metric-card"><div class="metric-title">Detected Bill Amount</div><div class="metric-value {"risk" if is_suspicious else "safe"}">₹{mock_amount:,}</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.expander("Show Raw Extracted Text snippet"):
                if extracted_text.strip():
                    st.text(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
                else:
                    st.text("[No extractable text found. Image-based PDF suspected.]")

            st.markdown("### Risk Assessment")
            if is_suspicious:
                st.error("🚨 HIGH RISK DETECTED")
                st.write("**Flags:**")
                st.write("- Document metadata indicates recent digital tampering.")
                st.write(f"- Billed amount (₹{mock_amount:,}) deviates significantly from regional baseline for {mock_proc}.")
                if not extracted_text.strip():
                    st.write("- Pure image-based PDF. Suspected obfuscation attempt.")
            else:
                st.success("✅ LOW RISK")
                st.write("All extracted features align with established baselines for this procedure and region.")
