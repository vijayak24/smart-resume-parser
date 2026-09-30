import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Smart Resume & Portfolio Parser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    
    .main-header p {
        font-size: 1.05rem;
        color: #c7d2fe;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    .badge-pill-success {
        display: inline-block;
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    
    .badge-pill-danger {
        display: inline-block;
        background-color: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    
    .badge-pill-phrase {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.86rem;
        font-weight: 500;
        margin: 3px 4px;
    }
    
    .card-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.2rem;
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>📄 Smart Automated Resume & Portfolio Parser</h1>
    <p>Semantic resume matching & skill gap analysis powered by SentenceTransformers & spaCy</p>
</div>
""", unsafe_allow_html=True)

# Configuration & Backend health
BACKEND_URL = "http://localhost:8000"

# Check backend status
backend_healthy = False
try:
    health_res = requests.get(f"{BACKEND_URL}/health", timeout=1.5)
    if health_res.status_code == 200:
        backend_healthy = True
except Exception:
    backend_healthy = False

# Sidebar with status and sample data
with st.sidebar:
    st.subheader("⚙️ System Status")
    if backend_healthy:
        st.success("🟢 FastAPI Backend Online (Port 8000)")
    else:
        st.warning("🟡 FastAPI Backend Connecting...")
        st.caption("Ensure `backend/main.py` is running on port 8000.")
        
    st.markdown("---")
    st.subheader("💡 Sample Job Descriptions")
    
    sample_jd_ai = """Senior AI/ML Engineer
Requirements:
- Strong proficiency in Python, PyTorch, and TensorFlow.
- Experience with NLP, spaCy, HuggingFace Transformers, and LLMs.
- Solid background in REST API development using FastAPI or Flask.
- Knowledge of Docker, Kubernetes, CI/CD pipelines, and AWS cloud deployment.
- Experience building scalable microservices and database solutions with PostgreSQL and Redis.
- Excellent communication and Agile/Scrum team collaboration skills."""

    sample_jd_fullstack = """Full Stack Software Engineer
Requirements:
- Proven experience with Python, FastAPI, and PostgreSQL.
- Strong frontend skills with React, TypeScript, and modern CSS/Tailwind.
- Hands-on experience with Docker, Git, CI/CD, and Linux environments.
- Knowledge of REST API architecture and Unit Testing.
- Familiarity with cloud platforms (AWS/GCP)."""

    selected_sample = st.selectbox(
        "Load sample job description:",
        ["None", "Senior AI/ML Engineer", "Full Stack Software Engineer"]
    )
    
    st.markdown("---")
    st.caption("Developed with FastAPI, Streamlit, PyPDF2, Sentence-Transformers & spaCy.")

# Main input columns
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 1. Upload Resume (PDF)")
    uploaded_file = st.file_uploader(
        "Choose a PDF resume file",
        type=["pdf"],
        help="Upload candidate resume in PDF format."
    )
    
    if uploaded_file:
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        st.success(f"📎 **{uploaded_file.name}** ({file_size_kb:.1f} KB ready for parsing)")

with col_right:
    st.markdown("### 2. Target Job Description")
    
    default_text = ""
    if selected_sample == "Senior AI/ML Engineer":
        default_text = sample_jd_ai
    elif selected_sample == "Full Stack Software Engineer":
        default_text = sample_jd_fullstack
        
    job_description = st.text_area(
        "Paste the job posting / description text here:",
        value=default_text,
        height=240,
        placeholder="Paste requirements, key skills, responsibilities, and qualifications..."
    )
    
    if job_description:
        word_count = len(job_description.split())
        st.caption(f"📝 {word_count} words in job description")

st.markdown("<br>", unsafe_allow_html=True)

# Submit button
submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
with submit_col2:
    analyze_btn = st.button("🚀 Analyze Resume & Match Job", use_container_width=True, type="primary")

if analyze_btn:
    if not uploaded_file:
        st.error("⚠️ Please upload a PDF resume first.")
    elif not job_description or len(job_description.strip()) < 20:
        st.error("⚠️ Please paste a comprehensive job description (at least 20 characters).")
    else:
        with st.spinner("🧠 Extracting text, generating embeddings, and analyzing semantic match..."):
            try:
                # Prepare payload for FastAPI
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                }
                data = {
                    "job_description": job_description
                }
                
                response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=90)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis completed successfully!")
                    
                    match_score = result.get("match_score", 0.0)
                    matched_skills = result.get("matched_skills", [])
                    missing_skills = result.get("missing_skills", [])
                    missing_phrases = result.get("missing_key_phrases", [])
                    
                    st.markdown("---")
                    st.markdown("## 📊 Analysis Results")
                    
                    # Top Metric Cards
                    m_col1, m_col2, m_col3 = st.columns([1.5, 1, 1])
                    
                    # Score color
                    score_color = "#10b981" if match_score >= 70 else "#f59e0b" if match_score >= 45 else "#ef4444"
                    status_text = "Strong Match" if match_score >= 70 else "Moderate Match" if match_score >= 45 else "Low Match"
                    
                    with m_col1:
                        st.markdown(f"""
                        <div class="card-box" style="text-align: center;">
                            <div style="color: #64748b; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">Semantic Match Score</div>
                            <div class="metric-value" style="color: {score_color}; margin: 8px 0;">{match_score}%</div>
                            <div style="font-weight: 700; color: {score_color};">{status_text}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with m_col2:
                        st.markdown(f"""
                        <div class="card-box" style="text-align: center;">
                            <div style="color: #64748b; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">Matched Skills</div>
                            <div class="metric-value" style="color: #059669; margin: 8px 0;">{len(matched_skills)}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Present in Resume</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with m_col3:
                        st.markdown(f"""
                        <div class="card-box" style="text-align: center;">
                            <div style="color: #64748b; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">Missing Skills</div>
                            <div class="metric-value" style="color: #dc2626; margin: 8px 0;">{len(missing_skills)}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">In Job, Not Resume</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Visual Progress Bar
                    st.progress(min(1.0, match_score / 100.0))
                    
                    # Skill Breakdown Sections
                    st.markdown("<br>", unsafe_allow_html=True)
                    skill_col1, skill_col2 = st.columns(2, gap="large")
                    
                    with skill_col1:
                        st.markdown("### ❌ Missing Skills & Keywords")
                        st.caption("These keywords from the job description were not found in your resume:")
                        if missing_skills:
                            badges_html = "".join([f'<span class="badge-pill-danger">✕ {s}</span>' for s in missing_skills])
                            st.markdown(f'<div style="margin-top: 10px;">{badges_html}</div>', unsafe_allow_html=True)
                        else:
                            st.info("🎉 Excellent! No standard required tech skills were missing.")
                            
                        if missing_phrases:
                            st.markdown("<br><b>Role-Specific Domain Keywords:</b>", unsafe_allow_html=True)
                            phrase_badges = "".join([f'<span class="badge-pill-phrase">• {p}</span>' for p in missing_phrases])
                            st.markdown(f'<div style="margin-top: 8px;">{phrase_badges}</div>', unsafe_allow_html=True)
                            
                    with skill_col2:
                        st.markdown("### ✅ Matched Skills & Strengths")
                        st.caption("Skills found in both the resume and the job description:")
                        if matched_skills:
                            matched_html = "".join([f'<span class="badge-pill-success">✓ {s}</span>' for s in matched_skills])
                            st.markdown(f'<div style="margin-top: 10px;">{matched_html}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("No direct technical skill overlaps detected.")
                    
                    # Resume Extracted Text Snippet
                    with st.expander("📄 View Extracted Resume Preview"):
                        st.text(result.get("resume_snippet", "No preview available."))
                        
                else:
                    error_detail = response.json().get("detail", response.text)
                    st.error(f"❌ Server Error ({response.status_code}): {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Could not connect to FastAPI server at http://localhost:8000. Please make sure the backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
