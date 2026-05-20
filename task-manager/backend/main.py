# ==============================
# Main application entry point
# ==============================
# Imports for lifespan, environment, and web framework.
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database initialization and API routers.
from database import init_db
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router


# ==============================
# Configuration helpers
# ==============================
# Determine which frontend URLs are allowed to access the API.
def get_cors_origins():
    raw = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5500,http://127.0.0.1:5500"
    )

    return [
        origin.strip()
        for origin in raw.split(",")
        if origin.strip()
    ]


# ==============================
# App startup lifecycle
# ==============================
# Initialize database tables before the API starts.
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# ==============================
# FastAPI application setup
# ==============================
app = FastAPI(
    title="Task Manager API",
    description="JWT Authenticated Task Manager",
    version="1.0.0",
    lifespan=lifespan
)


# ==============================
# Middleware configuration
# ==============================
# Enable CORS for frontend access during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# API routers
# ==============================
app.include_router(auth_router)
app.include_router(tasks_router)


# ROOT ROUTE
@app.get("/")
def root():
    return {
        "message": "Task Manager API Running Successfully",
        "docs": "/docs"
    }


# HEALTH CHECK
@app.get("/health")
def health():
    return {
        "status": "ok"
    }