# Render Deployment Guide

This guide shows how to deploy the backend of the Task Manager app on Render and connect it to a frontend host like Vercel.

---

## Why use Render?

Render is a simple cloud platform for hosting web apps. It can build and run the backend automatically from your GitHub repository.

This guide is written for a beginner and uses easy, step-by-step instructions.

---

## Prerequisites

Before you start, make sure you have:

- A Render account: https://render.com
- A GitHub repository with this project
- A frontend deployment URL (for example from Vercel)

> If you do not yet have a frontend deployed, you may use `http://localhost:5500` as a temporary value and update it later.

---

## Step 1 — Push the project to GitHub

If your project is not already in GitHub, follow these commands from the project root:

```powershell
cd "d:\Intern - Task\task-manager"
git init
git add .
git commit -m "Initial task manager deployment"
```

Create a repository on GitHub, then connect it:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/task-manager.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Deploy the backend on Render

There are two options for deployment:

### Option A — Use Render Blueprint (recommended)

1. Open https://dashboard.render.com
2. Click **New** → **Blueprint**
3. Connect your GitHub account
4. Choose the `task-manager` repository
5. Verify the generated settings and continue
6. When asked, enter the frontend URL:
   - Example: `https://your-app.vercel.app`
   - Or use `http://localhost:5500` temporarily
7. Click **Apply** and wait for the build

Render will use the `render.yaml` configuration in your repository.

### Option B — Create a Web Service manually

1. In Render, click **New** → **Web Service**
2. Connect your GitHub repo
3. Set these options:
   - **Name:** `task-manager-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

4. Add environment variables:
   - `SECRET_KEY` = a secure random string
   - `DATABASE_URL` = `sqlite:///./task_manager.db`
   - `FRONTEND_URL` = your frontend URL
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`

5. Click **Create Web Service**

---

## Step 3 — Check the deployed API

After deploy completes, test the API in your browser:

- `https://YOUR-SERVICE.onrender.com/health` should return `{ "status": "ok" }`
- `https://YOUR-SERVICE.onrender.com/docs` should open the FastAPI docs

If these pages work, the backend is deployed successfully.

---

## Step 4 — Connect the frontend

If your frontend is hosted on Vercel or another static host, point it to the Render API.

### On Vercel

In Vercel project settings, add:

- `API_BASE_URL` = `https://YOUR-SERVICE.onrender.com`

Then redeploy the frontend.

### On Render

In your Render web service settings, update:

- `FRONTEND_URL` = `https://your-app.vercel.app`

Save the environment variables and let Render redeploy.

---

## Step 5 — Test the full app

Once both backend and frontend are deployed:

1. Open your frontend site
2. Register a new user
3. Log in
4. Create a task
5. Refresh the page

If the task appears and the app works, deployment is complete.

---

## Notes for free tier users

| Topic | What to expect |
|------|----------------|
| Cold start | Free services sleep after inactivity. The first request may take longer. |
| SQLite storage | Data may be lost when the service restarts or redeploys. Good for demos, not production. |
| Production DB | For stable data, use PostgreSQL instead of SQLite. |

---

## Optional: Upgrade to PostgreSQL

If you want more reliable data storage:

1. Create a PostgreSQL database in Render
2. Copy the external database URL
3. Set `DATABASE_URL` in Render to that value
4. Redeploy the backend

The app already supports PostgreSQL-style URLs.

---

## Troubleshooting

| Issue | Fix |
|------|-----|
| Build fails | Make sure `Root Directory` is `backend` and Python version is supported. |
| 502 error | Check service logs and verify the start command uses `$PORT`. |
| CORS error | Ensure `FRONTEND_URL` exactly matches your frontend URL with `https://` and no trailing slash. |
| Login/register fails on live app | Confirm `API_BASE_URL` is set correctly in the frontend host. |
| Health endpoint fails | Use `/health` as the health check path. |

---

## Quick checklist

- [ ] Code is pushed to GitHub
- [ ] Render service is created
- [ ] `/health` endpoint returns OK
- [ ] Frontend URL is set in `FRONTEND_URL`
- [ ] `API_BASE_URL` points to Render API
- [ ] Frontend can register and create tasks

---

## Helpful links

- Render: https://render.com
- FastAPI docs: https://fastapi.tiangolo.com/
- Vercel: https://vercel.com
