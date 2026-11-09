# 04 · Datasets and benchmarks

Full detail: [`research/planning_docs/02_data_training_deployment_plan.md`](../research/planning_docs/02_data_training_deployment_plan.md).

**Strategy.** Every claim except work-instruction drafting is validated on **peer-reviewed public benchmarks**
with published baselines (reviewers can't question how that data was built). Only SOP revisions have no public
benchmark, so we add a small, reproducible **MACH-Bench** built with a published method (counterfactual edits,
as in RGB / Xie et al. / ConflictBank) and checked against **real FAA supersessions**.

Rules: public test splits are **evaluation only, never tuning**. Sample 200–500 items per benchmark so runs
finish in hours. Use official scoring code where it exists. Note licences (SlideVQA etc. are research-only).

## A. Public benchmarks (evaluation)

| Claim | Benchmark | Venue | What it tests |
|---|---|---|---|
| Revision-safe answers / conflicts | **WikiContradict** | NeurIPS 2024 D&B | Real contradictions between retrieved passages |
| | ConflictBank | NeurIPS 2024 | Knowledge conflicts at scale incl. outdated facts |
| | **FreshQA**; SituatedQA; RealTime QA | Findings ACL 2024; EMNLP 2021; NeurIPS 2023 D&B | Picking the currently valid answer |
| Multimodal page retrieval | **MMLongBench-Doc** | NeurIPS 2024 D&B | Long PDFs with charts/tables/figures + unanswerables |
| | OHRBench | ICCV 2025 | Scanned/OCR-noisy vs clean pages |
| | **SlideVQA**; DocVQA; InfographicVQA; ChartQA; TAT-DQA | AAAI 2023; WACV 2021/22; Findings ACL 2022; ACM MM 2022 | Reading slides, forms, diagrams, charts, tables |
| | ViDoRe v1 (+v2/v3) | ColPali paper (venue to confirm) | Visual retriever sanity check |
| Technical manuals | **E-Manual QA** (Samsung manual) | Findings EMNLP 2021 | Closest peer-reviewed match to SOPs |
| | TechQA | ACL 2020 | Tech-support Q from technical docs |
| | IKEA-Manual | NeurIPS 2022 D&B | Step-by-step assembly diagrams |
| Citations | **ALCE (ASQA, QAMPARI, ELI5)** | EMNLP 2023 | Citation precision/recall, official code |
| | RAGTruth | ACL 2024 | Span-level hallucination labels |
| Abstention / robustness | **RGB** | AAAI 2024 | Negative rejection, counterfactual robustness |
| | CRAG (Meta) | NeurIPS 2024 D&B | Accurate/missing/hallucinated scoring |
| | SQuAD 2.0 | ACL 2018 | Unanswerable questions |
| Router | **MuSiQue + HotpotQA** (+2WikiMultiHopQA, NQ, TriviaQA) | TACL 2022; EMNLP 2018 | Exact Adaptive-RAG (NAACL 2024) setup → direct comparison |
| Shop-floor photos (optional) | MMAD; IndustReal; MVTec AD/LOCO, VisA | ICLR 2025; WACV 2024 | Industrial defect Qs; procedure-step errors |
| Drafted WIs | none exists | — | Human review with seeded faults (our C5) |

**Minimal one-week suite:** MMLongBench-Doc + SlideVQA, E-Manual QA, ALCE-ASQA, RGB, WikiContradict,
MuSiQue + HotpotQA subsets (+ FreshQA). Compare against the same baselines with the same local generator.

Most are on Hugging Face or authors' GitHub. Loaders go in `eval/benchmarks/`.

## B. Source documents for the MACH-Bench corpus

| Source | Gives | Revisions / supersession | Licence |
|---|---|---|---|
| **FAA Airworthiness Directives** (Federal Register, FAA DRS) | Mandatory maintenance actions, part numbers, applicability by model + serial range | **Explicit**: "This AD supersedes AD 20XX-YY-ZZ" + effective date → regulator-given ground truth | Public domain |
| FAA handbooks / Advisory Circulars (AMT handbooks, AC 43.13-1B) | Diagram-heavy manuals with torque tables | Lettered revisions, change pages | Public domain |
| NHTSA recalls + technical service bulletins | Automotive repair procedures | Bulletins superseded by later ones | Public; check manufacturer docs |
| iFixit guides (API) | Step-by-step with photos, tools, parts | Edit history = real step-level changes | CC BY-NC-SA (academic OK, link don't copy) |
| OSHA eTools + LOTO material | Safety steps, PPE, energy isolation | Occasional | Public domain — seed safety steps |
| US Army / DoD TMs marked "Distribution A" | Real maintenance manuals | Numbered Change pages | Public only if Distribution A |
| MaintNet; FAA SDRs; NASA ASRS; NHTSA complaints | Realistic operator language, symptom→procedure queries | — | Public |

## C. MACH-Bench v0 (our benchmark)

- **Scope:** 3 product families (e.g. FAA aircraft system, NHTSA vehicle system, iFixit device), 40–60 docs,
  1,500–3,000 pages, ≥ 15 docs with ≥ 2 revisions; pages tagged scanned vs born-digital; frozen snapshot with
  SHA-256 per file.
- **Metadata per doc:** `doc_id, revision, effective_from, effective_to, supersedes, applicability (model,
  serial range, plant), status (released/draft/temporary deviation), source_licence`.
- **Scripted counterfactual revisions** (each logged in a changelog → known gold):

| Edit | Example | Tests |
|---|---|---|
| Parameter change | 25 N·m → 30 N·m | citing superseded value |
| Inserted safety step | new LOTO/PPE step before step 4 | safety-step recall |
| Reordered steps | swap 6 and 7 | order fidelity (Kendall τ) |
| Tool/part change | part number replaced | exact match on IDs |
| Deleted step | obsolete step removed | answering with a removed step |
| Scoped deviation | serials 1001–1200 until date | applicability + expiry |
| ECN | separate notice changes one step | cross-document supersession |
| Conflict | WI vs SOP disagree on a value | conflict detection + escalation |

- **Real-supersession subset:** 30–50 FAA AD chains (+ iFixit history), reported separately to show results
  aren't an artefact of synthetic edits.
- **Question mix (~250–300 queries + 20–40 drafting tasks):** ~25% single lookups · ~20% full procedures ·
  ~15% diagram/table-only · ~10% multi-hop · ~10% superseded-revision traps · ~5% mixed-revision/conflict traps
  · 10–15% unanswerable (+ unsafe asks). ~36% are traps.
- **Labels:** gold answer, all valid evidence element IDs (multi-gold), expected behaviour (answer/abstain/
  clarify/refuse/escalate), ordered steps, critical values. Two annotators on ≥ 25%, report Cohen's κ.
  Someone with plant experience reviews the set ("expert-authored question set").
- **Split:** 30% dev (tuning prompts, fusion weights, thresholds) / 70% test touched once.
- **Private set (if possible):** 5–10 real LTTS SOPs under NDA as a held-out test, reported separately.
- **Release:** public-domain material, synthetic revisions, questions and scripts; links for non-redistributable items.

## D. What gets trained vs used off the shelf

| Component | Choice | Train? |
|---|---|---|
| Layout parsing + element IDs | Docling + step-numbering rules | No |
| Visual retriever | ColQwen2.5 / ColPali (`vidore` checkpoints) | Optional LoRA (rank 32, 1 epoch) only if dev shows a gap; **other revisions of the same page as hard negatives** |
| Text retrieval | BM25 + BGE-M3 + ID regex | No |
| Reranker | bge-reranker-v2-m3 (or jina-reranker-m0 multimodal) | No |
| Fusion weights | weighted RRF | **Fit** by grid search on dev (1–2 h) |
| Revision filter + coherence check | deterministic code | No (that's what makes it auditable) |
| Router | DeBERTa-v3-small / LR on embeddings | **Yes** — a few hours on one GPU; 1.5–3k auto-labelled queries (+TechQA, MaintNet-style rewrites). Report its accuracy (Adaptive-RAG's was only 54.5%) |
| Generator | Qwen2.5-VL-7B AWQ, JSON schema | **No fine-tuning** (Trust-Align-style tuning is future work) |
| Step-support checker | off-the-shelf NLI or the VLM | Optional |
| Abstention thresholds | split-conformal per tier on dev | **Calibrate** (1–2 h) |
| Judge | LLM from a different family, validated on ≥ 100 human labels | No |
