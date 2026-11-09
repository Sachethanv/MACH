# M.A.C.H. data, training and deployment plan

Nov 5, 2026 · @Sachethan

## Summary

This plan covers the three things the accepted abstract still needs before results can be filled in: where the data comes from, what has to be trained, and where the system should run. It keeps the five contributions in the abstract as they are.

**Data.** No public shop-floor SOP corpus with revisions exists, which is why MACH-Bench is a contribution. Build it from public-domain documents that already carry real revisions and supersession (FAA Airworthiness Directives, FAA handbooks and advisory circulars, NHTSA recall and service bulletins, iFixit guides with edit history, OSHA lockout/tagout material), then add controlled synthetic revisions on top. Use existing public benchmarks (ViDoRe, REAL-MM-RAG, MMDocIR, OHRBench, ALCE, RGB) only to check that each component works, not as the headline result.

**Training.** Almost everything runs off the shelf. Within the one-week deadline, train only the small four-way query router and fit (not train) the fusion weights and the conformal abstention thresholds. A LoRA adaptation of the visual retriever is the one optional fine-tune, and only if the dev set shows a gap. Do not fine-tune the generator LLM this week.

**Deployment.** Recommend a **hybrid, edge-first** design. Everything on the answer path runs on an on-premise GPU server in the plant. The cloud is used only for offline work: ingestion, synthetic data, training, calibration and work-instruction drafting. Safety answers then never depend on the internet connection, and SOPs and drawings never leave the plant. Make this a measured result in the paper by running the same pipeline with a local 7–8B model and with a cloud model.

## Update: validating on peer-reviewed public benchmarks

Every contribution except work-instruction drafting can be tested on public benchmarks that were published at peer-reviewed venues. Each one also comes with published baselines to compare against. This becomes the main evaluation. MACH-Bench shrinks to a small extra test of SOP revisions (see the end of this section).

| Abstract claim | Peer-reviewed public benchmark | Venue | What it shows |
| --- | --- | --- | --- |
| (1) Revision-safe answers under conflicting evidence | WikiContradict | NeurIPS 2024 Datasets & Benchmarks | Real contradictions between retrieved passages: does the system flag the conflict instead of blending the two? |
| (1) | ConflictBank | NeurIPS 2024 (confirm track) | Knowledge conflicts at scale, including outdated facts |
| (1) | FreshQA; SituatedQA; RealTime QA | Findings of ACL 2024; EMNLP 2021; NeurIPS 2023 D&B | Answers that change over time: does it pick the currently valid answer? |
| (2) Multimodal page retrieval | MMLongBench-Doc | NeurIPS 2024 D&B | Long PDFs with charts, tables and figures, including unanswerable questions |
| (2) | OHRBench | ICCV 2025 | Scanned and OCR-noisy pages against clean pages |
| (2) | SlideVQA; DocVQA; InfographicVQA; ChartQA; TAT-DQA | AAAI 2023; WACV 2021; WACV 2022; Findings ACL 2022; ACM MM 2022 | Reading slides, forms, diagrams, charts and tables |
| (2) | ViDoRe v1 | ColPali paper (venue still to confirm; cite as arXiv until then) | The standard visual-retrieval leaderboard, used to sanity-check the retriever |
| Technical manuals specifically | E-Manual QA (Samsung device manual) | Findings of EMNLP 2021 | Questions answered from a real product manual: the closest peer-reviewed match to SOPs |
|  | TechQA | ACL 2020 | Technical-support questions answered from technical documents |
|  | IKEA-Manual | NeurIPS 2022 D&B | Step-by-step assembly diagrams |
| (3) Citations and attribution | ALCE (ASQA, QAMPARI, ELI5) | EMNLP 2023 | Citation precision and recall, with official scoring code |
| (3) | RAGTruth | ACL 2024 | Hallucination labels at the span level |
| (4) Abstention and robustness | RGB | AAAI 2024 | Refusing when the answer is missing, and resisting wrong context |
| (4) | CRAG | NeurIPS 2024 D&B | Accurate / missing / hallucinated scoring with a penalty for hallucination |
| (4) | SQuAD 2.0 | ACL 2018 | Unanswerable questions |
| (4) Four-way router | MuSiQue; HotpotQA; 2WikiMultiHopQA; NQ; TriviaQA | TACL 2022; EMNLP 2018; COLING 2020; TACL 2019; ACL 2017 | The exact setup of Adaptive-RAG (NAACL 2024), so router accuracy and speed compare directly to a published result |
| Shop-floor photos (optional) | MMAD; IndustReal | ICLR 2025; WACV 2024 | Industrial defect questions and procedure-step errors |
| (5) Drafted work instructions | None exists |  | Stays a human review with seeded faults, as in the abstract |

