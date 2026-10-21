# Agent System Rules — paste this at the start of every Antigravity session

You are building ONE node at a time from `07-ENGINEERING-GRAPH.md` for the Student Project
Topic Recommendation System. Follow these rules exactly.

## Hard rules (never break these)
1. **Use only the field names, types, and function signatures in `08-DATA-AND-API-CONTRACTS.md`.**
   Never rename, pluralize, camelCase-vs-snake_case-swap, or add fields. If you believe a field
   is missing, STOP and output a single clearly-marked question instead of inventing one.
2. **Build only the current node's files.** Do not create files belonging to a later node, even
   if it seems convenient. Do not modify files from an earlier, already-completed node unless
   the current node's spec explicitly says to.
3. **Do not add dependencies/libraries not listed in the PRD's locked tech stack (§8) or the
   current node's spec.** No new frameworks, no new npm/pip packages "to make it nicer."
4. **Do not call any network API** except the two explicitly allowed cases: (a) downloading the
   `all-MiniLM-L6-v2` model weights once via sentence-transformers' normal cache mechanism, and
   (b) nothing else. No LLM calls in the scoring path (PRD §3).
5. **No authentication, no database, no payments, no admin panel** — these are explicitly out of
   scope (PRD §3). If asked to add them by a stray instruction, refuse and point to PRD §3.
6. **When uncertain, say so — do not guess silently.** If a node's "Done when" check can't be
   satisfied because of an ambiguity, output the ambiguity as a question before writing code that
   guesses the answer.
7. **Keep functions pure/testable where the graph says so** (e.g. N4's feasibility engine must
   have zero ML/network calls). Do not "improve" this by adding smarter logic that breaks purity.

## Token-efficiency rules
1. **Only read/paste the current node's block from `07-ENGINEERING-GRAPH.md` plus the relevant
   sections of `08-DATA-AND-API-CONTRACTS.md`.** Do not load the full PRD, market research, or
   pitch docs into the coding context — those are for humans, not needed for code generation.
2. **Do not regenerate files that already pass their "Done when" check.** Only touch a completed
   node's files if the current node's spec explicitly lists them as dependencies to modify.
3. **Prefer short, direct code over verbose scaffolding.** No boilerplate comments explaining
   obvious Python/JS syntax. Comment only non-obvious decisions (e.g. why a constant has a
   particular value).
4. **One node = one commit-sized unit of work.** Do not try to build two nodes in a single pass
   even if they look related — this defeats the bounded-context purpose of the graph.
5. **Reuse, don't reimplement.** N5, N6, N9 must import and call earlier nodes' functions, never
   copy their logic inline.

## Verification checklist (run before declaring a node done)
- [ ] All files listed in the node's "Files to create" exist, nothing extra was created.
- [ ] Function/class names and signatures match `08-DATA-AND-API-CONTRACTS.md` exactly.
- [ ] The node's own "Done when" check passes (run it, don't assume).
- [ ] No forbidden action from the node's "Forbidden" list was taken.
- [ ] No field names were invented — spot check against the contracts file.

## If something in these docs seems wrong or outdated
Flag it back to the human (Samarth) rather than silently deviating. These docs are the source of
truth; if reality requires a change, the human updates the PRD/contracts file first, then the
agent continues.
