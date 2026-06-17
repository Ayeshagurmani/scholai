import streamlit as st
from agents import read_cv, analyze_cv, match_scholarships, generate_sop

# ── Page Setup ────────────────────────────────────────────
st.set_page_config(
    page_title="ScholAI - Scholarship Finder",
    page_icon="🎓",
    layout="wide"
)

# ── Custom Styling ────────────────────────────────────────
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .match-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.title("🎓 ScholAI")
st.subheader("AI-Powered Scholarship Finder for Pakistani Students")
st.caption("Upload your CV → Get matched to scholarships → Generate your SOP instantly")
st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# ── Session State Setup ───────────────────────────────────
# WHY: Streamlit reruns the whole script on every click
# Session state saves our data between reruns
if "profile" not in st.session_state:
    st.session_state.profile = None
if "matches" not in st.session_state:
    st.session_state.matches = None
if "cv_analyzed" not in st.session_state:
    st.session_state.cv_analyzed = False

# ── Step 1: Upload CV ─────────────────────────────────────
st.subheader("📄 Step 1 — Upload Your CV")
st.write("Supported formats: PDF or Word (.docx)")

uploaded_file = st.file_uploader(
    "Choose your CV file",
    type=["pdf", "docx"],
    label_visibility="collapsed"
)

if uploaded_file and not st.session_state.cv_analyzed:
    # ── Step 2: Read and Analyze CV ──────────────────────
    with st.spinner("📖 Reading your CV..."):
        cv_text = read_cv(uploaded_file)

    if len(cv_text.strip()) < 50:
        st.error("Could not read your CV properly. Please make sure it has readable text.")
        st.stop()

    with st.spinner("🧠 AI is analyzing your profile..."):
        profile = analyze_cv(cv_text)
        st.session_state.profile = profile
        st.session_state.cv_analyzed = True

    # ── Step 3: Match Scholarships ────────────────────────
    with st.spinner("🔍 Finding your best scholarship matches..."):
        matches = match_scholarships(profile)
        st.session_state.matches = matches

# ── Show Results if CV is analyzed ───────────────────────
if st.session_state.cv_analyzed and st.session_state.profile:
    profile = st.session_state.profile
    matches = st.session_state.matches

    st.divider()

    # ── Profile Summary ───────────────────────────────────
    st.subheader("👤 Your Profile")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Name", profile.get("name", "N/A"))
    with col2:
        st.metric("GPA", f"{profile.get('gpa', 'N/A')}/4.0")
    with col3:
        st.metric("Experience", f"{profile.get('experience_years', 0)} years")
    with col4:
        st.metric("Education", profile.get("education_level", "N/A"))

    # Skills
    st.write("**🛠️ Skills identified:**")
    skills = profile.get("skills", [])
    cols = st.columns(len(skills) if skills else 1)
    for i, skill in enumerate(skills):
        with cols[i]:
            st.success(skill)

    st.info(f"💬 {profile.get('summary', '')}")

    st.divider()

    # ── Scholarship Matches ───────────────────────────────
    st.subheader("🏆 Your Scholarship Matches")
    st.write(f"Found **{len(matches)}** scholarships ranked by your match score")

    for i, match in enumerate(matches):
        # Color based on match score
        score = match.get("match_score", 0)
        if score >= 70:
            color = "🟢"
        elif score >= 40:
            color = "🟡"
        else:
            color = "🔴"

        with st.expander(
            f"{color} {match['name']} — {match['country']} | "
            f"Match: {score}% | Priority: {match.get('priority', 'N/A')}"
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**✅ Why you match:**")
                st.write(match.get("why_match", ""))

                eligible = match.get("eligible", False)
                if eligible:
                    st.success("✅ You meet basic eligibility requirements")
                else:
                    st.error("❌ You don't meet basic requirements yet")

            with col2:
                st.write("**⚠️ Gaps to fill:**")
                gaps = match.get("gaps", [])
                for gap in gaps:
                    st.warning(f"• {gap}")

            # ── Generate SOP Button ───────────────────────
            if match.get("eligible", False):
                if st.button(
                    f"✍️ Generate SOP for {match['name']}",
                    key=f"sop_{i}"
                ):
                    with st.spinner(f"Writing your SOP for {match['name']}..."):
                        # Find full scholarship details from database
                        sop = generate_sop(profile, match)

                    st.subheader("📝 Your Statement of Purpose")
                    st.text_area(
                        "Copy and use this SOP:",
                        value=sop,
                        height=400,
                        key=f"sop_text_{i}"
                    )
                    st.download_button(
                        label="⬇️ Download SOP",
                        data=sop,
                        file_name=f"SOP_{match['name'].replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"download_{i}"
                    )

    # ── Reset Button ──────────────────────────────────────
    st.divider()
    if st.button("🔄 Analyze Another CV"):
        st.session_state.profile = None
        st.session_state.matches = None
        st.session_state.cv_analyzed = False
        st.rerun()

else:
    # ── Instructions when no CV uploaded ─────────────────
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📄 **Step 1**\nUpload your CV in PDF or Word format")
    with col2:
        st.info("🧠 **Step 2**\nAI analyzes your profile, skills and education")
    with col3:
        st.info("🎓 **Step 3**\nGet matched to scholarships + generate your SOP")
        