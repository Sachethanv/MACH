# 08 · Tools, libraries, models, MCP servers and plugins

Everything the build needs. Versions are not pinned here; pin them in `pyproject.toml` / `uv.lock` when installing.
Items marked *(optional)* can wait.

## 1. Environment (Windows PC)

| Tool | Why |
|---|---|
| Git + GitHub account (private repo) | Version control |
| GitHub CLI `gh` *(optional)* | Create repo / PRs from the terminal |
| Antigravity IDE + **Claude Code** CLI | Coding environment (Claude Code reads `CLAUDE.md`) |
| Python 3.11 + **uv** | Fast env/dependency manager |
| **WSL2 (Ubuntu 22.04/24.04)** | vLLM and most GPU tooling need Linux |
| NVIDIA driver with WSL CUDA support (+ CUDA toolkit inside WSL) | GPU inference |
| **Docker Desktop** (WSL2 backend, GPU enabled) | Postgres, Qdrant, vLLM containers via `docker-compose.yml` |
| Node.js LTS *(optional)* | Only if we switch the UI to Next.js, and for some MCP servers (`npx`) |
| Poppler / Tesseract *(optional)* | PDF rasterising fallback / OCR fallback for scans |
| Ollama *(optional)* | Quick local LLM for dev without vLLM |

**Cloud GPU VM (for vLLM, embeddings, eval, demo):** Ubuntu 22.04 + NVIDIA driver + Docker + NVIDIA Container
Toolkit, 24 GB GPU (GCP L4 `g2-standard-8` or RunPod/Vast RTX 4090), ~150 GB persistent disk for weights and
indexes. Connect from the PC with SSH (port-forward the UI/API) or VS Code/Antigravity Remote-SSH. Because the
dev PC has an NPU and no NVIDIA GPU, WSL2 + CUDA below is only needed if you later get an NVIDIA card.

## 2. Models

| Role | Model | Notes |
|---|---|---|
| Generator (main) | **Qwen2.5-VL-7B-Instruct, AWQ 4-bit** | One 24 GB GPU, served by vLLM |
| Generator (bigger) | Qwen2.5-VL-32B-Instruct AWQ / Qwen3-VL-30B-A3B | 48 GB GPU; for the 7B-vs-32B result |
| Generator (cloud, offline/demo only) | Gemini via Vertex AI | Same interface; never on the plant answer path |
| Visual retriever | **ColQwen2.5** (or ColPali v1.x) from `vidore` on Hugging Face | Multi-vector page embeddings |
| Dense text embedder | **BGE-M3** (`BAAI/bge-m3`) | Multilingual (helps Hindi/Hinglish) |
| Reranker | **bge-reranker-v2-m3** (or jina-reranker-m0 multimodal) | Top-20 rerank |
| Router | DeBERTa-v3-small (or logistic regression on BGE-M3 embeddings) | The only model we train |
| Verifier (NLI) | an off-the-shelf NLI cross-encoder (e.g. a DeBERTa-v3 MNLI model) | Text entailment; values are exact-match |
| Judge (eval) | LLM from a different family than the generator | Validated on ≥ 100 human labels |
| Translation *(optional)* | IndicTrans2 or the generator itself | Hindi/regional queries; citations stay English |

## 3. Python libraries

