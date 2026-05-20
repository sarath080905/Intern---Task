import os
from uvicorn import run

from main import app

port = int(os.environ.get("PORT", "8000"))
run(app, host="0.0.0.0", port=port)
