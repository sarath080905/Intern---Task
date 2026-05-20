# Task Manager

A modern full-stack task manager application built with React, Vite, FastAPI, and SQLite.

This repository includes a secure backend API with JWT authentication and a React frontend for task creation, viewing, updating, and deletion.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Environment Variables](#environment-variables)
- [API Overview](#api-overview)
- [Frontend Setup](#frontend-setup)
- [Database Details](#database-details)
- [Docker Setup](#docker-setup)
- [Deployment](#deployment)
- [Testing](#testing)
- [Useful Commands](#useful-commands)

---

## Tech Stack

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **Database:** SQLite (local development) with optional PostgreSQL support
- **Auth:** JWT access tokens
- **HTTP client:** Axios

---

## Project Structure

```
task-manager/
├── backend/                 # FastAPI backend
│   ├── auth.py              # Authentication helpers
│   ├── crud.py              # Database operations
│   ├── database.py          # SQLAlchemy config and session
│   ├── main.py              # FastAPI application entrypoint
│   ├── models.py            # ORM models for users and tasks
│   ├── routes/              # API routes
│   ├── schemas.py           # Request and response models
│   ├── utils/               # Security helpers
│   └── tests/               # Pytest coverage
├── frontend/                # React frontend
│   ├── src/
│   │   ├── api/             # Axios API client
│   │   ├── components/      # UI components
│   │   ├── context/         # Auth state management
│   │   ├── pages/           # Login, register, dashboard
│   │   ├── routes.jsx       # App routes
│   │   ├── App.jsx
│   │   └── styles/main.css  # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml      # Local Docker stack
├── README.md
├── RENDER.md               # Render deployment guide
└── DEPLOYMENT.md           # Deployment notes
```

---

## Backend Setup

### 1. Enter backend folder

```bash
cd task-manager/backend
```

### 2. Create and activate virtual environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API base URL: `http://localhost:8000`
- Open API docs: `http://localhost:8000/docs`

---

## Environment Variables

Create a `.env` file in `backend/` or set these values in your environment.

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for JWT signing | `super-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `30` |
| `DATABASE_URL` | Database connection string | `sqlite:///./task_manager.db` |
| `FRONTEND_URL` | Allowed frontend origin for CORS | `http://localhost:5500` |

> The backend supports `postgres://` style URLs for PostgreSQL. SQLAlchemy converts this automatically.

---

## API Overview

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | No | Register a new user (`email`, `password`) |
| `POST` | `/login` | No | Login and receive JWT token (form data) |
| `GET` | `/me` | Yes | Get current authenticated user |

### Tasks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/tasks` | Yes | Create a new task |
| `GET` | `/tasks` | Yes | List tasks with optional filters |
| `GET` | `/tasks/{id}` | Yes | Get details for one task |
| `PUT` | `/tasks/{id}` | Yes | Update task fields |
| `DELETE` | `/tasks/{id}` | Yes | Delete a task |

### Task list query parameters

- `completed=true` — filter completed tasks
- `page=1` — pagination page number
- `limit=10` — number of tasks per page

### Example response for task listing

```json
{
  "items": [
    {
      "id": 1,
      "title": "Example task",
      "description": "Sample description",
      "completed": false,
      "owner_id": 1,
      "created_at": "2026-05-20T...",
      "updated_at": "2026-05-20T..."
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

### Authorization header

Use the JWT access token returned by `/login`:

```http
Authorization: Bearer <access_token>
```

---

## Frontend Setup

### 1. Install dependencies

```bash
cd task-manager/frontend
npm install
```

### 2. Start the frontend

```bash
npm run dev
```

This starts Vite and serves the app locally.

### 3. Open the app

Open the local Vite URL shown in the terminal, typically:

- `http://localhost:5173`

### Notes

- Auth state is stored in `localStorage`.
- API requests use `frontend/src/api/axios.js`.
- Protected routes are handled with `ProtectedRoute`.

---

## Database Details

### SQLite

By default the backend stores data in a local SQLite file:

- `backend/task_manager.db`

### Tables

- `users` — registered user accounts
- `tasks` — tasks owned by users with `owner_id`

### PostgreSQL support

The backend can also run with PostgreSQL by setting `DATABASE_URL` to a PostgreSQL connection string.

---

## Docker Setup

Use Docker Compose from the repository root to run the backend and frontend together.

```bash
docker compose up --build
```

### Local service URLs

- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5500`

### Stop services

```bash
docker compose down
```

---

## Deployment

Full deployment guidance is available in `DEPLOYMENT.md` and `RENDER.md`.

### Quick deployment summary

- Deploy backend from `backend/` using Render, Railway, or similar.
- Deploy frontend as a static site using Vercel or another host.
- Set `API_BASE_URL` for the frontend to point at the backend service.
- Set `FRONTEND_URL` on the backend for CORS.

---

## Testing

Run backend tests from the `backend/` folder:

```bash
pytest -v
```

The test suite covers:

- user registration
- login and authentication
- protected routes
- task CRUD operations
- access control between users

---

## Useful Commands

### Backend

```bash
cd task-manager/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pytest -v
```

### Frontend

```bash
cd task-manager/frontend
npm install
npm run dev
npm run build
npm run preview
```

### Docker

```bash
docker compose up --build
docker compose down
```

---

## Contact

If you want to improve or extend this project, good areas to explore include:

- adding PostgreSQL production support
- improving task UI/UX
- adding task categories or due dates
- implementing refresh token support for JWT
