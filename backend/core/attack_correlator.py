from collections import defaultdict


# Store recent events by source IP
attack_history = defaultdict(list)


def correlate_attack(event):

    """
    Track events from the same source IP
    and detect simple attack chains.
    """

    source_ip = event.source_ip
    event_type = event.event_type

    # Store current event
    attack_history[source_ip].append(event_type)

    # Keep only the latest 20 events
    if len(attack_history[source_ip]) > 20:
        attack_history[source_ip] = attack_history[source_ip][-20:]

    events = attack_history[source_ip]

    # -----------------------------
    # Attack chain detection
    # -----------------------------

    has_port_scan = "PORT_SCAN" in events

    failed_logins = events.count("FAILED_LOGIN")

    has_successful_login = (
        "SUCCESSFUL_LOGIN" in events
        or "SUCCESS_LOGIN" in events
        or "NORMAL_LOGIN" in events
    )

    has_malware = "MALWARE_DETECTED" in events

    # Full attack chain
    if (
        has_port_scan
        and failed_logins >= 3
        and has_successful_login
        and has_malware
    ):

        return {
            "attack_detected": True,
            "attack_type": "MULTI_STAGE_ATTACK",
            "attack_stage": "MALWARE_EXECUTION",
            "description": (
                "Port scan followed by brute force, "
                "successful login and malware activity"
            ),
            "risk_boost": 40
        }

    # Brute force followed by successful login
    if (
        failed_logins >= 3
        and has_successful_login
    ):

        return {
            "attack_detected": True,
            "attack_type": "ACCOUNT_COMPROMISE",
            "attack_stage": "INITIAL_ACCESS",
            "description": (
                "Multiple failed logins followed "
                "by successful login"
            ),
            "risk_boost": 30
        }

    # Reconnaissance pattern
    if has_port_scan:

        return {
            "attack_detected": True,
            "attack_type": "RECONNAISSANCE",
            "attack_stage": "DISCOVERY",
            "description": "Port scanning activity detected",
            "risk_boost": 15
        }

    # No attack chain detected yet
    return {
        "attack_detected": False,
        "attack_type": None,
        "attack_stage": None,
        "description": None,
        "risk_boost": 0
    }