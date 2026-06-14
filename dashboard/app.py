import streamlit as st
import pandas as pd
import glob
import os
import importlib.util
import sys

st.set_page_config(
    page_title="Pakistan Crime Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Pakistan Crime & Safety Dashboard")
st.markdown("Real-time crime intelligence from Dawn, Geo, and Express Tribune")

@st.cache_data(ttl=300)
def load_aggregated():
    path = "data/processed/aggregated_latest.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data(ttl=300)
def load_cleaned():
    path = "data/processed/cleaned_latest.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

df_agg = load_aggregated()
df_clean = load_cleaned()

if df_agg.empty:
    st.error("No data found. Run the pipeline first.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
crime_types = ["All"] + sorted(df_agg["crime_type"].unique().tolist())
selected_crime = st.sidebar.selectbox("Crime Type", crime_types)
cities = ["All"] + sorted(df_agg["city"].unique().tolist())
selected_city = st.sidebar.selectbox("City", cities)

if selected_crime != "All":
    df_agg = df_agg[df_agg["crime_type"] == selected_crime]
    df_clean = df_clean[df_clean["crime_type"] == selected_crime]
if selected_city != "All":
    df_agg = df_agg[df_agg["city"] == selected_city]
    df_clean = df_clean[df_clean["city"] == selected_city]

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", int(df_agg["crime_count"].sum()))
col2.metric("Cities Affected", df_agg["city"].nunique())
col3.metric("Avg Severity", round(df_agg["avg_severity"].mean(), 1))
col4.metric("Crime Types", df_agg["crime_type"].nunique())

st.divider()

# Navigation
page = st.sidebar.radio(
    "View",
    ["Crime Map", "Trend Charts", "Category Breakdown", "Heatmap"]
)

def load_page(module_path, function_name):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)

if page == "Crime Map":
    show_map = load_page("dashboard/dashboard_pages/map_view.py", "show_map")
    show_map(df_agg)
elif page == "Trend Charts":
    show_trends = load_page("dashboard/dashboard_pages/trends.py", "show_trends")
    show_trends(df_clean)
elif page == "Category Breakdown":
    show_categories = load_page("dashboard/dashboard_pages/categories.py", "show_categories")
    show_categories(df_agg)
elif page == "Heatmap":
    show_heatmap = load_page("dashboard/dashboard_pages/heatmap.py", "show_heatmap")
    show_heatmap(df_agg)