import streamlit as st
import tempfile
from pathlib import Path
from html import escape

from modules.auth import Auth
from modules.register import Register

from modules.parser import ResumeParser
from modules.extractor import ResumeExtractor
from modules.ats_engine import ATSEngine
from modules.gemini_ai import GeminiAI
from modules.database import Database
from modules.dashboard import RecruiterDashboard
from modules.report import ReportGenerator
from modules.ui import load_css, hero, feature_cards, topbar, section_title
from modules.icons import svg

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Recruitment Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
load_css()

# -------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------

auth = Auth()
register = Register()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        auth.login()

    with tab2:
        register.show()

    st.stop()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">AI</div>
            <p class="sidebar-title">AI Recruit</p>
            <p class="sidebar-subtitle">Recruitment intelligence suite</p>
        </div>
        <div class="sidebar-pill">Pipeline tools for screening, scoring, analytics, and reporting.</div>
        """,
        unsafe_allow_html=True
    )

    current_user = st.session_state.get("user", {})

    if current_user:

        display_name = escape(str(current_user.get("name", "Recruiter")))
        display_role = escape(str(current_user.get("role", "Recruiter")))
        initials = "".join([part[0] for part in display_name.split()[:2]]).upper() or "R"

        st.markdown(
            f"""
            <div class="sidebar-user">
                <div class="sidebar-user-avatar">{initials}</div>
                <div>
                    <p class="sidebar-user-name">{display_name}</p>
                    <p class="sidebar-user-role">{display_role}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<p class="sidebar-nav-label">Navigation</p>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠 Resume Screening",
            "📊 Recruiter Dashboard"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption("Workspace")
    st.success("AI Powered Recruitment Platform")

    st.caption("Version 2.0")

    auth.logout()
# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if page == "📊 Recruiter Dashboard":

    topbar("Recruiter Dashboard", live_label="Live pipeline")
    hero()
    feature_cards()

    st.write("")

    dashboard = RecruiterDashboard()

    dashboard.show_dashboard()

# -------------------------------------------------
# SCREENING
# -------------------------------------------------