### Minimal suite for one week

Running all of these is too much for one week. Use this set and sample 200–500 items from each so the runs finish in hours:

1. **MMLongBench-Doc** and **SlideVQA** for multimodal retrieval and answering.
2. **E-Manual QA** for manual-style questions.
3. **ALCE-ASQA** for citation quality.
4. **RGB** for abstention and robustness to wrong context.
5. **WikiContradict** for conflicting evidence.
6. **MuSiQue + HotpotQA** subsets for the router, against Adaptive-RAG.

Compare each against the baselines already in the plan (BM25 + LLM, dense text RAG, hybrid), using the same local generator for all.

### What happens to MACH-Bench

No public benchmark tests SOP revisions, so the revision claim still needs a small test of its own. Keep it small and easy to defend, at about 100 items:

- **Real supersession pairs** from FAA Airworthiness Directives. Nobody invents these: the FAA itself states which directive replaces which and when, so the gold answer comes from the regulator.
- **Scripted edits** (a changed torque value, an added safety step, swapped steps), produced by a published script with a logged changelog, so anyone can regenerate it.

This is how RGB, CRAG, FreshQA and ALCE were made: their authors built them, documented the process and released the data. Reviewers accept that when the process is open. If you would rather not claim "the first public benchmark", a minor rewording of contribution (2) to "a small, reproducible supersession test suite" keeps the abstract intact.

**How the revision test rests on peer-reviewed methods.** (1) Test the behaviour first on peer-reviewed proxies: WikiContradict for conflicting documents, and FreshQA and SituatedQA for answers that change over time. (2) Build the SOP edits with the counterfactual-editing method of RGB (AAAI 2024) and Xie et al. (ICLR 2024), which ConflictBank (NeurIPS 2024) also uses at scale, and cite it as the method. (3) Check the results against 30–50 real FAA supersession cases, where the regulator states the answer. Two annotators label a sample, we report Cohen's κ, and we publish the script.

## Update: local model and the 15-second budget

**Model choice.** For the demo, run **Qwen2.5-VL-7B-Instruct (4-bit AWQ)** with vLLM on one 24 GB GPU (RTX 4090 class), with ColQwen2.5 retrieval on the same card. If a 48 GB GPU is available (RTX 6000 Ada or L40S class), use **Qwen2.5-VL-32B-Instruct (AWQ)** for stronger answers, or **Qwen3-VL-30B-A3B**. That second model is a mixture-of-experts with about 3B active parameters, so it is far faster than its size suggests. Since everything must run locally, the earlier cloud-versus-local experiment becomes **7B against 32B local**. Running both shows whether the bigger model is worth its latency.

**Latency budget (estimates to be measured on the real box):**

| Stage | Expected time |
| --- | --- |
| Encode the query and search the precomputed page index | under 0.5 s |
| BM25, dense and part-number match, then fusion | under 0.3 s |
| Rerank the top 20 | 0.5–1.5 s |
| Revision filter | negligible (metadata lookup) |
| Generator reads 3–4 page images | 1–3 s |
| Generator writes about 300 tokens (7B, 4-bit) | 3–6 s |
| Step-support and revision-coherence checks | 0.5–1.5 s |
| **Single-retrieval answer** | **about 6–12 s** |

