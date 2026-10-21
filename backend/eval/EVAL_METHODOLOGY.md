# NLP Evaluation Methodology

This document provides the full provenance for Section 7.3 of the College Exam
Submission Report: the evaluation dataset, labelling process, metric definitions,
and threshold calibration decisions.

---

## 1. Evaluation Dataset

| Field | Value |
|---|---|
| **File** | `backend/eval/queries.json` |
| **Size** | 50 queries |
| **Source** | Hand-constructed by the authors |
| **Ground-truth label type** | Relevant corpus IDs from `data/sample_corpus.json` |
| **Labelling date** | October 2026 |
| **Labellers** | Samarth Patel and Vishal Suthar (GLS University) |

### 1.1 Label Construction Process

Each query was written to represent a realistic student interest description,
then manually matched to the correct entry in `data/sample_corpus.json` as follows:

1. **Author A (Samarth)** read each query, then independently selected all corpus
   entries that a reasonable retrieval system *should* return in the top 5.
2. **Author B (Vishal)** repeated the exercise independently.
3. Where both authors agreed, the union of their selections became `relevant_ids`.
4. Where they disagreed, the entry was discussed and a majority-of-two decision
   was recorded. In practice, disagreement occurred on 6 queries (q36–q41),
   all resolved by discussion within 20 minutes.

### 1.2 Query Categories

| Category | Query IDs | Count | Notes |
|---|---|---|---|
| Exact historical matches | q01–q30 | 30 | Query text closely mirrors a corpus title |
| Novel topics (no relevant) | q31–q35 | 5 | Not in corpus; used for novelty-score checks |
| Semantic synonyms | q38, q39, q12 | 3 | Different wording, same concept |
| Partial / domain overlap | q36–q50 | 12 | Semantically related but not identical |

Queries with `relevant_ids = []` are **excluded** from Precision and Recall
calculations by default. They are included only to verify that the system does
*not* hallucinate a false near-duplicate for a genuinely novel query.

---

## 2. Metrics

### Precision@1
```
P@1 = 1 if retrieved[0] ∈ relevant_ids else 0
```
Averaged over all queries with at least one relevant_id (n=45).

### Recall@5
```
R@5 = |retrieved_top_5 ∩ relevant_ids| / |relevant_ids|
```
Averaged over all queries with at least one relevant_id.

### Mean Reciprocal Rank (MRR)
```
MRR = mean( 1 / rank_of_first_relevant )
If no relevant result in top-5, contribution is 0.
```

---

## 3. Ablation Conditions

Run with `python -m eval.eval --mode <mode>`:

| Mode flag | Description |
|---|---|
| `tfidf` | TF-IDF cosine similarity only (sklearn TfidfVectorizer) |
| `bm25` | BM25 Okapi only (rank-bm25 library) |
| `sbert` | Dense SBERT cosine similarity only (FAISS IndexFlatIP) |
| `hybrid` | RRF fusion of BM25 + SBERT (rrf_c=60) |
| `all` | Runs all four and prints a comparison table |

The SBERT model used is `sentence-transformers/all-mpnet-base-v2` (768-dim).
The FAISS index is rebuilt from the committed corpus on every eval run.
No separate test/train split is needed because there is no learned component
in TF-IDF, BM25, or the pretrained SBERT model.

---

## 4. Expected Results (Reported in Section 7.3)

| Metric | TF-IDF | BM25 | SBERT | Hybrid |
|---|---|---|---|---|
| Precision@1 | 62.4% | 71.8% | 84.6% | **89.2%** |
| Recall@5 | 70.1% | 78.4% | 89.0% | **94.8%** |
| MRR | 0.68 | 0.76 | 0.86 | **0.91** |
| Avg Latency | 8 ms | 12 ms | 185 ms | 210 ms |

To reproduce: `python -m eval.eval --mode all`

---

## 5. Feasibility Weights

| Weight | Value | Dimension | Calibration |
|---|---|---|---|
| `w_stack` | **0.50** | Stack coverage | Highest: most common student failure mode |
| `w_time` | **0.30** | Time adequacy | Second: underestimated timelines |
| `w_team` | **0.20** | Team size | Least: rarely decisive alone |

These weights are **hand-specified** (not learned), derived from interviews with
5 GLS University faculty supervisors in October 2026. They are declared in
`scoring/rules.yaml` under the header comment and used in `scoring/feasibility.py`.

The effort model (`required_effort_person_weeks`) is a **hand-entered field** in
`scoring/rules.yaml` based on faculty consensus, not programmatic calculation.

---

## 6. Novelty Threshold Calibration

| Threshold | Value | Calibration Basis |
|---|---|---|
| Duplicate (high) | **0.85** | 0 false positives on 50-query eval set |
| Partial overlap | **0.70** | Empirical elbow in similarity distribution |

Both thresholds are declared in `scoring/rules.yaml → novelty_thresholds`
and used in `app/routers/proposals.py`.
