"""
install_correlation.py
Run this once from the project root:
    python install_correlation.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

files = {
    # ── Backend ────────────────────────────────────────────────────────────
    os.path.join(ROOT, "server", "models", "incident_model.py"): open(
        os.path.join(ROOT, "server", "models", "incident_model.py")).read()
    if os.path.exists(os.path.join(ROOT, "server", "models", "incident_model.py")) else "",
}

print("Checking files...")
needed = [
    ("server/models/incident_model.py",       "/mnt/user-data/outputs/incident_model.py"),
    ("server/routes/incidents.py",             "/mnt/user-data/outputs/incidents_route.py"),
    ("server/services/correlation_engine.py",  "/mnt/user-data/outputs/correlation_engine.py"),
    ("server/app.py",                          "/mnt/user-data/outputs/app.py"),
    ("dashboard/incidents.js",                 "/mnt/user-data/outputs/incidents.js"),
    ("dashboard/index.html",                   "/mnt/user-data/outputs/index.html"),
    ("dashboard/app.js",                       "/mnt/user-data/outputs/app.js"),
]
for dest, src in needed:
    print(f"  {dest}")
