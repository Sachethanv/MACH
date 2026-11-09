# 02 · System architecture

M.A.C.H. has three parts:

1. **Offline ingestion** turns documents into searchable, revision-tagged elements.
2. **The online answer path** runs every question through a chain of checks before anything reaches the operator.
3. **Governance** handles experts, change control and the audit trail.

Full figure: [`research/brief/figures/fig1.svg`](../research/brief/figures/fig1.svg) (architecture) and
[`fig2.svg`](../research/brief/figures/fig2.svg) (change-control state machine).

```
                 ┌──────────────────────────── OFFLINE (plant server; cloud allowed only for non-sensitive jobs) ─┐
 PDFs, scans,    │ parse (Docling/PyMuPDF) → typed elements + bboxes → page images 150 dpi → VLM captions      │
 photos, ECNs,   │ → step detection → cross-ref edges → criticality κ(e) → instruction stripping → registry     │
 alerts, RCAs ──▶│ → indexes: exact-ID · BM25 · BGE-M3 dense · ColQwen2.5 visual (Qdrant) · snapshot hash        │
                 └───────────────────────────────────────────────────────────────────────────────────────────────┘

 ONLINE (plant-side GPU, p95 < 15 s)
 operator query (text / photo / Hindi)
   │ + session context c = (time, site, line, station, model, serial, role, shift)
   ▼
 [1 Context lock] → [Router] ─ escalate-now ─────────────────────────────────────────────┐
   │ direct / single / multi-hop                                                         │
   ▼                                                                                     │
 [2 Revision Guard: E(c) hard pre-filter in EVERY lane] → 4 lanes → weighted RRF → rerank │
   → cross-ref 1-hop expansion → [3 CRAG grader] ─ ambiguous → re-search (≤2) ─ irrelevant → abstain
   ▼
 [4 Conflict detector] ─ conflict → show both + escalate
   ▼
 Generator (Qwen2.5-VL-7B AWQ, JSON schema, cites element IDs only) + supersession statements in context
   ▼
 [5 Number lock] → [6 Citation + coherence + safety-completeness verifier] → [7 Hazard-tiered gate]
   │ pass                          │ partial                          │ fail
   ▼                               ▼                                  ▼
 answer + highlighted source   certified steps + "escalate X–Y"     abstain + expert inbox
   └──────────────── everything → append-only audit log (replayable) ─────────────────────┘

 GOVERNANCE: expert inbox → expert notes (dated, expiring, advisory) → repeated notes trigger a draft
             RCA/ECN → Drafter → Compliance (SOP conflicts, required fields, STE) → human approval
             → new effective revision (old one superseded) → back into ingestion
```

## Data model (from the paper, Section III)

- A **document** `d` has **revisions** `r(d,1), r(d,2), …`. Each revision carries metadata
  `m = (doc_id, rev, status, t_from, t_to, scope, superseded_by, access_role)`.
  - `status ∈ {draft, in_review, effective, superseded, obsolete}` (+ `withdrawn`)
  - `scope` = set of constraints on (site, line, station, product/model, serial range)
- A revision is parsed into **elements** `e`: `element_id` (`doc:rev:page:element`), type (text, step, table,
  table_cell, figure, callout, warning), page, bbox, caption, and **criticality** `κ(e) ∈ {0 informational,
  1 quality-critical, 2 safety-critical}`.
- **Effective set**: `E(c) = { e ∈ r : r.status = effective ∧ t_from ≤ t < t_to ∧ s ⊨ r.scope ∧ u ∈ r.access_role }`.
- A **deviation / ECN overlay** is a scoped, time-limited override of named steps; when active it replaces
  those steps inside `E(c)` (it is not a competing document).
- **Revision coherence**: for every document, all citations in one answer come from a single revision.

Postgres tables (planned): `documents`, `revisions`, `elements`, `supersessions`, `overlays`, `roles`,
`users`, `audit_log` (append-only), `escalations`, `expert_notes`, `drafts`, `draft_transitions`,
`corpus_snapshots`.

## The 7 checks every answer passes

1. **Context lock.** Role, station, machine model, serial range and shift come from the session (never from
   the prompt), so search only sees documents the user may read and that apply to their machine.
