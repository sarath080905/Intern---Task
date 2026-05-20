import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
backend = root / "task-manager" / "backend"
port = os.environ.get("PORT", "8000")

print(f"Starting backend from {backend} on port {port}")
subprocess.run([sys.executable, "start.py"], cwd=backend)
