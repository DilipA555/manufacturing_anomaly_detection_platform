import sys
import os
import streamlit as st

# Fix import path (important)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import run_pipeline

# Title
st.title("Manufacturing Anomaly Detection Dashboard")

st.write("Running pipeline...")

# Run backend
result = run_pipeline(generate=False)

st.success("Pipeline executed successfully")

# Extract data
processed_data = result["processed_data"]
anomalies = result["anomalies"]
alerts = result["alerts"]

# Display summary
st.subheader("System Summary")
st.write(f"Total records processed: {len(processed_data)}")
st.write(f"Total anomalies detected: {len(anomalies)}")
st.write(f"Total alerts generated: {len(alerts)}")