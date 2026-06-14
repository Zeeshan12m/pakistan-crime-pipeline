import streamlit as st
import plotly.express as px
import pandas as pd

def show_map(df):
    st.subheader("🗺️ Crime Map — Pakistan")

    df_map = df.dropna(subset=["lat", "lon"]).copy()

    if df_map.empty:
        st.warning("No geo-tagged data available.")
        return

    df_map["size"] = df_map["crime_count"] * 10
    df_map["label"] = df_map.apply(
        lambda r: f"{r['city']}: {r['crime_count']} {r['crime_type']} (severity {r['avg_severity']})",
        axis=1
    )

    color_map = {
        "murder": "#FF0000",
        "terrorism": "#FF4500",
        "assault": "#FF8C00",
        "robbery": "#FFD700",
        "kidnapping": "#9400D3",
        "sexual_crime": "#FF1493",
        "drug_crime": "#00CED1",
        "cybercrime": "#1E90FF",
        "corruption": "#32CD32",
        "extortion": "#A0522D",
        "other": "#808080"
    }

    fig = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        color="crime_type",
        size="size",
        hover_name="city",
        hover_data={
            "crime_type": True,
            "crime_count": True,
            "avg_severity": True,
            "lat": False,
            "lon": False,
            "size": False
        },
        color_discrete_map=color_map,
        zoom=5,
        center={"lat": 30.3753, "lon": 69.3451},
        height=600,
        title="Crime Incidents by City"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("City-level Data")
    city_summary = df.groupby("city").agg(
        total_crimes=("crime_count", "sum"),
        avg_severity=("avg_severity", "mean"),
        crime_types=("crime_type", "nunique")
    ).reset_index().sort_values("total_crimes", ascending=False)
    st.dataframe(city_summary, use_container_width=True)