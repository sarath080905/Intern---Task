# Deploy backend on Render

## Prerequisites

- [Render](https://render.com) account (free tier works)
- Project on **GitHub** (Render deploys from Git)
- Your **Vercel frontend URL** (if already deployed) — or use a placeholder and update later

---

## Step 1 — Push code to GitHub

From the project folder:

```powershell
cd "d:\Intern - Task\task-manager"
git init
git add .
git commit -m "Task manager app"
```

Create a new repository on GitHub, then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/task-manager.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Create the web service on Render

### Option A — Blueprint (fastest)

1. [dashboard.render.com](https://dashboard.render.com) → **New** → **Blueprint**
2. Connect GitHub → select your `task-manager` repo
3. Render reads `render.yaml` at the repo root
4. When asked, set **`FRONTEND_URL`** manually, e.g.:
   ```
   https://your-app.vercel.app
   ```
   (Or `http://localhost:5500` until Vercel is live)
5. Click **Apply** → wait for deploy (~2–5 min)

### Option B — Web Service (manual)

1. **New** → **Web Service**
2. Connect the same GitHub repo
3. Settings:

   | Field | Value |
   |-------|--------|
   | **Name** | `task-manager-api` |
   | **Root Directory** | `backend` |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | **Health Check Path** | `/health` |

4. **Environment** → add:

   | Key | Value |
   |-----|--------|
   | `SECRET_KEY` | Click **Generate** or paste a long random string |
   | `DATABASE_URL` | `sqlite:///./task_manager.db` |
   | `FRONTEND_URL` | `https://your-app.vercel.app` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

5. **Create Web Service**

---

## Step 3 — Verify the API

When deploy status is **Live**, open:

| URL | Expected |
|-----|----------|
| `https://YOUR-SERVICE.onrender.com/health` | `{"status":"ok"}` |
| `https://YOUR-SERVICE.onrender.com/docs` | Swagger UI |

Example URL shape: `https://task-manager-api.onrender.com`

---

## Step 4 — Connect Vercel frontend

**Before you proceed:** You need the **URL** of your deployed Render service.
- Example: `https://task-manager-api.onrender.com`
- Find it on your Render service page under "Settings" → "URL"

In **Vercel** → Project → **Settings** → **Environment Variables**:

| Name | Value |
|------|--------|
| `API_BASE_URL` | `https://task-manager-api.onrender.com` (replace with your Render URL) |

**Save** and **Redeploy** the Vercel project (Deployments → Redeploy).

Wait for Vercel to finish deploying (~2 min).

Then, in **Render** → your service → **Environment**:

| Name | Value |
|------|--------|
| `FRONTEND_URL` | `https://your-app.vercel.app` (replace with your Vercel URL) |

**Save** → Render redeploys automatically.

---

## Step 5 — Test end-to-end

1. Open your Vercel site
2. **Register** a new account
3. **Create** a task
4. Refresh — task should still be there (until server redeploy on free SQLite; see below)

---

## Free tier notes

| Topic | Detail |
|-------|--------|
| **Cold start** | Free services sleep after ~15 min idle; first request may take 30–60s |
| **SQLite** | Data may reset when Render redeploys or restarts — OK for demos |
| **Production DB** | Add Render **PostgreSQL**, set `DATABASE_URL`, redeploy (app supports `postgres://` URLs) |

### Optional: PostgreSQL on Render

1. **New** → **PostgreSQL** → create database
2. Copy **External Database URL**
3. On the web service, set `DATABASE_URL` to that URL
4. Redeploy

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Root Directory must be `backend`; Python 3.11 |
| 502 on start | Check logs; ensure start command uses `$PORT` |
| CORS error from Vercel | `FRONTEND_URL` must match Vercel URL exactly (`https`, no trailing `/`) |
| Register works locally but not live | Set `API_BASE_URL` on Vercel to Render URL and redeploy |
| Health check fails | Path must be `/health` |

---

## Quick checklist

- [ ] GitHub repo pushed
- [ ] Render web service **Live**
- [ ] `/health` returns OK
- [ ] `SECRET_KEY` set (not empty)
- [ ] `FRONTEND_URL` = Vercel URL
- [ ] Vercel `API_BASE_URL` = Render URL
- [ ] Register + create task works on live site
