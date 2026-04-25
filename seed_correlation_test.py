#!/usr/bin/env python3
"""
seed_correlation_test.py
=========================
Injects logs designed to trigger ALL 5 correlation rules.

Usage:
    python seed_correlation_test.py
    python seed_correlation_test.py --server http://192.168.0.108:5000

Rules tested:
    SAME_IP_ATTACK     — 5 alerts from 10.0.0.66 in 1 minute
    RECON_TO_EXPLOIT   — port scan then SQL injection from 185.220.1.1
    PERSISTENCE_CHAIN  — priv esc + new user + crontab on same machine
    LATERAL_MOVEMENT   — same IP hits 4 different machines
    KILL_CHAIN         — full recon → exploit → privesc → persist chain
"""

import argparse
import time
import requests

SERVER = "http://localhost:5000"
DELAY  = 0.3

GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ship(server, agent_id, agent_os, source_ip, username, event_type, severity, message):
    try:
        r = requests.post(f"{server}/api/logs/ingest", json={
            "agent_id":    agent_id,
            "agent_os":    agent_os,
            "source_ip":   source_ip,
            "username":    username,
            "event_type":  event_type,
            "severity":    severity,
            "raw_message": message,
        }, timeout=5)
        ok = r.status_code == 201
        sym = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
        sev_color = {
            "CRITICAL": f"{BOLD}{RED}",
            "HIGH":     RED,
            "MEDIUM":   YELLOW,
            "LOW":      CYAN,
        }.get(severity, "")
        print(f"  {sym} [{sev_color}{severity:8}{RESET}] {agent_id:20} {source_ip or '':18} {message[:55]}")
        return ok
    except Exception as e:
        print(f"  {RED}✗ ERROR: {e}{RESET}")
        return False

def section(title, color=CYAN):
    print(f"\n{BOLD}{color}{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}{RESET}")