else:

    topbar("Resume Screening", live_label="Ready to screen")
    hero()

    section_title(
        "Resume Screening",
        "Upload a candidate resume and paste a job description to generate ATS insights.",
        icon_name="upload"
    )

    with st.container(border=True):

        upload_col, jd_col = st.columns([1, 1.25])

        with upload_col:
            st.markdown(f"**{svg('file', 15)} Candidate Resume**", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload Resume",
                type=["pdf", "docx"],
                help="Supported formats: PDF and DOCX",
                label_visibility="collapsed"
            )

        with jd_col:
            st.markdown(f"**{svg('briefcase', 15)} Job Description**", unsafe_allow_html=True)
            job_description = st.text_area(
                "Paste Job Description",
                height=190,
                placeholder="Paste the job description, required skills, and role expectations...",
                label_visibility="collapsed"
            )

    if uploaded_file:

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(uploaded_file.read())

            temp_path = temp_file.name

        parser = ResumeParser()

        result = parser.parse_resume(temp_path)

        result["file_name"] = uploaded_file.name

        if result["success"]:

            extractor = ResumeExtractor()

            info = extractor.extract(result["text"])

            st.success("Resume parsed successfully.")

            st.divider()
            # =====================================================
            # Resume Information
            # =====================================================

            section_title(
                "Resume Information",
                "File metadata extracted from the uploaded candidate resume.",
                icon_name="file",
                tone="dark"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📄 File Name",
                    result["file_name"]
                )

            with col2:
                st.metric(
                    "📑 File Type",
                    result["file_type"]
                )

            with col3:
                st.metric(
                    "📚 Pages",
                    result["pages"]
                )

            st.divider()

            # =====================================================
            # Candidate Information
            # =====================================================

            section_title(
                "Candidate Details",
                "Contact information and professional links detected from the resume.",
                icon_name="id",
                tone="brand"
            )

            left, right = st.columns(2)

            with left:

                name = escape(str(info.get("name", "Unknown")))
                email = escape(str(info.get("email", "Not Found")))
                phone = escape(str(info.get("phone", "Not Found")))

                st.markdown(
                    f"""
                    <div class="info-card">
                        <h3>{svg('user', 16)} Contact</h3>
                        <div class="contact-grid">
                            <div class="contact-item">
                                <p class="contact-label">{svg('user', 12)} Name</p>
                                <p class="contact-value">{name}</p>
                            </div>
                            <div class="contact-item">
                                <p class="contact-label">{svg('mail', 12)} Email</p>
                                <p class="contact-value">{email}</p>
                            </div>
                            <div class="contact-item">
                                <p class="contact-label">{svg('phone', 12)} Phone</p>
                                <p class="contact-value">{phone}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right:

                linkedin = escape(str(info.get("linkedin") or "Not Found"))
                github = escape(str(info.get("github") or "Not Found"))

                st.markdown(
                    f"""
                    <div class="info-card">
                        <h3>{svg('link', 16)} Professional Links</h3>
                        <div class="contact-grid">
                            <div class="contact-item">
                                <p class="contact-label">{svg('link', 12)} LinkedIn</p>
                                <p class="contact-value">{linkedin}</p>
                            </div>
                            <div class="contact-item">
                                <p class="contact-label">{svg('link', 12)} GitHub</p>
                                <p class="contact-value">{github}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            # =====================================================
            # Skills
            # =====================================================

            section_title(
                "Technical Skills",
                "Skills detected from the candidate resume.",
                icon_name="layers",
                tone="accent"
            )

            if info["skills"]:

                skills_html = "".join(
                    f'<span class="skill-chip">{escape(str(skill))}</span>'
                    for skill in info["skills"]
                )

                st.markdown(
                    f'<div class="skill-cloud">{skills_html}</div>',
                    unsafe_allow_html=True
                )

            else:

                st.warning("No technical skills detected.")

            st.divider()

            # =====================================================
            # Job Description Check
            # =====================================================

            if not job_description.strip():

                st.info("👆 Paste a Job Description to continue ATS Analysis.")

            else:

                job_info = extractor.extract(job_description)

                ats = ATSEngine()

                ats_result = ats.calculate_score(
                    info["skills"],
                    job_info["skills"]
                )

                section_title(
                    "ATS Score",
                    "Resume fit based on overlap with the job description skills.",
                    icon_name="target",
                    tone="brand"
                )

                score_value = ats_result["score"]

                if score_value >= 85:
                    score_tone = "var(--success)"
                    score_word = "Excellent Match"
                elif score_value >= 70:
                    score_tone = "var(--warning)"
                    score_word = "Good Match"
                else:
                    score_tone = "var(--danger)"
                    score_word = "Needs Improvement"

                score_col, note_col = st.columns([1, 2.2])

                with score_col:
                    st.markdown(
                        f"""
                        <div class="metric-card" style="align-items:center;">
                            <div class="score-ring" style="--pct:{score_value};--ring-color:{score_tone};margin:0 auto;">
                                <span class="score-ring-value">{score_value}%</span>
                            </div>
                            <p class="metric-note" style="text-align:center;margin-top:10px;">{score_word}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with note_col:
                    st.markdown(
                        f"""
                        <div class="metric-card" style="justify-content:center;">
                            <p class="metric-label">Resume Match</p>
                            <p class="metric-value" style="color:{score_tone};">{score_value}%</p>
                            <p class="metric-note">Overlap between resume skills and job requirements</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.progress(score_value / 100)

                st.divider()
                # =====================================================
                # Matching & Missing Skills
                # =====================================================

                col1, col2 = st.columns(2)

                with col1:

                    section_title("Matching Skills", icon_name="check", tone="success")

                    if ats_result["matching_skills"]:

                        for skill in ats_result["matching_skills"]:
                            st.markdown(
                                f'<div class="match-chip yes">{svg("check", 14)} {escape(str(skill))}</div>',
                                unsafe_allow_html=True
                            )

                    else:
                        st.info("No matching skills found.")

                with col2:

                    section_title("Missing Skills", icon_name="cross", tone="danger")

                    if ats_result["missing_skills"]:

                        for skill in ats_result["missing_skills"]:
                            st.markdown(
                                f'<div class="match-chip no">{svg("cross", 14)} {escape(str(skill))}</div>',
                                unsafe_allow_html=True
                            )

                    else:
                        st.success("No missing skills missing!")

                st.divider()

                # =====================================================
                # Save Candidate
                # =====================================================

                db = Database()

                try:

                    db.insert_candidate(
                        name=info.get("name", "Unknown"),
                        email=info.get("email", ""),
                        phone=info.get("phone", ""),
                        ats_score=ats_result["score"],
                        skills=info["skills"],
                        file_name=result["file_name"]
                    )

                except Exception:
                    pass

                # =====================================================
                # AI Resume Analysis
                # =====================================================

                section_title(
                    "AI Resume Analysis",
                    "Generate a recruiter-ready AI assessment and downloadable PDF report.",
                    icon_name="sparkles",
                    tone="brand"
                )

                if st.button("🚀 Generate AI Analysis"):

                    with st.spinner("Gemini AI is analyzing the resume..."):

                        ai = GeminiAI()

                        analysis = ai.analyze_resume(
                            result["text"],
                            ats_result["score"],
                            ats_result["matching_skills"],
                            ats_result["missing_skills"]
                        )

                    st.markdown(analysis)

                    # ===============================================
                    # PDF Report
                    # ===============================================

                    report = ReportGenerator()

                    pdf_path = "reports/report.pdf"

                    report.generate_report(
                        pdf_path,
                        info,
                        ats_result,
                        analysis
                    )

                    with open(pdf_path, "rb") as pdf:

                        st.download_button(
                            "📄 Download AI Report",
                            pdf,
                            file_name="AI_Resume_Report.pdf",
                            mime="application/pdf"
                        )

            st.divider()

            # =====================================================
            # Resume Viewer
            # =====================================================

            with st.expander("📄 View Extracted Resume Text", expanded=False):

                st.text_area(
                    "Resume Content",
                    result["text"],
                    height=400,
                    label_visibility="collapsed"
                )

            # =====================================================
            # Footer
            # =====================================================

            st.divider()

            st.caption("AI Recruitment Platform | Built with Streamlit, Gemini AI & Python")

        else:

            st.error("Failed to parse the uploaded resume.")

    else:

        st.info("Upload a resume to begin screening.")
