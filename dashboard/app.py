import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.data_loader import load_data
from src.preprocess import clean_data
from src.feature_engineering import create_features
from src.train_anomaly import train_anomaly_model

st.set_page_config(
    page_title="CICADA Cyber Dashboard",
    layout="wide"
)

st.title("🛡️ CICADA – Cyber Threat Detection Dashboard")
st.markdown("AI-powered Intrusion Detection and Anomaly Monitoring System")


@st.cache_data
def load_pipeline():
    path = "data/raw/network_data.csv"

    df = load_data(path)
    df = clean_data(df)
    df = create_features(df)
    df_result = train_anomaly_model(df)

    df_result = df_result.copy()
    df_result["threat"] = df_result["anomaly"].map({1: "Normal", -1: "Anomaly"})

    # Simple threat score
    if "packet_rate" in df_result.columns and "byte_rate" in df_result.columns:
        packet_norm = (
            (df_result["packet_rate"] - df_result["packet_rate"].min()) /
            (df_result["packet_rate"].max() - df_result["packet_rate"].min() + 1e-9)
        )
        byte_norm = (
            (df_result["byte_rate"] - df_result["byte_rate"].min()) /
            (df_result["byte_rate"].max() - df_result["byte_rate"].min() + 1e-9)
        )

        df_result["threat_score"] = ((0.6 * packet_norm) + (0.4 * byte_norm)) * 100
        df_result["threat_score"] = df_result["threat_score"].round(2)
    else:
        df_result["threat_score"] = 0

    return df_result


df_result = load_pipeline()

total_records = len(df_result)
anomaly_count = int((df_result["anomaly"] == -1).sum())
normal_count = int((df_result["anomaly"] == 1).sum())
anomaly_rate = (anomaly_count / total_records) * 100 if total_records > 0 else 0
avg_threat_score = df_result.loc[df_result["anomaly"] == -1, "threat_score"].mean()
avg_threat_score = 0 if np.isnan(avg_threat_score) else round(avg_threat_score, 2)

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{total_records:,}")

with col2:
    st.metric("Anomalies Detected", f"{anomaly_count:,}")

with col3:
    st.metric("Anomaly Rate", f"{anomaly_rate:.2f}%")

with col4:
    st.metric("Avg Threat Score", f"{avg_threat_score:.2f}")

st.markdown("---")

# Charts row
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Traffic Distribution")
    threat_counts = df_result["threat"].value_counts().reset_index()
    threat_counts.columns = ["Threat Type", "Count"]

    fig_bar = px.bar(
        threat_counts,
        x="Threat Type",
        y="Count",
        title="Normal vs Anomalous Traffic"
    )
    fig_bar.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig_bar, use_container_width=True)

with right_col:
    st.subheader(" Threat Score Distribution")
    fig_hist = px.histogram(
        df_result[df_result["anomaly"] == -1],
        x="threat_score",
        nbins=30,
        title="Threat Scores for Anomalous Records"
    )
    fig_hist.update_layout(xaxis_title="Threat Score", yaxis_title="Frequency")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# Feature row
feat1, feat2 = st.columns(2)

with feat1:
    st.subheader("Packet Rate Sample")
    if "packet_rate" in df_result.columns:
        st.line_chart(df_result["packet_rate"].head(500))
    else:
        st.info("packet_rate column not found.")

with feat2:
    st.subheader("📈 Byte Rate Sample")
    if "byte_rate" in df_result.columns:
        st.line_chart(df_result["byte_rate"].head(500))
    else:
        st.info("byte_rate column not found.")

st.markdown("---")

# Top suspicious records
st.subheader("🔍 Top Suspicious Records")

suspicious_df = df_result[df_result["anomaly"] == -1].copy()

show_cols = [col for col in [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Length of Fwd Packets",
    "packet_rate",
    "byte_rate",
    "high_traffic_flag",
    "threat_score"
] if col in suspicious_df.columns]

if len(suspicious_df) > 0:
    suspicious_df = suspicious_df.sort_values(by="threat_score", ascending=False)
    st.dataframe(suspicious_df[show_cols].head(20), use_container_width=True)
else:
    st.info("No anomalies detected.")

st.markdown("---")

with st.expander("Show Raw Processed Data"):
    st.dataframe(df_result.head(100), use_container_width=True)





import time

st.markdown("---")
st.subheader("Real-Time Traffic Simulation")

run_simulation = st.button("Start Simulation")

if run_simulation:
    placeholder = st.empty()

    sample_data = df_result.sample(100).reset_index(drop=True)

    for i in range(len(sample_data)):
        row = sample_data.iloc[i]

        status = " ANOMALY" if row["anomaly"] == -1 else " NORMAL"

        with placeholder.container():
            st.write(f"### Packet {i+1}")
            st.write(f"Status: {status}")
            st.write(f"Threat Score: {row['threat_score']}")
            st.write("---")

        time.sleep(0.3)