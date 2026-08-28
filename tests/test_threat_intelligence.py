from backend.core.threat_intelligence import check_ip_reputation


# ==========================================
# Test known malicious IP
# ==========================================

known_ip = "192.168.50.200"

result = check_ip_reputation(known_ip)

print("KNOWN IP TEST")
print(result)


# ==========================================
# Test unknown IP
# ==========================================

unknown_ip = "192.168.1.100"

result = check_ip_reputation(unknown_ip)

print("\nUNKNOWN IP TEST")
print(result)