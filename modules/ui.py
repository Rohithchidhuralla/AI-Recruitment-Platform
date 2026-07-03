import streamlit as st

from modules.icons import svg, icon_tile


def load_css():

    with open(
        "modules/static/style.css"
    ) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )


def topbar(section: str, live_label: str = "System operational"):
    """Slim breadcrumb strip rendered above the hero on every page."""

    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-crumbs">
                <span>{svg('layers', 14)} Workspace</span>
                <span class="sep">/</span>
                <span class="current">{section}</span>
            </div>
            <div class="topbar-tag"><span class="dot"></span>{live_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def hero():

    st.markdown(
        f"""
        <div class="app-hero">
            <div class="hero-orb"></div>
            <p class="eyebrow">{svg('sparkles', 14)} AI-powered hiring intelligence</p>
            <h1>AI Recruitment Platform</h1>
            <p>
                Screen resumes, compare role fit, analyze talent signals, and
                export recruiter-ready reports from one polished workspace.
            </p>
            <div class="hero-stats">
                <span>{svg('file', 14)} Resume Parsing</span>
                <span>{svg('target', 14)} ATS Scoring</span>
                <span>{svg('sparkles', 14)} Gemini Analysis</span>
                <span>{svg('chart', 14)} Recruiter Analytics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_cards():

    cards = [
        (
            "Intake",
            "Upload PDF and DOCX resumes with clean extraction.",
            "upload",
            "brand"
        ),
        (
            "Match",
            "Compare candidate skills against role requirements.",
            "target",
            "accent"
        ),
        (
            "Decide",
            "Review analytics, exports, and AI-generated reports.",
            "chart",
            "success"
        )
    ]

    columns = st.columns(3)

    for column, (title, body, icon_name, tone) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    {icon_tile(icon_name, size=18, tone=tone)}
                    <h3>{title}</h3>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


def section_title(title: str, description: str = "", icon_name: str = None, tone: str = "brand"):
    """Renders a section header, optionally with a leading icon tile."""

    icon_html = icon_tile(icon_name, size=17, tone=tone) if icon_name else ""
    desc_html = f'<p>{description}</p>' if description else ""

    st.markdown(
        f"""
        <div class="section-title">
            {icon_html}
            <div class="section-title-text">
                <h2>{title}</h2>
                {desc_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def empty_state(title: str, description: str, icon_name: str = "database", tone: str = "brand"):

    st.markdown(
        f"""
        <div class="empty-state">
            {icon_tile(icon_name, size=22, tone=tone)}
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
