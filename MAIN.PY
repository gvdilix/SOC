"""Gadilix SOC Platform — Entry Point"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)