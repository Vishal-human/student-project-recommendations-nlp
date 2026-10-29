# TopicMatch — Exam Study Notes (quick read)

## 1. What is the project? (say this first)
**TopicMatch** is a web app that helps final-year students pick a project topic.
Problem: many students pick the same/similar topics, and teachers check duplicates by hand.
Solution: the student types their **interests, tech skills, team size, weeks available** →
the system uses **NLP** to find the most **relevant, unique and doable** topics → student submits a
proposal → teacher approves/rejects → approved topics disappear from other students' suggestions.

**Three roles**
| Role | What they do |
|---|---|
| Student | Sign up, get AI recommendations, submit proposal, see status |
| Teacher | See pending proposals, run duplicate detector, approve/reject |
| Supervisor | Oversight of all proposals, duplicate check |

## 2. Tech stack (one line each)
- **Frontend:** React + Vite (pages: Login, Signup, Student/Teacher/Supervisor dashboards)
- **Backend:** FastAPI (Python) — REST API
- **Database:** SQLite (dev) / PostgreSQL (Docker); SQLAlchemy ORM; 2 tables: `users`, `project_proposals`
- **Security:** bcrypt password hashing + JWT token login + role check (`require_role("teacher")`)
- **NLP/ML:** SentenceTransformers (`all-mpnet-base-v2`) + FAISS vector search
- **Rules:** `rules.yaml` for feasibility scoring
- **Docker Compose** to run everything

## 3. How it works (flow)
```
Student form → React → POST /topics/recommend (JWT) → FastAPI
   → NLP pipeline (embed → FAISS search → score → rank)
   → remove topics already approved → top 5 shown
Student picks one → POST /proposals/submit (status = pending)
Teacher → approve / reject → status saved in DB
Approved title → treated as "taken" → hidden from others
```
Data: a corpus of **120 past project entries** (`sample_corpus.json`: title, abstract, tags, year, department).

## 3B. What is NLP, how it works, and what we used (read this first for theory)

### What is NLP?
**Natural Language Processing** = the branch of AI that lets computers **read, understand and compare human language** (English text). Computers only understand numbers, so NLP's main job is: **text → numbers → do maths on the numbers**.

### How NLP works (simple 4 steps)
1. **Text input** — e.g. "I like chatbots and Python".
2. **Pre-processing / tokenisation** — split text into words/pieces (tokens). The model does this itself.
3. **Representation (embedding)** — a model converts the text into a **vector** (a list of numbers). Similar meaning → vectors that point in a similar direction.
4. **Task** — compare vectors (similarity), classify, search, etc. *Our task: similarity search + ranking.*

Evolution (good to mention): Bag-of-words / TF-IDF (counts words, ignores meaning) → Word2Vec (word meaning) → **Transformers / BERT family** (understand whole sentence and context). We used the last one.

### What we used — the 3 tools, what each is, and WHY
| What | What it is | Where in code | Why we used it |
|---|---|---|---|
| **SentenceTransformers + `all-mpnet-base-v2`** | A pre-trained transformer model (Hugging Face). Input: a sentence. Output: 768-number vector. Based on **MPNet** (improved BERT), fine-tuned so that similar sentences have similar vectors. ~420 MB, runs on CPU. | `ml/index.py` (`_MODEL`, `_embed`) | Understands **meaning**, not just keywords, so "student attendance system" matches "face-recognition class register". Pre-trained, so **no training data or GPU needed**. More accurate than the smaller MiniLM model (the code comments say this). |
| **Cosine similarity** | Maths measure of the angle between two vectors. 1 = same meaning, 0 = unrelated. | Used everywhere in `recommend.py`, `supervisor.py`, `topics.py` | Standard, simple, ignores text length. Gives a number we can use for relevance, novelty and duplicate thresholds. |
| **FAISS (`IndexFlatIP`)** | Facebook AI Similarity Search — a library that stores vectors and finds the nearest ones quickly. | `ml/index.py` (`build_index`, `query`) | Fast nearest-neighbour search. `IndexFlatIP` = inner product; because we **L2-normalise** vectors, inner product = cosine similarity. Exact search is fine for 120 entries. |
| **Rule engine (YAML)** | Not NLP/ML — plain if-then rules for skills, timeline, team size. | `scoring/feasibility.py`, `rules.yaml` | Feasibility is a logic question, not a language question. Rules are **explainable** ("−15: missing skill python") and editable without changing code. |