def main(server):
    print(f"\n{BOLD}{'═'*60}")
    print(f"  GADILIX — Correlation Engine Test Seed")
    print(f"  Server: {server}")
    print(f"{'═'*60}{RESET}")

    # ── RULE 1: SAME_IP_ATTACK ─────────────────────────────────────────────
    section("Rule 1: SAME_IP_ATTACK (5 alerts, same IP 10.0.0.66)", YELLOW)
    print(f"  {YELLOW}Trigger: 3+ alerts from same IP in 10 minutes{RESET}\n")

    for i in range(5):
        ship(server, "linux-server-01", "linux", "10.0.0.66", "root",
             "failed_login", "MEDIUM",
             f"Mar 22 10:0{i}:01 server sshd[100{i}]: Failed password for root from 10.0.0.66 port 22 ssh2")
        time.sleep(DELAY)

    # ── RULE 2: RECON_TO_EXPLOIT ───────────────────────────────────────────
    section("Rule 2: RECON_TO_EXPLOIT (scan then SQLi from 185.220.1.1)", YELLOW)
    print(f"  {YELLOW}Trigger: port scan followed by web attack same IP{RESET}\n")

    ship(server, "web-server-01", "linux", "185.220.1.1", None,
         "port_scan", "HIGH",
         "Nmap scan report for 192.168.1.1 Host is up 1000 ports scanned")
    time.sleep(DELAY)

    ship(server, "web-server-01", "linux", "185.220.1.1", None,
         "web_scanner", "HIGH",
         "GET /index.php HTTP/1.1 User-Agent: sqlmap/1.7.8#stable")
    time.sleep(DELAY)

    ship(server, "web-server-01", "linux", "185.220.1.1", None,
         "sql_injection", "HIGH",
         "GET /login?user=admin' UNION SELECT username,password FROM users-- HTTP/1.1")
    time.sleep(DELAY)

    ship(server, "web-server-01", "linux", "185.220.1.1", None,
         "command_injection", "CRITICAL",
         "POST /ping?host=127.0.0.1;cat /etc/shadow HTTP/1.1 200")
    time.sleep(DELAY)

    # ── RULE 3: PERSISTENCE_CHAIN ──────────────────────────────────────────
    section("Rule 3: PERSISTENCE_CHAIN (priv esc + user created + crontab)", YELLOW)
    print(f"  {YELLOW}Trigger: privilege escalation then persistence on same machine{RESET}\n")

    ship(server, "linux-server-02", "linux", None, "www-data",
         "privilege_escalation", "HIGH",
         "Mar 22 10:05:00 server sudo: www-data : TTY=pts/1 ; PWD=/ ; USER=root ; COMMAND=/bin/bash")
    time.sleep(DELAY)

    ship(server, "linux-server-02", "linux", None, "backdoor_user",
         "user_created", "MEDIUM",
         "Mar 22 10:05:30 server useradd[2001]: new user: name=backdoor_user, UID=1337, GID=1337")
    time.sleep(DELAY)

    ship(server, "linux-server-02", "linux", None, "backdoor_user",
         "group_change", "HIGH",
         "Mar 22 10:05:35 server usermod[2002]: add 'backdoor_user' to group 'sudo'")
    time.sleep(DELAY)

    ship(server, "linux-server-02", "linux", None, "www-data",
         "crontab_modified", "HIGH",
         "Mar 22 10:06:00 server cron[2006]: (www-data) REPLACE (crontabs/www-data)")
    time.sleep(DELAY)

    ship(server, "linux-server-02", "linux", None, "root",
         "critical_file_modified", "HIGH",
         "Mar 22 10:06:10 server audit[2005]: type=PATH name=/etc/passwd inode=12345")
    time.sleep(DELAY)

    # ── RULE 4: LATERAL_MOVEMENT ───────────────────────────────────────────
    section("Rule 4: LATERAL_MOVEMENT (same IP attacks 4 machines)", YELLOW)
    print(f"  {YELLOW}Trigger: 1 IP hitting 3+ different machines{RESET}\n")

    machines = ["dc-server-01", "file-server-01", "mail-server-01", "db-server-01"]
    for machine in machines:
        ship(server, machine, "windows", "203.0.113.99", "administrator",
             "failed_login", "MEDIUM",
             f"EventID=4625 An account failed to log on User=administrator IP=203.0.113.99 Machine={machine}")
        time.sleep(DELAY)

        ship(server, machine, "windows", "203.0.113.99", "administrator",
             "failed_login", "MEDIUM",
             f"EventID=4625 An account failed to log on User=administrator IP=203.0.113.99 Machine={machine}")
        time.sleep(DELAY)

    # ── RULE 5: KILL_CHAIN ─────────────────────────────────────────────────
    section("Rule 5: KILL_CHAIN (full attack lifecycle from 45.33.32.200)", YELLOW)
    print(f"  {YELLOW}Trigger: recon + exploit + privesc + persist same IP{RESET}\n")

    # Recon
    ship(server, "linux-server-03", "linux", "45.33.32.200", None,
         "port_scan", "HIGH",
         "Nmap scan report for 192.168.1.5 Host is up 65535 ports scanned masscan")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", None,
         "web_scanner", "HIGH",
         "GET /index.php HTTP/1.1 User-Agent: nikto/2.1.6 (Nikto)")
    time.sleep(DELAY)

    # Initial access
    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "failed_login", "MEDIUM",
         "Mar 22 11:00:01 server sshd[3001]: Failed password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "failed_login", "MEDIUM",
         "Mar 22 11:00:03 server sshd[3002]: Failed password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "failed_login", "MEDIUM",
         "Mar 22 11:00:05 server sshd[3003]: Failed password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "failed_login", "MEDIUM",
         "Mar 22 11:00:07 server sshd[3004]: Failed password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "failed_login", "MEDIUM",
         "Mar 22 11:00:09 server sshd[3005]: Failed password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    # Privilege escalation
    ship(server, "linux-server-03", "linux", "45.33.32.200", "www-data",
         "privilege_escalation", "HIGH",
         "Mar 22 11:01:00 server sudo: www-data : TTY=pts/0 ; USER=root ; COMMAND=/bin/bash")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "root_login_attempt", "HIGH",
         "Mar 22 11:01:10 server sshd[3010]: Accepted password for root from 45.33.32.200 port 22 ssh2")
    time.sleep(DELAY)

    # Persistence
    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "user_created", "MEDIUM",
         "Mar 22 11:02:00 server useradd[4001]: new user: name=hax0r, UID=1338, GID=1338")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "crontab_modified", "HIGH",
         "Mar 22 11:02:30 server cron: root REPLACE (crontabs/root) added reverse shell")
    time.sleep(DELAY)

    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "kernel_module", "HIGH",
         "Mar 22 11:03:00 server kernel: insmod rootkit.ko loaded successfully")
    time.sleep(DELAY)

    # Exfiltration
    ship(server, "linux-server-03", "linux", "45.33.32.200", "root",
         "data_exfiltration", "CRITICAL",
         "ALLOW outbound 192.168.1.5 -> 45.33.32.200:443 350 MB sent upload transferred")
    time.sleep(DELAY)

    # ── Done ───────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"  {GREEN}All logs injected!{RESET}")
    print(f"\n  Next steps:")
    print(f"  1. Go to dashboard → Incidents page")
    print(f"  2. Click {CYAN}'Run Correlation Now'{RESET}")
    print(f"  3. You should see 5 incidents created:")
    print(f"     {RED}• SAME_IP_ATTACK{RESET}     — from 10.0.0.66")
    print(f"     {RED}• RECON_TO_EXPLOIT{RESET}   — from 185.220.1.1")
    print(f"     {RED}• PERSISTENCE_CHAIN{RESET}  — on linux-server-02")
    print(f"     {RED}• LATERAL_MOVEMENT{RESET}   — from 203.0.113.99")
    print(f"     {RED}• KILL_CHAIN{RESET}         — from 45.33.32.200")
    print(f"\n  Or wait 2 minutes for auto-correlation.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Correlation Engine test seed")
    parser.add_argument("--server", default=SERVER)
    args = parser.parse_args()
    main(args.server)
