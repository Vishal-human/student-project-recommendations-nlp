# TopicMatch (working name) — Master Plan
### Student Project Topic Recommendation System → Campus Startup
Prepared for: Samarth & partner (Sem 9 NLP Practical, GLS University)
Prepared by: Virtual Tech Team (CTO / COO / EdTech Strategist / ML+Fine-tuning Leads)
Timeline: 4 weeks (parallel with 2–3 other active projects)

---

## 1. What this document set is

This is a professional-grade planning pack, split into files so each can be fed to an AI coding agent (Antigravity IDE) as a standalone spec, the same way a real startup's tech team would hand a PRD + architecture doc + sprint plan to engineering.

| File | Purpose |
|---|---|
| `00-EXECUTIVE-SUMMARY.md` | This file — scope, roles, non-negotiables |
| `01-MARKET-RESEARCH-AND-GAP.md` | What exists today, what's actually missing, why this can be a real product |
| `02-PRODUCT-AND-ML-ARCHITECTURE.md` | Full system design + ML/NLP model recommendation (builds on your Sentence-BERT/FAISS/FastAPI prototype) |
| `03-4WEEK-EXECUTION-SPRINT-PLAN.md` | Day-by-day plan sized for 1 month + parallel course load, 2 people |
| `04-AI-AGENT-BUILD-SPECS.md` | Copy-paste-ready prompts/specs for building each module with an AI agent (Antigravity-style) |
| `05-STARTUP-PITCH-UNIVERSITY.md` | How to pitch this to GLS University first, then beyond |

## 2. The core insight (read this first)

A "topic recommender" alone is a **student project**. What makes it a **startup** is solving the problem universities and students actually have, which isn't "suggest me an idea" — it's:

> *"Is my idea original, is it actually buildable by me in the time I have, and will it matter to an evaluator/recruiter/industry — or am I about to spend 3 months on a rehashed Netflix-clone-tier topic that 40 other students in India are also submitting this semester?"*

Your MVP (Sentence-BERT + FAISS + FastAPI matching) is the right technical seed. The startup wrapper adds **novelty scoring, feasibility scoring against the student's actual skill stack, and a supervisor-facing duplicate-prevention layer** — none of which the generic "50 AI project ideas" blogs or paid "project vendor" shops (who sell the *same* ready-made projects to hundreds of students — see market research) provide.

## 3. Roles (how to use AI agents to fill these)

Treat each of these as a persona/system-prompt you load into your AI coding agent for the relevant module. Details and exact prompts are in `04-AI-AGENT-BUILD-SPECS.md`.

- **CTO persona** — architecture, API contracts, model choice, infra cost control (free-tier discipline, matching your InboxIntel pattern).
- **COO persona** — scope cuts, timeline realism against your other 2–3 projects, what NOT to build this month.
- **EdTech Strategist persona** — what supervisors/HODs actually score projects on, how universities currently allocate/approve topics, where the real pain is.
- **ML/Fine-tuning Lead persona** — embedding model selection, novelty scoring math, later fine-tuning plan once you have real usage data.
- **Growth/Pitch persona** — positioning for the university pitch, then a public launch.

## 4. Non-negotiables for the NLP practical submission

- Must **actually use NLP** substantively (embeddings, semantic similarity, topic modeling/keyword extraction) — not just a keyword filter — since this is graded as an NLP practical.
- Must be demoable end-to-end in a short viva: input → recommended topics with novelty + feasibility scores → explanation of *why*.
- Must be buildable by 2 people in real remaining hours, with your existing JS/Python/CSS/Docker/HTML stack, alongside your other coursework (Big Data capstone, RPA project, campus placement prep).

## 5. Definition of done for Month 1

1. Working deployed prototype (Docker-composed, free-tier hosted) with a **golden dataset of 150–300 real past GLS/IMCA project titles** (your unfair advantage — a generic online tool has no access to this).
2. Novelty + feasibility scoring pipeline, explainable in plain language.
3. NLP practical report + viva demo script.
4. A 1-page pitch + working demo link ready to show your HOD/dean as a potential department tool — this is the "university pitch" step referenced in your ask.
