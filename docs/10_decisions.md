# 10 · Decisions log

Short ADR-style record. Add a row whenever a design decision changes.

| # | Date | Decision | Why | Source |
|---|---|---|---|---|
| D1 | 2026-11-05 | Keep the accepted abstract; only "minor changes" in implementation | Abstract already shortlisted | User, data thread |
| D2 | 2026-11-05 | Pitch as a **trust layer for safety-critical SOPs**, not "multimodal RAG" | Retrieval/self-check parts are already published | Literature review |
| D3 | 2026-11-05 | **Local model**, hybrid edge-first deployment; inference < 15 s | Privacy, availability; user requirement | User, data plan |
| D4 | 2026-11-05 | Generator **Qwen2.5-VL-7B-Instruct AWQ on vLLM**, 24 GB GPU; 32B as comparison | Fits 15 s budget (est. 6–12 s) | Data plan |
| D5 | 2026-11-05 | Validate on **peer-reviewed public benchmarks**; MACH-Bench kept small (~100–250) and built with published counterfactual-edit method + real FAA AD supersessions | User worried a self-built dataset would be questioned | Data thread |
| D6 | 2026-11-05 | Qdrant for multi-vector; Postgres for registry/audit (not Cloud SQL for vectors) | pgvector lacks native late-interaction MaxSim | Build plan |
| D7 | 2026-11-05 | Layout parser (Docling/PyMuPDF) replaces DocLLM | No usable public DocLLM checkpoint | Build plan |
| D8 | 2026-11-05 | CRAG-style prompted grader instead of trained Self-RAG; RAGAS instead of ARES | Self-RAG/ARES need trained models | Build plan |
| D9 | 2026-11-05 | Only the router is trained this phase; fusion weights fit, thresholds calibrated; no generator fine-tune | Time; retrieval beats fine-tuning for new knowledge | Data plan |
| D10 | 2026-11-05 | Agents as an auditable state graph (LangGraph / Python), LLM proposes, code decides | Auditability, latency | Paper IV |
| D11 | 2026-11-06 | Narrow 3 novelty claims (supersession, benchmark, controlled-language drafting) | HoH, Morita, DesignQA, SOPRAG, Jonek & Manns found | IEEE/ACM pass |
| D12 | 2026-11-06 | Drafting claim = "under change control" (planted faults, safety-step survival); Becker's 4 criteria as rubric | Becker et al. 2026 read in full | Research thread |
| D13 | 2026-11-07 | PPT: 15 slides, template order, official challenge statement verbatim on slide 2; no extra sections beyond the template | User feedback | PPT thread |
| D14 | 2026-11-09 | Project folder `Documents\MACH framework`, Git + GitHub, Claude Code in Antigravity | User | This thread |

| D15 | 2026-11-09 | Dev PC has an NPU (no NVIDIA GPU) → **rented 24 GB cloud GPU VM** for dev + demo, same Docker Compose; architecture stays edge-first (self-hosted open weights, no cloud LLM API on the answer path) | vLLM needs CUDA | User |
| D16 | 2026-11-09 | Cloud GPU = **GCP `g2-standard-8`, 1 × L4 24 GB**, Mumbai if available (else Singapore), paid from GCP credits; setup in `docs/11_gcp_gpu_setup.md` | User has GCP credits | User |

## Open decisions

- UI: Streamlit (fast demo) vs Next.js (nicer, slower to build). Default: Streamlit.
- LangGraph vs plain Python state machine. Default: LangGraph if it doesn't fight the audit log.
