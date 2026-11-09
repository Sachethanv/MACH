# CLAUDE.md — context for Claude Code

Read this first in every session. It is the short version of everything in `docs/` and `research/`.

## What we are building

**M.A.C.H. — Multimodal Agentic Compliance & Heuristics for the Shop Floor.**
TECHgium 10th edition (L&T Technology Services), PID **TG0903606**, challenge:
*"GenAI-Powered Intelligent Manufacturing Knowledge Assistant for Shop Floor Operations."*

A shop-floor assistant that answers operator questions from the plant's own SOPs, work
instructions (WIs), diagrams, tables, quality alerts, ECNs and RCA reports. It:

1. cites the exact document, revision, page/section, step and image region for every statement,
2. never answers from a superseded revision and never mixes two revisions in one answer,
3. abstains or escalates to a human expert when evidence is missing, conflicting or the step is hazardous,
4. drafts new work instructions from RCA records, which only become official after human approval (change control),
5. is evaluated against keyword search (BM25) and text-only RAG on a fixed question set.

The pitch: M.A.C.H. is a **trust layer for safety-critical procedures**, not "just multimodal RAG".
Page-image retrieval (ColPali) and self-checking RAG (Self-RAG/CRAG) are already published; our
novelty is Revision Guard, step-level safety-complete citations, number lock, hazard-tiered
abstention and drafting under change control. See `docs/09_novelty_and_claims.md`.

## Hard rules for code in this repo

- **Revision Guard is deterministic code, never an LLM decision.** Filter by effectivity
  (status = effective, `t_from <= now < t_to`, scope matches the operator's site/line/station/model/serial,
  role allowed) *before* any ranking, in every retrieval lane.
- **Access control happens before retrieval**, not after generation. No restricted element ID may
  ever appear in a lower-role prompt, trace or answer.
- **Number lock:** torques, temperatures, pressures, dimensions, tolerances, units and part numbers
  in an answer are copied by code from the cited element. The LLM never types them.
- **The LLM cites from a closed list of pre-parsed element IDs** (`doc:rev:page:element`). It never draws boxes.
- **Retrieved document text is data, not instructions.** Strip/flag instruction-like text at ingestion;
  output is schema-enforced JSON.
- **Nothing the AI drafts is auto-published.** Draft → In review → Approved/Rejected → Published, every
  transition logged with user + timestamp.
- **Everything is logged** to an append-only audit log (query, context, retrieved IDs, revisions, answer,
  verifier verdicts, model version, corpus snapshot hash) so any answer can be replayed.
- **Latency budget: p95 < 15 s** end-to-end on one 24 GB GPU. Precompute embeddings/captions, send ≤ 4
  page images to the generator, cap multi-hop at 2 rounds, stream first steps.
- **Never tune on test splits.** MACH-Bench is 30% dev / 70% test; public benchmarks are eval-only.
- Never claim "world first". Use "we found no prior work on X".

## Stack (decided)

| Layer | Choice |
|---|---|
| Language | Python 3.11, managed with `uv` |
| Parsing | Docling (primary) / PyMuPDF; page images at 150 dpi |
| Visual retrieval | ColQwen2.5 (or ColPali) multi-vector, stored in **Qdrant** (MaxSim) |
| Text retrieval | BM25 (`rank_bm25` or Postgres FTS) + **BGE-M3** dense + exact-ID regex lane |
| Fusion / rerank | weighted RRF tuned on dev + `bge-reranker-v2-m3` |
| Generator (local, main) | **Qwen2.5-VL-7B-Instruct AWQ 4-bit** served with **vLLM** (24 GB GPU) |
| Generator (optional) | Qwen2.5-VL-32B-Instruct AWQ or Qwen3-VL-30B-A3B on 48 GB GPU; Gemini via Vertex AI only for offline jobs / hosted demo |
| Router | small classifier (DeBERTa-v3-small or logistic regression on embeddings), 4 classes |
| Verifier | exact-match for values + NLI model for text entailment |
| Agents | LangGraph (or a plain Python state machine) |
| Registry / audit / approvals | PostgreSQL |
| API | FastAPI |
| UI | Streamlit for the demo (operator chat, PDF viewer with highlighted box, expert inbox, draft diff view) |
| Eval | RAGAS + custom trust-metric scripts + pytest edge-case harness (YAML fixtures) |
| Deploy | Docker Compose on one plant-side GPU box (edge-first); Cloud Run only for a hosted demo |

