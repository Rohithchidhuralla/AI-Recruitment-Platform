import pandas as pd
import streamlit as st

from modules.database import Database
from modules.charts import Charts
from modules.export_excel import ExcelExporter
from modules.cards import CandidateCards


class RecruiterDashboard:

    def __init__(self):
        self.db = Database()

    def show_dashboard(self):

        st.markdown(
            """
            <div class="section-title">
                <h2>Recruiter Dashboard</h2>
                <p>Track candidate volume, ATS quality, shortlisted talent, and hiring signals.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        candidates = self.db.get_candidates()

        if not candidates:
            st.info("No candidates found. Upload and score a resume to build your pipeline.")
            return

        charts = Charts()
        exporter = ExcelExporter()
        candidate_cards = CandidateCards()

        df = pd.DataFrame(
            candidates,
            columns=[
                "ID",
                "Name",
                "Email",
                "Phone",
                "ATS Score",
                "Skills",
                "Resume"
            ]
        )

        # ===========================================
        # Dashboard Metrics
        # ===========================================

        average_ats = df["ATS Score"].mean()
        highest_ats = df["ATS Score"].max()
        shortlisted = len(df[df["ATS Score"] >= 70])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <p class="metric-label">Candidates</p>
                    <p class="metric-value">{len(df)}</p>
                    <p class="metric-note">Total profiles reviewed</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <p class="metric-label">Average ATS</p>
                    <p class="metric-value">{average_ats:.1f}%</p>
                    <p class="metric-note">Mean candidate fit</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <p class="metric-label">Highest ATS</p>
                    <p class="metric-value">{highest_ats}%</p>
                    <p class="metric-note">Best current match</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <p class="metric-label">Shortlisted</p>
                    <p class="metric-value">{shortlisted}</p>
                    <p class="metric-note">Candidates above 70%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # ===========================================
        # Search
        # ===========================================

        st.markdown(
            """
            <div class="section-title">
                <h2>Search Candidates</h2>
                <p>Filter the pipeline by technical skill or keyword.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        search = st.text_input(
            "Search by Skill",
            placeholder="Try Python, SQL, Streamlit, Machine Learning..."
        )

        filtered_df = df.copy()

        if search:
            filtered_df = filtered_df[
                filtered_df["Skills"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        # ===========================================
        # Candidate List
        # ===========================================

        if filtered_df.empty:
            st.warning("No candidates matched your search.")
            return

        candidate_cards.show(filtered_df)

        st.markdown(
            """
            <div class="section-title">
                <h2>Candidate Database</h2>
                <p>Detailed table view for quick scanning and validation.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ===========================================
        # Top Candidate
        # ===========================================

        st.markdown(
            """
            <div class="section-title">
                <h2>Top Candidate</h2>
                <p>The highest-scoring profile in the current filtered view.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        top = filtered_df.sort_values(
            by="ATS Score",
            ascending=False
        ).head(1)

        st.dataframe(
            top,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ===========================================
        # Analytics
        # ===========================================

        st.markdown(
            """
            <div class="section-title">
                <h2>Recruitment Analytics</h2>
                <p>Visualize score distribution and in-demand skill patterns.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        left, right = st.columns(2)

        with left:
            charts.ats_chart(candidates)

        with right:
            charts.top_skills_chart(candidates)

        st.divider()

        # ===========================================
        # Export
        # ===========================================

        st.markdown(
            """
            <div class="section-title">
                <h2>Export Candidate Data</h2>
                <p>Download the current candidate database as an Excel workbook.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        excel_path = "reports/candidates.xlsx"

        exporter.export(
            candidates,
            excel_path
        )

        with open(excel_path, "rb") as file:

            st.download_button(
                label="📊 Download Excel Report",
                data=file,
                file_name="Candidates.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
