# M.A.C.H. build plan for TechiGum

Nov 5, 2026 · @Sachethan

## The short version

The judges will score you against the 7 deliverables in the challenge statement, not against the buzzwords in the abstract. The winning move is a small, honest system that demonstrably cites, abstains, detects superseded revisions, and beats two baselines on a fixed question set. Keep the abstract's ideas (vision-native retrieval, self-checking, multi-agent drafting) but implement each at the smallest scale that still proves it.

## Where the abstract over-promises

| Claim in abstract | Reality for a student team | What to do instead |
| --- | --- | --- |
| GKE + vLLM KV-cache for multi-agent throughput | You will not self-host an LLM if you use the Gemini API. vLLM only matters if you serve open weights on your own GPUs, which costs money and weeks. | Drop it from the build. Run on Cloud Run (or a laptop with Docker Compose). Mention vLLM in the deployment report as the on-prem path for clients who cannot send data to a cloud API. |
| DocLLM spatial attention | DocLLM is a research model with no easy public checkpoint and no plug-in API. | Use ColPali/ColQwen2 for page-image retrieval, plus a layout parser (Docling or PyMuPDF) for bounding boxes. Say "layout-aware" rather than naming DocLLM. |
| "Bypass OCR" entirely | Sentence-level citations, keyword baseline, and supersession checks all need text. | Hybrid: page images for retrieval, extracted text + boxes for citation and BM25. This is stronger, not weaker. |
| ColPali embeddings in Cloud SQL | ColPali is multi-vector (one vector per patch, roughly 1000 per page). pgvector does not do late-interaction MaxSim natively. | Use Qdrant (has multi-vector MaxSim) or byaldi for the prototype. Keep Postgres for metadata, revisions and audit logs. |
| Self-RAG and CRAG | Self-RAG needs a fine-tuned model with reflection tokens. | Implement the CRAG idea as a prompt-based grader: score retrieved evidence, then answer, abstain, or re-retrieve. Call it "Self-RAG/CRAG-style". |
| ARES | Needs training judge classifiers; heavy. | Ragas plus your own scripted metrics. ARES is optional stretch. |
| AutoGen-inspired agents | Fine, but easy to over-build. | Two agents (Drafter, Compliance Checker) plus a human approver, built with LangGraph or plain Python. |
| "Expert time saved" | Needs real experts. | Timed study: 3–5 people answer 10 questions with keyword search vs. M.A.C.H. Report minutes per correct answer. |

## Minimal viable stack

- **Corpus**: 30–60 synthetic but realistic docs for one line (e.g. a brake-caliper assembly cell): SOPs with 2–3 revisions each, work instructions, 2–3 ECNs that supersede steps, quality alerts, RCA reports, annotated equipment photos. Generate drafts with an LLM, then hand-edit, and plant deliberate conflicts and superseded steps.
- **Parsing**: Docling or PyMuPDF for text, tables and bounding boxes; page images rendered at 150 dpi.
- **Retrieval**: ColQwen2/ColPali (via byaldi or Qdrant multi-vector) for visual pages + BM25 (rank\_bm25 or Postgres full-text) + a text embedding model; fuse with reciprocal rank fusion.
- **Generation**: Gemini 2.x via Vertex AI with structured JSON output: each sentence carries `doc_id`, `page`, `section`, `bbox`, `revision`, `effective_date`.
- **Metadata and governance**: Postgres tables for documents, revisions, supersession links, roles, audit log, approval queue.
- **Escalation**: a Postgres approval queue first; Pub/Sub only if you deploy on GCP (it is a one-line swap).
- **UI**: Streamlit or Next.js with an operator chat, a PDF viewer that highlights the cited box, and an expert review inbox.
- **Eval**: Ragas + a custom script over a 60–100 question gold set.
- **Deploy**: Docker Compose locally, Cloud Run for the demo.

## Deliverables mapped to components

### 1. Versioned multimodal corpus, access controls, metadata, expert Q/A set