Multi-hop questions are the risk. Cap them at two retrieval rounds, and stream the first steps to the screen while the rest generates. Escalations go to an expert in the background, so they do not count against the 15 seconds.

**What keeps it under 15 s:** compute every page embedding and figure caption offline at ingestion; cap image resolution and send at most 3–4 pages; keep all models loaded and warm; cache the fixed system prompt; ask for short, structured output. Report p50 and p95 latency over the whole test set, plus the share of queries answered in under 15 seconds.

## 1. Public datasets

### 1a. Source documents for the MACH-Bench corpus

These are the documents M.A.C.H. retrieves from. The best sources are ones that already contain real revisions, because they make the supersession traps credible to reviewers.

| Source | What it gives M.A.C.H. | Revisions / supersession | Licence and caveats |
| --- | --- | --- | --- |
| FAA Airworthiness Directives (Federal Register, FAA DRS) | Mandatory maintenance actions with steps, part numbers, applicability by model and serial range, compliance times | **Explicit**: each superseding AD states "This AD supersedes AD 20XX-YY-ZZ" and gives an effective date. Ready-made ground truth | US government work, public domain |
| FAA handbooks and advisory circulars (e.g. AMT handbooks, AC 43.13-1B) | Long, diagram-heavy maintenance manuals with torque tables and figures | Some ACs have lettered revisions and change pages | Public domain |
| NHTSA recalls, technical service bulletins and manufacturer communications | Automotive repair procedures and service bulletins | Bulletins are often superseded by later ones | Public; check each manufacturer document before redistribution |
| iFixit repair guides (API) | Step-by-step procedures with one or more photos per step, tools and parts lists | Guides keep an edit history, so real step-level changes exist | CC BY-NC-SA: fine for academic use, cite and keep non-commercial |
| IKEA-Manual (NeurIPS 2022 Datasets & Benchmarks) | Assembly manuals with diagrams aligned to individual steps and 3D parts | None; use as the diagram-only stratum | Research licence; check terms |
| OSHA eTools and lockout/tagout (LOTO) material | Safety steps, PPE and energy-isolation procedures | Occasional updates | Public domain. Use it to seed safety steps into synthetic SOPs |
| US Army / DoD technical manuals marked "Distribution A" | Real maintenance manuals with numbered "Change" pages | Real change pages that replace earlier pages | Public only when marked Distribution A; check each manual |

### 1b. Benchmarks for checking components

These test each part of the system against published numbers. They do not include SOP revisions, so they cannot replace MACH-Bench.

| Benchmark | Used to check | Note |
| --- | --- | --- |
| ViDoRe v1/v2/v3 (Hugging Face `vidore`) | The visual page retriever (ColPali/ColQwen) | v3 is an arXiv preprint covering enterprise domains; confirm which subsets are industrial before citing |
| REAL-MM-RAG (IBM, arXiv 2502.12342) | Retrieval on technical reports and slides with rephrased queries | Has `TechReport` and `TechSlides` subsets, the closest public match to manuals |
| MMDocIR | Page and layout-level retrieval over long documents | Has an industry/admin domain |
| OHRBench (ICCV 2025) | The scanned-versus-born-digital comparison and OCR noise | Supports reporting the two strata separately |
| DocVQA, InfographicVQA, ChartQA, TAT-DQA | Generator reading of tables, charts and forms | Small samples are enough for sanity checks |
| ALCE, RAGTruth, RGB, CRAG | Citation precision/recall, hallucination labels, refusal and counterfactual robustness | Use their metric code; RGB's design informs the unanswerable and trap items |

### 1c. Industrial images and shop-floor photos

These support query-by-photo, which the literature review flagged as untested. Treat it as an extra, not a core claim.

| Dataset | Content |
| --- | --- |
| MVTec AD, VisA, MVTec LOCO | Photos of industrial parts with defects |
| MMAD (ICLR 2025) | A benchmark of multimodal LLMs on industrial anomaly questions built on the sets above |
| IndustReal (WACV 2024) | Egocentric video of an assembly procedure, with step labels and execution errors |
| Assembly101, HA-ViD | Assembly videos with step annotations |

