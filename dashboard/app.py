import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from textwrap import dedent


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


def render_html(markup: str, unsafe_allow_html: bool = True) -> None:
    st.html(dedent(markup))


st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refresh dashboard every 3 seconds
st_autorefresh(
    interval=3000,
    key="cybershield_refresh"
)


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
    <style>

    /* --------------------------------------------------------
       MAIN APPLICATION
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 20%,
                rgba(0, 255, 255, 0.06),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 80%,
                rgba(0, 120, 255, 0.05),
                transparent 30%
            ),
            #05080d;
        color: #e8f7ff;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #050b12 0%,
                #07121c 50%,
                #04080d 100%
            );

        border-right: 1px solid rgba(0, 220, 255, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: #d9f7ff;
    }


    /* --------------------------------------------------------
       HEADER
    -------------------------------------------------------- */

    .cyber-header {
        padding: 20px 25px;
        border: 1px solid rgba(0, 230, 255, 0.28);
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                rgba(0, 255, 255, 0.08),
                rgba(0, 70, 120, 0.08)
            );

        box-shadow:
            0 0 25px rgba(0, 220, 255, 0.08);

        margin-bottom: 20px;
    }

    .cyber-title {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 5px;
        color: #00eaff;

        text-shadow:
            0 0 8px rgba(0, 234, 255, 0.8),
            0 0 20px rgba(0, 234, 255, 0.35);

        line-height: 1.1;
    }

    .cyber-subtitle {
        margin-top: 8px;
        font-size: 12px;
        letter-spacing: 3px;
        color: #82b9c7;
    }


    /* --------------------------------------------------------
       STATUS
    -------------------------------------------------------- */

    .live-status {
        text-align: center;
        padding: 10px 16px;

        border-radius: 8px;

        background: rgba(0, 255, 120, 0.08);
        border: 1px solid rgba(0, 255, 120, 0.35);

        color: #00ff88;
        font-weight: 700;
        letter-spacing: 2px;

        box-shadow:
            0 0 15px rgba(0, 255, 120, 0.10);
    }


    /* --------------------------------------------------------
       METRIC CARDS
    -------------------------------------------------------- */

    .metric-card {
        position: relative;

        padding: 18px;
        min-height: 125px;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                rgba(10, 25, 38, 0.95),
                rgba(4, 12, 20, 0.95)
            );

        border: 1px solid rgba(0, 220, 255, 0.18);

        box-shadow:
            inset 0 0 20px rgba(0, 220, 255, 0.025),
            0 0 20px rgba(0, 0, 0, 0.25);
    }

    .metric-label {
        color: #7898a5;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .metric-value {
        margin-top: 8px;

        color: #e9fbff;

        font-size: 31px;
        font-weight: 800;

        text-shadow:
            0 0 10px rgba(0, 220, 255, 0.20);
    }


    /* --------------------------------------------------------
       PANELS
    -------------------------------------------------------- */

    .cyber-panel {
        padding: 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                rgba(8, 20, 30, 0.92),
                rgba(3, 10, 16, 0.95)
            );

        border: 1px solid rgba(0, 220, 255, 0.15);

        margin-bottom: 15px;
    }

    .panel-title {
        font-size: 13px;
        letter-spacing: 2px;
        color: #00dfff;
        font-weight: 700;
        margin-bottom: 10px;
    }


    /* --------------------------------------------------------
       ALERTS
    -------------------------------------------------------- */

    .alert-critical {
        padding: 15px;

        border-radius: 10px;

        background: rgba(255, 30, 60, 0.08);
        border: 1px solid rgba(255, 40, 70, 0.40);

        color: #ff6b7d;

        box-shadow:
            0 0 20px rgba(255, 30, 60, 0.08);
    }

    .alert-high {
        padding: 15px;

        border-radius: 10px;

        background: rgba(255, 150, 0, 0.08);
        border: 1px solid rgba(255, 150, 0, 0.35);

        color: #ffb347;
    }

    .alert-medium {
        padding: 15px;

        border-radius: 10px;

        background: rgba(255, 210, 0, 0.06);
        border: 1px solid rgba(255, 210, 0, 0.25);

        color: #ffe066;
    }

    .alert-low {
        padding: 15px;

        border-radius: 10px;

        background: rgba(0, 220, 255, 0.05);
        border: 1px solid rgba(0, 220, 255, 0.20);

        color: #8cefff;
    }


    /* --------------------------------------------------------
       TERMINAL
    -------------------------------------------------------- */

    .terminal {
        background: #020508;

        border: 1px solid rgba(0, 220, 255, 0.18);

        border-radius: 10px;

        padding: 15px;

        font-family:
            Consolas,
            "Courier New",
            monospace;

        font-size: 12px;

        line-height: 1.7;

        max-height: 420px;

        overflow-y: auto;

        box-shadow:
            inset 0 0 30px rgba(0, 220, 255, 0.025);
    }

    .terminal-line {
        color: #82dff0;
    }

    .terminal-time {
        color: #547985;
    }

    .terminal-critical {
        color: #ff5067;
    }

    .terminal-high {
        color: #ffad42;
    }

    .terminal-medium {
        color: #ffe066;
    }

    .terminal-low {
        color: #66e6ff;
    }


    /* --------------------------------------------------------
       SECTION TITLES
    -------------------------------------------------------- */

    .section-title {
        margin-top: 20px;
        margin-bottom: 12px;

        color: #bfefff;

        font-size: 18px;
        font-weight: 700;

        letter-spacing: 2px;

        border-left: 3px solid #00eaff;
        padding-left: 10px;
    }


    /* --------------------------------------------------------
       ATTACK CHAIN
    -------------------------------------------------------- */

    .attack-chain {
        display: flex;
        align-items: center;
        justify-content: center;

        gap: 8px;

        flex-wrap: wrap;

        padding: 20px;
    }

    .attack-node {
        padding: 12px 16px;

        border-radius: 8px;

        background: rgba(0, 220, 255, 0.06);

        border: 1px solid rgba(0, 220, 255, 0.25);

        color: #9defff;

        font-size: 11px;

        letter-spacing: 1px;

        text-align: center;
    }

    .attack-arrow {
        color: #00eaff;
        font-size: 20px;
    }


    /* --------------------------------------------------------
       PIPELINE
    -------------------------------------------------------- */

    .pipeline {
        display: flex;
        justify-content: space-between;
        align-items: center;

        gap: 8px;

        padding: 15px;

        overflow-x: auto;
    }

    .pipeline-node {
        min-width: 120px;

        padding: 14px 10px;

        text-align: center;

        border-radius: 8px;

        background: rgba(0, 220, 255, 0.05);

        border: 1px solid rgba(0, 220, 255, 0.20);

        font-size: 11px;
        color: #bcefff;
    }

    .pipeline-arrow {
        color: #00eaff;
        font-size: 20px;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        margin-top: 35px;
        padding: 15px;

        text-align: center;

        color: #4f7782;

        font-size: 10px;

        letter-spacing: 2px;

        border-top: 1px solid rgba(0, 220, 255, 0.10);
    }


    /* --------------------------------------------------------
       STREAMLIT UI CLEANUP
    -------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background: transparent;
    }

    div[data-testid="stMetricLabel"] {
        color: #7898a5;
    }

    div[data-testid="stMetricValue"] {
        color: #e8fbff;
    }

    .stButton button {
        border: 1px solid rgba(0, 220, 255, 0.25);
        background: rgba(0, 220, 255, 0.05);
        color: #bcefff;
    }

    .stButton button:hover {
        border-color: #00eaff;
        color: #00eaff;
    }

    </style>
    """
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_value(value, default="N/A"):
    """Return a safe display value."""
    if value is None:
        return default

    if pd.isna(value):
        return default

    return value


def severity_class(severity):
    """Return CSS class based on severity."""
    severity = str(severity).upper()

    if severity == "CRITICAL":
        return "terminal-critical"

    if severity == "HIGH":
        return "terminal-high"

    if severity == "MEDIUM":
        return "terminal-medium"

    return "terminal-low"


def format_timestamp(timestamp):
    """Format API timestamp safely."""

    if not timestamp:
        return "N/A"

    try:
        dt = pd.to_datetime(timestamp)

        return dt.strftime("%Y-%m-%d %H:%M:%S")

    except Exception:
        return str(timestamp)


def get_risk_color(score):
    """Return color based on risk score."""

    try:
        score = float(score)
    except Exception:
        score = 0

    if score >= 80:
        return "#ff3355"

    if score >= 60:
        return "#ff9d2e"

    if score >= 40:
        return "#ffe066"

    return "#00eaff"


# ============================================================
# API DATA
# ============================================================

events = []
threats = []

stats = {
    "total_events": 0,
    "critical_events": 0,
    "high_events": 0,
    "detected_threats": 0
}

api_online = False

try:

    events_response = requests.get(
        f"{API_URL}/events",
        timeout=5
    )

    stats_response = requests.get(
        f"{API_URL}/stats",
        timeout=5
    )

    threats_response = requests.get(
        f"{API_URL}/threats",
        timeout=5
    )

    if events_response.status_code == 200:
        events = events_response.json()

    if stats_response.status_code == 200:
        stats = stats_response.json()

    if threats_response.status_code == 200:
        threats = threats_response.json()

    api_online = True

except Exception as e:

    api_online = False

    st.error(
        f"CyberShield API connection failed: {e}"
    )


# ============================================================
# DATAFRAME
# ============================================================

if events:

    df = pd.DataFrame(events)

else:

    df = pd.DataFrame()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div style="
            text-align:center;
            padding:15px 5px;
        ">

            <div style="
                font-size:32px;
                color:#00eaff;
                text-shadow:0 0 15px #00eaff;
            ">
                ◈
            </div>

            <div style="
                font-size:22px;
                font-weight:800;
                letter-spacing:3px;
                color:#00eaff;
            ">
                CYBERSHIELD
            </div>

            <div style="
                font-size:9px;
                letter-spacing:2px;
                color:#638894;
                margin-top:5px;
            ">
                SECURITY INTELLIGENCE PLATFORM
            </div>

        </div>
        """
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "COMMAND CENTER",
            "LIVE MONITORING",
            "THREAT INTELLIGENCE",
            "ATTACK ANALYTICS",
            "SECURITY EVENTS",
            "SYSTEM HEALTH"
        ]
    )

    st.divider()

    if api_online:

        st.success("● API ONLINE")

    else:

        st.error("● API OFFLINE")

    st.caption(
        "AUTO REFRESH: 3 SECONDS"
    )

    st.caption(
        "CyberShield v1.0"
    )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="cyber-header">

        <div class="cyber-title">
            ◈ CYBERSHIELD
        </div>

        <div class="cyber-subtitle">
            REAL-TIME CYBERSECURITY MONITORING // SECURITY OPERATIONS CENTER
        </div>

    </div>
    """
)


# ============================================================
# LIVE STATUS
# ============================================================

status_col1, status_col2 = st.columns([5, 1])

with status_col2:

    if api_online:

        render_html(
            """
            <div class="live-status">
                ● SYSTEM LIVE
            </div>
            """
        )

    else:

        render_html(
            """
            <div class="live-status"
                 style="
                 color:#ff5067;
                 border-color:rgba(255,50,70,.4);
                 background:rgba(255,50,70,.08);
                 ">
                ● OFFLINE
            </div>
            """
        )


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "COMMAND CENTER":

    render_html(
        '<div class="section-title">COMMAND CENTER</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    TOTAL EVENTS
                </div>

                <div class="metric-value">
                    {stats.get("total_events", 0):,}
                </div>

            </div>
            """
        )

    with c2:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    DETECTED THREATS
                </div>

                <div class="metric-value">
                    {stats.get("detected_threats", 0):,}
                </div>

            </div>
            """
        )

    with c3:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    CRITICAL ALERTS
                </div>

                <div class="metric-value">
                    {stats.get("critical_events", 0):,}
                </div>

            </div>
            """
        )

    with c4:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    HIGH ALERTS
                </div>

                <div class="metric-value">
                    {stats.get("high_events", 0):,}
                </div>

            </div>
            """
        )

    st.markdown("")


    # --------------------------------------------------------
    # LATEST EVENT + RISK GAUGE
    # --------------------------------------------------------

    left, right = st.columns([1.35, 1])

    with left:

        render_html(
            '<div class="section-title">LATEST SECURITY EVENT</div>',
            unsafe_allow_html=True
        )

        if not df.empty:

            latest = df.iloc[0]

            severity = str(
                safe_value(
                    latest.get("severity"),
                    "UNKNOWN"
                )
            ).upper()

            event_type = safe_value(
                latest.get("event_type"),
                "UNKNOWN"
            )

            risk_score = safe_value(
                latest.get("risk_score"),
                0
            )

            source_ip = safe_value(
                latest.get("source_ip"),
                "UNKNOWN"
            )

            timestamp = format_timestamp(
                latest.get("timestamp")
            )

            if severity == "CRITICAL":

                css_class = "alert-critical"

            elif severity == "HIGH":

                css_class = "alert-high"

            elif severity == "MEDIUM":

                css_class = "alert-medium"

            else:

                css_class = "alert-low"

            render_html(
                f"""
                <div class="{css_class}">

                    <div style="
                        font-size:11px;
                        letter-spacing:2px;
                        opacity:.7;
                    ">
                        {timestamp}
                    </div>

                    <div style="
                        font-size:24px;
                        font-weight:800;
                        margin-top:8px;
                    ">
                        {event_type}
                    </div>

                    <div style="
                        margin-top:12px;
                        font-size:13px;
                    ">
                        SEVERITY:
                        <b>{severity}</b>
                    </div>

                    <div style="
                        font-size:13px;
                    ">
                        RISK SCORE:
                        <b>{risk_score}/100</b>
                    </div>

                    <div style="
                        font-size:13px;
                    ">
                        SOURCE:
                        <b>{source_ip}</b>
                    </div>

                </div>
                """
            )

        else:

            st.info(
                "Waiting for security events..."
            )


    with right:

        render_html(
            '<div class="section-title">CURRENT RISK LEVEL</div>',
            unsafe_allow_html=True
        )

        if not df.empty:

            try:

                current_risk = float(
                    df.iloc[0].get(
                        "risk_score",
                        0
                    )
                )

            except Exception:

                current_risk = 0

        else:

            current_risk = 0

        gauge_color = get_risk_color(
            current_risk
        )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=current_risk,

                title={
                    "text": "RISK SCORE"
                },

                number={
                    "font": {
                        "size": 42,
                        "color": "#e8fbff"
                    }
                },

                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickcolor": "#648894"
                    },

                    "bar": {
                        "color": gauge_color
                    },

                    "bgcolor": "#07121b",

                    "bordercolor": "#173442",

                    "steps": [
                        {
                            "range": [0, 39],
                            "color": "#08242d"
                        },
                        {
                            "range": [40, 59],
                            "color": "#2b2810"
                        },
                        {
                            "range": [60, 79],
                            "color": "#34200e"
                        },
                        {
                            "range": [80, 100],
                            "color": "#351019"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            height=250,
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=10
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#bcefff"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    if not df.empty:

        chart1, chart2 = st.columns(2)

        with chart1:

            render_html(
                '<div class="section-title">EVENT ACTIVITY</div>',
                unsafe_allow_html=True
            )

            if "event_type" in df.columns:

                event_counts = (
                    df["event_type"]
                    .fillna("UNKNOWN")
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
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=350,
                    xaxis_title="",
                    yaxis_title="EVENT COUNT"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


        with chart2:

            render_html(
                '<div class="section-title">SEVERITY DISTRIBUTION</div>',
                unsafe_allow_html=True
            )

            if "severity" in df.columns:

                severity_counts = (
                    df["severity"]
                    .fillna("UNKNOWN")
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
                    hole=0.55,
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=350,
                    legend_title=""
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


    # --------------------------------------------------------
    # ATTACK CHAIN
    # --------------------------------------------------------

    render_html(
        '<div class="section-title">ATTACK CHAIN MONITOR</div>',
        unsafe_allow_html=True
    )

    render_html(
        """
        <div class="attack-chain">

            <div class="attack-node">
                RECONNAISSANCE
            </div>

            <div class="attack-arrow">
                →
            </div>

            <div class="attack-node">
                DISCOVERY
            </div>

            <div class="attack-arrow">
                →
            </div>

            <div class="attack-node">
                INITIAL ACCESS
            </div>

            <div class="attack-arrow">
                →
            </div>

            <div class="attack-node">
                EXECUTION
            </div>

            <div class="attack-arrow">
                →
            </div>

            <div class="attack-node">
                MALWARE
            </div>

            <div class="attack-arrow">
                →
            </div>

            <div class="attack-node">
                MULTI-STAGE ATTACK
            </div>

        </div>
        """
    )


# ============================================================
# LIVE MONITORING
# ============================================================

elif page == "LIVE MONITORING":

    render_html(
        '<div class="section-title">LIVE SECURITY MONITOR</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        terminal_lines = []

        for _, row in df.head(20).iterrows():

            timestamp = format_timestamp(
                row.get("timestamp")
            )

            event_type = safe_value(
                row.get("event_type"),
                "UNKNOWN"
            )

            severity = str(
                safe_value(
                    row.get("severity"),
                    "UNKNOWN"
                )
            ).upper()

            source_ip = safe_value(
                row.get("source_ip"),
                "UNKNOWN"
            )

            risk = safe_value(
                row.get("risk_score"),
                0
            )

            css = severity_class(
                severity
            )

            terminal_lines.append(
                f"""
                <div class="terminal-line {css}">
                    <span class="terminal-time">
                        [{timestamp}]
                    </span>
                    &nbsp;
                    {severity:<8}
                    |
                    {event_type}
                    |
                    SRC={source_ip}
                    |
                    RISK={risk}/100
                </div>
                """
            )

        render_html(
            f"""
            <div class="terminal">
                {''.join(terminal_lines)}
            </div>
            """
        )

    else:

        st.info(
            "No events received yet."
        )


    # Live table

    render_html(
        '<div class="section-title">LIVE EVENT STREAM</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        display_columns = [
            "id",
            "timestamp",
            "source_ip",
            "destination_ip",
            "event_type",
            "severity",
            "risk_score"
        ]

        available = [
            col for col in display_columns
            if col in df.columns
        ]

        st.dataframe(
            df[available],
            use_container_width=True,
            hide_index=True,
            height=500
        )

    else:

        st.info(
            "Waiting for events..."
        )


# ============================================================
# THREAT INTELLIGENCE
# ============================================================

elif page == "THREAT INTELLIGENCE":

    render_html(
        '<div class="section-title">THREAT INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    if threats:

        threats_df = pd.DataFrame(
            threats
        )

        if "status" in threats_df.columns:

            open_count = len(
                threats_df[
                    threats_df["status"] == "OPEN"
                ]
            )

            acknowledged_count = len(
                threats_df[
                    threats_df["status"] == "ACKNOWLEDGED"
                ]
            )

        else:

            open_count = 0
            acknowledged_count = 0

        t1, t2, t3 = st.columns(3)

        with t1:

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        TOTAL THREATS
                    </div>

                    <div class="metric-value">
                        {len(threats_df)}
                    </div>

                </div>
                """
            )

        with t2:

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        OPEN THREATS
                    </div>

                    <div class="metric-value">
                        {open_count}
                    </div>

                </div>
                """
            )

        with t3:

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        ACKNOWLEDGED
                    </div>

                    <div class="metric-value">
                        {acknowledged_count}
                    </div>

                </div>
                """
            )

        render_html(
            '<div class="section-title">THREAT DATABASE</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            threats_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )

    else:

        st.success(
            "No threat records currently available."
        )


# ============================================================
# ATTACK ANALYTICS
# ============================================================

elif page == "ATTACK ANALYTICS":

    render_html(
        '<div class="section-title">ATTACK ANALYTICS</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        col1, col2 = st.columns(2)

        with col1:

            render_html(
                '<div class="section-title">RISK DISTRIBUTION</div>',
                unsafe_allow_html=True
            )

            if "risk_score" in df.columns:

                fig = px.histogram(
                    df,
                    x="risk_score",
                    nbins=20,
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=350,
                    xaxis_title="RISK SCORE",
                    yaxis_title="EVENT COUNT"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


        with col2:

            render_html(
                '<div class="section-title">TOP SOURCE IPS</div>',
                unsafe_allow_html=True
            )

            if "source_ip" in df.columns:

                ip_counts = (
                    df["source_ip"]
                    .fillna("UNKNOWN")
                    .value_counts()
                    .head(10)
                    .reset_index()
                )

                ip_counts.columns = [
                    "source_ip",
                    "count"
                ]

                fig = px.bar(
                    ip_counts,
                    x="count",
                    y="source_ip",
                    orientation="h",
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=350,
                    xaxis_title="EVENT COUNT",
                    yaxis_title=""
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


        # ----------------------------------------------------
        # EVENT TYPE ANALYSIS
        # ----------------------------------------------------

        render_html(
            '<div class="section-title">EVENT TYPE ANALYSIS</div>',
            unsafe_allow_html=True
        )

        if "event_type" in df.columns:

            type_counts = (
                df["event_type"]
                .fillna("UNKNOWN")
                .value_counts()
                .reset_index()
            )

            type_counts.columns = [
                "event_type",
                "count"
            ]

            fig = px.bar(
                type_counts,
                x="event_type",
                y="count",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    else:

        st.info(
            "Insufficient data for analytics."
        )


# ============================================================
# SECURITY EVENTS
# ============================================================

elif page == "SECURITY EVENTS":

    render_html(
        '<div class="section-title">SECURITY EVENT DATABASE</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        filtered_df = df.copy()

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        f1, f2, f3 = st.columns(3)

        with f1:

            if "severity" in filtered_df.columns:

                severities = sorted(
                    filtered_df[
                        "severity"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                severity_filter = st.multiselect(
                    "SEVERITY",
                    severities
                )

                if severity_filter:

                    filtered_df = filtered_df[
                        filtered_df["severity"]
                        .astype(str)
                        .isin(severity_filter)
                    ]


        with f2:

            if "event_type" in filtered_df.columns:

                event_types = sorted(
                    filtered_df[
                        "event_type"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                event_filter = st.multiselect(
                    "EVENT TYPE",
                    event_types
                )

                if event_filter:

                    filtered_df = filtered_df[
                        filtered_df["event_type"]
                        .astype(str)
                        .isin(event_filter)
                    ]


        with f3:

            if "source_ip" in filtered_df.columns:

                ip_options = sorted(
                    filtered_df[
                        "source_ip"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                ip_filter = st.multiselect(
                    "SOURCE IP",
                    ip_options
                )

                if ip_filter:

                    filtered_df = filtered_df[
                        filtered_df["source_ip"]
                        .astype(str)
                        .isin(ip_filter)
                    ]


        st.write(
            f"Showing **{len(filtered_df)}** events"
        )

        columns = [
            "id",
            "timestamp",
            "source_ip",
            "destination_ip",
            "event_type",
            "severity",
            "risk_score",
            "username",
            "message"
        ]

        available_columns = [
            col for col in columns
            if col in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[available_columns],
            use_container_width=True,
            hide_index=True,
            height=600
        )

    else:

        st.info(
            "No security events found."
        )


# ============================================================
# SYSTEM HEALTH
# ============================================================

elif page == "SYSTEM HEALTH":

    render_html(
        '<div class="section-title">SYSTEM HEALTH</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # COMPONENT STATUS
    # --------------------------------------------------------

    h1, h2, h3 = st.columns(3)

    with h1:

        if api_online:

            st.success(
                "● FASTAPI\n\nONLINE"
            )

        else:

            st.error(
                "● FASTAPI\n\nOFFLINE"
            )

    with h2:

        st.success(
            "● MYSQL\n\nDATABASE"
        )

    with h3:

        st.success(
            "● MONGODB\n\nRAW EVENTS"
        )


    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    render_html(
        '<div class="section-title">CYBERSHIELD PIPELINE</div>',
        unsafe_allow_html=True
    )

    render_html(
        """
        <div class="pipeline">

            <div class="pipeline-node">
                EVENT<br>
                SOURCE
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                FASTAPI
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                THREAT<br>
                DETECTOR
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                RISK<br>
                ANALYZER
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                MYSQL
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                MONGODB
            </div>

            <div class="pipeline-arrow">
                →
            </div>

            <div class="pipeline-node">
                STREAMLIT
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # API INFORMATION
    # --------------------------------------------------------

    render_html(
        '<div class="section-title">SYSTEM INFORMATION</div>',
        unsafe_allow_html=True
    )

    info = {
        "CyberShield API": API_URL,
        "Dashboard": "Streamlit",
        "Refresh Interval": "3 seconds",
        "Database": "MySQL",
        "Raw Event Storage": "MongoDB",
        "Realtime Channel": "WebSocket",
        "Monitoring": "ACTIVE"
    }

    info_df = pd.DataFrame(
        list(info.items()),
        columns=[
            "COMPONENT",
            "VALUE"
        ]
    )

    st.dataframe(
        info_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        ◈ CYBERSHIELD
        &nbsp; // &nbsp;
        REAL-TIME CYBERSECURITY MONITORING
        &nbsp; // &nbsp;
        THREAT INTELLIGENCE PLATFORM

    </div>
    """
)