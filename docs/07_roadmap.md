# 07 · Roadmap

Principle: **a working end-to-end slice matters more than any single component. Build thin, then deepen.**

## Where we are (9 Nov 2026)

- [x] Abstract accepted / shortlisted (PID TG0903606)
- [x] Peer-reviewed literature review (+ IEEE/ACM/ScienceDirect early-access pass, Becker et al. read)
- [x] Project brief PDF (12 pages), explainer, data/training/deployment plan, paper draft (IEEE layout,
      results are placeholders [R1]–[R10]), 55-case test plan
- [x] Presentation-round PPT (15 slides) — due **12 Nov, 11:59 PM IST**; team names/photos/college still to add
- [ ] Code: nothing yet. This repo is the starting point.

## Phases (≈ 8 weeks; adjust once the next-round timeline is known)

| Phase | Weeks | Exit criteria |
|---|---|---|
| 0. Repo, corpus, gold set | 1–2 | Dev env works (WSL2/Docker + GPU); 40+ docs with revisions and planted conflicts; registry schema; 60+ gold questions (target ~250) |
| 1. Baselines | 2–3 | B1–B4 answer the gold set; eval script prints a results table |
| 2. Multimodal retrieval + citations | 3–5 | ColQwen2.5 + hybrid fusion; element-ID citations with bbox highlight in UI |
| 3. Trust layer | 5–6 | Revision Guard, coherence check, number lock, grader, conflict detector, tiered gate, expert inbox |
| 4. WI drafting workflow | 6–7 | RCA → draft → compliance → approval → new revision |
| 5. Eval, report, demo | 7–8 | Full results table + ablations, public-benchmark runs, timed user study, security & deployment report, 3-min demo video |

**End-to-end slice by week 3.**

## First tasks for Claude Code (in order)

1. `uv` project + `pyproject.toml` deps; `docker-compose.yml` with Postgres + Qdrant; health checks.
2. `registry/` Postgres schema + migrations (documents, revisions, elements, supersessions, overlays, roles,
   audit_log, escalations, expert_notes, drafts, draft_transitions, corpus_snapshots).
3. **Tests first** for `guard/`: effective set E(c), coherence check, deviation overlay + expiry, plant-time-zone
   boundary, withdrawn/reinstated revision. Then implement.
4. `ingestion/` for one PDF: Docling → elements with IDs + bboxes + page images; criticality rules.
5. `retrieval/` BM25 + ID lane; then dense (BGE-M3); then visual (ColQwen2.5 → Qdrant).
6. `generation/` vLLM client + JSON schema; `verify/` number lock + validity.
7. `api/` FastAPI `/ask`, `/escalations`, `/drafts`; `ui/` Streamlit operator view with highlighted citation.
8. `baselines/` B1–B4 and `eval/` metrics + MACH-Bench loader + edge-case harness.
9. Script `eval/mach_bench/build.py`: download FAA ADs, freeze, hash, scripted counterfactual edits + changelog.

## Seven-day PPT plan (already used; kept for reference)

Day 1 corpus + schema · Day 2 synthetic revisions + questions · Day 3 baselines · Day 4 full M.A.C.H., router,
fusion + thresholds · Day 5 test split, ablations, latency · Day 6–7 drafting review with seeded faults, fill
[R1]–[R10], write-up. If time runs out, drop the retriever LoRA and query-by-photo first; keep the revision-
safety results, which are the main claim.

## Suggested team split (3–4 people)

- **Data & eval:** corpus, gold set, metrics, user study
- **Retrieval:** parsing, ColQwen, hybrid search, Revision Guard filters
- **LLM & agents:** answer schema, grader, abstention, drafting workflow
- **App & infra:** UI, approval inbox, RBAC, deployment, security report

## Risks

| Risk | Mitigation |
|---|---|
| Synthetic revisions easier than real | Report FAA AD / iFixit real subset separately |
| Public docs aren't shop-floor SOPs | Say so; add private NDA set if LTTS provides one |
| Licences block redistribution | Release scripts + links |
| 7B too weak for multi-hop | Report 32B run; router can escalate multi-hop |
| No NVIDIA GPU on dev PC (NPU only) | Rented 24 GB cloud GPU VM for GPU work and the demo; local PC for code + unit tests; stop the VM when idle |
| One week is tight | Revision safety first; photo query and LoRA last |