### 1d. Maintenance logs and root-cause analysis text

These give realistic operator language for queries and the material for the expert-note and escalation path.

| Dataset | Content | Note |
| --- | --- | --- |
| MaintNet (COLING 2020 demo) | Maintenance logbooks from aviation, automotive and facilities, with NLP tools | Short, noisy free text, good for writing realistic queries |
| FAA Service Difficulty Reports, NASA ASRS | Free-text failure and incident reports | Public; use to write "symptom → which procedure?" queries |
| NHTSA complaints | Owner-reported failures linked to vehicle models | Pairs with the NHTSA bulletins above for multi-hop queries |
| TechQA (IBM, ACL 2020) | Technical-support questions answered from technical notes | Text only; useful for the router's training data |
| AssetOpsBench (IBM, arXiv 2506.03828) | Agent tasks for industrial asset operations and maintenance | Preprint; useful as a second agentic test if time allows |

## 2. Assembling MACH-Bench v0

### Scope

Aim for 3 product families (for example a small aircraft system from FAA material, a vehicle system from NHTSA material, and a consumer device from iFixit), about 40–60 documents and 1,500–3,000 pages. At least 15 documents should have two or more revisions. Mark every page as scanned or born-digital. Freeze the snapshot and record a SHA-256 hash for each file.

### Metadata for every document and element

Each document gets `doc_id`, `revision`, `effective_from`, `effective_to`, `supersedes`, `applicability` (model, serial range, plant), `status` (released, draft, temporary deviation) and `source_licence`. Parsing (Docling or a similar layout parser) splits each page into elements with stable IDs: `doc:rev:page:step`, `figure`, `table` and `warning`. These element IDs are what the generator cites, which is contribution 3 in the abstract.

### Synthetic revisions and conflicts

Real revisions are too few to test every failure, so generate controlled ones. For each base document, a script makes a new revision with one or more labelled edits and re-renders it with the same layout:

| Edit type | Example | Failure it tests |
| --- | --- | --- |
| Parameter change | Torque 25 N·m becomes 30 N·m | Citing the superseded value |
| Inserted safety step | A new LOTO or PPE step before step 4 | Safety-step recall |
| Reordered steps | Steps 6 and 7 swapped | Order fidelity (Kendall τ) |
| Tool or part change | Part number or tool ID replaced | Exact-match on identifiers |
| Deleted step | An obsolete step removed | Answering with a step that no longer exists |
| Scoped deviation | Temporary change for serials 1001–1200, expiring on a date | Applicability and expiry filtering |
| Engineering change notice | A separate notice that changes one step of one document | Cross-document supersession |
| Conflict | Work instruction and SOP disagree on one value | Detecting the conflict and escalating |

Every edit is written to a changelog, so the gold answer for each revision is known. For the scanned stratum, rasterise a share of the pages and add scan noise (skew, blur, JPEG artefacts). Real revisions from FAA ADs and iFixit edit history form a separate "real supersession" subset, so the paper can show the results are not an artefact of synthetic edits.

### The question set

Aim for 250–300 queries plus 20–40 drafting tasks, in line with the literature review's protocol.

| Share | Query type |
| --- | --- |
| \~25% | Single lookups (a value, tool or part) |
| \~20% | Full procedures (ordered steps) |
| \~15% | Diagram or table evidence only |
| \~10% | Multi-hop or cross-document (log symptom → procedure → torque table) |
| \~10% | Superseded-revision traps (the answer differs between revisions) |
| \~5% | Mixed-revision and conflict traps |
| 10–15% | Unanswerable from the corpus |

An LLM proposes questions from each element and the team edits them. Rewrite a share in operator language using MaintNet and FAA reports as the style guide. Gold labels give the answer, every supporting element ID, the ordered steps and the critical values. Two annotators label at least 25% of items and report Cohen's κ. Split 30/70 into dev and test, and tune only on dev. For the drafting tasks, seed known faults (a wrong value, a missing safety step, a swapped order) for the blinded review in contribution 5.

