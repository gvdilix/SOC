# GADILIX — Mini SOC Platform

```
 ██████╗  █████╗ ██████╗ ██╗██╗     ██╗██╗  ██╗
██╔════╝ ██╔══██╗██╔══██╗██║██║     ██║╚██╗██╔╝
██║  ███╗███████║██║  ██║██║██║     ██║ ╚███╔╝ 
██║   ██║██╔══██║██║  ██║██║██║     ██║ ██╔██╗ 
╚██████╔╝██║  ██║██████╔╝██║███████╗██║██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝╚═╝  ╚═╝
      Security Operations Center Platform
```

---

## Architecture

```
mini-soc-v3/ (gadilix/)
├── agent/
│   ├── linux_agent.py        # Tails /var/log/auth.log, ships logs via HTTP
│   └── windows_agent.py      # Reads Windows Event Log (or simulates)
│
├── server/
│   ├── app.py                # Flask application factory + scheduler
│   ├── config.py             # All config / env vars
│   ├── extensions.py         # Shared Flask extensions (DB, JWT, Bcrypt…)
│   │
│   ├── routes/
│   │   ├── auth.py           # Login / Register / Me
│   │   ├── logs.py           # Ingest + query logs
│   │   ├── alerts.py         # Alert CRUD + chart data
│   │   └── dashboard.py      # KPI summary + heatmap
│   │
│   ├── services/
│   │   ├── analyzer.py       # Rule-based + ML analysis pipeline
│   │   ├── ml_engine.py      # Isolation Forest anomaly detection
│   │   ├── alert_engine.py   # Alert creation + deduplication
│   │   └── notification.py   # Telegram + Email notifications
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── log_model.py
│   │   └── alert_model.py
│   │
│   └── security/
│       ├── jwt_handler.py    # Token generation / identity helpers
│       └── rbac.py           # Role decorators (admin_required, analyst_or_admin_required)
│
├── database/
│   └── soc.db                # SQLite (auto-created on first run)
│
├── dashboard/
│   ├── index.html            # Main dashboard
│   ├── login.html            # Auth page
│   ├── app.js                # Core logic, API calls, navigation
│   ├── charts.js             # Chart.js instances
│   ├── heatmap.js            # 7d×24h heatmap renderer
│   └── style.css             # Dark cyber-ops theme
│
├── docker/
│   └── Dockerfile
│
├── seed_test_logs.py         # Test log generator
└── requirements.txt
```

---

## Quick Start (Local)

### 1. Install dependencies
```bash
cd gadilix
pip install -r requirements.txt
```

### 2. Run the server
```bash
python -m server.app
# Server starts on http://localhost:5000
```

### 3. Open dashboard
```
http://localhost:5000/login
Username: admin
Password: gadilix2024
```

### 4. Seed test data
```bash
python seed_test_logs.py --server http://localhost:5000
```

### 5. Start an agent (Linux)
```bash
# Real mode (requires /var/log/auth.log access)
python agent/linux_agent.py --server http://localhost:5000 --agent-id my-server

# Point to a custom log file for testing
python agent/linux_agent.py --server http://localhost:5000 --log-file /tmp/test_auth.log
```

### 6. Start Windows agent (simulator mode)
```bash
python agent/windows_agent.py --server http://localhost:5000 --agent-id win-lab01
```

---

## Docker

```bash
# Build
docker build -f docker/Dockerfile -t gadilix .

# Run
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/database:/app/database \
  -e SECRET_KEY=your-secret \
  -e JWT_SECRET_KEY=your-jwt-secret \
  --name gadilix \
  gadilix

# View logs
docker logs -f gadilix
```

---

## Environment Variables

