# Deployment Guide (Step 10)

Deploy **backend** to Render or Railway, and **frontend** to Vercel.

## Prerequisites

- GitHub repo with this project pushed
- Free accounts: [Render](https://render.com), [Railway](https://railway.app), [Vercel](https://vercel.com)

---

## 1. Deploy backend (Render — recommended)

**Full guide:** [RENDER.md](RENDER.md)

1. Push `task-manager` to GitHub.
2. In Render → **New** → **Blueprint** (or **Web Service**).
3. Connect the repo.
4. Blueprint uses `render.yaml` at the **repo root** (`rootDir: backend`).
5. Set environment variables:

   | Variable | Example |
   |----------|---------|
   | `SECRET_KEY` | long random string (Render can auto-generate) |
   | `FRONTEND_URL` | `https://your-app.vercel.app` (add after frontend deploy) |
   | `DATABASE_URL` | `sqlite:///./task_manager.db` (demo) or PostgreSQL URL |

6. Deploy. Copy your API URL, e.g. `https://task-manager-api.onrender.com`.

**Health check:** `GET /health`  
**Docs:** `https://your-api.onrender.com/docs`

### PostgreSQL on Render (optional, production)

1. Create a **PostgreSQL** database on Render.
2. Copy the **Internal Database URL**.
3. Set `DATABASE_URL` on the web service (Render uses `postgres://` — the app normalizes it).
4. Add `psycopg2-binary` (already in `requirements.txt`).

> Free SQLite on Render uses ephemeral disk — data may reset on redeploy. Use PostgreSQL for real production.

---

## 2. Deploy backend (Railway — alternative)

1. **New Project** → **Deploy from GitHub repo**.
2. Set **Root Directory** to `backend`.
3. Railway uses `railway.toml` / `Procfile` start command.
4. Add variables: `SECRET_KEY`, `FRONTEND_URL`, `DATABASE_URL`.
5. Deploy and copy the public URL (`https://xxx.up.railway.app`).

---

## 3. Deploy frontend (Vercel)

1. Import the GitHub repo in Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework preset: **Vite** (or **Other** if Vercel does not detect it automatically).
4. Add environment variable:

   | Name | Value |
   |------|--------|
   | `API_BASE_URL` | `https://your-api.onrender.com` (no trailing slash) |

5. Deploy. Vercel will build the frontend from the `frontend` directory.

6. Copy your frontend URL, e.g. `https://task-manager.vercel.app`.

---

## 4. Connect frontend ↔ backend

1. In **Render/Railway**, set `FRONTEND_URL` to your Vercel URL (comma-separate multiple origins if needed):

   ```
   https://task-manager.vercel.app,https://task-manager-*.vercel.app
   ```

   For preview deploys, add each preview URL or use your production URL only.

2. Redeploy the backend so CORS picks up the new origin.

3. Open the Vercel site → Register → create tasks.

---

## 5. Update README live links

After deploy, edit root `README.md`:

```markdown
## Live link

- **Frontend:** https://your-app.vercel.app
- **API:** https://your-api.onrender.com
- **API docs:** https://your-api.onrender.com/docs
```

Add screenshots under `docs/screenshots/` and link them in README.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| CORS error in browser | Set `FRONTEND_URL` on backend to exact Vercel URL (https, no trailing slash) |
| API calls go to localhost | Set `API_BASE_URL` on Vercel and redeploy frontend |
| 401 on all requests | Check clock skew; verify token in DevTools → Application → localStorage |
| DB empty after redeploy | Expected with free SQLite on Render — use PostgreSQL |
| Build fails on Vercel | Ensure root directory is `frontend` and `API_BASE_URL` is configured correctly |

---

## Quick checklist

- [ ] Backend deployed, `/health` returns `{"status":"ok"}`
- [ ] `SECRET_KEY` set (not default)
- [ ] `API_BASE_URL` set on Vercel
- [ ] `FRONTEND_URL` set on backend
- [ ] Register + login + create task works on live site
- [ ] README updated with live URLs
