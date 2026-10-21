# 4-Week Execution Plan (COO persona)

**Ground truth constraint**: 2 people, ~1 month, 2–3 other active projects (Big Data capstone, RPA project, placement season). This plan assumes **realistic 8–10 focused hours/week per person**, not full-time. Every week is designed to leave a demoable artifact even if the next week gets compressed by other deadlines — that's the actual COO skill: sequencing so a partial month still ships something gradeable.

## Week 1 — Foundation + Data (highest priority, do not skip or delay)
**Owner split**: you (Samarth) own backend/ML given your FastAPI/embeddings prototype history; partner owns frontend + data collection coordination — swap tasks if your partner's strengths differ.

- Get the real GLS past-project-title dataset (ask coordinator/HOD/seniors; scrape your own department's project report archive/library if a digital list exists). Target 150+ entries minimum.
- Clean into the schema from `02-PRODUCT-AND-ML-ARCHITECTURE.md`.
- Stand up FastAPI skeleton + embed corpus into FAISS index (reuse your prior Sentence-BERT/FAISS/FastAPI prototype work — this is largely already validated by you, so this week should mostly be integration, not invention).
- **Checkpoint (end of week)**: `POST /recommend` returns nearest-neighbor titles for a hardcoded query, via curl/Postman. No UI needed yet.

## Week 2 — Scoring + Explainability
- Implement feasibility scoring table (stack/time/data-availability rules).
- Implement novelty score formula + top-3 nearest-neighbor surfacing.
- Implement template-based explanation generator.
- Basic frontend form (HTML/CSS/JS) wired to the API — ugly is fine, functional is required.
- **Checkpoint**: end-to-end demo — type interests+stack, get 5 scored topics with explanations, in a browser.

## Week 3 — Hardening + Docker + NLP-practical alignment
- Dockerize both services (Compose file), confirm it runs clean from a fresh clone (this is what your practical evaluator and any future pilot user will actually run).
- Add the multilingual-readiness schema field (don't build multilingual UI yet, just don't block it).
- Write the NLP practical report section: problem statement, dataset, embedding model choice + justification, evaluation approach (e.g., manually verify novelty scores against 10–15 known-duplicate and known-novel title pairs as a mini eval set — this doubles as your "evaluation metrics" section for grading).
- Buffer slack built in here deliberately — this is the week most likely to get squeezed by your other 2 projects; nothing new is introduced, only polish.

## Week 4 — Demo polish + University pitch prep
- Record/rehearse a 5-minute demo script (see pitch doc) for your NLP viva.
- Package the 1-page pitch for your HOD (see `05-STARTUP-PITCH-UNIVERSITY.md`).
- Deploy a public demo link (free tier) so it's shareable beyond the classroom.
- Stretch (only if ahead of schedule): supervisor-facing view — a simple `/admin` page listing flagged potential duplicates across submitted topics this semester, which is your strongest "this is a real tool the department could use" proof point.

## Explicit descoping rules if time runs out
1. Cut multilingual support entirely (already isolated to a schema field, safe to defer).
2. Cut the LLM-polish explanation step — raw template text is acceptable for grading.
3. Cut the admin/supervisor view — it's a stretch goal, not core to the NLP practical grade.
4. Never cut: real dataset, working novelty score, working feasibility score, Docker deploy, viva demo script. These are the graded/demoable core.