### Where each concept is used in the project
| Concept | Used for |
|---|---|
| Embedding (SBERT) | Converting student interests, corpus topics, and proposal titles to vectors |
| Cosine similarity + FAISS | 1) Find topics matching interests · 2) Novelty score · 3) Duplicate detection · 4) Hide taken topics |
| Rule-based scoring | Feasibility score and missing-skill list |

### Why this design (answer if faculty ask "why not X?")
- **Why not keyword search / TF-IDF?** It can't match different words with the same meaning (synonyms/paraphrases). Embeddings can.
- **Why not train our own model?** We don't have a large labelled dataset; pre-trained models already know English (**transfer learning**).
- **Why not ChatGPT/LLM?** Slower, costs money, not repeatable, and we only need similarity, not text generation. (LLM briefs are listed as future work.)
- **Why FAISS instead of a loop?** Built for vector search and scales to thousands/millions of entries.
- **Why normalise vectors?** So a simple dot product gives cosine similarity.
- **Why a hybrid of ML + rules?** ML for meaning (relevance, novelty, duplicates), rules for things that need to be transparent (feasibility).

### One-paragraph answer to memorise
> "We use NLP to understand the meaning of project topics. The student's interest text and our 120-topic corpus are converted into 768-dimensional vectors using the pre-trained `all-mpnet-base-v2` sentence-transformer. We store the vectors in a FAISS index and use cosine similarity to find the closest topics. The same similarity gives us a novelty score and detects duplicate proposals. A separate rule-based engine scores feasibility. We chose pre-trained embeddings because they capture meaning without needing training data."

## 4. WHERE and HOW NLP is used (most important)
### a) Text → numbers (Embeddings) — `backend/ml/index.py`
- Model **all-mpnet-base-v2** (a transformer, Hugging Face) converts a sentence into a **768-number vector**.
- Sentences with similar *meaning* get similar vectors. "chatbot for students" ≈ "AI assistant for college" even with different words. This is **semantic similarity** (better than keyword matching).
- Each corpus entry = `title + abstract` → embedded once at startup.

### b) Cosine similarity + FAISS
- Vectors are **L2-normalised**, so inner product = **cosine similarity** (0 to 1).
- **FAISS** (`IndexFlatIP`) is Facebook's library for fast nearest-neighbour vector search.
- Student's interest text → vector → FAISS returns the closest topics.

### c) Relevance, Novelty, Feasibility — `backend/pipeline/recommend.py`
| Score | Meaning | How |
|---|---|---|
| Relevance | Matches my interests | Cosine sim of my text vs topic |
| Novelty | Is it unique? | `(1 − similarity to nearest *other* past project) × 100` |
| Feasibility | Can I build it? | Rule-based (see d) |

Final rank = `0.6 × relevance + 0.4 × (0.5 × novelty + 0.5 × feasibility)`
Retrieve top 20 by similarity → re-rank → show top 5 with an explanation text.

### d) Feasibility (rule-based, not ML) — `scoring/feasibility.py` + `rules.yaml`
Start at 100, deduct points: **−15** per missing skill, **−15/−30** for tight timeline, **−10** small team. Every deduction has a stated reason (explainable).

### e) Duplicate detection — `routers/supervisor.py`
All proposal titles are embedded; pairs with cosine similarity **> 0.75** are flagged as likely duplicates (catches paraphrased titles).

### f) "Taken topic" filter — `routers/topics.py`
Approved titles are embedded; any recommendation with similarity **≥ 0.82** to an approved title is removed.

**Short answer if asked "where is NLP?"** → *Sentence embeddings (transformer) + cosine-similarity semantic search with FAISS, used in 3 places: recommendation, duplicate detection, and taken-topic filtering.*

