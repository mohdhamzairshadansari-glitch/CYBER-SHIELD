from collections import defaultdict
from datetime import datetime, timedelta


# Store recent events per source IP
recent_events = defaultdict(list)


def analyze_behavior(event):
    """
    Analyze recent activity from the same source IP
    and detect suspicious behavior patterns.
    """

    now = datetime.utcnow()

    source_ip = event.source_ip

    # Store current event
    recent_events[source_ip].append({
        "timestamp": now,
        "event_type": event.event_type
    })

    # Keep only events from the last 5 minutes
    cutoff = now - timedelta(minutes=5)

    recent_events[source_ip] = [
        e
        for e in recent_events[source_ip]
        if e["timestamp"] >= cutoff
    ]

    events = recent_events[source_ip]

    # ==================================================
    # 1. BRUTE FORCE DETECTION
    # ==================================================

    failed_logins = sum(
        1
        for e in events
        if e["event_type"] == "FAILED_LOGIN"
    )

    if failed_logins >= 5:

        return {
            "behavior_detected": True,
            "threat_type": "BRUTE_FORCE",
            "risk_boost": 40,
            "reason": f"{failed_logins} failed login attempts in 5 minutes"
        }


    # ==================================================
    # 2. PORT SCAN DETECTION
    # ==================================================

    port_scans = sum(
        1
        for e in events
        if e["event_type"] == "PORT_SCAN"
    )

    if port_scans >= 3:

        return {
            "behavior_detected": True,
            "threat_type": "PORT_SCAN",
            "risk_boost": 35,
            "reason": f"{port_scans} port scan events detected"
        }


    # ==================================================
    # 3. EVENT FLOOD DETECTION
    # ==================================================

    if len(events) >= 20:

        return {
            "behavior_detected": True,
            "threat_type": "EVENT_FLOOD",
            "risk_boost": 30,
            "reason": f"{len(events)} events from the same IP"
        }


    # ==================================================
    # NO SUSPICIOUS BEHAVIOR
    # ==================================================

    return {
        "behavior_detected": False,
        "threat_type": None,
        "risk_boost": 0,
        "reason": None
    }