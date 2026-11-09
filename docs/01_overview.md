# 01 · Overview: challenge, deliverables, and what M.A.C.H. is

## The official challenge statement (LTTS, TECHgium 10)

**Title:** GenAI-Powered Intelligent Manufacturing Knowledge Assistant for Shop Floor Operations · Manufacturing

> Develop a multimodal manufacturing knowledge assistant for one production line using a governed corpus of
> SOPs, work instructions, annotated equipment images, quality alerts, and maintenance/RCA reports. The system
> shall answer operator questions, retrieve procedures from images or text, and draft a change-controlled work
> instruction. Every statement must cite the exact source document, page/section, image region where
> applicable, and revision date. It must detect superseded documents, abstain when evidence is missing or
> conflicting, and route high-risk answers for expert approval. Compare with keyword search and a basic
> text-only RAG baseline on a fixed expert-authored question set.

**Deliverables (scored by the jury):**

1. Versioned multimodal corpus with access controls, metadata, and expert question/answer set.
2. Text, table, and image ingestion with revision and supersession handling.
3. Multimodal retrieval and answer generation with sentence-level citations and confidence.
4. Abstention, conflicting-source detection, freshness checks, and expert escalation.
5. Draft work-instruction workflow with change control and approval.
6. Evaluation versus keyword and text-only RAG using answer correctness, citation precision, retrieval recall,
   abstention quality, freshness accuracy, latency, and expert time saved.
7. Security and deployment report.

## Our submitted (accepted) abstract

> **The M.A.C.H. Framework: Multimodal Agentic Compliance & Heuristics for the Shop Floor.**
> Factory floors lose up to 30% of productivity because operators cannot find the right SOPs, ECNs, or RCA
> reports. Standard text-only LLMs fail here by hallucinating, which poses critical safety risks. To solve
> this, we are building a Vision-Native, Multi-Agent Knowledge Assistant for LTTS's Mobility verticals,
> prioritizing exact traceability and verifiable change control.
>
> We bypass brittle OCR. Our multimodal ingestion pipeline embeds document page images directly using ColPali
> late interaction and DocLLM spatial attention. This preserves complex layouts, tabular data, and annotated
> schematics, storing embeddings in Cloud SQL. For industrial auditability, we integrate Self-RAG and CRAG
> protocols to force self-evaluation of retrievals. The system outputs verifiable, sentence-level citations
> mapped exactly to document IDs, pages, and visual bounding boxes.
>
> Because ECNs change constantly, our temporal reasoning engine tracks strict versioning histories to flag
> superseded procedures. When data conflicts occur or confidence drops, our epistemic abstention policy
> triggers. Instead of guessing, the system routes out-of-scope queries to human experts via Pub/Sub.
>
> Workflow execution relies on an AutoGen-inspired multi-agent architecture on Cloud Run. Specialized drafter
> and compliance agents autonomously write change-controlled work instructions from RCA records, using Vertex
> AI and the Gemini API. We benchmark against keyword and baseline RAG pipelines using ARES and Ragas for
> atomic factual precision. To guarantee real-time latency, the containerized architecture is orchestrated on
> Google Kubernetes Engine (GKE), utilizing vLLM KV-cache memory management to maximize multi-agent inference
> throughput.

The abstract is kept; implementation changes ("minor changes" the user approved) are in
[`10_decisions.md`](10_decisions.md).

## How M.A.C.H. meets each deliverable

| # | Deliverable | How M.A.C.H. meets it | Novel part |
|---|---|---|---|
| 1 | Versioned corpus + access control | Revision registry (status, effective dates, scope: site/line/station/model/serial, supersedes links, deviation overlays). Role filter applied before search. Expert-reviewed gold Q/A set (MACH-Bench). | Step-level deviation overlays with expiry |
| 2 | Text/table/image ingestion with supersession | Layout parser gives every step, table, cell and figure a stable ID `doc:rev:page:element`; page images kept for visual search; scans routed to the image lane; cross-references parsed as graph edges. | Cross-reference following |
| 3 | Multimodal answers with citations + confidence | Four retrieval lanes fused; each step cites doc, revision, page, step and figure/box; numbers copied from source cells by code; confidence High/Medium/Low. | Step-level safety-complete citations, number lock, context lock |
| 4 | Abstention, conflicts, freshness, escalation | CRAG-style grader, conflict detector, Revision Guard, hazard-tiered conformal gate, partial answers, expert inbox with candidate answers. | Revision Guard; hazard-tiered and shift-aware abstention |
| 5 | Change-controlled WI drafting | Drafter + Compliance agents produce a draft from an RCA/ECN; human approval required; approved draft becomes a new revision and supersedes the old one. | Planted-fault reviewer test, STE rule check |
| 6 | Evaluation vs keyword + text-only RAG | MACH-Bench (~250 Q in 8 buckets, FAA AD supersessions + scripted edits) + 8 peer-reviewed public benchmarks; paired statistics; 11 ablations. | Multimodal SOP benchmark with revision traps |
| 7 | Security + deployment report | RBAC, append-only audit log with replay, prompt-injection defences, edge-first deployment, keyword-only fallback when the LLM is down. | Audit replay |

## The problem in numbers (sources in the literature review)

- One stale document overturns **17–91%** of otherwise-correct RAG answers (arXiv 2026, not peer-reviewed);
  HoH (ACL 2025) confirms outdated info harms RAG; version-unaware evaluation misreports recall by up to 25.7
  points (Morita et al., EMNLP 2026 Industry).
- Commercial legal RAG tools hallucinate on **17–33%** of queries (J. Empirical Legal Studies 2025).
- **ISO 9001 §7.5** requires only the current revision at the point of use; **21 CFR 211.100(b)** requires
  deviations to be recorded and justified.
- Manufacturing workers spend 20–30% of time searching for information (from the LTTS challenge background).

## Glossary

| Term | Meaning |
|---|---|
| SOP / WI | Standard Operating Procedure / Work Instruction (station-level step sheet) |
| ECN | Engineering Change Notice — official change to a part or process; can patch one step |
| RCA | Root Cause Analysis report written after a defect; triggers new WIs |
| Deviation | Temporary, scoped, time-limited change to specific steps |
| Supersession | A newer revision/ECN replaces an older one |
| Effective set E(c) | Elements a user may act on given time, scope and role |
| LOTO / PPE | Lockout/Tagout energy isolation / Personal Protective Equipment |
| RAG | Retrieval-Augmented Generation |
| ColPali / ColQwen | Vision-language retrievers that embed page images as many patch vectors (late interaction, MaxSim) |
| CRAG / Self-RAG | Self-checking RAG: grade retrieved evidence, then answer / re-retrieve / abstain |
| Conformal risk control | Statistical method to set thresholds with a target error rate |
| STE | Simplified Technical English (ASD-STE100) controlled language |
| MACH-Bench | Our benchmark: multimodal SOP questions with revision traps and unsafe asks |
