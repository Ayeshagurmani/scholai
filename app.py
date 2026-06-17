import streamlit as st
from agents import read_cv, analyze_cv, match_scholarships, generate_sop

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="ScholAI - Scholarship Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4e 50%, #0d1235 100%);
        min-height: 100vh;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 2rem 2rem 2rem;
        background: linear-gradient(180deg, rgba(255,215,0,0.05) 0%, transparent 100%);
        border-bottom: 1px solid rgba(255,215,0,0.2);
        margin-bottom: 2rem;
    }
    
    .hero-logo {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #a0aec0;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,215,0,0.1);
        border: 1px solid rgba(255,215,0,0.3);
        color: #FFD700;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 1rem;
    }
    
    /* Step cards */
    .steps-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
    }
    
    .step-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        flex: 1;
        max-width: 200px;
    }
    
    .step-number {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .step-title {
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }
    
    .step-desc {
        color: #718096;
        font-size: 0.75rem;
        margin-top: 0.2rem;
    }
    
    /* Upload area */
    .upload-section {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(255,215,0,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Profile card */
    .profile-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Metric styling */
    .metric-box {
        background: rgba(255,215,0,0.08);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        color: #FFD700;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }
    
    /* Scholarship card */
    .schol-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .schol-card:hover {
        border-color: rgba(255,215,0,0.4);
        background: rgba(255,215,0,0.05);
    }
    
    .match-high { color: #48BB78; font-weight: 700; font-size: 1.3rem; }
    .match-mid { color: #ECC94B; font-weight: 700; font-size: 1.3rem; }
    .match-low { color: #FC8181; font-weight: 700; font-size: 1.3rem; }
    
    /* Section headers */
    .section-header {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: 600;
        border-bottom: 1px solid rgba(255,215,0,0.2);
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Skill tag */
    .skill-tag {
        display: inline-block;
        background: rgba(255,215,0,0.1);
        border: 1px solid rgba(255,215,0,0.3);
        color: #FFD700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    
    /* Override streamlit elements */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        color: #0a0e27 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3) !important;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,215,0,0.2) !important;
        border-radius: 12px !important;
    }
    
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,215,0,0.2) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-logo">🎓</div>
    <h1 class="hero-title">ScholAI</h1>
    <p class="hero-subtitle">Your AI-Powered Gateway to Global Scholarships</p>
    <span class="hero-badge">✨ Powered by Llama 3.3 • Built for Pakistani Students</span>
</div>
""", unsafe_allow_html=True)

# ── How It Works Steps ────────────────────────────────────
st.markdown("""
<div class="steps-container">
    <div class="step-card">
        <div class="step-number">01</div>
        <div class="step-title">Upload CV</div>
        <div class="step-desc">PDF or Word format</div>
    </div>
    <div class="step-card">
        <div class="step-number">02</div>
        <div class="step-title">AI Analyzes</div>
        <div class="step-desc">Extracts your profile</div>
    </div>
    <div class="step-card">
        <div class="step-number">03</div>
        <div class="step-title">Get Matched</div>
        <div class="step-desc">Ranked scholarships</div>
    </div>
    <div class="step-card">
        <div class="step-number">04</div>
        <div class="step-title">Generate SOP</div>
        <div class="step-desc">Personalized instantly</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Session State ─────────────────────────────────────────
if "profile" not in st.session_state:
    st.session_state.profile = None
if "matches" not in st.session_state:
    st.session_state.matches = None
if "cv_analyzed" not in st.session_state:
    st.session_state.cv_analyzed = False

# ── Upload Section ────────────────────────────────────────
if not st.session_state.cv_analyzed:
    st.markdown('<p class="section-header">📄 Upload Your CV</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        uploaded_file = st.file_uploader(
            "Drop your CV here",
            type=["pdf", "docx"],
            help="Upload your CV in PDF or Word format"
        )

        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")

            if st.button("🚀 Find My Scholarships", use_container_width=True):
                with st.spinner("📖 Reading your CV..."):
                    cv_text = read_cv(uploaded_file)

                if len(cv_text.strip()) < 50:
                    st.error("Could not read CV properly. Please ensure it has readable text.")
                    st.stop()

                with st.spinner("🧠 Analyzing your profile with AI..."):
                    profile = analyze_cv(cv_text)
                    st.session_state.profile = profile

                with st.spinner("🔍 Matching you to scholarships..."):
                    matches = match_scholarships(profile)
                    st.session_state.matches = matches
                    st.session_state.cv_analyzed = True

                st.rerun()

# ── Results Section ───────────────────────────────────────
if st.session_state.cv_analyzed and st.session_state.profile:
    profile = st.session_state.profile
    matches = st.session_state.matches

    # ── Profile Summary ───────────────────────────────────
    st.markdown('<p class="section-header">👤 Your Profile</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{profile.get('gpa', 'N/A')}</div>
            <div class="metric-label">GPA / 4.0</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{profile.get('experience_years', 0)}</div>
            <div class="metric-label">Years Experience</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{profile.get('education_level', 'N/A')}</div>
            <div class="metric-label">Education Level</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{profile.get('english_test', 'N/A')}</div>
            <div class="metric-label">English Test</div>
        </div>""", unsafe_allow_html=True)

    # Skills
    st.markdown("<br>", unsafe_allow_html=True)
    skills_html = " ".join([f'<span class="skill-tag">{s}</span>'
                            for s in profile.get("skills", [])])
    st.markdown(f'<div>{skills_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.2);
    border-radius:12px;padding:1rem;margin-top:1rem;color:#a0aec0;font-style:italic;">
    💬 {profile.get('summary', '')}
    </div>""", unsafe_allow_html=True)

    # ── Scholarship Matches ───────────────────────────────
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🏆 Your Scholarship Matches</p>',
                unsafe_allow_html=True)
    st.markdown(f'<p style="color:#718096">Found <b style="color:#FFD700">'
                f'{len(matches)}</b> scholarships ranked by compatibility</p>',
                unsafe_allow_html=True)

    for i, match in enumerate(matches):
        score = match.get("match_score", 0)
        if score >= 70:
            score_class = "match-high"
            icon = "🟢"
        elif score >= 40:
            score_class = "match-mid"
            icon = "🟡"
        else:
            score_class = "match-low"
            icon = "🔴"

        with st.expander(
            f"{icon} {match['name']} — {match['country']} | "
            f"{score}% Match | {match.get('priority', '')} Priority"
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<p style="color:#48BB78;font-weight:600">'
                           f'✅ Why You Match</p>', unsafe_allow_html=True)
                st.write(match.get("why_match", ""))

                if match.get("eligible", False):
                    st.success("✅ You meet basic eligibility requirements")
                else:
                    st.error("❌ Requirements not fully met yet")

            with col2:
                st.markdown(f'<p style="color:#FC8181;font-weight:600">'
                           f'⚠️ Gaps To Fill</p>', unsafe_allow_html=True)
                for gap in match.get("gaps", []):
                    st.markdown(f'<p style="color:#a0aec0">• {gap}</p>',
                               unsafe_allow_html=True)

            if match.get("eligible", False):
                if st.button(f"✍️ Generate My SOP for {match['name']}",
                            key=f"sop_{i}",
                            use_container_width=True):
                    with st.spinner("✍️ Writing your personalized SOP..."):
                        sop = generate_sop(profile, match)

                    st.markdown('<p style="color:#FFD700;font-weight:600">'
                               '📝 Your Statement of Purpose</p>',
                               unsafe_allow_html=True)
                    st.text_area("", value=sop, height=400, key=f"sop_text_{i}")
                    st.download_button(
                        label="⬇️ Download SOP as Text File",
                        data=sop,
                        file_name=f"SOP_{match['name'].replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_{i}",
                        use_container_width=True
                    )

    # ── Reset ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🔄 Analyze Another CV", use_container_width=True):
            st.session_state.profile = None
            st.session_state.matches = None
            st.session_state.cv_analyzed = False
            st.rerun()

    # ── Footer ────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#4a5568;font-size:0.8rem;
    border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;">
        🎓 ScholAI • Built for Pakistani Students • 
        Powered by Llama 3.3 on Groq • Made with ❤️
    </div>
    """, unsafe_allow_html=True)