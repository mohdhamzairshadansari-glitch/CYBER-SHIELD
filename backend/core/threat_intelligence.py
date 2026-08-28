# ==========================================
# CyberShield Threat Intelligence
# ==========================================

THREAT_INTELLIGENCE = {

    "192.168.50.200": {
        "reputation": 95,
        "threat_type": "KNOWN_ATTACKER",
        "description": "Known malicious source"
    },

    "10.10.10.50": {
        "reputation": 90,
        "threat_type": "BOTNET",
        "description": "Known botnet activity"
    },

    "172.16.50.25": {
        "reputation": 85,
        "threat_type": "SCANNER",
        "description": "Known malicious scanner"
    }

}


def check_ip_reputation(source_ip):

    """
    Check whether an IP exists in the
    local threat-intelligence database.
    """

    result = THREAT_INTELLIGENCE.get(source_ip)

    if result:

        return {
            "known": True,
            "reputation": result["reputation"],
            "threat_type": result["threat_type"],
            "description": result["description"]
        }

    return {
        "known": False,
        "reputation": 0,
        "threat_type": None,
        "description": None
    }