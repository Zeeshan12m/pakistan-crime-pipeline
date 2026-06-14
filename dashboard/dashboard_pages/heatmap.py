import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_heatmap(df):
    st.subheader("🌡️ Crime Heatmap — City vs Crime Type")

    pivot = df.pivot_table(
        index="city",
        columns="crime_type",
        values="crime_count",
        aggfunc="sum",
        fill_value=0
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="Reds",
        text=pivot.values,
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False
    ))

    fig.update_layout(
        title="Crime Frequency Heatmap (City vs Crime Type)",
        xaxis_title="Crime Type",
        yaxis_title="City",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Severity Heatmap")
    pivot_sev = df.pivot_table(
        index="city",
        columns="crime_type",
        values="avg_severity",
        aggfunc="mean",
        fill_value=0
    ).round(1)

    fig2 = go.Figure(data=go.Heatmap(
        z=pivot_sev.values,
        x=pivot_sev.columns.tolist(),
        y=pivot_sev.index.tolist(),
        colorscale="RdYlGn_r",
        text=pivot_sev.values,
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False
    ))

    fig2.update_layout(
        title="Average Severity Heatmap (City vs Crime Type)",
        xaxis_title="Crime Type",
        yaxis_title="City",
        height=600
    )

    st.plotly_chart(fig2, use_container_width=True)