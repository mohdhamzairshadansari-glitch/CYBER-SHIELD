from datetime import datetime
from backend.core.alert_formatter import create_alert



class TestEvent:

    def __init__(self):

        self.timestamp = datetime.fromisoformat(
    "2026-08-31T12:00:00+00:00"
)

        self.source_ip = "10.0.0.99"

        self.destination_ip = "192.168.1.10"

        self.event_type = "MALWARE_DETECTED"

        self.severity = "CRITICAL"

        self.message = "Malware detected after attack chain"


event = TestEvent()


analysis = {
    "risk_score": 90,
    "threat_type": "MALWARE"
}


behavior = {
    "behavior_detected": False,
    "threat_type": None
}


reputation = {
    "known": False,
    "threat_type": None
}


correlation = {
    "attack_detected": True,
    "attack_type": "MULTI_STAGE_ATTACK"
}


alert = create_alert(
    event=event,
    analysis=analysis,
    final_risk_score=100,
    final_threat_type="MULTI_STAGE_ATTACK",
    behavior=behavior,
    reputation=reputation,
    correlation=correlation
)


print(alert)