import pandas as pd
import streamlit as st

from modules.database import Database
from modules.charts import Charts
from modules.export_excel import ExcelExporter
from modules.cards import CandidateCards
from modules.ui import section_title, empty_state
from modules.icons import svg


class RecruiterDashboard:

    def __init__(self):
        self.db = Database()

    def show_dashboard(self):

        section_title(
            "Recruiter Dashboard",
            "Track candidate volume, ATS quality, shortlisted talent, and hiring signals.",
            icon_name="dashboard",
            tone="brand"
        )

        candidates = self.db.get_candidates()

        if not candidates:
            empty_state(
                "No candidates yet",
                "Upload and score a resume on the Resume Screening page to build your pipeline.",
                icon_name="database",
                tone="brand"
            )
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

        metric_defs = [
            (col1, "users", "brand", "Candidates", f"{len(df)}", "Total profiles reviewed"),
            (col2, "trending", "accent", "Average ATS", f"{average_ats:.1f}%", "Mean candidate fit"),
            (col3, "award", "warning", "Highest ATS", f"{highest_ats}%", "Best current match"),
            (col4, "star", "success", "Shortlisted", f"{shortlisted}", "Candidates above 70%"),
        ]

        for column, icon_name, tone, label, value, note in metric_defs:
            with column:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-card-top">
                            <p class="metric-label">{label}</p>
                            <span class="icon-tile icon-tile-{tone}">{svg(icon_name, 16)}</span>
                        </div>
                        <div>
                            <p class="metric-value">{value}</p>
                            <p class="metric-note">{note}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        # ===========================================
        # Search
        # ===========================================

        section_title(
            "Search Candidates",
            "Filter the pipeline by technical skill or keyword.",
            icon_name="search",
            tone="dark"
        )

        with st.container(border=True):

            search = st.text_input(
                "Search by Skill",
                placeholder="Try Python, SQL, Streamlit, Machine Learning...",
                label_visibility="collapsed"
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

        section_title(
            "Candidate Database",
            "Detailed table view for quick scanning and validation.",
            icon_name="database",
            tone="dark"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ATS Score": st.column_config.ProgressColumn(
                    "ATS Score",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                )
            }
        )

        st.divider()

        # ===========================================
        # Top Candidate
        # ===========================================

        section_title(
            "Top Candidate",
            "The highest-scoring profile in the current filtered view.",
            icon_name="award",
            tone="warning"
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

        section_title(
            "Recruitment Analytics",
            "Visualize score distribution and in-demand skill patterns.",
            icon_name="chart",
            tone="accent"
        )

        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                charts.ats_chart(candidates)

        with right:
            with st.container(border=True):
                charts.top_skills_chart(candidates)

        st.divider()

        # ===========================================
        # Export
        # ===========================================

        section_title(
            "Export Candidate Data",
            "Download the current candidate database as an Excel workbook.",
            icon_name="download",
            tone="success"
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
