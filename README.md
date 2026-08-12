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

## Setup on Windows

Everything below (all commands, all URLs) is identical on Windows — Docker Compose
behaves the same on every OS. The only Windows-specific steps are installing Docker
itself and getting the project folder onto the machine.

1. **Install Docker Desktop for Windows**: https://www.docker.com/products/docker-desktop/
   - During install, keep **"Use WSL 2 instead of Hyper-V"** checked (the default) —
     this is required.
   - If setup complains that WSL2 isn't installed, open PowerShell **as
     Administrator** and run `wsl --install`, reboot, then re-run the Docker installer.
   - If it complains about virtualization, enable "Virtualization Technology" /
     "Intel VT-x" / "AMD-V" in the laptop's BIOS (varies by manufacturer).
   - After install, **launch Docker Desktop** and wait for the whale icon in the
     system tray to say it's running before doing anything else.

2. **Get the project folder onto the Windows machine.** Since this isn't in a git
   repo yet, pick one:
   - Zip the `NLP-Project` folder and share it (USB / Drive / WhatsApp / etc.), then
     unzip it on Windows.
   - Or push it to a GitHub repo and have your friend `git clone` it — better if
     you'll both keep editing it. Ask if you want help setting that up.

3. **Open PowerShell in the project folder** (Shift + right-click the folder in File
   Explorer → "Open in Terminal" / "Open PowerShell window here"), then run the exact
   same commands as below (`docker compose up -d --build`, etc.).

**Windows-specific gotchas:**
- Port `5432` (Postgres) is sometimes already taken by a locally-installed Postgres
  on dev machines. If `docker compose up` fails with a port-in-use error, either
  stop the local Postgres service or change the left side of `"5432:5432"` in
  `docker-compose.yml` (e.g. `"5433:5432"` — only affects host access, containers
  still talk to each other on 5432 internally).
- Use **PowerShell**, not the old `cmd.exe` — smoother with Docker Desktop and quoting.
- `localhost` URLs (`:5173`, `:8000`, `:5050`) work the same in a Windows browser.

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