If LTTS or a partner plant can share even 5–10 real SOPs under NDA, keep them as a private held-out test and report them separately. This is the strongest answer to the question "does it work on real plant documents?"

### Release

Publish only the public-domain material, the synthetic revisions, the questions and the scripts. Link to iFixit guides and other non-redistributable items instead of copying them.

## 3. What to train and what to use off the shelf

| Component | Choice | Train? | Effort |
| --- | --- | --- | --- |
| Layout parsing and element IDs | Docling (or similar) plus rules for step numbering | No | Engineering |
| Visual page retriever | ColQwen2.5 / ColPali checkpoints from `vidore` | Optional LoRA (below) | 0 or about half a day |
| Text retrieval | BM25 plus BGE-M3 dense; exact matcher for part, tool and SOP numbers by regex | No | Engineering |
| Reranker | bge-reranker-v2-m3, or a multimodal reranker such as jina-reranker-m0 | No | 0 |
| Fusion weights | Weighted reciprocal-rank fusion | **Fit** by grid search on dev | 1–2 hours |
| Revision filter and revision-coherence check | Deterministic code over the metadata | No; it is code, which is what makes it auditable | Engineering |
| Four-way router (direct lookup, single retrieval, multi-hop, escalate) | Small classifier, e.g. logistic regression on embeddings or DeBERTa-v3-small | **Yes** | A few hours on one GPU |
| Generator | Qwen2.5-VL-7B or a similar 7–8B open VLM, 4-bit, with a JSON output schema that forces element-ID citations | No this week | 0 |
| Step-support checker | Off-the-shelf NLI model, or the VLM as a checker | Optional | 0 |
| Abstention and escalation thresholds | Conformal calibration per safety tier on the dev split | **Calibrate**, no gradient training | 1–2 hours |
| Judge | An LLM from a different model family, checked against ≥100 human labels | No | Human labelling time |

### Training plan for the router

Build 1,500–3,000 labelled queries automatically. Questions generated from a single element are labelled "direct" or "single". Questions built by chaining two elements are "multi-hop". Questions with no answer in the corpus, or that touch a high-criticality step with weak evidence, are "escalate". Add TechQA and MaintNet-style rewrites for variety. Train, then report accuracy on the human-written test queries. The literature review notes that Adaptive-RAG's router was only 54.5% accurate, so reporting router accuracy is itself useful.

### Optional LoRA for the visual retriever

Do this only if ColQwen on the dev set falls well short of BM25 on identifier-heavy pages or of its ViDoRe numbers. Generate 5,000–10,000 (page, synthetic query) pairs from the corpus. Use **other revisions of the same page as hard negatives**, which teaches the retriever to tell Rev B from Rev C. That is a small, defensible twist on standard practice. One epoch of rank-32 LoRA should fit on a single 24–48 GB GPU in a few hours (an estimate; measure it). Never train on test-split documents.

### Left for after the deadline

Trust-Align-style fine-tuning of the generator for citations and refusals, and training element-level visual grounding. Both are listed in the literature review as strong future work, and both need more data and time than one week allows.

### Suggested week

| Day | Work |
| --- | --- |
| 1 | Download and freeze the sources; parse to elements; metadata schema |
| 2 | Synthetic revision script; real-revision subset; start question generation |
| 3 | Finish questions and double annotation; run baselines 1–4 (BM25, BM25 + LLM, dense text RAG, hybrid) |
| 4 | Full M.A.C.H.; train the router; fit fusion and conformal thresholds on dev |
| 5 | Test-split evaluation, ablations, latency runs on the edge box and the cloud model |
| 6–7 | Drafting review with seeded faults; fill in \[R1\]–\[R10\]; write up |

## 4. Edge, cloud or hybrid

### How the options compare

