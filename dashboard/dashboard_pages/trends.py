import streamlit as st
import plotly.express as px
import pandas as pd

def show_trends(df):
    st.subheader("📈 Crime Trends Over Time")

    if df.empty:
        st.warning("No data available.")
        return

    if "scraped_at" not in df.columns:
        st.warning("No timestamp data available.")
        return

    df["date"] = pd.to_datetime(df["scraped_at"]).dt.date

    daily = df.groupby(["date", "crime_type"]).size().reset_index(name="count")

    fig1 = px.line(
        daily,
        x="date",
        y="count",
        color="crime_type",
        title="Daily Crime Incidents by Type",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        daily_total = df.groupby("date").size().reset_index(name="count")
        fig2 = px.bar(
            daily_total,
            x="date",
            y="count",
            title="Total Daily Incidents"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        severity_trend = df.groupby("date")["severity"].mean().reset_index()
        fig3 = px.line(
            severity_trend,
            x="date",
            y="severity",
            title="Average Daily Severity Score",
            markers=True
        )
        fig3.add_hline(y=7, line_dash="dash", line_color="red",
                       annotation_text="High Severity Threshold")
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Recent Articles")
    cols = ["headline", "crime_type", "city", "severity", "source"]
    available = [c for c in cols if c in df.columns]
    st.dataframe(df[available].head(20), use_container_width=True)