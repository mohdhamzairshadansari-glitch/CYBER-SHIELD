def create_alert(event, analysis, final_risk_score, final_threat_type,
                 behavior, reputation, correlation):
    """
    Create a SOC-friendly real-time alert.
    """

    # -----------------------------
    # Determine alert priority
    # -----------------------------

    if final_risk_score >= 80:
        alert_level = "CRITICAL"
        priority = 1
    elif final_risk_score >= 60:
        alert_level = "HIGH"
        priority = 2
    elif final_risk_score >= 30:
        alert_level = "MEDIUM"
        priority = 3
    else:
        alert_level = "LOW"
        priority = 4

    # -----------------------------
    # Create alert title
    # -----------------------------

    if correlation["attack_detected"]:

        title = f"{correlation['attack_type']} DETECTED"

    elif behavior["behavior_detected"]:

        title = f"{behavior['threat_type']} DETECTED"

    elif reputation["known"]:

        title = f"{reputation['threat_type']} DETECTED"

    elif final_threat_type:

        title = f"{final_threat_type} DETECTED"

    else:

        title = "SECURITY EVENT DETECTED"

    # -----------------------------
    # Create alert object
    # -----------------------------

    return {
        "alert_level": alert_level,
        "priority": priority,
        "title": title,

        "timestamp": event.timestamp.isoformat(),

        "source_ip": event.source_ip,
        "destination_ip": event.destination_ip,

        "event_type": event.event_type,

        "severity": event.severity,

        "risk_score": final_risk_score,

        "threat_type": final_threat_type,

        "behavior_detected": behavior["behavior_detected"],

        "ip_known_malicious": reputation["known"],

        "attack_detected": correlation["attack_detected"],

        "message": event.message
    }