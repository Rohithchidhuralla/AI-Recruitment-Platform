import streamlit as st
from html import escape

from modules.ui import section_title
from modules.icons import svg


class CandidateCards:

    def show(self, df):

        section_title(
            "Candidate Profiles",
            "Review ranked candidates with contact details, skills, and match status.",
            icon_name="users",
            tone="brand"
        )

        for _, row in df.iterrows():

            score = row["ATS Score"]

            if score >= 85:
                badge = "Excellent Match"
                card_class = "candidate-card strong"
                ring_color = "var(--success)"
                badge_icon = "check"
            elif score >= 70:
                badge = "Good Match"
                card_class = "candidate-card good"
                ring_color = "var(--warning)"
                badge_icon = "star"
            else:
                badge = "Needs Improvement"
                card_class = "candidate-card"
                ring_color = "var(--brand)"
                badge_icon = "target"

            name = escape(str(row["Name"]))
            email = escape(str(row["Email"]))
            phone = escape(str(row["Phone"]))
            skills = escape(str(row["Skills"]))

            name_parts = [p for p in str(row["Name"]).strip().split() if p]
            initials = "".join(part[0] for part in name_parts[:2]).upper() or "?"

            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="candidate-top">
                        <div class="candidate-identity">
                            <div class="candidate-avatar">{initials}</div>
                            <div>
                                <h3 class="candidate-name">{name}</h3>
                                <div class="candidate-meta">
                                    <span>{svg('mail', 13)} {email}</span>
                                    <span>{svg('phone', 13)} {phone}</span>
                                    <span>{svg('layers', 13)} {skills}</span>
                                </div>
                                <span class="status-badge">{svg(badge_icon, 12)} {badge}</span>
                            </div>
                        </div>
                        <div class="score-ring" style="--pct:{score};--ring-color:{ring_color};">
                            <span class="score-ring-value">{score}%</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
