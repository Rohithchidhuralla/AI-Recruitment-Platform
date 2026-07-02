import streamlit as st


def load_css():

    with open(
        "modules/static/style.css"
    ) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )


def hero():

    st.markdown(
        """
        <div class="app-hero">
            <p class="eyebrow">AI-powered hiring intelligence</p>
            <h1>AI Recruitment Platform</h1>
            <p>
                Screen resumes, compare role fit, analyze talent signals, and
                export recruiter-ready reports from one polished workspace.
            </p>
            <div class="hero-stats">
                <span>Resume Parsing</span>
                <span>ATS Scoring</span>
                <span>Gemini Analysis</span>
                <span>Recruiter Analytics</span>
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
            "📄"
        ),
        (
            "Match",
            "Compare candidate skills against role requirements.",
            "🎯"
        ),
        (
            "Decide",
            "Review analytics, exports, and AI-generated reports.",
            "📊"
        )
    ]

    columns = st.columns(3)

    for column, (title, body, icon) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
