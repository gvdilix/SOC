#!/usr/bin/env python3
"""
gadilix/seed_test_logs.py
==========================
Sends realistic sample logs to the Gadilix server for testing.
Run AFTER starting the server:
  python seed_test_logs.py --server http://localhost:5000
"""

import time
import random
import requests
import argparse

SERVER = "http://localhost:5000"

SAMPLE_LOGS = [
    # Normal logins
    {"agent_id":"linux-01","agent_os":"linux","event_type":"accepted_login","severity":"INFO",
     "source_ip":"192.168.1.10","username":"alice","raw_message":"Accepted password for alice from 192.168.1.10 port 22 ssh2"},
    {"agent_id":"linux-01","agent_os":"linux","event_type":"accepted_login","severity":"INFO",
     "source_ip":"192.168.1.15","username":"bob","raw_message":"Accepted publickey for bob from 192.168.1.15 port 44320 ssh2"},

    # Failed logins
    {"agent_id":"linux-01","agent_os":"linux","event_type":"failed_login","severity":"MEDIUM",
     "source_ip":"45.33.32.156","username":"root","raw_message":"Failed password for root from 45.33.32.156 port 22 ssh2"},
    {"agent_id":"linux-02","agent_os":"linux","event_type":"failed_login","severity":"MEDIUM",
     "source_ip":"178.62.52.236","username":"admin","raw_message":"Failed password for admin from 178.62.52.236 port 22 ssh2"},

    # Invalid users
    {"agent_id":"linux-01","agent_os":"linux","event_type":"invalid_user","severity":"MEDIUM",
     "source_ip":"103.21.244.0","username":"hacker","raw_message":"Invalid user hacker from 103.21.244.0 port 60434"},

    # Sudo commands
    {"agent_id":"linux-02","agent_os":"linux","event_type":"sudo_command","severity":"LOW",
     "source_ip":None,"username":"alice","raw_message":"sudo: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/bin/cat /etc/shadow"},

    # Windows events
    {"agent_id":"win-dc01","agent_os":"windows","event_type":"accepted_login","severity":"INFO",
     "source_ip":"10.0.0.5","username":"DOMAIN\\john.doe","raw_message":"EventID=4624 An account was successfully logged on"},
    {"agent_id":"win-dc01","agent_os":"windows","event_type":"failed_login","severity":"MEDIUM",
     "source_ip":"10.0.0.99","username":"administrator","raw_message":"EventID=4625 An account failed to log on User=administrator"},
    {"agent_id":"win-dc01","agent_os":"windows","event_type":"account_lockout","severity":"HIGH",
     "source_ip":"10.0.0.99","username":"administrator","raw_message":"EventID=4740 A user account was locked out"},
]

BRUTE_FORCE_BURST = [
    {"agent_id":"linux-01","agent_os":"linux","event_type":"failed_login","severity":"MEDIUM",
     "source_ip":"45.33.32.156","username":"root",
     "raw_message":f"Failed password for root from 45.33.32.156 port {random.randint(40000,65000)} ssh2"}
    for _ in range(8)
]


def ship(server, payload):
    try:
        r = requests.post(f"{server}/api/logs/ingest", json=payload, timeout=5)
        status = "✓" if r.status_code == 201 else f"✗ ({r.status_code})"
        print(f"  {status} {payload['event_type']:20s} {payload.get('source_ip',''):18s} {payload.get('username','')}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main(server):
    print(f"\n[Gadilix Seeder] → {server}\n")

    print("── Normal & misc events ──")
    for log in SAMPLE_LOGS:
        ship(server, log)
        time.sleep(0.2)

    print("\n── Brute-force burst (should trigger HIGH alert) ──")
    for log in BRUTE_FORCE_BURST:
        ship(server, log)
        time.sleep(0.15)

    print("\n[Seeder] Done. Check the dashboard.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default=SERVER)
    args = parser.parse_args()
    main(args.server)
