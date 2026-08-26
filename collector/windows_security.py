import subprocess
import json
import requests
import time


API_URL = "http://127.0.0.1:8000/events"


def get_security_events():

    powershell_command = """
    Get-WinEvent -FilterHashtable @{
        LogName='Security';
        Id=4624,4625
    } -MaxEvents 10 |
    ForEach-Object {
        [PSCustomObject]@{
            TimeCreated = $_.TimeCreated.ToString("o")
            Id = $_.Id
            MachineName = $_.MachineName
            Message = $_.Message
        }
    } |
    ConvertTo-Json -Depth 3
    """

    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            powershell_command
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print("\n[WINDOWS LOG ERROR]")
        print(result.stderr)

        return []

    if not result.stdout.strip():

        return []

    try:

        data = json.loads(
            result.stdout
        )

    except json.JSONDecodeError as e:

        print("\n[JSON ERROR]")
        print(e)
        print(result.stdout)

        return []

    if isinstance(data, dict):

        data = [data]

    return data


def convert_event(event):

    event_id = int(
        event["Id"]
    )

    if event_id == 4625:

        event_type = "FAILED_LOGIN"

        severity = "MEDIUM"

        message = (
            "Windows failed login detected"
        )

    else:

        event_type = "NORMAL_LOGIN"

        severity = "LOW"

        message = (
            "Windows successful login detected"
        )

    return {

        "timestamp": event["TimeCreated"],

        "source_ip": "WINDOWS_HOST",

        "destination_ip": "LOCAL_MACHINE",

        "event_type": event_type,

        "severity": severity,

        "username": "WINDOWS_USER",

        "message": message
    }


def send_event(event):

    try:

        response = requests.post(
            API_URL,
            json=event,
            timeout=5
        )

        print(
            f"[WINDOWS] "
            f"{event['event_type']} "
            f"-> HTTP {response.status_code}"
        )

    except requests.exceptions.RequestException as e:

        print(
            "[API ERROR]",
            e
        )


def main():

    print("=" * 55)
    print("   CYBERSHIELD WINDOWS SECURITY COLLECTOR")
    print("=" * 55)
    print()
    print("Monitoring Windows Security events...")
    print("Press CTRL+C to stop.")
    print()

    processed = set()

    while True:

        events = get_security_events()

        print(
            f"[+] Found {len(events)} Windows events"
        )

        for event in events:

            event_key = (
                str(event["TimeCreated"])
                + "_"
                + str(event["Id"])
            )

            if event_key in processed:

                continue

            processed.add(event_key)

            converted_event = convert_event(
                event
            )

            send_event(
                converted_event
            )

        time.sleep(5)


if __name__ == "__main__":

    main()