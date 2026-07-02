import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


class Charts:

    def ats_chart(self, candidates):

        if not candidates:
            st.info("No data available.")
            return

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

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(df["Name"], df["ATS Score"])

        ax.set_xlabel("Candidate")
        ax.set_ylabel("ATS Score")
        ax.set_title("ATS Score Comparison")

        plt.xticks(rotation=30)

        st.pyplot(fig)

    def top_skills_chart(self, candidates):

        if not candidates:
            return

        skills = []

        for row in candidates:
            skills.extend(row[5].split(","))

        series = pd.Series(skills)

        counts = series.value_counts().head(10)

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(counts.index, counts.values)

        ax.set_title("Top Skills")

        st.pyplot(fig)