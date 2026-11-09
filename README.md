# M.A.C.H. Framework

**Multimodal Agentic Compliance & Heuristics for the Shop Floor** — a revision-safe, citation-grounded,
multimodal RAG assistant for SOPs and work instructions.

TECHgium 10th edition (L&T Technology Services) · PID TG0903606 · Challenge: *GenAI-Powered Intelligent
Manufacturing Knowledge Assistant for Shop Floor Operations*.

> **Status:** planning complete, code not started. This repo holds the design docs, all research so far,
> and an empty package skeleton. Every result number in the paper/PPT is still a placeholder.

## The idea in one line

An assistant that answers from the plant's own SOPs, diagrams and tables, cites the exact step it used,
refuses or calls an expert when unsure, and **never answers from a superseded revision**.

## Read in this order

1. [`CLAUDE.md`](CLAUDE.md) — one-page context and hard rules (also what Claude Code reads)
2. [`docs/01_overview.md`](docs/01_overview.md) — challenge statement, the 7 deliverables, how we meet them
3. [`docs/02_architecture.md`](docs/02_architecture.md) — system design and the 7 checks every answer passes
4. [`docs/03_agentic_design.md`](docs/03_agentic_design.md) — the agents, their graph and shared state
5. [`docs/04_datasets_and_benchmarks.md`](docs/04_datasets_and_benchmarks.md) — public datasets + MACH-Bench
6. [`docs/05_edge_vs_cloud.md`](docs/05_edge_vs_cloud.md) — hybrid, edge-first deployment decision
7. [`docs/06_evaluation_and_test_plan.md`](docs/06_evaluation_and_test_plan.md) — baselines, metrics, release gates, edge cases
8. [`docs/07_roadmap.md`](docs/07_roadmap.md) — build phases and first tasks
9. [`docs/08_tools_libraries_mcp.md`](docs/08_tools_libraries_mcp.md) — every tool, library, model, MCP server and plugin
10. [`docs/09_novelty_and_claims.md`](docs/09_novelty_and_claims.md) — 17 novelty ideas, safe wording, jury Q&A
11. [`docs/10_decisions.md`](docs/10_decisions.md) — decisions log (what changed from the abstract and why)

Research material is in [`research/`](research/README.md): the 12-page project brief, the
peer-reviewed literature review with five topic notes, the five planning docs (build plan, data/training/
deployment plan, explainer, paper draft, 55-case test plan) and the submitted presentation.

## Getting started (Windows + Antigravity + Claude Code)

```powershell
cd "$HOME\Documents\MACH framework"
git init -b main
git add .
git commit -m "Initial project scaffold, design docs and research"
```

Create an **empty private** repository on GitHub (no README, no .gitignore), then:

```powershell
git remote add origin https://github.com/<your-user>/mach-framework.git
git push -u origin main
```

Then open the folder in Antigravity, start the Claude Code terminal (`claude`), and it will pick up
`CLAUDE.md` automatically.

Python environment (once code starts):

```powershell
winget install astral-sh.uv        # or: pip install uv
uv venv --python 3.11
uv sync                            # installs from pyproject.toml
copy .env.example .env             # fill in values
```

GPU serving (vLLM) needs Linux: use WSL2 Ubuntu with the NVIDIA CUDA driver, or Docker Desktop with the
WSL2 backend. See `docs/08_tools_libraries_mcp.md` → *Environment*.

## Repo layout

```
MACH framework/
├── CLAUDE.md, README.md, pyproject.toml, .gitignore, .env.example, docker-compose.yml
├── docs/            design documents
├── research/        brief, literature review, planning docs, paper draft, PPT
├── src/mach/        package skeleton (ingestion, registry, retrieval, guard, router, generation,
│                    verify, abstain, escalation, drafting, agents, api, ui, audit)
├── baselines/       BM25 and text-only RAG baselines
├── eval/            metrics, benchmark loaders, MACH-Bench builder, edge-case fixtures
├── configs/         settings, hazard tiers, glossary
├── data/            raw/ and processed/ (gitignored)
├── scripts/         CLI entry points
└── tests/           unit tests (Revision Guard, access, number lock first)
```

## Key dates

- **12 Nov 2026, 11:59 PM IST** — presentation-round PPT deadline (15 slides max, 7 min talk + 5 min Q&A on Teams).
