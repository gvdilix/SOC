#!/usr/bin/env python3
"""
seed_threat_test.py — Test AbuseIPDB Threat Intelligence
Run: python seed_threat_test.py
"""
import time, requests, argparse

SERVER = "http://localhost:5000"
DELAY  = 0.4

THREAT_IPS = [
    {"ip": "185.220.101.1", "label": "Tor Exit Node DE — score ~100"},
    {"ip": "45.33.32.156",  "label": "Shodan Scanner US — score ~80"},
    {"ip": "198.235.24.130","label": "Known Brute Force — score ~90"},
    {"ip": "80.82.77.139",  "label": "Scanner NL — score ~85"},
    {"ip": "162.247.74.74", "label": "Tor Exit Node US — score ~95"},
]

def ship(server, agent_id, source_ip, event_type, severity, message):
    try:
        r = requests.post(f"{server}/api/logs/ingest", json={
            "agent_id": agent_id, "agent_os": "linux",
            "source_ip": source_ip, "username": "root",
            "event_type": event_type, "severity": severity,
            "raw_message": message,
        }, timeout=5)
        ok = r.status_code == 201
        print(f"  {'✓' if ok else '✗'} [{severity:8}] {source_ip:20} {message[:50]}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

def main(server):
    print(f"\n{'='*60}\n  GADILIX — Threat Intel Test Seed\n  Server: {server}\n{'='*60}")
    for entry in THREAT_IPS:
        ip = entry["ip"]
        print(f"\n── {ip} — {entry['label']}")
        for i in range(3):
            ship(server, "linux-server-01", ip, "failed_login", "MEDIUM",
                 f"Failed password for root from {ip} port 22 ssh2 attempt {i+1}")
            time.sleep(DELAY)
        ship(server, "linux-server-01", ip, "port_scan", "HIGH",
             f"Nmap scan report from {ip} — 1000 ports scanned")
        time.sleep(DELAY)
        ship(server, "web-server-01", ip, "sql_injection", "HIGH",
             f"GET /login?id=1' UNION SELECT * FROM users-- from {ip}")
        time.sleep(DELAY)
    print(f"\n  Done! Go to Alerts → Investigate → Check Now\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default=SERVER)
    main(parser.parse_args().server)
