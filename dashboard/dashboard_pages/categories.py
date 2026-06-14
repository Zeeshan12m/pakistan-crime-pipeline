import streamlit as st
import plotly.express as px
import pandas as pd

def show_categories(df):
    st.subheader("📊 Crime Category Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        crime_totals = df.groupby("crime_type")["crime_count"].sum().reset_index()
        crime_totals = crime_totals.sort_values("crime_count", ascending=False)
        fig1 = px.bar(
            crime_totals,
            x="crime_type",
            y="crime_count",
            color="crime_type",
            title="Total Incidents by Crime Type"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(
            crime_totals,
            values="crime_count",
            names="crime_type",
            title="Crime Type Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Severity by Crime Type")
    severity_by_type = df.groupby("crime_type")["avg_severity"].mean().reset_index()
    severity_by_type = severity_by_type.sort_values("avg_severity", ascending=False)

    fig3 = px.bar(
        severity_by_type,
        x="crime_type",
        y="avg_severity",
        color="avg_severity",
        color_continuous_scale="Reds",
        title="Average Severity Score by Crime Type"
    )
    fig3.add_hline(y=7, line_dash="dash", line_color="red",
                   annotation_text="Alert Threshold")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("City vs Crime Type Counts")
    city_crime = df.groupby(["city", "crime_type"])["crime_count"].sum().reset_index()
    fig4 = px.bar(
        city_crime,
        x="city",
        y="crime_count",
        color="crime_type",
        title="Crime Types per City",
        barmode="stack"
    )
    st.plotly_chart(fig4, use_container_width=True)