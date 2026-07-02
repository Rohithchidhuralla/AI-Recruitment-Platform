import streamlit as st
from html import escape


class CandidateCards:

    def show(self, df):

        st.markdown(
            """
            <div class="section-title">
                <h2>Candidate Profiles</h2>
                <p>Review ranked candidates with contact details, skills, and match status.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        for _, row in df.iterrows():

            score = row["ATS Score"]

            if score >= 85:
                badge = "Excellent Match"
                card_class = "candidate-card strong"
            elif score >= 70:
                badge = "Good Match"
                card_class = "candidate-card good"
            else:
                badge = "Needs Improvement"
                card_class = "candidate-card"

            name = escape(str(row["Name"]))
            email = escape(str(row["Email"]))
            phone = escape(str(row["Phone"]))
            skills = escape(str(row["Skills"]))

            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="candidate-top">
                        <div>
                            <h3 class="candidate-name">{name}</h3>
                            <div class="candidate-meta">
                                <span>Email: {email}</span>
                                <span>Phone: {phone}</span>
                                <span>Skills: {skills}</span>
                            </div>
                            <span class="status-badge">{badge}</span>
                        </div>
                        <div class="score-badge">
                            <span>ATS</span>
                            {score}%
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
