import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time


API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

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


# ============================================================
# HEADER
# ============================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.title("🛡️ CyberShield")

    st.caption(
        "Real-Time Cybersecurity Threat Monitoring"
    )

with col2:

    st.success("🟢 LIVE")


st.divider()


# ============================================================
# GET EVENTS
# ============================================================

try:

    # -----------------------------------------
    # Recent events
    # -----------------------------------------

    events_response = requests.get(
        f"{API_URL}/events",
        timeout=5
    )


    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    stats_response = requests.get(
        f"{API_URL}/stats",
        timeout=5
    )


    if events_response.status_code == 200:

        events = events_response.json()

    else:

        events = []


    if stats_response.status_code == 200:

        stats = stats_response.json()

    else:

        stats = {
            "total_events": 0,
            "critical_events": 0,
            "high_events": 0,
            "detected_threats": 0
        }


except Exception as e:

    events = []

    stats = {
        "total_events": 0,
        "critical_events": 0,
        "high_events": 0,
        "detected_threats": 0
    }

    st.error(
        f"API connection failed: {e}"
    )


# ============================================================
# DATAFRAME
# ============================================================

if events:

    df = pd.DataFrame(events)

else:

    df = pd.DataFrame()


# ============================================================
# METRICS
# ============================================================

if not df.empty:

    total_events = len(df)

    critical_events = len(
        df[df["severity"] == "CRITICAL"]
    )

    high_events = len(
        df[df["severity"] == "HIGH"]
    )

    detected_threats = len(
        df[
            df["risk_score"] >= 60
        ]
    )

else:

    total_events = 0
    critical_events = 0
    high_events = 0
    detected_threats = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Events",
        total_events
    )


with col2:

    st.metric(
        "Detected Threats",
        detected_threats
    )


with col3:

    st.metric(
        "Critical Alerts",
        critical_events
    )


with col4:

    st.metric(
        "High Alerts",
        high_events
    )


st.divider()


# ============================================================
# LATEST THREAT
# ============================================================

if not df.empty:

    latest = df.iloc[0]

    severity = latest.get(
        "severity",
        "UNKNOWN"
    )

    event_type = latest.get(
        "event_type",
        "UNKNOWN"
    )

    risk_score = latest.get(
        "risk_score",
        0
    )

    source_ip = latest.get(
        "source_ip",
        "UNKNOWN"
    )

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


# ============================================================
# CHARTS
# ============================================================

if not df.empty:

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # EVENT TYPES
    # --------------------------------------------------------

    with col1:

        st.subheader("🎯 Event Types")

        event_counts = (
            df["event_type"]
            .value_counts()
            .reset_index()
        )

        event_counts.columns = [
            "event_type",
            "count"
        ]

        fig = px.bar(
            event_counts,
            x="event_type",
            y="count",
            title="Security Events"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    with col2:

        st.subheader("🚨 Severity")

        severity_counts = (
            df["severity"]
            .value_counts()
            .reset_index()
        )

        severity_counts.columns = [
            "severity",
            "count"
        ]

        fig = px.pie(
            severity_counts,
            names="severity",
            values="count",
            title="Severity Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# SECURITY EVENTS TABLE
# ============================================================

st.divider()

st.subheader("🚨 Security Events")


if not df.empty:

    columns = [
        "id",
        "timestamp",
        "source_ip",
        "event_type",
        "severity",
        "risk_score",
        "message"
    ]

    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    st.dataframe(
        df[available_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Waiting for security events..."
    )


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(2)

st.rerun()