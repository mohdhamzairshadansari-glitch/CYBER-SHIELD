from datetime import datetime, timedelta
from collections import defaultdict


# Store recent events in memory.
# Later we can move this to Redis for a production architecture.
recent_events = defaultdict(list)


def calculate_risk(event):
    """
    Calculate a risk score from 0-100.
    """

    score = 0

    event_type = event.event_type.upper()

    # --------------------------------
    # Base score based on event type
    # --------------------------------

    base_scores = {
        "NORMAL_LOGIN": 5,
        "FAILED_LOGIN": 20,
        "SUSPICIOUS_REQUEST": 35,
        "PORT_SCAN": 60,
        "SQL_INJECTION": 80,
        "MALWARE_DETECTED": 90
    }

    score += base_scores.get(event_type, 10)

    # --------------------------------
    # Track events from the same IP
    # --------------------------------

    ip = event.source_ip

    now = datetime.now()

    recent_events[ip].append(now)

    # Remove events older than 60 seconds

    recent_events[ip] = [
        timestamp
        for timestamp in recent_events[ip]
        if now - timestamp <= timedelta(seconds=60)
    ]

    event_count = len(recent_events[ip])

    # --------------------------------
    # Frequency-based detection
    # --------------------------------

    if event_count >= 10:
        score += 30

    elif event_count >= 5:
        score += 15

    # --------------------------------
    # Specific attack patterns
    # --------------------------------

    threat_type = None

    if event_type == "FAILED_LOGIN" and event_count >= 5:
        threat_type = "BRUTE_FORCE"
        score += 30

    elif event_type == "PORT_SCAN" and event_count >= 3:
        threat_type = "PORT_SCANNING"
        score += 20

    elif event_type == "SQL_INJECTION":
        threat_type = "SQL_INJECTION"

    elif event_type == "MALWARE_DETECTED":
        threat_type = "MALWARE"

    elif event_type == "SUSPICIOUS_REQUEST":
        threat_type = "SUSPICIOUS_ACTIVITY"

    # --------------------------------
    # Cap score
    # --------------------------------

    score = min(score, 100)

    # --------------------------------
    # Determine severity
    # --------------------------------

    if score >= 80:
        severity = "CRITICAL"

    elif score >= 60:
        severity = "HIGH"

    elif score >= 30:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    return {
        "risk_score": score,
        "severity": severity,
        "threat_type": threat_type,
        "event_count": event_count
    }