# Pitch Plan — University First, Then Beyond

## 1. Why "university first" is the right sequencing
You already have distribution: GLS University, your own department, a real dataset source, and a credible reason to talk to your HOD (submitting an NLP practical). Pitching internally first lets you:
- Get real usage data and supervisor feedback before showing it to anyone external.
- Convert "student project" into "adopted department tool," which is a genuinely strong resume/LinkedIn line and startup proof point — stronger than a cold external pitch with zero users.

## 2. Who to pitch, in order
1. **Your NLP practical evaluator/guide** — frame it as exceeding the assignment (they grade the NLP rigor; give them the evaluation harness from Spec 7).
2. **Your IMCA HOD/coordinator** — frame it as a tool that reduces their manual duplicate-checking workload every semester. This is the real pitch, not "cool AI project."
3. **GLS innovation/incubation cell (if one exists)** — ask your placement/T&P cell or check GLS's official channels; many Indian universities have an E-cell or incubation center that's a natural next step for a validated department tool.

## 3. The 1-page pitch structure
1. **Problem** (1-2 lines): Supervisors manually check for duplicate/overlapping project topics every semester; students often don't know if their idea is novel or feasible until they're already committed.
2. **Solution** (1-2 lines): An NLP tool that scores any proposed topic for novelty (vs. real past submissions) and feasibility (vs. the student's actual skills/time), with plain-language explanations.
3. **Proof**: live demo link + your evaluation harness numbers (precision/recall on the labeled duplicate-pair set).
4. **Data moat**: grows every semester, GLS-specific, hard to replicate cold.
5. **Ask**: (a) permission/support to use anonymized historical project titles going forward, (b) a pilot with your department for the next intake, (c) optionally, incubation cell introduction.

## 4. Demo script (5 minutes, also reusable for your viva)
1. 30s: state the problem in one sentence (see above).
2. 60s: show a student typing interests + stack → get scored recommendations with explanations.
3. 60s: show the novelty score catching a near-duplicate against a real historical title — this is the "aha" moment, lead with it.
4. 60s: show the feasibility score flagging a mismatched-skill topic, and how it's rule-based/explainable, not a black box.
5. 30s: close with the data-moat/growth story and the university-tool framing, not "just an AI project."

## 5. Beyond GLS — realistic expansion path (don't overbuild this now)
- **Phase 2 (next semester)**: pilot with 1-2 more departments/colleges you have personal reach into (batchmates at other institutions, GDG/Hack2Skill network you're already part of).
- **Phase 3**: cross-institution aggregated (anonymized) novelty corpus — this is where the real long-term product/startup value is, since no single college's dataset is enough to be a moat alone, but a federated/aggregated one is hard for anyone to replicate.
- **Monetization (later, not now)**: B2B SaaS to university departments (per-semester or per-cohort licensing) is the more durable model vs. B2C-per-student, given Indian students' price sensitivity and the vendor-shop competition described in the market research doc. Don't design pricing yet — prove adoption first.

## 6. Guardrails so this stays fundable/credible
- Be explicit in every pitch that this is a **novelty and feasibility aid, not an academic-integrity replacement** — it should never be framed as "guaranteed plagiarism-free" (that's the shady vendor-shop framing you're explicitly positioned against).
- Keep supervisor-in-the-loop: the tool scores and explains, a human still approves. This is both the ethically correct design and the safer pitch to a university administration.
