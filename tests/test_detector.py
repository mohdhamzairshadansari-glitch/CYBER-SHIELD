from types import SimpleNamespace
from backend.core.threat_detector import calculate_risk


event = SimpleNamespace(
    source_ip="192.168.1.100",
    event_type="SQL_INJECTION"
)


result = calculate_risk(event)

print(result)