- Document registry schema: `doc_id, type, line, station, revision, effective_date, supersedes, status, owner, access_role`.
- Role-based filtering at retrieval time (operator, quality engineer, maintenance, admin), so an operator never retrieves restricted RCA content.
- Gold set of 60–100 questions in 5 buckets: text lookup, table lookup, image-based, superseded-revision traps, unanswerable/conflicting. Each has expected answer, expected citation, and expected behaviour (answer / abstain / escalate). Get a faculty member or anyone with plant experience to review it, and say so.

### 2. Text, table, image ingestion with revision and supersession

- Ingestion job: parse → chunk by section → extract tables as markdown + keep page image → store boxes.
- Supersession: explicit `supersedes` links from ECNs plus a check that flags two active docs covering the same station/step.
- Retrieval filters out superseded revisions by default and can show them with a warning ("Rev C superseded by ECN-014 on 2026-03-02").

### 3. Multimodal retrieval and answers with sentence-level citations and confidence

- Query by text or by uploaded photo (photo → ColPali query or Gemini caption → retrieval).
- Answer schema forces one citation per sentence; a post-check verifies each cited span actually exists on that page (drop or flag sentences that fail).
- Confidence = combination of retrieval score, grader score, and citation-verification pass rate. Show it as High/Medium/Low.

### 4. Abstention, conflict detection, freshness, escalation

- Evidence grader (CRAG-style): relevant / ambiguous / irrelevant → answer / re-retrieve / abstain.
- Conflict check: if two active sources give different values for the same parameter (torque, temperature), abstain and show both.
- Freshness: every answer states the revision and effective date; warn if a newer revision exists.
- High-risk classifier (safety, lockout/tagout, torque specs, anything with a quality alert) → route to the expert inbox instead of answering directly.

### 5. Draft work-instruction workflow with change control

- Input: an RCA record. Drafter agent writes a WI draft citing the RCA and current SOP. Compliance agent checks it against active SOPs and required fields.
- State machine: Draft → In review → Approved/Rejected → Published as new revision, with the old one marked superseded. Every transition is logged with user and timestamp.

### 6. Evaluation vs. keyword search and text-only RAG

- Three systems on the same gold set: BM25, text-only RAG (same LLM, no images, no grader), M.A.C.H.
- Metrics: answer correctness (LLM judge + spot human check), citation precision, retrieval recall@k, abstention precision/recall on the unanswerable bucket, freshness accuracy on the superseded bucket, p50/p95 latency, and the timed expert study.
- Present one results table and 3–4 failure-case examples. Honest failures score well with judges.

### 7. Security and deployment report

- RBAC, audit logging, prompt-injection handling for ingested docs, PII/IP considerations of sending docs to a cloud LLM, data residency.
- Deployment options: Cloud Run + Vertex (what you built), and an on-prem path with open weights on vLLM (where the GKE/vLLM idea belongs).

## Phased milestones (assuming about 8 weeks; adjust once the timeline is known)

| Phase | Weeks | Exit criteria |
| --- | --- | --- |
| 0. Corpus and gold set | 1–2 | 40+ docs with revisions and planted conflicts; 60+ gold questions; schema done |
| 1. Baselines | 2–3 | BM25 and text-only RAG answer the gold set; eval script prints a table |
| 2. Multimodal retrieval and citations | 3–5 | ColPali + hybrid fusion; sentence citations with bbox highlight in the UI |
| 3. Trust layer | 5–6 | Grader, abstention, conflict and supersession checks, expert inbox |
| 4. WI drafting workflow | 6–7 | RCA → draft → compliance check → approval → new revision |
| 5. Eval, report, demo | 7–8 | Full results table, timed user study, security report, 3-minute demo video |

A working end-to-end slice by week 3 matters more than any single component. Build thin, then deepen.

## Suggested team split (for 3–4 people)

- Data and eval: corpus, gold set, metrics, user study.
- Retrieval: parsing, ColPali, hybrid search, supersession filters.
- LLM and agents: answer schema, grader, abstention, drafting workflow.
- App and infra: UI, approval inbox, RBAC, deployment, security report.

## Open questions for Sachiv

1. What is the next round: a demo, a presentation to faculty/LTTS, or a full working prototype, and when is it due?
2. How many people are on the team, and what are their strengths?
3. Do you have GCP credits or a GPU, or should the plan assume free tiers and a laptop?
4. Has LTTS or your faculty mentor provided any real or sample documents?