2. **Revision Guard.** Hard filter, not a re-rank: only effective, in-window, in-scope, role-allowed chunks are
   searchable. ECNs/deviations patch the specific steps. Superseded content only via an explicit history mode
   with a banner. The generator context includes explicit statements like *"WI-214 Rev B was superseded by
   Rev C on 2026-03-02 via ECN-014; Rev B must not be used."*
3. **Evidence grading.** CRAG-style grader: relevant → answer; ambiguous → up to 2 re-searches; irrelevant → abstain.
4. **Conflict detection.** Two effective sources giving different values for the same parameter at the same
   scope → show both, escalate, open a document-control ticket. A quality alert outranks the SOP until resolved.
5. **Number lock.** Every torque, temperature, pressure, dimension, tolerance, unit and part number is copied by
   code from the cited element. Units converted by code. OCR vs image-reading digit mismatch → abstain.
6. **Citation + safety verification.** Each step's citation must be in `E(c)` and entail the step (exact match
   for values, NLI for text); one revision per document; cited variant matches the machine; every warning,
   PPE and LOTO step in the source appears in the answer, warnings first, never truncated.
7. **Hazard-tiered gate.** Required confidence depends on the step's hazard tier:

| Tier | Examples | Target max error on answered steps | Below threshold |
|---|---|---|---|
| 1 · Critical | LOTO, pressure release, lifting, torque on safety fasteners | ≤ 1% | Abstain, "stop and hold", escalate |
| 2 · Quality | Torque specs, temperatures, inspection criteria | ≤ 5% | Partial answer, escalate uncertain steps |
| 3 · General | Tool locations, part descriptions, cosmetic steps | ≤ 10% | Answer with "low confidence" label |

Thresholds are calibrated per tier with split-conformal risk control on the dev set (Mohri & Hashimoto,
ICML 2024; C-RAG, ICML 2024) and **re-checked whenever an SOP family gets a new revision**. Error targets are
our design choice.

Deferral rule (paper IV-F): escalate if `max_i p̂_err(y_i)·w_κ(y_i) > λ·cost_expert(t, s)`, where
`cost_expert` rises when fewer experts are on shift (shift-aware escalation).

## Retrieval lanes

| Lane | What | Why |
|---|---|---|
| Exact-ID | regex + normalisation for part, tool, SOP, ECN numbers | keywords/IDs still win on part numbers |
| BM25 | over layout-aware chunks + captions | keyword baseline, jargon |
| Dense text | BGE-M3 | paraphrase / semantic |
| Visual | ColQwen2.5 / ColPali page images, multi-vector MaxSim in Qdrant | answers hidden in diagrams/tables (VisRAG: +20–40% vs text-only) |

Fusion: weighted reciprocal-rank fusion (weights grid-searched on dev; naive fusion hurts 8–21% of queries),
then `bge-reranker-v2-m3`, then 1-hop cross-reference expansion ("see Fig. 3, step 4"). Photo queries go to
the visual lane and are captioned for the text lanes.

## Latency budget (estimates — measure on the real box)

| Stage | Expected |
|---|---|
| Encode query + search precomputed page index | < 0.5 s |
| BM25 + dense + ID match + fusion | < 0.3 s |
| Rerank top 20 | 0.5–1.5 s |
| Revision filter | negligible |
| Generator reads 3–4 page images | 1–3 s |
| Generator writes ~300 tokens (7B, 4-bit) | 3–6 s |
| Verifier checks | 0.5–1.5 s |
| **Single-retrieval answer** | **≈ 6–12 s** |

Keep models warm, cache the system prompt, cap image resolution, stream first steps, escalations run in the
background (not counted against 15 s).

## Security and governance

- RBAC enforced inside the effectivity gate; cache keyed by role + effective set.
- Instruction-like text neutralised at ingestion (also inside images/figures, via captioning); retrieved text
  treated as data; fixed JSON output schema.
- PII in RCA reports redacted at ingestion; no per-operator analytics.
- Append-only audit log: query, context, retrieved IDs per lane, gate decisions, router path, prompt, raw
  output, verifier verdicts, model version, corpus snapshot hash, latency per stage → **audit replay**.
- Index rebuilds are atomic snapshots: a query sees the old or the new effective set, never a mix.
- Kill-switch fallback: if the model server is down/slow, show keyword-search source pages with a banner within 3 s.
- Model version pinned; full regression suite reruns on any model/prompt/index/threshold change.
