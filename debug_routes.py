"""Run this once to print all registered routes"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server.app import create_app

app = create_app()
print("\n=== ALL REGISTERED ROUTES ===")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
    print(f"  {str(rule):50s}  {','.join(rule.methods - {'HEAD','OPTIONS'})}")
print("=============================\n")
