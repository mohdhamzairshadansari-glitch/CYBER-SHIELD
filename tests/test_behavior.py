from backend.core.behavior_analyzer import analyze_behavior


class TestEvent:

    def __init__(self, source_ip, event_type):
        self.source_ip = source_ip
        self.event_type = event_type


ip = "192.168.1.50"


for i in range(5):

    event = TestEvent(
        source_ip=ip,
        event_type="FAILED_LOGIN"
    )

    result = analyze_behavior(event)

    print(
        f"Attempt {i + 1}:",
        result
    )