| Area | Libraries |
|---|---|
| Parsing / layout | `docling`, `pymupdf` (PyMuPDF), `pdf2image`, `pillow`, `opencv-python-headless` (skew/blur checks) |
| Visual retrieval | `colpali-engine`, `byaldi` *(optional quick start)*, `qdrant-client` |
| Text retrieval | `rank-bm25`, `FlagEmbedding` (BGE-M3 + reranker), `sentence-transformers` |
| LLM serving / clients | `vllm` (in WSL/Docker), `openai` (vLLM's OpenAI-compatible API), `google-genai` / `google-cloud-aiplatform` *(optional)* |
| Agents | `langgraph`, `langchain-core` (only what LangGraph needs) |
| Structured output | `pydantic` v2, `jsonschema`; vLLM guided decoding / `outlines` *(optional)* |
| Units / numbers | `pint` (unit conversion for number lock) |
| Training | `transformers`, `datasets`, `peft` (retriever LoRA), `accelerate`, `scikit-learn` (router LR, calibration) |
| Conformal / stats | `numpy`, `scipy`, `statsmodels` (McNemar, Holm), `mapie` *(optional)* |
| Data / DB | `sqlalchemy`, `alembic`, `psycopg[binary]`, `pandas`, `pyyaml` |
| API / UI | `fastapi`, `uvicorn`, `streamlit`, `streamlit-pdf-viewer` or PDF.js for bbox highlight |
| Eval | `ragas`, `pytest`, `pytest-xdist`, `hypothesis` *(optional)*, `evaluate` |
| Security | `presidio-analyzer` / `presidio-anonymizer` (PII redaction in RCAs) |
| Observability | `structlog`, `opentelemetry-sdk` *(optional)*, `langfuse` *(optional, self-hosted)* |
| Dev quality | `ruff`, `mypy`, `pre-commit` |

## 4. Services (docker-compose)

| Service | Image | Use |
|---|---|---|
| PostgreSQL 16 | `postgres:16` | Registry, overlays, roles, audit log, approvals |
| Qdrant | `qdrant/qdrant` | Multi-vector (MaxSim) visual index + dense text vectors |
| vLLM | `vllm/vllm-openai` | Serves Qwen2.5-VL with the OpenAI-compatible API |
| API | local build | FastAPI app |
| UI | local build | Streamlit app |

## 5. Data sources and benchmarks

See [`04_datasets_and_benchmarks.md`](04_datasets_and_benchmarks.md). Access: Hugging Face Hub (`huggingface_hub`),
Federal Register / FAA DRS (ADs), NHTSA APIs, iFixit API, OSHA eTools.

## 6. MCP servers for Claude Code *(recommended, add as needed)*

Add with `claude mcp add …` (project scope writes `.mcp.json`). Check each server's README for the exact command.

| MCP server | Why | Priority |
|---|---|---|
| **GitHub** (official `github-mcp-server`) | Issues, PRs, reviews from Claude Code (or just use `gh`) | High |
| **Hugging Face** MCP | Search/inspect models and datasets (ColQwen, Qwen2.5-VL, benchmarks) | High |
| **Context7** (or similar docs server) | Up-to-date library docs for docling, colpali-engine, vLLM, LangGraph, Qdrant | High |
| **Postgres** MCP (read-only role) | Inspect registry/audit tables while debugging | Medium |
| **Qdrant** MCP (official `mcp-server-qdrant`) | Inspect collections / test queries | Medium |
| **Playwright** MCP | Drive the Streamlit UI for demo checks / screenshots | Low |
| alphaXiv, research-desk reference lookup (already connected in Claude) | Paper lookup and citation checks for the paper | Paper work |

Never give an MCP server write access to production data; use a read-only DB role.

## 7. Claude Code plugins / skills already used in this project

| Plugin / skill | Use here |
|---|---|
| **superpowers** (brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, requesting-code-review) | Default dev workflow: plan → TDD for the hard gates → verify |
| **engineering** (architecture, system-design, testing-strategy, code-review, deploy-checklist, documentation) | Design reviews, the security & deployment report |
| **research-desk** (citation-check, paper-critique, related-work) | Keep the paper's references verified |
| **research-superpowers** (literature-review, drafting-manuscript, requesting-peer-review) | Paper drafting and mock peer review |
| **education-agent-skills** | Used for the explainer / learning material (optional for code) |
| anthropic-skills **pptx / pdf / docx** | Slides, brief PDF, reports |
| **desktop-commander** | Local file / process access from Claude on this PC |
| `/code-review`, `/security-review`, `/simplify` (built-in) | Before each merge |

## 8. Cloud (optional, offline jobs / hosted demo)

GCP project with Vertex AI (Gemini), Cloud Run (hosted demo), Pub/Sub (escalation swap-in), Cloud Storage.
Not needed for the edge configuration.
