<div align="center">

<br/>

```
 ██████╗  █████╗ ██████╗ ██╗██╗     ██╗██╗  ██╗
██╔════╝ ██╔══██╗██╔══██╗██║██║     ██║╚██╗██╔╝
██║  ███╗███████║██║  ██║██║██║     ██║ ╚███╔╝
██║   ██║██╔══██║██║  ██║██║██║     ██║ ██╔██╗
╚██████╔╝██║  ██║██████╔╝██║███████╗██║██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝╚═╝  ╚═╝
```

# Gadilix SOC Platform

### Security Information and Event Management System

<br/>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK%20v14-FF0000?style=for-the-badge)](https://attack.mitre.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **Real-time threat detection · ML anomaly detection · Automated incident response · Remote machine control**

<br/>

---

</div>

## What is Gadilix?

**Gadilix** is a full-featured, open-source Security Operations Center (SOC) platform built from the ground up in Python and Flask. It centralizes log collection from Linux and Windows machines, analyzes every event through a multi-layer detection pipeline, correlates related alerts into multi-stage incidents, and lets your SOC team respond to threats — all from a single dark-themed web dashboard.

No agents required on the server side. No license fees. No black boxes.

<br/>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GADILIX DATA FLOW                                  │
├──────────────┬──────────────┬─────────────────────────┬─────────────────────┤
│   COLLECT    │  TRANSPORT   │         ANALYZE          │      RESPOND        │
│              │              │                          │                     │
│ linux_agent  │              │  ┌─ ECS Normalize      ─┤                     │
│ .py          │  HTTP POST   │  ├─ Rule Engine (38)   ─┤  Alert → Telegram   │
│              │  ──────────► │  ├─ Brute Force BF     ─┤  Alert → Email      │
│ windows_     │  JSON        │  ├─ ML Engine (×3)     ─┤  Incident Created   │
│ agent.py     │              │  ├─ AbuseIPDB Intel    ─┤  Auto Block IP      │
│              │              │  └─ Correlation (10)   ─┤  Auto Isolate Host  │
│              │              │                          │  SOAR (11 actions)  │
└──────────────┴──────────────┴─────────────────────────┴─────────────────────┘
```

<br/>

---

## Key Numbers

<div align="center">

| 38 Rules | 10 Correlations | 3 ML Algos | 11 SOAR Actions |
|:--------:|:---------------:|:----------:|:---------------:|
| Linux · Windows · Web · Network | Incident auto-creation | IF · Behavioral · Velocity | Full machine control |

</div>

<br/>

---

## Features

### 🔍 Layer 1 — Rule Engine

38 detection rules across 4 source categories, evaluated on every log with compiled regex. First match wins.

<details>
<summary><strong>Linux — 20 rules (click to expand)</strong></summary>

<br/>

| ID | Rule | Severity | Pattern |
|----|------|:--------:|---------|
| LNX-001 | Failed SSH Login | `MEDIUM` | `Failed password for <user> from <ip>` |
| LNX-002 | Invalid SSH User | `MEDIUM` | `Invalid user <user> from <ip>` |
| LNX-003 | Accepted SSH Login | `INFO` | `Accepted password/publickey for <user>` |
| LNX-004 | SSH Break-in Attempt | `HIGH` | `BREAK-IN ATTEMPT` in auth.log |
| LNX-005 | Sudo Command | `LOW` | `sudo: <user> : USER=root ; COMMAND=` |
| LNX-006 | Privilege Escalation | `HIGH` | `sudo: <user> USER=root COMMAND=/bin/bash` |
| LNX-007 | New User Created | `MEDIUM` | `useradd: new user name=<user>` |
| LNX-008 | User Added to Sudo | `HIGH` | `usermod: add '<user>' to group 'sudo'` |
| LNX-009 | Password Changed | `LOW` | `passwd: password changed for <user>` |
| LNX-010 | User Deleted | `MEDIUM` | `userdel: delete user '<user>'` |
| LNX-011 | Root Login | `HIGH` | `Accepted password for root from <ip>` |
| LNX-012 | /etc/passwd Modified | `HIGH` | `audit: type=PATH name=/etc/passwd` |
| LNX-013 | /etc/sudoers Modified | `HIGH` | `audit: type=PATH name=/etc/sudoers` |
| LNX-014 | Crontab Modified | `HIGH` | `crontab: (user) REPLACE (crontabs/user)` |
| LNX-015 | Suspicious Process | `HIGH` | `netcat / nmap / nc / python -c exec` |
| LNX-016 | Failed su Attempt | `MEDIUM` | `su: FAILED SU (to <user>)` |
| LNX-017 | SSH Key Added | `HIGH` | `key added to authorized_keys` |
| LNX-018 | Kernel Module Loaded | `HIGH` | `insmod / modprobe <module>.ko` |
| LNX-019 | Firewall Rule Changed | `MEDIUM` | `iptables -I / -A / -D` |
| LNX-020 | Account Spray | `MEDIUM` | Same username targeted by multiple IPs |

</details>

<details>
<summary><strong>Windows — 15 rules (click to expand)</strong></summary>

<br/>

| ID | Rule | Severity | Event ID |
|----|------|:--------:|----------|
| WIN-001 | Failed Logon | `MEDIUM` | 4625 |
| WIN-002 | Successful Logon | `INFO` | 4624 |
| WIN-003 | Account Lockout | `HIGH` | 4740 |
| WIN-004 | New User Created | `MEDIUM` | 4720 |
| WIN-005 | User Added to Admin | `HIGH` | 4732 / 4756 |
| WIN-006 | User Deleted | `HIGH` | 4726 |
| WIN-007 | New Service Installed | `HIGH` | 7045 |
| WIN-008 | Scheduled Task Created | `HIGH` | 4698 |
| WIN-009 | Audit Log Cleared | `CRITICAL` | 1102 |
| WIN-010 | Pass-the-Hash | `HIGH` | 4648 |
| WIN-011 | Special Privileges | `HIGH` | 4672 |
| WIN-012 | Suspicious Process | `HIGH` | 4688 |
| WIN-013 | PowerShell Encoded | `HIGH` | 4104 |
| WIN-014 | Registry Run Key | `HIGH` | 4657 |
| WIN-015 | RDP Login | `MEDIUM` | 4624 LogonType=10 |

</details>

<details>
<summary><strong>Web — 10 rules & Network — 7 rules (click to expand)</strong></summary>

<br/>

**Web**

| ID | Rule | Severity | Pattern |
|----|------|:--------:|---------|
| WEB-001 | SQL Injection | `HIGH` | `UNION SELECT / OR 1=1 / SLEEP()` |
| WEB-002 | XSS Attempt | `HIGH` | `<script> / onerror= / document.cookie` |
| WEB-003 | Path Traversal | `HIGH` | `../../../etc/passwd` |
| WEB-004 | Command Injection | `CRITICAL` | `;cat /etc/shadow / && id` |
| WEB-005 | Web Scanner | `HIGH` | User-Agent: sqlmap / nikto / nessus |
| WEB-006 | Admin Panel Access | `MEDIUM` | `/admin/ / /wp-admin/ / /phpmyadmin/` |
| WEB-007 | Excessive 404 | `MEDIUM` | High volume of 404 from same IP |
| WEB-008 | HTTP Flood | `HIGH` | Abnormal request volume |
| WEB-009 | File Inclusion LFI/RFI | `HIGH` | `php://filter / http://evil.com/shell.php` |
| WEB-010 | Suspicious User-Agent | `MEDIUM` | zgrab / masscan / Go-http-client |

**Network**

| ID | Rule | Severity | Condition |
|----|------|:--------:|-----------|
| NET-001 | Port Scan | `HIGH` | nmap / masscan / SYN scan |
| NET-002 | C2 Port Connection | `HIGH` | Ports 4444 / 1337 / 6667 / 31337 / 9001 |
| NET-003 | DNS Tunneling | `HIGH` | Abnormally long DNS queries |
| NET-004 | Data Exfiltration | `CRITICAL` | Outbound transfer > 100 MB |
| NET-005 | Tor Exit Node | `HIGH` | IP is a known Tor exit node |
| NET-006 | ICMP Flood | `MEDIUM` | High volume pings from one IP |
| NET-007 | Unusual Outbound | `MEDIUM` | Connection to non-standard port |

</details>

<br/>

### ⚡ Layer 2 — Brute-Force Engine

Stateful detection using in-memory sliding windows. Independent from the rule engine.

| Attack Type | Threshold | Window | Description |
|-------------|:---------:|:------:|-------------|
| SSH Brute Force | 5 fails | 60s | Same IP + same username |
| Credential Stuffing | 3 users | 60s | Same IP targeting multiple usernames |
| Password Spray | 10 IPs | 120s | Multiple IPs targeting same username |

<br/>

### 🤖 Layer 3 — ML Engine v2 (3 Algorithms)

```python
# Every log triggers a prediction
is_anomaly, reason, score = MLEngine.get_instance().predict(log)

# Example output
# is_anomaly : True
# reason     : "User behavior: unusual hour 3h (normal: 12h ±2h) | Velocity: 30 events/5min (15x normal)"
# score      : 0.87  →  severity upgraded to HIGH
```

**Isolation Forest**
- 150 decision trees, 14 extracted features
- Retrained every 5 minutes on the last 7 days of logs
- Detects: globally anomalous behavior (rare events in the population)

**Behavioral Profiling**
- Builds a unique baseline per `(username, agent)` and `(source_ip, agent)`
- Flags deviations > 2.5 standard deviations from entity's own history
- Requires 10+ events before activation
- Detects: events that are normal globally but abnormal for this specific entity

**Velocity Detector**
- Sliding 5-minute window per IP and per username
- Flags if current rate > 3× rolling historical average
- Detects: slow brute-force, progressive scans, stealthy exfiltration

<br/>

### 🔗 Correlation Engine — 10 Rules

Runs every 2 minutes. Groups related alerts into multi-stage incidents.

| Rule | Severity | Condition | Auto-Response |
|------|:--------:|-----------|:-------------:|
| `KILL_CHAIN` | `CRITICAL` | Recon + Exploit + PrivEsc + Persist, same IP | Block IP + Isolate |
| `LATERAL_MOVEMENT` | `CRITICAL` | Same IP attacks 3+ different machines | Block IP + Isolate |
| `DATA_EXFIL_CHAIN` | `CRITICAL` | Exploit/PrivEsc followed by large data transfer | Block IP + Isolate |
| `PERSISTENCE_CHAIN` | `CRITICAL` | PrivEsc + new user/crontab, same machine | Block IP |
| `BRUTE_THEN_SUCCESS` | `CRITICAL` | 3+ failed logins then success, same IP | Block IP |
| `ACCOUNT_TAKEOVER` | `CRITICAL` | Lockout then successful login, same username | Block IP |
| `DEFENSE_EVASION` | `CRITICAL` | Audit log cleared + persistence, same machine | Block IP |
| `RECON_TO_EXPLOIT` | `HIGH` | Scan followed by attack, same IP | Manual |
| `MULTI_VECTOR_ATTACK` | `HIGH` | Web + Network + Auth attacks simultaneously | Manual |
| `SAME_IP_ATTACK` | `HIGH` | 3+ alerts from same IP in 10 minutes | Manual |

CRITICAL incidents with auto-response display a **🔒 AUTO** badge in the Incidents page. Every auto-generated action is logged in the incident notes and the SOAR history.

<br/>

### 🛡️ SOAR — 11 Remote Actions

Commands are delivered to agents via HTTP polling every 30 seconds.

```
Dashboard  →  POST /api/soar/<action>
           →  SoarAction created (status: pending)
           →  Agent polls every 30s
           →  Agent executes locally
           →  Agent ACKs result
           →  Status: executed / failed
```

| # | Action | Role | What it does |
|---|--------|:----:|--------------|
| 1 | `block_ip` | Analyst+ | `iptables -A INPUT -s <ip> -j DROP` |
| 2 | `unblock_ip` | Analyst+ | Remove iptables block rule |
| 3 | `isolate_host` | Analyst+ | Block all traffic except SOC server |
| 4 | `shutdown` | Admin | `sudo shutdown -h now` |
| 5 | `restart` | Admin | `sudo shutdown -r now` |
| 6 | `sleep` | Admin | `systemctl suspend` |
| 7 | `lock_screen` | Analyst+ | `loginctl lock-sessions` |
| 8 | `kill_process` | Analyst+ | `kill -9 <PID>` or `pkill -9 <name>` |
| 9 | `get_processes` | Analyst+ | `ps aux` — returns live process list |
| 10 | `take_screenshot` | Analyst+ | `scrot` (auto-detects DISPLAY) |
| 11 | `run_command` | Admin | Arbitrary shell — fully audited |

<br/>

### 🌐 Threat Intelligence — AbuseIPDB

Every alert with a source IP is automatically enriched. No manual lookup needed.

| Field | Description |
|-------|-------------|
| `score` | Abuse confidence score 0–100 |
| `country` | IP origin country (ISO code) |
| `isp` | Internet service provider |
| `is_tor` | True if known Tor exit node |
| `tags` | VPN / Proxy / Data Center / Mass Reporter |
| `total_reports` | Community report count |

> If score ≥ 80 and alert is `MEDIUM` → automatically upgraded to `HIGH`

> Results cached 60 minutes in `threat_cache` table (free tier: 1000 checks/day)

<br/>

### 🏹 MITRE ATT&CK v14

Every alert includes automatic MITRE ATT&CK mapping. The dashboard includes an interactive matrix showing coverage and alert counts per technique.

| Tactic | Technique | Rules Covering |
|--------|-----------|---------------|
| Reconnaissance | T1595 Active Scanning | NET-001, WEB-005 |
| Initial Access | T1190 Exploit Public App | WEB-001, WEB-004 |
| Execution | T1059.001 PowerShell | WIN-013 |
| Persistence | T1053 Scheduled Task | LNX-014, WIN-008 |
| Privilege Escalation | T1548.003 Sudo | LNX-005, LNX-006 |
| Defense Evasion | T1070.001 Clear Logs | WIN-009 |
| Credential Access | T1110 Brute Force | LNX-001, BF Engine |
| Lateral Movement | T1021.001 RDP | WIN-015 |
| Command & Control | T1571 Non-Standard Port | NET-002 |
| Exfiltration | T1041 Over C2 Channel | NET-004 |

<br/>

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### 1 — Install

```bash
git clone https://github.com/yourname/gadilix.git
cd gadilix
pip install -r requirements.txt
```

### 2 — Configure

```bash
cp .env.example .env
# Edit .env — minimum: set SECRET_KEY and JWT_SECRET_KEY
```

### 3 — Run

```bash
python MAIN.PY
# Server starts at http://localhost:5000
# Default credentials: admin / gadilix2024
#
# ⚠️  Change the default password immediately after first login
```

### 4 — Start Agents

```bash
# Linux agent — monitors /var/log/auth.log
python agent/linux_agent.py \
  --server http://localhost:5000 \
  --agent-id my-linux-server

# Linux with custom log file
python agent/linux_agent.py \
  --server http://localhost:5000 \
  --log-file /var/log/syslog \
  --agent-id syslog-server

# Windows agent — reads Windows Security Event Log
python agent/windows_agent.py \
  --server http://localhost:5000 \
  --agent-id win-dc01
```

### 5 — Docker

```bash
# Build
docker build -f docker/Dockerfile -t gadilix .

# Run
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/database:/app/database \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-key \
  -e ABUSEIPDB_KEY=your-key \
  --name gadilix \
  gadilix

# Logs
docker logs -f gadilix
```

### 6 — Inject Test Data

```bash
# Full test — all 38 rules + brute-force + ML + correlation
python seed_full_test.py

# New v10 features — 9 attack scenarios
python seed_new_features_test.py

# Specific scenarios only
python seed_new_features_test.py --only brute_success
python seed_new_features_test.py --only exfil
python seed_new_features_test.py --only auto_response     # Full KILL_CHAIN → auto block + isolate
python seed_new_features_test.py --only ml_behavior       # Behavioral profiling anomaly
python seed_new_features_test.py --only defense_evasion

# Skip specific sections
python seed_new_features_test.py --skip ml_behavior ml_velocity

# After seeding:
# Dashboard → Incidents → Run Correlation Now
# Check for 🔒 AUTO badge on CRITICAL incidents
# Check SOAR page for auto-generated block/isolate actions
```

<br/>

---

## Configuration

All settings via `.env` — changes to notification settings take effect **immediately** without restart.

```env
# ── Security (required — CHANGE IN PRODUCTION) ──────────────────────────────
SECRET_KEY=change-this-to-a-long-random-string
JWT_SECRET_KEY=change-this-jwt-key-too

# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL=sqlite:///soc.db
# PostgreSQL: postgresql://user:password@localhost:5432/gadilix

# ── Threat Intelligence ───────────────────────────────────────────────────────
ABUSEIPDB_KEY=                # https://abuseipdb.com — free, 1000 checks/day

# ── Notifications ─────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN=           # Create bot via @BotFather on Telegram
TELEGRAM_CHAT_ID=             # Your Telegram chat or group ID
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=your-app-password   # Gmail: Settings → Security → App Passwords
ALERT_EMAIL_TO=soc@company.com

# ── Detection Thresholds ──────────────────────────────────────────────────────
BRUTE_FORCE_THRESHOLD=5       # Failed logins before brute-force alert
BRUTE_FORCE_WINDOW=60         # Window in seconds

# ── Machine Learning ──────────────────────────────────────────────────────────
ML_CONTAMINATION=0.1          # Expected anomaly rate (0.05 = 5%, 0.1 = 10%)
ML_RETRAIN_INTERVAL=300       # Retrain interval in seconds (default: 5 min)

# ── Scaling (optional) ────────────────────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0   # Enables async log queue
PORT=5000
DEBUG=false
```

<br/>

---

## Project Structure

```
gadilix/
│
├── MAIN.PY                          # Entry point
├── requirements.txt
├── .env.example
├── README.md
│
├── agent/
│   ├── linux_agent.py               # tail -f + SOAR polling thread
│   └── windows_agent.py             # Windows Event Log + SOAR thread
│
├── server/
│   ├── app.py                       # Flask application factory + APScheduler
│   ├── config.py                    # Environment-driven config
│   ├── extensions.py                # SQLAlchemy · JWT · bcrypt · CORS
│   │
│   ├── routes/                      # REST API — 10 Blueprints
│   │   ├── auth.py                  # Login · register · users
│   │   ├── logs.py                  # Ingestion + query
│   │   ├── alerts.py                # CRUD + investigation workflow
│   │   ├── incidents.py             # Correlated incidents
│   │   ├── dashboard.py             # KPIs · heatmap · MITRE matrix · ML stats
│   │   ├── soar.py                  # 11 SOAR actions + agent polling
│   │   ├── threat.py                # Threat intelligence
│   │   ├── reports.py               # PDF export
│   │   ├── agents.py                # Agent management
│   │   └── settings.py              # Live platform settings
│   │
│   ├── services/                    # Core business logic
│   │   ├── analyzer.py              # 3-layer analysis pipeline
│   │   ├── alert_engine.py          # Alert creation + deduplication (60s)
│   │   ├── correlation_engine.py    # 10 correlation rules + auto-response
│   │   ├── ml_engine.py             # Isolation Forest + Behavioral + Velocity
│   │   ├── threat_intel.py          # AbuseIPDB + 60-min cache
│   │   ├── ecs_normalizer.py        # Elastic Common Schema 8.11
│   │   ├── mitre_mapping.py         # MITRE ATT&CK v14 (38 techniques)
│   │   ├── log_queue.py             # Redis / in-memory async queue
│   │   ├── notification.py          # Telegram + Email (live settings)
│   │   ├── pdf_report.py            # PDF generation
│   │   └── rules/
│   │       ├── linux_rules.py       # LNX-001 → LNX-020
│   │       ├── windows_rules.py     # WIN-001 → WIN-015
│   │       ├── web_rules.py         # WEB-001 → WEB-010
│   │       ├── network_rules.py     # NET-001 → NET-007
│   │       └── brute_force_engine.py
│   │
│   ├── models/                      # SQLAlchemy ORM
│   │   ├── log_model.py             # logs table — 19 columns
│   │   ├── alert_model.py           # alerts table — 18 columns
│   │   ├── incident_model.py        # incidents + auto_blocked field
│   │   ├── user_model.py            # users — bcrypt passwords
│   │   ├── soar_model.py            # soar_actions — pending → executed
│   │   └── threat_model.py          # threat_cache — 60-min TTL
│   │
│   └── security/
│       ├── jwt_handler.py           # Token generation
│       └── rbac.py                  # @admin_required · @analyst_or_admin_required
│
├── dashboard/                       # Frontend SPA (zero framework)
│   ├── index.html                   # All 10 pages in one file
│   ├── login.html
│   ├── app.js                       # Navigation + API calls + ML stats
│   ├── alerts_page.js               # Alerts table + investigation modal
│   ├── soar.js                      # SOAR control + MITRE matrix
│   ├── incidents.js                 # Incidents + 🔒 AUTO badge
│   ├── investigation.js             # Alert detail modal
│   ├── charts.js                    # Chart.js instances
│   ├── heatmap.js                   # 7d × 24h canvas grid
│   ├── users.js                     # User management (admin)
│   ├── reports.js                   # PDF export
│   └── style.css                    # Dark cyber-ops theme
│
├── docker/
│   └── Dockerfile
│
└── seeds/
    ├── seed_full_test.py            # Complete test — all features
    ├── seed_new_features_test.py    # v10 new features (9 scenarios)
    ├── seed_correlation_test.py     # Original 5 correlation rules
    └── seed_threat_test.py          # AbuseIPDB enrichment test
```

<br/>

---

## API Reference

**Base URL:** `http://localhost:5000/api`
**Auth:** `Authorization: Bearer <token>`

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/auth/login` | — | Returns JWT access token |
| `POST` | `/auth/register` | Admin | Create a new user |
| `GET` | `/auth/me` | JWT | Current user profile |
| `GET` | `/auth/users` | Admin | List all users |
| `PUT` | `/auth/users/<id>` | Admin | Update role or active status |
| `DELETE` | `/auth/users/<id>` | Admin | Delete user |

### Logs

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/logs/ingest` | — | Agent submission — triggers full analysis |
| `GET` | `/logs` | Analyst+ | Paginated list (filter: severity, agent) |
| `GET` | `/logs/<id>` | Analyst+ | Single log detail |
| `GET` | `/logs/stats` | Analyst+ | Stats by event type and agent |

### Alerts

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/alerts` | Analyst+ | Paginated list (filter: status, severity) |
| `GET` | `/alerts/recent` | Analyst+ | Last N alerts |
| `GET` | `/alerts/chart-data` | Analyst+ | Data for Chart.js graphs |
| `GET` | `/alerts/<id>` | Analyst+ | Single alert with enrichment |
| `PUT` | `/alerts/<id>/investigate` | JWT | Update status + analyst notes |
| `PUT` | `/alerts/<id>/resolve` | JWT | Close alert |

### Incidents

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/incidents` | Analyst+ | Paginated list (filter: status, severity) |
| `GET` | `/incidents/<id>` | Analyst+ | Incident with all linked alerts |
| `PUT` | `/incidents/<id>` | JWT | Update status + notes |
| `POST` | `/incidents/run` | Analyst+ | Trigger correlation engine manually |
| `GET` | `/incidents/stats` | Analyst+ | Total / open / critical counts |

### SOAR

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/soar/block-ip` | Analyst+ | Block IP on agent |
| `POST` | `/soar/unblock-ip` | Analyst+ | Remove IP block |
| `POST` | `/soar/isolate-host` | Analyst+ | Isolate machine from network |
| `POST` | `/soar/shutdown` | Admin | Shut down agent machine |
| `POST` | `/soar/restart` | Admin | Restart agent machine |
| `POST` | `/soar/sleep` | Admin | Put machine to sleep |
| `POST` | `/soar/lock-screen` | Analyst+ | Lock screen |
| `POST` | `/soar/kill-process` | Analyst+ | Kill process by name or PID |
| `POST` | `/soar/get-processes` | Analyst+ | Get live process list |
| `POST` | `/soar/take-screenshot` | Analyst+ | Capture screen as PNG |
| `POST` | `/soar/run-command` | Admin | Execute shell command (audited) |
| `GET` | `/soar/pending/<agent_id>` | — | Agent polls for pending commands |
| `POST` | `/soar/ack/<action_id>` | — | Agent reports execution result |
| `GET` | `/soar/actions` | Analyst+ | Full SOAR action history |

### Dashboard & Analytics

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/dashboard/summary` | Analyst+ | KPIs: logs · alerts · anomalies · agents |
| `GET` | `/dashboard/heatmap` | Analyst+ | 7d × 24h alert frequency matrix |
| `GET` | `/dashboard/mitre-matrix` | Analyst+ | ATT&CK coverage with alert counts |
| `GET` | `/dashboard/ml-stats` | Analyst+ | ML engine stats (3 algorithms) |

<br/>

---

## Dashboard

10-page Single Page Application — JavaScript Vanilla, no framework.

| Page | Description |
|------|-------------|
| **Overview** | KPIs in real time · alerts/hour graph · attack types · severity breakdown · active agents. Auto-refresh every 8 seconds. |
| **Agents** | All connected machines · log count per agent · connection status |
| **Logs** | Paginated log table · filter by severity and agent |
| **Alerts** | Full alert management · investigation modal · MITRE ATT&CK · knowledge base · workflow |
| **Incidents** | 10 correlation rules · 🔒 AUTO badge · attack timeline · linked alerts |
| **SOAR** | 4 control panels (Network · Machine · Process · Shell) · MITRE matrix · action history |
| **Heatmap** | 7-day × 24-hour alert frequency canvas grid |
| **Settings** | 6 tabs: Notifications · Detection · ML Engine · Correlation · Auto-Response · Security |
| **Users** | Create · assign roles · deactivate users *(admin only)* |
| **Reports** | PDF export of alerts and incidents |

<br/>

---

## Security

### Authentication & Access Control

| Mechanism | Implementation |
|-----------|---------------|
| Password hashing | bcrypt — cost factor 12 |
| Tokens | JWT HS256 — 1 hour expiry |
| RBAC | 2 roles: `admin` and `analyst` |
| CORS | Restricted to `/api/*` paths only |

### Role Permissions

| Action | Analyst | Admin |
|--------|:-------:|:-----:|
| View logs · alerts · incidents · dashboard | ✅ | ✅ |
| Investigate alerts · add analyst notes | ✅ | ✅ |
| Block IP · isolate host · lock screen | ✅ | ✅ |
| Kill process · get processes · take screenshot | ✅ | ✅ |
| Trigger correlation manually | ✅ | ✅ |
| Shutdown · restart · sleep machine | ❌ | ✅ |
| Execute arbitrary shell command | ❌ | ✅ |
| Create · modify · delete users | ❌ | ✅ |
| Modify platform configuration | ❌ | ✅ |

<br/>

---

## SOAR — Agent Setup

### Sudoers (Linux — required for shutdown and restart)

```bash
# Replace 'yourusername' with the OS user running the agent (check with: whoami)

sudo tee /etc/sudoers.d/gadilix-agent << 'EOF'
yourusername ALL=(ALL) NOPASSWD: /sbin/shutdown
yourusername ALL=(ALL) NOPASSWD: /sbin/reboot
yourusername ALL=(ALL) NOPASSWD: /bin/systemctl
EOF

sudo chmod 440 /etc/sudoers.d/gadilix-agent
```

### Screenshots on Linux

```bash
sudo apt install scrot -y
```

### Screenshots on Windows

```bash
pip install Pillow
```

<br/>

---

## How Severity is Determined

Severity is set by 4 independent sources. It can only go **up** — never down.

```
Log ingested
    │
    ▼
[1] Rule assigns initial severity
    (e.g. FAILED_LOGIN → MEDIUM, AUDIT_LOG_CLEARED → CRITICAL)
    │
    ▼
[2] If a second rule matches with higher severity → upgrade
    │
    ▼
[3] ML Engine: score ≥ 0.8 → HIGH  |  score ≥ 0.5 → MEDIUM
    │
    ▼
[4] AbuseIPDB: IP score ≥ 80 and alert is MEDIUM → upgrade to HIGH
    │
    ▼
 Final severity stored in database
```

<br/>

---

## Scheduler — Background Jobs

Two jobs run automatically in the background via APScheduler:

| Job | Interval | What it does |
|-----|:--------:|--------------|
| `ml_retrain` | 5 minutes | Retrains Isolation Forest on last 7 days of logs |
| `correlate` | 2 minutes | Runs correlation engine — creates incidents from related alerts |

<br/>

---

## Default Credentials

```
Username : admin
Password : gadilix2024
```

> **Change this immediately after first login.**
> Settings → Security → Change My Password

<br/>

---

## Roadmap

- [ ] WebSocket real-time alert push (no polling)
- [ ] Geographic attack map (Leaflet.js + GeoIP)
- [ ] VirusTotal + Shodan threat intelligence
- [ ] Threat Hunting — ad-hoc query interface with DSL
- [ ] Dynamic per-agent risk score (0–100)
- [ ] PostgreSQL migration for production scale
- [ ] Swagger / OpenAPI interactive documentation
- [ ] Multi-tenancy support

<br/>

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Free to use, modify, and distribute.

<br/>

---

<div align="center">

**Gadilix SIEM v10**

*Built for the SOC community — Detect. Correlate. Respond.*

<br/>

If this project helped you, please consider giving it a ⭐

</div>