**Hardware (decided):** the dev PC is Windows with an **NPU and no NVIDIA GPU**, so vLLM/ColQwen do not run
locally. GPU work (vLLM, embeddings, indexing, eval, the demo) runs on a **GCP `g2-standard-8` VM with one
NVIDIA L4 24 GB** (paid from GCP credits; setup in `docs/11_gcp_gpu_setup.md`) with the same `docker-compose.yml`. The local PC edits code,
runs unit tests (no GPU needed for Revision Guard, access, number lock) and can run the UI against the remote
API via an SSH tunnel. Keep all GPU-dependent code behind interfaces with config-selected backends
(`generator.backend: vllm | gemini | ollama`). See `docs/05_edge_vs_cloud.md` → *Demo setup*.

## Repo map

```
src/mach/            the package (skeleton only so far)
  ingestion/         parse PDFs -> typed elements, page images, captions, criticality labels
  registry/          document/revision metadata, supersession links, deviation overlays (Postgres)
  retrieval/         exact-ID, BM25, dense, visual lanes; fusion; rerank; cross-ref expansion
  guard/             Revision Guard: effective-set filter, supersession statements, coherence check, conflict detector
  router/            4-way query router (direct / single / multi-hop / escalate)
  generation/        prompt + JSON schema, VLM client (vLLM / Gemini behind one interface)
  verify/            citation validity, number lock, NLI entailment, safety-step completeness
  abstain/           risk scoring + per-hazard-tier conformal thresholds
  escalation/        expert inbox, candidate answers, expert notes with expiry
  drafting/          Drafter + Compliance agents, change-control state machine
  agents/            LangGraph graph wiring the above
  api/               FastAPI app
  ui/                Streamlit app
  audit/             append-only audit log + replay
baselines/           B1 BM25, B2 BM25+LLM, B3 dense text RAG, B4 hybrid, B5 hybrid+date sort
eval/                metrics, benchmark loaders, MACH-Bench builder, edge-case fixtures + harness
configs/             settings.yaml, hazard tiers, glossary
data/                raw/ processed/ (gitignored) — see data/README.md
docs/                design docs (start with docs/README.md)
research/            brief, literature review, planning docs, paper draft, PPT
```

## Where to look

- Architecture and the 7 checks: `docs/02_architecture.md`
- Agent graph and state: `docs/03_agentic_design.md`
- Datasets and benchmarks: `docs/04_datasets_and_benchmarks.md`
- Edge vs cloud: `docs/05_edge_vs_cloud.md`
- Release gates + 55 edge cases: `docs/06_evaluation_and_test_plan.md`
- What to build next: `docs/07_roadmap.md`
- Tools, libraries, MCP servers, plugins: `docs/08_tools_libraries_mcp.md`
- Paper draft (placeholders [R1]–[R10] still unmeasured): `research/planning_docs/04_paper_draft.md`

## Working style

- Build a **thin end-to-end slice first** (ingest 1 doc → retrieve → answer with citation → audit log), then deepen.
- Write tests for Revision Guard, access control and number lock **before** the code (TDD) — they are hard gates.
- Keep every threshold and weight in `configs/`, never hard-coded.
- No result is real until measured. Keep paper/PPT numbers marked as placeholders until the harness produces them.

## Open questions (ask the user if relevant)

- Team size and who owns what; GPU available (24 GB? 48 GB?) on the dev PC; GCP credits.
- Someone with plant experience to review the gold question set.
- Whether LTTS can share 5–10 real SOPs under NDA as a private test set.