## 5. Who did what
Based on git history (verify with your friend; README author list differs slightly).

### 🟦 What YOU (Vishal) did — "Stage 1" commit
- Project setup: Docker, docker-compose, `.env`, Dockerfiles, `.gitignore`
- **Authentication:** signup, login, forgot/reset password (`auth.py`), password hashing (bcrypt), JWT tokens (`security.py`)
- **Roles & access control:** student / teacher / supervisor, `require_role` (`deps.py`); signup always creates a student, teachers are created by `seed.py`
- **Database setup:** SQLAlchemy `User` model, `database.py`
- **Frontend base:** React app, routing, `ProtectedRoute`, `AuthContext`, Login/Signup/Forgot/Reset pages, Navbar
- `topics.json` (150 topics dataset), `PROJECT_PLAN.md`

### 🟧 What your friend (Samarth) did — "Stage 2"
- **The whole NLP pipeline:** embeddings + FAISS (`ml/index.py`), recommend pipeline, feasibility engine + `rules.yaml`
- Corpus `sample_corpus.json` (120 entries), loader/schema/tags
- **Proposal system:** submit / approve / reject, one-proposal-per-student rule, timestamp priority
- **Supervisor duplicate check** API
- Student, Teacher, Supervisor dashboards (frontend)
- Docs: report, README rewrite, `docs/`

### How to say it
> "I built the foundation — authentication, role-based access, database, Docker and the React app structure. My teammate built the NLP recommendation engine and proposal workflow on top. I understand the full flow and the NLP concepts."

⚠️ README says you did "Frontend, Integration, Dataset Curation" and Samarth did "NLP, Backend, Architecture". Git shows the dashboards were Samarth's. Be honest about it; stick to what you did, and *understand* the rest.

## 6. Likely faculty questions — quick answers
- **What is NLP?** Making computers understand human language.
- **What is an embedding?** A vector (list of numbers) representing a text's meaning.
- **Why embeddings, not keyword search?** They capture meaning/synonyms, so paraphrases still match.
- **What is cosine similarity?** Angle-based similarity between two vectors; 1 = same meaning, 0 = unrelated.
- **What is a transformer / SBERT?** A neural network using attention; Sentence-BERT gives a good sentence-level vector. MPNet is a stronger variant.
- **What is FAISS?** A library for fast similarity search over vectors.
- **Why normalise vectors?** So inner product equals cosine similarity.
- **Is feasibility ML?** No — rule-based, so it's transparent and editable in YAML.
- **What is JWT?** A signed token the server gives after login; sent with each request to prove identity/role.
- **Why bcrypt?** Passwords are stored hashed + salted, never plain text.
- **How do you stop a student becoming teacher?** Signup always sets role = student; teachers come from the seed script; endpoints check role.
- **How are duplicates handled?** Embedding similarity > 0.75 flagged; first-submitted (timestamp) has priority.
- **Limitations?** Small corpus (120), fixed thresholds (0.75/0.82), feasibility is rule-based, complexity tier hard-coded to "intermediate".
- **Future work:** LLM-generated briefs, email notifications, analytics, bigger dataset.

## 7. Things to know (be careful in the exam)
The README is more ambitious than the code. In the actual code:
- **BM25 / TF-IDF / RRF hybrid search is NOT implemented** — only dense embeddings + FAISS. Don't claim hybrid search.
- The ">93% recall" and "<350 ms" numbers aren't backed by an evaluation script in the repo (`eval/` is empty).
- `requirements.txt` doesn't list `sentence-transformers`/`faiss-cpu`/`numpy`/`pyyaml` — install them if you run it locally.
- The README says the topic index has "100+" entries; it's exactly 120.
- Novelty is measured against *past projects only*, not the other students' current proposals (that's the duplicate checker's job).

## 8. Run it (for demo)
`docker compose up -d --build` → `docker compose exec backend python -m app.seed`
Frontend http://localhost:5173 · API docs http://localhost:8000/docs
Teacher login: `teacher@college.edu` / `teacher123` · Student: sign up on `/signup`.
