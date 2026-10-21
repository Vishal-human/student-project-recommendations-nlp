# 🎓 TopicMatch — AI-Powered Student Project Recommendation System

> **Smart, Fair, and Scalable — Built for Universities.**

TopicMatch eliminates the chaos of final-year project allocation. Using transformer-based NLP, vector similarity search, and a rule-based feasibility engine, it gives every student a *personalized* list of project topics ranked by relevance to their interests, novelty against historical submissions, and technical feasibility for their skill-set and timeline.

Built as a full-stack, startup-grade platform — not just a college project.

---

## ✨ Key Features

### 🧠 NLP & AI Recommendation Engine
- **Hybrid Search (Dense + Sparse):** Combines `sentence-transformers/all-mpnet-base-v2` (768-dim dense embeddings) with TF-IDF/BM25 lexical matching, fused via Reciprocal Rank Fusion (RRF).
- **FAISS Vector Index:** Sub-millisecond cosine similarity retrieval over a curated corpus of 100+ past projects.
- **Duplicate Detection:** Flags near-duplicate proposals using cross-corpus cosine distance before any committee approval.
- **Novelty Scoring:** Each topic gets a mathematical novelty score — how unique is it compared to what past batches already built?
- **Feasibility Analysis:** Rule-based engine (`scoring/rules.yaml`) checks student's declared tech stack, team size, and time budget to compute a realistic feasibility score and highlight missing skills.

### 📋 Real-World Proposal Lifecycle
- Students submit a proposal for a recommended topic (or their own custom idea).
- **One active proposal per student** — enforced at the backend level.
- **Timestamp-based priority:** First student to submit a topic wins. Later duplicate submissions are flagged automatically.
- Teacher approves or rejects proposals with one click; approved topics are **automatically hidden from all other students' recommendation results**.
- Supervisor dashboard for institution-level oversight.

### 👥 Multi-Role Dashboards
| Role | Capabilities |
|---|---|
| **Student** | Get AI recommendations, submit proposals, track approval status |
| **Teacher** | View pending proposals, detect duplicates, approve/reject with timestamps |
| **Supervisor** | Institution-level overview of all proposals and activity |

### 🆘 First-Time User Guidance
- Interactive onboarding popup explains how the AI calculates scores.
- `?` help icon available at all times on the student dashboard.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                React Frontend (Vite)                 │
│   StudentDashboard  TeacherDashboard  SupervisorDash │
└────────────────────────┬─────────────────────────────┘
                         │ REST API (JWT Auth)
┌────────────────────────▼─────────────────────────────┐
│              FastAPI Backend (Python 3.11)            │
│  /auth   /topics   /proposals   /dashboard            │
└───┬──────────────┬─────────────────┬─────────────────┘
    │              │                 │
┌───▼───┐   ┌──────▼──────┐   ┌──────▼──────┐
│SQLite │   │ NLP Pipeline │   │  Scoring    │
│  / PG │   │ ml/index.py  │   │  Engine     │
│ RBAC  │   │FAISS + SBERT │   │ rules.yaml  │
└───────┘   └─────────────┘   └─────────────┘
```

---

## 🔧 Tech Stack

### NLP / ML
| Component | Technology |
|---|---|
| Embedding Model | `sentence-transformers/all-mpnet-base-v2` (Hugging Face) |
| Vector Index | FAISS `IndexFlatIP` (cosine similarity via L2 normalization) |
| Lexical Retrieval | TF-IDF / BM25 |
| Rank Fusion | Reciprocal Rank Fusion (RRF) |
| Duplicate Detection | Cosine distance on FAISS index |

### Backend
| Component | Technology |
|---|---|
| API Framework | FastAPI 0.111 + Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (dev) / PostgreSQL (prod via Docker) |
| Auth | JWT (`python-jose`) + bcrypt password hashing |
| Validation | Pydantic v2 |

### Frontend
| Component | Technology |
|---|---|
| Framework | React 18 + Vite |
| Icons | Lucide React |
| Routing | React Router v6 |

---

## 🚀 Quick Start

### Option A — Docker Compose (Recommended, zero local deps)

```bash
# 1. Clone the repo
git clone https://github.com/Vishal-human/student-project-recommendations-nlp.git
cd student-project-recommendations-nlp

# 2. Start all services
docker compose up -d --build

