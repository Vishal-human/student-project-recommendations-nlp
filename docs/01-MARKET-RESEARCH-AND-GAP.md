# Market Research & Gap Analysis

## 1. What already exists (researched)

**A. "Project idea" content sites (blogs, not products)**
Dozens of sites (GeeksforGeeks, ProjectPro, upGrad, GUVI, Nevonprojects, phdservices.org, etc.) publish static ranked lists like "50 AI Project Ideas for Final Year Students." They are:
- Generic, not personalized to a student's actual skill level, stack, or time budget.
- Not aware of what's already been done at your specific college/department — so "trending" ideas like chatbots, movie recommenders, and resume screeners get resubmitted by thousands of students every year.
- Zero novelty/plagiarism awareness; they exist to drive blog traffic or sell services.

**B. "Project vendor" shops (a uniquely Indian, somewhat predatory market)**
Businesses (e.g. Aislyn Technologies, ProjectsAtBangalore, and many similar Bangalore/Chennai/Pune outfits) sell **pre-built final-year projects with source code, PPT, and report** to students for a fee, sometimes explicitly marketing "plagiarism-free" as a differentiator — implying the norm is *not* original. This is a real, large, semi-informal market, and it is the actual competitor mindset your product should displace: it optimizes for "get marks" instead of "learn something real and build a portfolio."

**C. Academic literature / thesis prototypes**
Multiple university thesis projects (Nigeria, Ethiopia, Pakistan — per literature reviewed) propose "Final Year Project Management Systems with duplicate detection," but these are:
- Single-university, closed, never productized or open-sourced meaningfully.
- Focused on *duplicate title string-matching*, not semantic similarity, feasibility, or skill-fit.
- Built as one-off academic exercises, not maintained products — validating that the *problem is real and recognized academically* but **nobody has shipped a good product for it**, which is your opening.

**D. Generic recommender-system research (education-adjacent)**
Papers like "eDoer" (labor-market-driven learning recommender) show real research interest in mapping skills → learning goals → resources, but these target *course/resource* recommendation, not *capstone/thesis project topic* recommendation with originality and feasibility scoring. Different problem, adjacent techniques (embeddings, skill decomposition) — useful signal for your ML design, not a competitor.

## 2. The actual gap (what nobody has built well)

| Need | Covered by blogs? | Covered by project vendors? | Covered by academic prototypes? | Covered by you? |
|---|---|---|---|---|
| Personalized topic suggestions by skill/interest | Partial (static lists) | No | No | **Yes (core MVP)** |
| Semantic novelty check vs. real past submissions | No | No (actively undermines this) | Partial, keyword-only | **Yes — your differentiator** |
| Feasibility scoring vs. actual time + stack + team size | No | No | No | **Yes — new** |
| Supervisor/HOD dashboard to spot duplicate topics across sections before approval | No | No | Partial, single-institution, unshipped | **Yes — B2B wedge into university** |
| Explainable "why this scored this way" | No | No | No | **Yes** |
| Cross-institution reusable dataset/model that improves over time | No | No | No | **Yes — long-term moat** |

## 3. Why this can go beyond a course project

1. **Distribution is built in.** You have a captive first customer: your own department. IMCA/BCA/MCA/engineering departments across India run this exact "topic approval" process manually every semester — usually a spreadsheet + a supervisor eyeballing titles for overlap. That is a real, recurring, unglamorous administrative pain your EdTech Strategist persona should validate directly with your HOD.
2. **The vendor market proves willingness to spend.** Students already pay money to solve "I don't have a good, safe project topic" — currently by buying pre-made ones. You're offering the honest, better-for-learning version of the same underlying demand.
3. **Data moat compounds.** Every semester of usage at GLS adds real titles/abstracts to your novelty-detection corpus, making the tool better and harder to replicate cold.
4. **You already have the reusable core.** Sentence-BERT + FAISS + FastAPI is the correct architecture for semantic search over titles — this is not a rebuild, it's an extension.

## 4. Explicit non-goals for v1 (say no to these, on purpose)

- Do **not** try to build a general "AI project idea generator" (that's the crowded, low-value blog space).
- Do **not** try to fine-tune a large LLM from scratch this month — no dataset, no time, no GPU budget. (See ML doc for the realistic path.)
- Do **not** build a marketplace/payment system yet. Prove the workflow value first, monetize later (see pitch doc).
