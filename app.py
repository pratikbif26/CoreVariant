
import streamlit as st
import pandas as pd
import time
from src.vcf_parser import parse_uploaded_vcf
from src.api_fetcher import fetch_variant_from_api
from src.llm_generator import generate_acmg_report
from src.pdf_exporter import generate_pdf_bytes

# --- 1. PAGE & THEME CONFIGURATION ---
st.set_page_config(
    page_title="CoreVariant | AI Genomic Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Venice-AI / Claude Inspired CSS Injection
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }
    
    /* Cinematic Animation Keyframes */
    @keyframes cinematicReveal {
        0% { opacity: 0; filter: blur(12px); transform: translateY(20px); }
        100% { opacity: 1; filter: blur(0); transform: translateY(0); }
    }
    
    /* Hero Section Styling */
    .hero-container {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: cinematicReveal 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        margin-bottom: 0.2rem;
        line-height: 1.1;
        letter-spacing: -0.04em;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #10B981;
        font-weight: 500;
        animation: cinematicReveal 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards;
        opacity: 0; /* Start invisible for the delay */
        letter-spacing: 0.02em;
    }
    
    /* Center the Uploader */
    .uploader-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    
    /* Primary Buttons (Venice Emerald Accent) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
        border: none;
    }
    
    /* Auth Badge */
    .auth-badge {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. PERSISTENT SESSION STATE ---
if "groq_api_key" not in st.session_state:
    st.session_state["groq_api_key"] = ""

# --- 3. SIDEBAR AUTH & CONFIGURATION ---
with st.sidebar:
    st.title("⚡ CoreVariant")
    st.markdown("---")
    
    st.subheader("Authentication")
    
    # Check if API key is already saved in session memory
    if st.session_state["groq_api_key"]:
        st.markdown(
            '<div class="auth-badge">🟢 Engine Authenticated & Ready</div>', 
            unsafe_allow_html=True
        )
        if st.button("Change Key", key="reset_key"):
            st.session_state["groq_api_key"] = ""
            st.rerun()
    else:
        input_key = st.text_input("Enter Groq API Key", type="password", help="Requires a valid Groq API key for Llama 3.1 inference.")
        if st.button("Authenticate Engine", type="primary"):
            if input_key:
                st.session_state["groq_api_key"] = input_key.strip()
                st.success("Authenticated successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please paste a valid key.")
        st.markdown("[Get a free Groq Key](https://console.groq.com/keys)")

    st.markdown("---")
    st.caption("CoreVariant v2.0 | Architecture: MyVariant.info + Llama 3.1")

# --- 4. MAIN DASHBOARD UI (ANIMATED HERO) ---
st.markdown('''
<div class="hero-container">
    <div class="hero-title">CoreVariant</div>
    <div class="hero-subtitle">Precision genomics at the speed of thought.</div>
</div>
''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Center the file uploader using Streamlit columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_vcf = st.file_uploader("Drop your VCF file to begin", type=["vcf"])

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. DATA PIPELINE UI ---
if uploaded_vcf is not None:
    df_variants = parse_uploaded_vcf(uploaded_vcf)
    
    if not df_variants.empty:
        st.divider()
        st.subheader("Detected Loci")
        st.dataframe(df_variants, use_container_width=True)
        
        tab1, tab2 = st.tabs(["Single Locus Query", "Batch Pipeline"])
        
        # --- TAB 1: SINGLE QUERY ---
        with tab1:
            st.markdown("#### Analyze Individual Locus")
            variant_ids = df_variants['ID'].tolist()
            selected_variant = st.selectbox("Select variant ID:", variant_ids)
            
            if st.button("Synthesize Dossier", type="primary", key="btn_single"):
                if not st.session_state["groq_api_key"]:
                    st.error("⚠️ Please authenticate your Groq API Key in the sidebar first.")
                else:
                    with st.spinner(f"Retrieving global database evidence for {selected_variant}..."):
                        selected_row = df_variants[df_variants['ID'] == selected_variant].iloc[0]
                        retrieved_data = fetch_variant_from_api(
                            selected_row['CHROM'], selected_row['POS'], selected_row['REF'], selected_row['ALT']
                        )
                        
                        if retrieved_data:
                            llm_report = generate_acmg_report(selected_variant, retrieved_data, st.session_state["groq_api_key"])
                            
                            st.markdown("---")
                            st.subheader("📄 Clinical Interpretation Dossier")
                            with st.container(border=True):
                                st.markdown(llm_report)
                                
                            gene = retrieved_data["metadata"]["gene"]
                            classification = retrieved_data["metadata"]["classification"]
                            pdf_bytes = generate_pdf_bytes(llm_report, selected_variant, gene, classification)
                            
                            st.download_button(
                                label="📥 Export Clinical Report (PDF)",
                                data=pdf_bytes,
                                file_name=f"CoreVariant_{gene}_{selected_variant}.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                        else:
                            st.warning(f"⚠️ No documented clinical consensus found in global databases for {selected_variant}.")

        # --- TAB 2: BATCH PIPELINE ---
        with tab2:
            st.markdown("#### Batch Process Entire VCF")
            st.markdown("Automatically query global databases and generate structured summaries for all detected loci.")
            
            if st.button("Run Batch Pipeline", type="primary", key="btn_batch"):
                if not st.session_state["groq_api_key"]:
                    st.error("⚠️ Please authenticate your Groq API Key in the sidebar first.")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    batch_results = []
                    total_variants = len(df_variants)
                    
                    for i, row in df_variants.iterrows():
                        variant_id = row['ID']
                        status_text.text(f"Analyzing {variant_id} ({i+1}/{total_variants})...")
                        
                        retrieved_data = fetch_variant_from_api(row['CHROM'], row['POS'], row['REF'], row['ALT'])
                        
                        if retrieved_data:
                            llm_report = generate_acmg_report(variant_id, retrieved_data, st.session_state["groq_api_key"])
                            gene = retrieved_data["metadata"]["gene"]
                            classification = retrieved_data["metadata"]["classification"]
                        else:
                            llm_report = "Variant of Uncertain Significance (VUS). No global database hits."
                            gene = "Unknown"
                            classification = "VUS"
                            
                        batch_results.append({
                            "Variant ID": variant_id,
                            "Gene": gene,
                            "Classification": classification,
                            "ACMG Summary": llm_report
                        })
                        
                        time.sleep(0.5)
                        progress_bar.progress((i + 1) / total_variants)
                        
                    status_text.text("✅ CoreVariant Batch Execution Complete!")
                    
                    df_batch = pd.DataFrame(batch_results)
                    st.dataframe(df_batch, use_container_width=True)
                    
                    csv_data = df_batch.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Export Batch Summary (CSV)",
                        data=csv_data,
                        file_name="CoreVariant_Batch_Summary.csv",
                        mime="text/csv",
                        type="primary"
                    )
    else:
        st.error("Could not parse variants. Please ensure this is a valid VCF format.")
