# Student Project Topic Recommendation System — Project Plan

Final year NLP project, 2-person team. This file exists so either teammate (or their
AI assistant) can open the repo cold and know exactly what's built and what's next.
Read this before `README.md` (which only covers *how to run* things).

## The idea

A student describes their interests/skills in plain text. The system recommends
relevant final-year project topics from a curated topic bank, using NLP techniques
(sentence embeddings + cosine similarity, with topic clustering as a bonus) rather
than plain keyword search. Teachers get a separate dashboard to see registered
students.

## Why the stack looks like this

- **Backend**: FastAPI (Python) — needed anyway for the NLP/ML libraries (Stage 2),
  so the auth layer uses the same stack instead of introducing a second language.
- **DB**: Postgres, run as a container — chosen over SQLite specifically so we get a
  real DB browsable via **pgAdmin** (http://localhost:5050) instead of building a
  custom admin UI.
- **Frontend**: React + Vite — fast dev server, minimal boilerplate for a 2-person
  team on a deadline.
- **Everything runs in Docker** (`docker-compose.yml` at repo root) — no "works on my
  machine" issues when both teammates and the examiner run it.

## Stage 1 — Auth + Dashboards (DONE, this checkpoint)

- [x] Postgres + pgAdmin containers
- [x] FastAPI backend container, connects to Postgres via SQLAlchemy
- [x] `User` table: id, name, email, password_hash (bcrypt), role (`student`/`teacher`), created_at
- [x] `POST /auth/signup` — students self-register (role is always forced to `student`
      server-side, so nobody can sign up as a teacher)
- [x] `POST /auth/login` — shared login for both roles, returns a JWT + role
- [x] `GET /auth/me` — current user info from the JWT
- [x] `GET /dashboard/student` — placeholder student dashboard data
- [x] `GET /dashboard/teacher` + `GET /teacher/students` — teacher dashboard + student list
- [x] React app: `/login`, `/signup`, `/student`, `/teacher` (route-guarded by role)
- [x] Teacher account seeded via `backend/app/seed.py` (not self-signup — see README)

**Not done in Stage 1 on purpose:** no password reset, no email verification, no
refresh tokens (JWT just expires after 8h and the user logs in again). These are
polish items, not required for the exam checkpoint — add them only if time remains
after Stage 2/3.

## Stage 2 — NLP Recommendation Engine (NEXT — start here)

A curated dataset of 150 project topics across 15 domains already exists at
`backend/data/topics.json` (id, title, description, domain, tags, difficulty).
This is a hand-built seed dataset (no public "student project" dataset exists) —
say so explicitly in the report.

What's needed:

1. Add back to `backend/requirements.txt`:
   `sentence-transformers`, `scikit-learn`, `numpy` (removed from Stage 1 to keep
   the Docker image small/fast — Stage 1 doesn't need them).
2. `backend/app/nlp/`:
   - `preprocess.py` — basic text cleaning
   - `embeddings.py` — load `sentence-transformers/all-MiniLM-L6-v2` once, encode text
   - `recommend.py` — a `Recommender` class: loads `topics.json`, embeds the
     title+description of every topic once at startup, and for each query computes
     cosine similarity against all topics, returns the top-k
   - `clustering.py` (bonus) — KMeans over the topic embeddings to auto-discover
     domain groupings, independent of the hand-tagged `domain` field. Good "extra NLP
     technique" talking point for the report/viva.
3. `backend/app/routers/topics.py`:
   - `POST /recommend {interests, top_k, domain?}` → ranked topics + similarity score
   - `GET /topics`, `GET /domains`, `GET /clusters` (bonus)
   - Wire into `app/main.py` with `app.include_router(topics.router)`
4. Frontend: on `StudentDashboard.jsx`, replace the placeholder card with a search
   box (textarea for interests) + results list (title, domain, similarity %, tags).
   This is the actual demo-able core feature — prioritize it.
5. Write down (for the report): why Sentence-BERT over TF-IDF (semantic vs. lexical
   matching), and what the similarity score means to a grader.

## Stage 3 — Teacher Tools, Evaluation, Polish

- Teacher-side: ability to add/edit/remove topics (currently just a static JSON file)
- Some form of evaluation: even a small manual test set (10 student profiles →
  expected topic domain) with precision/recall, or a short user survey
- UI polish, error states, loading states
- Final report + slides + demo script
- Optional stretch: LLM-based "why this topic fits you" explanation on top of the
  retrieval core (only if time allows — the retrieval core is the real grade driver)

## Task split suggestion (2 people)

- **Person A**: Stage 2 NLP engine (embeddings, recommend, clustering) + report
  section on methodology
- **Person B**: Stage 2/3 frontend (search UI, results display, teacher topic
  management) + Stage 3 evaluation write-up

Swap or pair on whichever stage is running behind schedule — this split is a
starting point, not a hard boundary.

## Current file map

```
backend/
  app/
    core/        config.py (env vars), security.py (hashing + JWT)
    db/          database.py (SQLAlchemy engine), models.py (User table)
    schemas/     auth.py (pydantic request/response models)
    routers/     auth.py, dashboard.py   <- topics.py goes here in Stage 2
    nlp/         empty for now          <- Stage 2 lives here
    models/      schemas.py             <- pydantic Topic schemas, ready for Stage 2
    deps.py      get_current_user / require_role
    seed.py      creates the teacher account
    main.py
  data/topics.json   <- Stage 2 dataset, already built
frontend/
  src/
    pages/       Login.jsx, Signup.jsx, StudentDashboard.jsx, TeacherDashboard.jsx
    context/     AuthContext.jsx (JWT stored in localStorage)
    api.js       all backend calls go through here
docker-compose.yml   <- postgres, pgadmin, backend, frontend
```
