from pathlib import Path
import sys

# Ensure the backend directory is on sys.path when Render runs from repo root.
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "task-manager" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402, F401
