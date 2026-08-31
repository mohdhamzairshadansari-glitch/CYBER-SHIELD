from backend.core.attack_correlator import correlate_attack


class TestEvent:

    def __init__(self, source_ip, event_type):

        self.source_ip = source_ip
        self.event_type = event_type


ip = "10.0.0.99"


test_events = [

    "PORT_SCAN",

    "FAILED_LOGIN",
    "FAILED_LOGIN",
    "FAILED_LOGIN",

    "SUCCESSFUL_LOGIN",

    "MALWARE_DETECTED"
]


for event_type in test_events:

    event = TestEvent(
        source_ip=ip,
        event_type=event_type
    )

    result = correlate_attack(event)

    print(
        f"{event_type} → {result}"
    )