| Factor | Edge (on-premise in the plant) | Cloud | Hybrid, edge-first |
| --- | --- | --- | --- |
| Latency | No network round trip; a 7–8B 4-bit VLM on one modern GPU should give a few seconds per answer (to be measured) | Fast large models, but adds WAN latency and depends on the link | Answer path is local; slow work runs in the background |
| Availability | Works when the internet is down, including night shifts | Fails when the link fails | Safety answers never depend on the link |
| Privacy and IP | SOPs, drawings and logs stay in the plant | Proprietary and possibly export-controlled documents leave the site | Only redacted or non-sensitive data goes to the cloud, and only offline |
| OT network rules | Fits segmented plant networks (IEC 62443 zones) with no inbound internet | Needs an approved outbound path from the shop floor | Only the central IT zone talks to the cloud |
| Answer quality | Limited by a 7–8B model | Best models | Local model for answers, cloud model for drafting and data generation |
| Cost | One-time server cost plus power | Pay per query, which grows with users and shifts | Capex for one server plus small cloud bills for offline jobs |
| Operations | The plant must maintain a GPU server | The vendor maintains it | Both, but the cloud part is non-critical |

### Recommendation

Use the **hybrid, edge-first** design. The deciding factors are privacy and availability, not cost. A shop floor needs an answer when the link is down, and the abstract's own claim, never cite a superseded revision, is easiest to audit when the index, filter and model all sit inside the plant's change-controlled environment.

| Runs on the plant server | Runs in the cloud or central data centre, offline |
| --- | --- |
| Document index, all three retrievers, reranker, revision filter, router, 7–8B VLM generator, step checker, abstention, escalation tickets | Bulk captioning of figures at ingestion, synthetic question generation, router and LoRA training, conformal recalibration when SOPs change, drafting of work instructions under change control |

### Hardware tiers

| Tier | Hardware | Use |
| --- | --- | --- |
| TechiGum demo | One workstation with a 24 GB GPU (RTX 4090 class) | Fits ColQwen2.5, the reranker and a 4-bit 7B VLM together |
| Plant pilot | One rack server with a 48 GB GPU (L40S class) or two 24 GB inference GPUs | One line or one plant, with headroom for concurrent users |
| Line-side embedded | Jetson AGX Orin 64 GB class | Possible for a single station but slower; not recommended as the main server |

Operators use tablets or line-side terminals as thin clients over the plant network. Throughput and concurrency numbers above are estimates: measure p50/p95 latency on the demo box and report it as \[R10\].

### Cost: how to make the case

Do not quote prices from memory. Compute a break-even: monthly cloud cost = queries per day × 30 × tokens per query × price per token, compared with the server cost spread over three years plus power. A query with several page images costs thousands of input tokens, so per-query cloud cost grows fast with image-heavy retrieval. Put the current prices into this formula when writing the paper.

### Make it a result, not just an opinion

Run the same M.A.C.H. pipeline twice on the MACH-Bench test split: once with the local 4-bit 7–8B VLM on the demo box, once with a cloud frontier model as the generator. Report accuracy, superseded-citation rate, safety-step recall and p50/p95 latency for both. If the local model is close on the revision and safety metrics, which should hold because the filter and checks are deterministic, that is direct evidence for edge-first deployment.

## 5. Minor changes to the abstract

These keep the accepted abstract intact and only make it match the plan.

1. After introducing MACH-Bench, add that it is built from public-domain maintenance and regulatory documents with real and controlled synthetic revisions.
2. Add one sentence on deployment: M.A.C.H. runs on a single on-premise GPU server, with cloud use limited to offline ingestion and training.
3. Keep the p95 latency placeholder \[R10\] and state that it is measured on the edge configuration.

## 6. Risks

| Risk | Mitigation |
| --- | --- |
| Synthetic revisions are easier than real ones | Report the real-revision subset (FAA ADs, iFixit history) separately |
| Public documents are not shop-floor SOPs | Say so in limitations; add the private NDA test set if LTTS can provide one |
| Licences block redistribution | Release scripts and links for non-public-domain items |
| A 7B model is too weak for multi-hop queries | Report the cloud-generator run; the router can escalate multi-hop queries instead |
| One week is tight | Drop the retriever LoRA and query-by-photo first; keep the revision-safety results, which are the main claim |
