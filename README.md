# Student Project Topic Recommendation System

Final year NLP project. Stage 1 (this checkpoint): student signup/login, teacher
login, and role-based dashboards, fully containerized. See `PROJECT_PLAN.md` for
the full 3-stage roadmap and what to build next.

## Stack

- **Backend**: FastAPI (Python) + SQLAlchemy, JWT auth
- **Database**: PostgreSQL (official image) + pgAdmin (official web UI for the DB)
- **Frontend**: React + Vite
- **Everything runs via Docker Compose** — no local Python/Node install needed

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

That's it — you do not need Python, Node, or Postgres installed locally.

## Running the project

From the repo root:

```bash
docker compose up -d --build
```

First run takes a few minutes (pulling Postgres/pgAdmin images, installing
dependencies). Subsequent runs are fast.

Once it's up, create the teacher account (one-time, until the DB volume is reset):

```bash
docker compose exec backend python -m app.seed
```

### URLs

| Service | URL | Notes |
|---|---|---|
| Frontend | http://localhost:5173 | React app |
| Backend API | http://localhost:8000 | FastAPI |
| API docs | http://localhost:8000/docs | Auto-generated Swagger UI |
| pgAdmin | http://localhost:5050 | DB browser UI — see below to connect |

### Logging in

- **Student**: go to http://localhost:5173/signup, create an account, you're
  redirected to the student dashboard.
- **Teacher**: go to http://localhost:5173/login and use:
  - Email: `teacher@college.edu`
  - Password: `teacher123`

  (These come from `TEACHER_EMAIL` / `TEACHER_PASSWORD` in `docker-compose.yml` —
  change them there if you want different credentials, then re-run the seed command.)

### Browsing the database in pgAdmin

1. Open http://localhost:5050, log in with `admin@admin.com` / `admin`.
2. Add a new server (right-click "Servers" → Register → Server):
   - **General tab** → Name: anything, e.g. `NLP Project`
   - **Connection tab**:
     - Host: `postgres` (the container name, not `localhost`)
     - Port: `5432`
     - Username: `nlp_user`
     - Password: `nlp_password`
3. Expand Servers → NLP Project → Databases → `nlp_project` → Schemas → public →
   Tables → `users` to see registered accounts.

## Common commands

```bash
# View logs for one service
docker compose logs -f backend
docker compose logs -f frontend

# Stop everything
docker compose down

# Stop everything AND wipe the database
docker compose down -v

# Rebuild after changing requirements.txt or package.json
docker compose up -d --build
```

## Project structure

```
backend/    FastAPI app (see PROJECT_PLAN.md for the file map)
frontend/   React app
docker-compose.yml
PROJECT_PLAN.md   <- 3-stage roadmap, read this next
```
