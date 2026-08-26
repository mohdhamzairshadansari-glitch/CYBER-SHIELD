import random
import time
from datetime import datetime

import requests


API_URL = "http://127.0.0.1:8000/events"


EVENT_TYPES = [
    "NORMAL_LOGIN",
    "FAILED_LOGIN",
    "PORT_SCAN",
    "SQL_INJECTION",
    "MALWARE_DETECTED",
    "SUSPICIOUS_REQUEST"
]


SEVERITIES = {
    "NORMAL_LOGIN": "LOW",
    "FAILED_LOGIN": "MEDIUM",
    "PORT_SCAN": "HIGH",
    "SQL_INJECTION": "CRITICAL",
    "MALWARE_DETECTED": "CRITICAL",
    "SUSPICIOUS_REQUEST": "MEDIUM"
}


USERNAMES = [
    "admin",
    "user",
    "root",
    "guest",
    "john",
    "alice"
]


MESSAGES = {
    "NORMAL_LOGIN": "Successful user login",
    "FAILED_LOGIN": "Failed authentication attempt",
    "PORT_SCAN": "Multiple ports scanned from source IP",
    "SQL_INJECTION": "Possible SQL injection pattern detected",
    "MALWARE_DETECTED": "Malicious file signature detected",
    "SUSPICIOUS_REQUEST": "Abnormal HTTP request detected"
}


def generate_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def generate_event():

    event_type = random.choice(EVENT_TYPES)

    event = {
        "timestamp": datetime.now().isoformat(),
        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),
        "event_type": event_type,
        "severity": SEVERITIES[event_type],
        "username": random.choice(USERNAMES),
        "message": MESSAGES[event_type]
    }

    return event


def send_event(event):

    try:

        response = requests.post(
            API_URL,
            json=event,
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            print(
                f"[+] Event sent | "
                f"{event['event_type']} | "
                f"{event['source_ip']} | "
                f"Event ID: {data['event_id']}"
            )

        else:

            print(
                f"[!] API error: "
                f"{response.status_code}"
            )

    except requests.exceptions.RequestException as e:

        print(f"[!] Connection error: {e}")


def main():

    print("======================================")
    print("   CYBERSHIELD EVENT SIMULATOR")
    print("======================================")
    print("Sending events to:", API_URL)
    print("Press CTRL+C to stop.\n")

    while True:

        event = generate_event()

        send_event(event)

        time.sleep(random.randint(2, 5))


if __name__ == "__main__":
    main()