# 3. Seed teacher + supervisor accounts (one-time)
docker compose exec backend python -m app.seed
```

### Option B — Local Development

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## 🌐 Service URLs

| Service | URL | Notes |
|---|---|---|
| **Frontend** | http://localhost:5173 | React app |
| **Backend API** | http://localhost:8000 | FastAPI |
| **API Docs** | http://localhost:8000/docs | Auto-generated Swagger UI |
| **pgAdmin** | http://localhost:5050 | DB browser (Docker mode only) |

---

## 🔑 Demo Accounts

### Teacher
| Field | Value |
|---|---|
| Email | `teacher@college.edu` |
| Password | `teacher123` |

### Supervisor
| Field | Value |
|---|---|
| Email | `supervisor@college.edu` |
| Password | `supervisor123` |

### Student
Go to http://localhost:5173/signup — enter your name, email, interests, and tech stack. The NLP engine activates immediately.

---

## 🧪 How the Recommendation Works

1. **Student inputs:** Interests (free text), tech stack, team size, weeks available.
2. **Query embedding:** `all-mpnet-base-v2` encodes the interest text into a 768-dim vector.
3. **FAISS retrieval:** Top-20 cosine-similar topics fetched from the indexed corpus.
4. **Filtering:** Approved/taken topics are removed from the candidate pool.
5. **Re-ranking:** Each candidate is scored on:
   - `relevance` — cosine similarity to student query (weight: 0.6)
   - `novelty` — uniqueness vs. historical corpus (weight: 0.5)
   - `feasibility` — stack/timeline match (weight: 0.5)
6. **Top-5 recommendations** returned with explanations, suggested stack, and missing skill warnings.

---

## 📊 Performance

| Metric | Value |
|---|---|
| Top-5 Recall (benchmark corpus) | **>93%** |
| End-to-end query latency (CPU) | **<350 ms** |
| Corpus size | 100+ curated entries |

---

## 📁 Project Structure

```
student-project-recommendations-nlp/
├── backend/
│   ├── app/
│   │   ├── routers/         # auth, topics, proposals, dashboard, supervisor
│   │   ├── db/              # SQLAlchemy models & session
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── core/            # config, security
│   │   └── seed.py          # One-time DB seeder (teacher + supervisor accounts)
│   ├── ml/
│   │   └── index.py         # FAISS vector index + SBERT embeddings
│   ├── pipeline/
│   │   └── recommend.py     # Main recommendation pipeline (RRF fusion + scoring)
│   ├── scoring/
│   │   ├── feasibility.py   # Rule-based feasibility & skill-gap analysis
│   │   └── rules.yaml       # Domain-specific tech stack rules
│   ├── data/
│   │   ├── sample_corpus.json   # 100+ curated past project entries
│   │   ├── topics.json          # Extended topic dataset
│   │   └── schema.py            # ProjectEntry Pydantic model
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── pages/
│           ├── StudentDashboard.jsx    # AI recommendations + proposal submit
│           ├── TeacherDashboard.jsx    # Approve/reject + duplicate detection
│           ├── SupervisorDashboard.jsx # Institution-level oversight
│           ├── Login.jsx / Signup.jsx
│           └── ForgotPassword.jsx / ResetPassword.jsx
├── docker-compose.yml
├── COLLEGE_EXAM_SUBMISSION_REPORT.md   # Full academic report
├── PROJECT_PLAN.md                     # Original 3-stage roadmap
└── README.md
```

---

## 🗺️ Roadmap

- [ ] LLM-generated custom project briefs (Gemini / GPT integration)
- [ ] Institution-wide analytics dashboard for HODs
- [ ] CSV/Excel import for bulk student rosters
- [ ] Email notifications on proposal status change
- [ ] Multi-institution / SaaS multi-tenancy
- [ ] Mobile app (React Native)

---

## 📄 Documentation

| Document | Description |
|---|---|
| [`COLLEGE_EXAM_SUBMISSION_REPORT.md`](./COLLEGE_EXAM_SUBMISSION_REPORT.md) | Full academic report with NLP theory, methodology, and experiments |
| [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) | Original 3-stage engineering roadmap |
| [`UPGRADE_PLAN.md`](./UPGRADE_PLAN.md) | Planned enhancements and feature backlog |
| [`docs/`](./docs/) | Executive summary, market research, and technical specs |

---

## 🤝 Authors

- **Samarth Patel** — NLP Pipeline, Backend API, System Architecture
- **Vishal Suthar** — Frontend, Integration, Dataset Curation

*GLS University, Ahmedabad — Faculty of Computer Applications*

---

## 📜 License

MIT — free to use, adapt, and deploy in any university or EdTech platform.

---

> *"From hundreds of redundant project ideas to a fair, AI-curated shortlist in under 350ms."*
