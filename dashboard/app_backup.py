import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(interval=3000, key="live_refresh")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([4, 1])

with col1:
    st.title("🛡️ CyberShield")
    st.caption("Real-Time Cybersecurity Threat Monitoring")

with col2:
    st.success("🟢 LIVE")

st.divider()

try:
    events_response = requests.get(f"{API_URL}/events", timeout=5)
    stats_response = requests.get(f"{API_URL}/stats", timeout=5)
    threats_response = requests.get(f"{API_URL}/threats", timeout=5)

    events = events_response.json() if events_response.status_code == 200 else []
    stats = stats_response.json() if stats_response.status_code == 200 else {
        "total_events": 0, "critical_events": 0, "high_events": 0, "detected_threats": 0
    }
    threats = threats_response.json() if threats_response.status_code == 200 else []

except Exception as e:
    events = []
    stats = {"total_events": 0, "critical_events": 0, "high_events": 0, "detected_threats": 0}
    threats = []
    st.error(f"API connection failed: {e}")

if events:
    df = pd.DataFrame(events)
else:
    df = pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events", stats["total_events"])

with col2:
    st.metric("Detected Threats", stats["detected_threats"])

with col3:
    st.metric("Critical Alerts", stats["critical_events"])

with col4:
    st.metric("High Alerts", stats["high_events"])

st.divider()

if not df.empty:
    latest = df.iloc[0]
    severity = latest.get("severity", "UNKNOWN")
    event_type = latest.get("event_type", "UNKNOWN")
    risk_score = latest.get("risk_score", 0)
    source_ip = latest.get("source_ip", "UNKNOWN")

    if severity == "CRITICAL":
        st.error(
            f"🚨 CRITICAL: {event_type} | "
            f"Risk: {risk_score}/100 | "
            f"Source: {source_ip}"
        )
    elif severity == "HIGH":
        st.warning(
            f"⚠️ HIGH: {event_type} | "
            f"Risk: {risk_score}/100 | "
            f"Source: {source_ip}"
        )
    else:
        st.info(
            f"🔎 Latest Event: {event_type} | "
            f"Risk: {risk_score}/100 | "
            f"Source: {source_ip}"
        )

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Event Types")
        event_counts = df["event_type"].value_counts().reset_index()
        event_counts.columns = ["event_type", "count"]
        fig = px.bar(
            event_counts,
            x="event_type",
            y="count",
            title="Security Events by Type",
            color="event_type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🚨 Severity Distribution")
        severity_counts = df["severity"].value_counts().reset_index()
        severity_counts.columns = ["severity", "count"]
        color_map = {"CRITICAL": "#ff4444", "HIGH": "#ff8800", "MEDIUM": "#ffcc00", "LOW": "#44bb44"}
        fig = px.pie(
            severity_counts,
            names="severity",
            values="count",
            title="Severity Distribution",
            color="severity",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Risk Score Distribution")
        fig = px.histogram(
            df,
            x="risk_score",
            nbins=20,
            title="Risk Score Distribution",
            color_discrete_sequence=["#ff6666"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🌐 Top Source IPs")
        ip_counts = df["source_ip"].value_counts().head(10).reset_index()
        ip_counts.columns = ["source_ip", "count"]
        fig = px.bar(
            ip_counts,
            x="count",
            y="source_ip",
            orientation="h",
            title="Top 10 Source IPs",
            color="count",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🚨 Recent Security Events")

if not df.empty:
    columns = ["id", "timestamp", "source_ip", "destination_ip", "event_type", "severity", "risk_score", "username", "message"]
    available_columns = [column for column in columns if column in df.columns]

    def highlight_severity(row):
        severity = row.get("severity", "")
        if severity == "CRITICAL":
            return ["background-color: #ff444433"] * len(row)
        elif severity == "HIGH":
            return ["background-color: #ff880033"] * len(row)
        return [""] * len(row)

    styled_df = df[available_columns].style.apply(highlight_severity, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=400)
else:
    st.info("Waiting for security events...")

st.divider()

st.subheader("🔓 Active Threats")

if threats:
    threats_df = pd.DataFrame(threats)
    open_threats = threats_df[threats_df["status"] == "OPEN"]
    ack_threats = threats_df[threats_df["status"] == "ACKNOWLEDGED"]

    tcol1, tcol2 = st.columns(2)
    with tcol1:
        st.metric("Open Threats", len(open_threats))
    with tcol2:
        st.metric("Acknowledged", len(ack_threats))

    if not open_threats.empty:
        st.dataframe(open_threats, use_container_width=True, hide_index=True)
    else:
        st.success("No open threats!")
else:
    st.info("No threat records found.")