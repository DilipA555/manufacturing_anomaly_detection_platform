import sys
import os

# fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from database.database_manager import DatabaseManager


# configure page
st.set_page_config(page_title="Anomaly Dashboard", layout="wide")

# title
st.title("Manufacturing Anomaly Detection Dashboard")

# connect to database
db = DatabaseManager()
db.connect()

# fetch data
recent_alerts = db.fetch_anomalies(limit=50)  # can increase anytime
analytics = db.get_anomaly_analytics()
total_records, total_anomalies, total_alerts = db.get_dashboard_metrics()


# convert to dataframes
alerts_df = pd.DataFrame(recent_alerts)
analytics_df = pd.DataFrame(analytics, columns=["sector", "parameter", "count"])


# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background-color:#E8F5E9;padding:20px;border-radius:10px;">
        <div style="color:#2E7D32;font-weight:600;">Total Records</div>
        <div style="font-size:28px;font-weight:bold;">{total_records}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color:#FFEBEE;padding:20px;border-radius:10px;">
        <div style="color:#C62828;font-weight:600;">Total Anomalies</div>
        <div style="font-size:28px;font-weight:bold;">{total_anomalies}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color:#E3F2FD;padding:20px;border-radius:10px;">
        <div style="color:#1565C0;font-weight:600;">Total Alerts</div>
        <div style="font-size:28px;font-weight:bold;">{total_alerts}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# recent alerts
st.subheader("Recent Alerts")

if not alerts_df.empty:
    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"])
    alerts_df = alerts_df.sort_values(by="timestamp", ascending=False)

    alerts_df.reset_index(drop=True, inplace=True)
    alerts_df.index = alerts_df.index + 1

    # dynamic table height (always show 10 rows)
    VISIBLE_ROWS = 10
    ROW_HEIGHT = 35
    HEADER_HEIGHT = 40

    table_height = (VISIBLE_ROWS * ROW_HEIGHT) + HEADER_HEIGHT

    st.dataframe(
        alerts_df,
        use_container_width=True,
        height=table_height
    )
else:
    st.warning("No alerts available")


st.markdown("---")


# charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sector Summary")

    if not analytics_df.empty:
        sector_summary = analytics_df.groupby("sector")["count"].sum().reset_index()
        st.bar_chart(sector_summary.set_index("sector"))
    else:
        st.warning("No data")


with col2:
    st.subheader("Parameter Breakdown")

    if not analytics_df.empty:
        pivot_df = analytics_df.pivot(
            index="sector",
            columns="parameter",
            values="count"
        ).fillna(0)

        st.bar_chart(pivot_df)
    else:
        st.warning("No data")

db.close()