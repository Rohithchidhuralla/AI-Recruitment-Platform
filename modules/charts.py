import pandas as pd
import plotly.graph_objects as go
import streamlit as st


BRAND = "#5b4fe9"
ACCENT = "#12b8a6"
INK = "#0d1220"
MUTED = "#667085"
GRID = "#eef0f5"


def _base_layout(fig, height=340):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color=INK, size=13),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=13,
            font_family="Inter, sans-serif",
            bordercolor=GRID
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return fig


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

        colors = [
            "#12875a" if score >= 85
            else "#b4690e" if score >= 70
            else "#d1274a"
            for score in df["ATS Score"]
        ]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=df["Name"],
                    y=df["ATS Score"],
                    marker=dict(
                        color=colors,
                        line=dict(width=0),
                        cornerradius=6
                    ),
                    hovertemplate="<b>%{x}</b><br>ATS Score: %{y}%<extra></extra>"
                )
            ]
        )

        fig.update_layout(title=dict(text="ATS Score Comparison", font=dict(size=15, color=INK)))
        fig.update_yaxes(title_text="ATS Score (%)", range=[0, 105])
        fig.update_xaxes(title_text="Candidate", tickangle=-30)

        _base_layout(fig)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    def top_skills_chart(self, candidates):

        if not candidates:
            return

        skills = []

        for row in candidates:
            skills.extend(row[5].split(","))

        skills = [s.strip() for s in skills if s.strip()]

        if not skills:
            st.info("No skill data available.")
            return

        series = pd.Series(skills)

        counts = series.value_counts().head(10).sort_values(ascending=True)

        fig = go.Figure(
            data=[
                go.Bar(
                    x=counts.values,
                    y=counts.index,
                    orientation="h",
                    marker=dict(
                        color=counts.values,
                        colorscale=[[0, "#d8d4fb"], [1, BRAND]],
                        line=dict(width=0),
                        cornerradius=6
                    ),
                    hovertemplate="<b>%{y}</b><br>Mentions: %{x}<extra></extra>"
                )
            ]
        )

        fig.update_layout(title=dict(text="Top Skills", font=dict(size=15, color=INK)))
        fig.update_xaxes(title_text="Mentions")
        fig.update_yaxes(title_text="")

        _base_layout(fig)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
