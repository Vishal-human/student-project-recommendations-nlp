# Product & ML/NLP Architecture

## 1. Product shape (v1 scope)

**Input (from student):**
- Free-text: interests, prior skills, tech stack comfort (JS/Python/etc.), team size, time budget, department/domain constraints (from a course syllabus if given).
- Optional: paste a rough topic idea they already have.

**Output:**
- Top 5–10 recommended topics, each with:
  - **Novelty score** (0–100): semantic distance from existing corpus of past project titles/abstracts.
  - **Feasibility score** (0–100): fit against declared stack, time budget, team size — rule-based + embedding-assisted.
  - **Plain-language explanation**: "This is 91% novel vs. past GLS IMCA submissions; closest match is 'X' from 2023, which focused on Y instead of Z. Feasible in ~4 weeks for a 2-person JS/Python team."
  - Suggested minimal tech stack and a rough module breakdown.
- If the student pastes their own idea: same scoring, applied to that idea, plus 2–3 nearby "sharper" variants.

## 2. System architecture

```
┌─────────────────┐      ┌──────────────────────┐      ┌────────────────────┐
│  Frontend (JS/   │──────▶  FastAPI Backend      │──────▶  Vector Store       │
│  HTML/CSS)       │◀─────│  (Python)             │◀─────│  (FAISS, local)     │
└─────────────────┘      └──────────┬───────────┘      └────────────────────┘
                                     │
                     ┌───────────────┼────────────────┐
                     ▼               ▼                ▼
             Embedding model   Feasibility      Explanation
             (Sentence-BERT)   scoring engine   generator
                                (rule-based)     (template + LLM)
```

- **Frontend**: your existing JS/HTML/CSS. Keep it a single form + results page for v1 — no need for a heavy SPA framework given the timeline.
- **Backend**: FastAPI (matches your existing prototype and your team's Python comfort).
- **Vector store**: FAISS, in-process, no external DB needed for v1 (a few hundred to low-thousands of titles is trivially small for FAISS — don't over-engineer with a hosted vector DB yet).
- **Containerization**: Docker Compose with two services (frontend static/nginx + backend API) — matches your existing stack requirement and makes the "deploy for demo" step trivial.

## 3. ML/NLP model recommendation (from the ML + fine-tuning lead persona)

### Embedding model — do NOT train from scratch
Use a pretrained sentence-embedding model, not a custom-trained one. This is the correct engineering call given a 1-month timeline and no GPU cluster:

- **Primary recommendation**: `all-MiniLM-L6-v2` (Sentence-Transformers) — fast, small (~80MB), runs fine on CPU, good semantic quality for short texts like project titles/abstracts. This is very likely close to what you already prototyped.
- **If you want better quality and can afford slightly more latency**: `all-mpnet-base-v2` — stronger embeddings, still CPU-runnable, ~420MB.
- **Multilingual note**: if you want Hindi/Gujarati title support later (a genuine India-market differentiator), `paraphrase-multilingual-MiniLM-L12-v2` is the drop-in multilingual option — don't build this in v1, just don't paint yourself into an English-only corner in your schema (store raw text + detected language field).

### Why not fine-tune this month
Fine-tuning requires labeled pairs (title A, title B, similar/not-similar) at meaningful scale — you don't have that data yet. **The real fine-tuning opportunity is v2**, once you've collected real usage + supervisor feedback ("yes this was actually a duplicate" / "no it wasn't") — that becomes your labeled dataset. Document this as a deliberate phased plan, not a gap; that's exactly the kind of judgment an EdTech/ML team would show in a real pitch.

### Novelty scoring
1. Embed candidate topic + every corpus title/abstract with the chosen model.
2. Cosine similarity search via FAISS, top-k nearest neighbors.
3. Novelty score = `100 - (max_similarity * 100)`, clipped, with the top 2–3 nearest matches surfaced for transparency (this explainability is a key differentiator vs. black-box tools).
4. Optional second signal: keyword/TF-IDF overlap as a cheap sanity check that catches near-duplicate titles embeddings sometimes under-flag (e.g. "AI Resume Screener" vs "Resume Screening using AI").

### Feasibility scoring (mostly rule-based, deliberately simple and explainable)
- Stack-fit: does the topic's typical implementation require skills the student/team already listed? (simple keyword/ontology mapping: "chatbot" → NLP+backend; "computer vision" → needs OpenCV/CV comfort, flag if missing.)
- Time-fit: map topic complexity tier (seed a small manually-curated table: Beginner/Intermediate/Advanced) against declared time budget and team size.
- Data-availability-fit: flag topics that typically require hard-to-get datasets (medical imaging, proprietary data) as lower feasibility for a 1-month course project.
This layer should NOT be a neural model in v1 — keep it a transparent scoring table so you can explain every score in your viva without hand-waving.

### Explanation generation
Template-based natural language generation is enough for v1 (fill in nearest-neighbor title, similarity %, missing skills). If you want an LLM-polish pass, you can route the filled template through a free-tier LLM call for fluency — but the underlying numbers must come from your own pipeline, not be hallucinated by the LLM. This matters for grading integrity and for trust as a real product.

## 4. Data plan (your actual moat)

- **v1 corpus**: manually assembled 150–300 real past project titles + 1–2 line abstracts from GLS IMCA/BCA cohorts (ask your HOD/coordinator for past submission lists — this is a legitimate, low-effort ask and doubles as your first stakeholder conversation for the pitch).
- **Schema per entry**: `title, abstract_or_summary, year, department, tech_stack_tags, domain_tags`.
- **Growth path**: every semester this runs, the corpus grows and the tool gets structurally better than any generic competitor — this is the point to hammer in your pitch deck.

## 5. Tech stack confirmation (matches what you already have)

- Frontend: HTML/CSS/JS (static, framework-optional)
- Backend: Python + FastAPI
- ML: sentence-transformers + FAISS (CPU, free)
- Infra: Docker Compose, deploy on a free tier (Render/Railway free tier or similar — same "fully free-tier" discipline as your InboxIntel project)
- No paid APIs required for the core pipeline; reserve an optional LLM call (free-tier Gemini, matching your other projects) only for the explanation-polish step.