| Variable               | Default              | Description                     |
|------------------------|----------------------|---------------------------------|
| `SECRET_KEY`           | gadilix-super-secret | Flask secret key                |
| `JWT_SECRET_KEY`       | gadilix-jwt-secret   | JWT signing secret              |
| `DEBUG`                | false                | Enable Flask debug mode         |
| `DATABASE_URL`         | sqlite:///soc.db     | DB connection string            |
| `TELEGRAM_BOT_TOKEN`   | (empty)              | Telegram bot token              |
| `TELEGRAM_CHAT_ID`     | (empty)              | Telegram chat/group ID          |
| `SMTP_HOST`            | smtp.gmail.com       | SMTP server host                |
| `SMTP_PORT`            | 587                  | SMTP port                       |
| `SMTP_USER`            | (empty)              | SMTP username                   |
| `SMTP_PASS`            | (empty)              | SMTP password                   |
| `ALERT_EMAIL_TO`       | (empty)              | Alert recipient email           |
| `BRUTE_FORCE_THRESHOLD`| 5                    | Failed logins to trigger alert  |
| `BRUTE_FORCE_WINDOW`   | 60                   | Window in seconds               |
| `ML_CONTAMINATION`     | 0.1                  | Isolation Forest contamination  |
| `ML_RETRAIN_INTERVAL`  | 300                  | ML retrain interval (seconds)   |

---

## API Endpoints

### Auth
| Method | Endpoint            | Auth     | Description          |
|--------|---------------------|----------|----------------------|
| POST   | /api/auth/login     | None     | Get JWT token        |
| POST   | /api/auth/register  | Admin    | Create user          |
| GET    | /api/auth/me        | Any      | Current user info    |

### Logs
| Method | Endpoint            | Auth     | Description          |
|--------|---------------------|----------|----------------------|
| POST   | /api/logs/ingest    | None     | Agent log submission |
| GET    | /api/logs           | Analyst+ | List logs (paginated)|
| GET    | /api/logs/stats     | Analyst+ | Log statistics       |

### Alerts
| Method | Endpoint                    | Auth     | Description           |
|--------|-----------------------------|----------|-----------------------|
| GET    | /api/alerts                 | Analyst+ | List alerts           |
| GET    | /api/alerts/recent          | Analyst+ | Last N alerts         |
| GET    | /api/alerts/chart-data      | Analyst+ | Chart data            |
| PUT    | /api/alerts/<id>/resolve    | Admin    | Resolve alert         |

### Dashboard
| Method | Endpoint                    | Auth     | Description           |
|--------|-----------------------------|----------|-----------------------|
| GET    | /api/dashboard/summary      | Analyst+ | All KPIs + recent data|
| GET    | /api/dashboard/heatmap      | Analyst+ | 7d×24h matrix         |

---

## Security

- **Passwords**: bcrypt hashed (cost factor 12)
- **JWT**: HS256 tokens, 1h expiry
- **RBAC**:
  - `admin`: full access (create users, resolve alerts, read everything)
  - `analyst`: read-only (logs, alerts, dashboard)
- **CORS**: restricted to `/api/*` paths

---

## Detection Rules

| Rule              | Trigger                              | Severity |
|-------------------|--------------------------------------|----------|
| FAILED_LOGIN      | `Failed password` in log             | MEDIUM   |
| INVALID_USER      | `Invalid user` in log                | MEDIUM   |
| BRUTE_FORCE       | ≥5 failed logins from same IP / 60s  | HIGH     |
| ML_ANOMALY        | Isolation Forest score = -1          | MEDIUM   |

---

## ML Engine

The Isolation Forest model is:
- **Trained** every 5 minutes on the last 7 days of logs
- **Features**: hour, weekday, event_type encoding, failed/invalid flags, IP last-octet
- **Minimum samples**: 20 logs required before training
- **Contamination**: configurable (default 10%)
- **Inference**: synchronous on every ingested log

---

## Default Credentials

| Username | Password     | Role  |
|----------|--------------|-------|
| admin    | gadilix2024  | admin |

> ⚠️ Change the default password immediately in production!
#   G A D I L I X _ S O C _ P L A T E F O R M  
 