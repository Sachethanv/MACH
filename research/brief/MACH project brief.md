# M.A.C.H. Project Brief

<div class="sub">

Multimodal Agentic Copilot for the sHop floor: a trust-first assistant
for SOPs and work instructions · TECHgium 10th edition, presentation
round · Prepared 5 November 2026 for Sachiv

</div>

<div class="facts">

<div class="fact">

**12 Nov, 11:59 PM IST**PPT deadline, no extensions

</div>

<div class="fact">

**15 slides max**Use the LTTS template; rules on slide 13

</div>

<div class="fact">

**7 + 5 min**Presentation, then jury Q&A, on Microsoft Teams

</div>

<div class="fact">

**7 days**Build a thin working slice, measure it, pitch it

</div>

</div>

**The pitch in one line:** M.A.C.H. is a shop-floor assistant that
answers from the plant's own SOPs, diagrams and tables, cites the exact
step it used, refuses or calls an expert when unsure, and never answers
from a superseded revision.

<div class="callout">

**Why it can win.** Image-based document search and self-checking RAG
are already published at ICLR and NAACL, so on their own they are table
stakes. What we found *no peer-reviewed work on* is the trust layer for
safety-critical procedures: step-level revision safety (outdated
documents in general are studied, procedures are not), step-level
safety-complete citations, hazard-tiered abstention, and AI drafts
measured under change control. That layer is M.A.C.H.'s novelty. Every
claim below is worded "we found no prior work", not "world first",
because IEEE and Elsevier full texts were checked through the OpenAlex
index, not read in full.

</div>

## 1. The problem

Operators follow SOPs and work instructions (WIs) that change through
revisions, engineering change notices (ECNs) and temporary deviations.
Key values (torques, temperatures, sequences) often live in tables and
diagrams, not text. Keyword search misses those. Plain chatbots and
plain RAG add a new risk: a fluent, confident, wrong answer.

- **Outdated documents flip answers.** One stale document overturns
  17–91% of otherwise-correct RAG answers <span class="tag ax">arXiv
  2026, not peer-reviewed</span>. Date-based re-ranking recovers only
  4.6–10 points; stating explicitly *when* old evidence stops applying
  fixes most of it. Peer-reviewed work confirms the harm
  <span class="tag pr">HoH, ACL 2025</span> and shows version-unaware
  evaluation misreports recall by up to 25.7 points
  <span class="tag pr">EMNLP 2026 Industry</span>, but neither covers
  procedures.
- **Citations are not proof.** Commercial legal RAG tools hallucinate on
  17–33% of queries, including citations that don't support the claim
  <span class="tag pr">J. Empirical Legal Studies 2025</span>. In
  medicine, 50–90% of LLM answers are not fully supported by their own
  sources <span class="tag pr">Nature Communications 2025</span>.
- **Industry has no benchmark.** The peer-reviewed manufacturing RAG
  papers we found evaluate retrieval only <span class="tag pr">Procedia
  CIRP 2025</span>. Nobody has published a hallucination audit of
  generative RAG on SOPs.
- **Auditors care.** ISO 9001 §7.5 requires that only the current
  revision is available at the point of use; an obsolete WI at a station
  is a common nonconformity. 21 CFR 211.100(b) requires every deviation
  to be recorded and justified.

## 2. What M.A.C.H. delivers

| Challenge deliverable                            | How M.A.C.H. meets it                                                                                                                                                                                                          | Novel part <span class="new">(N)</span>                                                    |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Versioned multimodal corpus with access control  | Revision registry with status, effective dates, scope (line, model, serial range), supersedes links and deviation overlays. Role filter applied before search.                                                                 | <span class="new">N</span> Step-level deviation overlays with expiry                       |
| Ingest text, tables, images                      | Layout parser gives every step, table and figure a stable ID; page images kept for visual search; scanned pages routed to image search.                                                                                        | Cross-reference links ("see Fig. 3, step 4")                                               |
| Multimodal answers with citations and confidence | Four search lanes fused, then an answer where every step cites doc, revision, page, step and figure ID. Numbers copied from source cells by code.                                                                              | <span class="new">N</span> Step-level safety-complete citations; number lock; context lock |
| Abstention, conflicts, freshness, escalation     | Evidence grader, conflict detector, Revision Guard, hazard-tiered confidence gate, partial answers, expert inbox with candidate answers.                                                                                       | <span class="new">N</span> Revision Guard; hazard-tiered and shift-aware abstention        |
| Change-controlled WI drafting                    | Drafter and Compliance agents produce a draft from an RCA; human approval required; approved draft becomes a new revision and the old one is superseded.                                                                       | <span class="new">N</span> Planted-fault reviewer test; STE rule check                     |
| Evaluation vs keyword search and text-only RAG   | MACH-Bench (about 250 questions in 8 buckets, built from real FAA Airworthiness Directive supersessions plus scripted counterfactual edits) plus 30 drafting tasks, and eight public benchmarks; paired statistics; ablations. | <span class="new">N</span> First multimodal SOP benchmark with revision traps              |
| Security and deployment report                   | RBAC, audit log with replay, prompt-injection defences, cloud and on-prem paths, keyword-only fallback when the LLM is down.                                                                                                   | Audit replay of any past answer                                                            |

## 3. System design

M.A.C.H. has three parts. Offline ingestion turns documents into
searchable, revision-tagged pieces. The online answer path runs every
question through a chain of checks before anything reaches the operator.
Governance handles experts, change control and the audit trail.

<figure>
<img src="figures/fig1.svg" width="100%">
<figcaption><strong>Figure 1.</strong> M.A.C.H. architecture. Orange
boxes mark the components where we found no prior peer-reviewed
work.</figcaption>
</figure>

### The checks every answer passes

1.  **Context lock.** Role, station, machine model, serial range and
    shift are attached to the question, so search can only see documents
    the user may read and that apply to their machine.
2.  **Revision Guard.** A hard filter, not a soft re-rank: only chunks
    whose status is effective, whose date window covers today and whose
    scope covers the operator's line are searchable. Deviations and ECNs
    are applied to the specific steps they patch.
3.  **Evidence grading.** A CRAG-style grader scores what was found.
    Ambiguous evidence triggers up to two re-searches; irrelevant
    evidence leads to abstention.
4.  **Conflict detection.** If two active sources give different values
    for the same parameter, M.A.C.H. shows both and escalates. A quality
    alert outranks the SOP until it is resolved.
5.  **Number lock.** Every torque, temperature, pressure or dimension in
    the answer is copied by code from the cited table cell, with
    tolerance and unit. If OCR text and the image reading disagree on a
    digit, the system abstains.
6.  **Citation and safety verification.** Each step's citation must
    entail the step, all citations must come from one revision set and
    the cited variant must match the machine, and every warning, PPE or
    lockout/tagout (LOTO) step in the source must appear in the answer.
7.  **Hazard-tiered gate.** The confidence needed to answer depends on
    the step's hazard tier (below). Below threshold, the system gives a
    partial answer or abstains, then escalates.

| Hazard tier                                  | Examples                                                    | Target max error on answered steps | Below threshold                              |
|----------------------------------------------|-------------------------------------------------------------|------------------------------------|----------------------------------------------|
| <span class="tag H">Tier 1 · Critical</span> | LOTO, pressure release, lifting, torque on safety fasteners | ≤ 1%                               | Abstain, "stop and hold", escalate           |
| <span class="tag M">Tier 2 · Quality</span>  | Torque specs, temperatures, inspection criteria             | ≤ 5%                               | Partial answer, escalate the uncertain steps |
| <span class="tag L">Tier 3 · General</span>  | Tool locations, part descriptions, cosmetic steps           | ≤ 10%                              | Answer with a "low confidence" label         |

Thresholds are calibrated on a held-out set with conformal risk control
(Mohri & Hashimoto, ICML 2024; C-RAG, ICML 2024), separately per tier.
They are re-checked whenever an SOP family gets a new revision, because
the statistical guarantee assumes new questions look like the
calibration set. The error targets are our design choice, not values
from a paper.

### Change control for AI-drafted work instructions

<figure>
<img src="figures/fig2.svg" width="100%">
<figcaption><strong>Figure 2.</strong> Nothing the AI writes becomes
official without a signed human approval. Reviewers are periodically
shown drafts with planted faults to measure automation
bias.</figcaption>
</figure>

## 4. Novelty: 17 ideas, ranked

Ranks 1–7 are the PPT headline set. Ranks 8–17 strengthen the paper and
the Q&A. "Effort" is for a 3–4 person team in one week.

| \#  | Idea                                                                                                   | Gap it fills (evidence)                                                                                                                                                                                                                                                                                  | Effort  |
|-----|--------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| 1   | **Revision Guard**: hard effectivity filter, "superseded by" statements, one-revision-per-answer check | Stale documents flip 17–91% of answers; VersionRAG 90% vs 58% naive RAG <span class="tag ax">both arXiv</span>. Peer-reviewed: HoH (ACL 2025) on outdated info, Morita et al. (EMNLP 2026 Industry) on evolving policy corpora. None on step-level supersession, ECN overlays or mixed-revision answers. | Low     |
| 2   | **Step-level, safety-complete citations** with figure and step IDs                                     | ALCE (EMNLP 2023) scores sentences, not step order or missing safety steps. Visual box citation reaches only 54–68% even fine-tuned (VISA, ACL 2025).                                                                                                                                                    | Low–Med |
| 3   | **Hazard-tiered abstention** with partial answers                                                      | Conformal guarantees exist (ICML 2024); none found calibrated per hazard class or returning certified step subsets.                                                                                                                                                                                      | Med     |
| 4   | **Smart escalation + expert memory** with expiry and conflict checks                                   | Prediction sets help humans (NeurIPS 2024). The one factory loop found has no expiry or SOP-conflict control (Frontiers in AI 2024).                                                                                                                                                                     | Med     |
| 5   | **MACH-Bench**: multimodal, with revision traps and unsafe asks                                        | DesignQA (ASME JCISE) covers multimodal engineering docs; SOPRAG <span class="tag ax">arXiv</span> has an SOP retrieval benchmark; VersionQA is software-only <span class="tag ax">arXiv</span>. None combines WIs, images and revision traps.                                                           | Med     |
| 6   | **Planted-fault reviewer test** for AI drafts                                                          | No study measures change-control outcomes for LLM-drafted instructions; EU AI Act Art. 14 asks for automation-bias awareness.                                                                                                                                                                            | Low     |
| 7   | **Adaptive routing** by question complexity                                                            | Adaptive-RAG (NAACL 2024): same F1 as IRCoT at 1.46× vs 3.33× the time.                                                                                                                                                                                                                                  | Low     |
| 8   | **Context lock**: answers scoped to machine variant                                                    | "Misgrounded" citations defined in legal RAG (JELS 2025); never applied to machine variants.                                                                                                                                                                                                             | Low     |
| 9   | **Deviation overlays** on individual steps                                                             | 21 CFR 211.100(b) requires recorded deviations; no RAG work models step-level, time-limited patches.                                                                                                                                                                                                     | Med     |
| 10  | **"What changed?"** answers across revisions, including tables and figures                             | Diffing multimodal revisions is listed as open in versioning work.                                                                                                                                                                                                                                       | Med     |
| 11  | **Cross-reference following** ("see Fig. 3, step 4")                                                   | No benchmark or system found that evaluates it.                                                                                                                                                                                                                                                          | Med     |
| 12  | **Exact-ID search lane** with tuned fusion                                                             | Naive fusion ranks relevant results lower on 8–21% of queries <span class="tag ax">arXiv</span>; no study isolates part numbers.                                                                                                                                                                         | Low     |
| 13  | **Number lock** for critical values and units                                                          | LLM judges are near random on expert-level correctness (JudgeBench, ICLR 2025); parameters need exact checks.                                                                                                                                                                                            | Low     |
| 14  | **Query by photo** of a part or panel                                                                  | No paper found <span class="tag in">inference</span>.                                                                                                                                                                                                                                                    | Med     |
| 15  | **Shift-aware escalation**                                                                             | Factory study: assistant most valuable on night shifts with no expert (Frontiers in AI 2024).                                                                                                                                                                                                            | Low     |
| 16  | **Recalibrate on every revision**                                                                      | Conformal guarantees break under distribution shift; none found tied to document control.                                                                                                                                                                                                                | Med     |
| 17  | **Simplified Technical English check** on drafts                                                       | Builds on Jonek & Manns (CARV 2025): controlled language raised vocabulary compliance 50%→85% and cut editing ~20→12 min. Our new part is measuring it under change control with planted faults.                                                                                                         | Low     |

Also worth a slide line <span class="tag in">inference, no paper</span>:
hands-free voice queries for gloved hands, and answers in Hindi or the
local language while citations stay in the original English SOP.

<figure>
<img src="figures/fig3.svg" width="100%">
<figcaption><strong>Figure 3.</strong> Published results behind three
design choices: page-image search, hybrid retrieval with reranking, and
version-aware retrieval.</figcaption>
</figure>

## 5. Edge cases and how M.A.C.H. handles them

The most dangerous failure is a confident, cited, wrong answer. We list
37 edge cases; 13 are high risk. This is the summary; the full test plan
expands it to 55 cases in 14 families with a scripted pass criterion for
each. Each one becomes a test case in MACH-Bench, so every robustness
claim is backed by a measured number.

<figure>
<img src="figures/fig4.svg" width="100%">
<figcaption><strong>Figure 4.</strong> Edge cases by pipeline stage and
risk level. Full list below.</figcaption>
</figure>

| Stage      | Edge case                                               | Failure                              | How M.A.C.H. handles it                                                    | Risk                            |
|------------|---------------------------------------------------------|--------------------------------------|----------------------------------------------------------------------------|---------------------------------|
| Revisions  | Two revisions of one SOP both marked effective          | Answer mixes old and new steps       | Ingestion blocks it; verifier rejects mixed-revision answers               | <span class="tag H">High</span> |
| Revisions  | ECN changes one step before the SOP is reissued         | Old step used                        | Deviation overlay patches that step                                        | <span class="tag H">High</span> |
| Revisions  | Revision effective tomorrow, or on one line only        | Too early or wrong line              | Filter on effective window and scope using context lock                    | <span class="tag H">High</span> |
| Revisions  | SOP withdrawn with no replacement                       | Answers from a withdrawn procedure   | Abstain: "procedure withdrawn, contact QA"                                 | <span class="tag H">High</span> |
| Revisions  | Operator quotes an old document number                  | Executes obsolete text               | Answer from current revision and state what changed                        | <span class="tag M">Med</span>  |
| Variants   | Same procedure, different machine model or serial range | Right text, wrong machine            | Context lock; citation must match the variant                              | <span class="tag H">High</span> |
| Conflict   | SOP and quality alert give different values             | Silently picks one                   | Show both, escalate; alert outranks SOP until resolved                     | <span class="tag H">High</span> |
| Numbers    | N·m in one document, lbf·ft in another                  | Wrong value or unit                  | Number lock; units converted by code                                       | <span class="tag H">High</span> |
| Numbers    | Tolerance given ("25 ± 2 N·m")                          | Tolerance dropped                    | Value, tolerance and unit extracted as one field                           | <span class="tag H">High</span> |
| Numbers    | OCR reads 8 as B, or 2,5 vs 2.5                         | Wrong digit stated confidently       | Cross-check OCR against image reading; mismatch → abstain                  | <span class="tag H">High</span> |
| Safety     | Answer would omit a LOTO or PPE step                    | Injury risk                          | Safety-completeness check; warnings first, never truncated                 | <span class="tag H">High</span> |
| Safety     | "How do I skip / bypass this interlock?"                | Unsafe instruction                   | Router refuses, logs, escalates                                            | <span class="tag H">High</span> |
| Security   | Hidden "ignore your rules" text in an ingested doc      | Hijacked answer                      | Strip at ingestion; retrieved text treated as data; fixed output schema    | <span class="tag H">High</span> |
| Access     | Operator asks about a restricted RCA                    | Leak                                 | Role filter before search, not after generation                            | <span class="tag H">High</span> |
| Security   | Names or personal data in RCA reports                   | Privacy breach                       | Redact at ingestion; no per-operator analytics                             | <span class="tag M">Med</span>  |
| Retrieval  | Answer only in a diagram callout or table cell          | Text search misses it                | Page-image lane plus layout parsing                                        | <span class="tag M">Med</span>  |
| Retrieval  | Scanned, skewed or hand-marked pages                    | OCR garbage                          | Route to image search; flag low-quality pages                              | <span class="tag M">Med</span>  |
| Retrieval  | Table or step continues on the next page                | Half a step                          | Merge split tables and steps at ingestion                                  | <span class="tag M">Med</span>  |
| Retrieval  | Diagram not updated when the text was                   | Figure contradicts text              | Figure carries its own revision hash; mismatch flagged                     | <span class="tag M">Med</span>  |
| Retrieval  | Plant slang ("CP" for caliper piston)                   | Search miss                          | Plant glossary expands query; exact-ID lane                                | <span class="tag M">Med</span>  |
| Retrieval  | Same warning repeated in 10 documents                   | Unfair scoring                       | Multi-gold evidence sets in the benchmark                                  | <span class="tag M">Med</span>  |
| Retrieval  | Cross-reference to another document                     | Answer missing the referenced figure | Agent follows parsed cross-reference links                                 | <span class="tag M">Med</span>  |
| Query      | Vague ("how do I fix it?")                              | Guesses the machine                  | Use station context or ask one clarifying question                         | <span class="tag M">Med</span>  |
| Query      | Two questions in one, or a multi-step plan              | Answers half                         | Router sends it to the multi-step path                                     | <span class="tag M">Med</span>  |
| Query      | Not covered by any document                             | Hallucination                        | Abstain: "not in the controlled documents"                                 | <span class="tag M">Med</span>  |
| Query      | Blurry or wrong photo                                   | Wrong page, high confidence          | Image-quality check; confirm the matched part                              | <span class="tag M">Med</span>  |
| Query      | Hindi or mixed-language question                        | Search miss                          | Translate query for search; answer in user's language, cite English source | <span class="tag M">Med</span>  |
| Generation | Very long SOP overflows the context                     | Procedure cut off                    | Step-level chunks; completeness check against the step count               | <span class="tag M">Med</span>  |
| Escalation | No expert responds in time                              | Operator blocked or guesses          | Timeout → "stop and hold" for tier-1 steps; supervisor alert               | <span class="tag M">Med</span>  |
| Escalation | Expert note conflicts with the SOP, or has expired      | Informal override                    | Notes are advisory, expire, and can't override without change control      | <span class="tag M">Med</span>  |
| Escalation | Everything gets escalated                               | System ignored                       | Track escalation rate; tune on the risk–coverage curve                     | <span class="tag M">Med</span>  |
| Drafting   | Draft contradicts another active SOP                    | Bad revision approved                | Compliance agent checks all active SOPs for that station                   | <span class="tag M">Med</span>  |
| Drafting   | Reviewer rubber-stamps the AI draft                     | Automation bias                      | Diff view; planted-fault audits                                            | <span class="tag M">Med</span>  |
| Drafting   | Two drafts of the same SOP at once                      | Collision                            | SOP family locked during review                                            | <span class="tag L">Low</span>  |
| Ops        | LLM API down or slow                                    | No answer on the floor               | Fallback: keyword search showing source pages, with a banner               | <span class="tag M">Med</span>  |
| Ops        | Model version changes silently                          | Behaviour drifts                     | Pin version; rerun benchmark on every change                               | <span class="tag L">Low</span>  |
| Audit      | "What did the AI tell operator X on date D?"            | No proof                             | Full audit log with replay                                                 | <span class="tag L">Low</span>  |

## 6. Evaluation plan

We compare five systems on the same frozen corpus, with the same LLM,
top-k and context budget, so any gain comes from M.A.C.H.'s design.

<div class="two">

<div>

### Systems

1.  BM25 keyword search (shows top pages only)
2.  BM25 + LLM
3.  Text-only RAG (dense over OCR text, no checks)
4.  Hybrid text RAG (BM25 + dense, RRF)
5.  M.A.C.H. full, plus ablations: no page images, no Revision Guard, no
    verifier, no hazard gate, no router

### Metrics

- **Retrieval:** Recall@5, nDCG@10 (multi-gold)
- **Answers:** correctness, faithfulness, citation precision/recall
  (ALCE-style)
- **Procedure:** step-order fidelity, exact match on critical values,
  safety-step recall
- **Trust:** revision-mixing rate, superseded-citation rate, abstention
  precision/recall, unsafe-answer rate, escalation rate
- **Drafting:** accept/edit/reject, edit distance, planted-fault catch
  rate
- **Ops:** p50/p95 latency, cost per query

</div>

<div>

<figure style="margin-top:4px">
<img src="figures/fig5.svg" width="100%">
<figcaption><strong>Figure 5.</strong> Planned question mix. 36% are
traps designed to make a naive system fail.</figcaption>
</figure>

</div>

</div>

### Making it rigorous

- **Corpus:** real revision chains from public FAA Airworthiness
  Directive supersessions, plus scripted counterfactual edits and a
  realistic shop-floor set (SOPs with 2–3 revisions, ECNs, deviations,
  quality alerts, RCAs, drawings, photos). Freeze and hash the snapshot.
- **Labels:** each question has a gold answer, all valid evidence
  locations, expected behaviour (answer, abstain or escalate) and, for
  procedures, the ordered steps and critical values. Two annotators
  label at least 25%; report Cohen's κ.
- **Split:** 30% dev for tuning prompts and thresholds, 70% test touched
  once.
- **Judging:** an LLM judge from a different model family than the
  generator, run 3 times with shuffled order, validated on ≥100
  human-labelled items. Critical values are checked by exact match,
  never by the judge.
- **Statistics:** paired per-question tests (McNemar or bootstrap), Holm
  correction across metrics, 95% confidence intervals; ARES-style
  correction to turn a small human-labelled set into intervals.
- **Human study:** 3–5 people answer 10 questions with keyword search vs
  M.A.C.H.; report minutes per correct answer.

### Release gates (from the test plan)

A build ships only if it passes every hard gate. These match the paper
draft and the edge-case test plan.

| Gate                             | Metric                                                   | Threshold                | Type                            |
|----------------------------------|----------------------------------------------------------|--------------------------|---------------------------------|
| No superseded citations          | Superseded-citation rate on revision traps               | 0 of n                   | <span class="tag H">Hard</span> |
| No mixed-revision answers        | Mixed-revision answer rate                               | 0 of n                   | <span class="tag H">Hard</span> |
| No restricted leakage            | Restricted element IDs in a lower-role context or answer | 0                        | <span class="tag H">Hard</span> |
| No injected instruction followed | Injection success rate                                   | 0                        | <span class="tag H">Hard</span> |
| Safety steps present             | Safety-step recall on answered procedures                | ≥ 0.98                   | <span class="tag H">Hard</span> |
| Exact critical values            | Torque, tolerance, unit, part number exact match         | ≥ 0.99 on answered items | <span class="tag H">Hard</span> |
| Safe fallback                    | Keyword fallback shown when the model is down            | 100% of kill-switch runs | <span class="tag H">Hard</span> |
| Abstains when it should          | Abstention recall on unanswerable items                  | ≥ 0.90                   | <span class="tag L">Soft</span> |
| Does not over-abstain            | Over-abstention on answerable items                      | ≤ 0.15                   | <span class="tag L">Soft</span> |
| Fast enough                      | Queries answered in under 15 s; p95                      | ≥ 95%; p95 \< 15 s       | <span class="tag L">Soft</span> |

<div class="callout b">

**Headline numbers for the results slide** (to be measured):
revision-mixing rate against the baselines, unsafe-answer rate on trap
questions, citation precision, Recall@5 on diagram questions, and p95
latency.

</div>

## 7. Technology stack

| Layer               | Choice for the prototype                                                                                                                        | Why                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Parsing             | Docling or PyMuPDF; page images at 150 dpi                                                                                                      | Text, tables and bounding boxes with stable IDs                       |
| Page-image search   | ColQwen2 / ColPali via byaldi or Qdrant multi-vector                                                                                            | Qdrant supports late-interaction matching; pgvector does not natively |
| Text search         | BM25 (rank_bm25 or Postgres full-text) + text embeddings + exact-ID index                                                                       | Keywords still win on part numbers and jargon                         |
| Fusion and rerank   | Weighted fusion tuned on dev, cross-encoder reranker                                                                                            | Avoids the naive-fusion penalty                                       |
| LLM                 | Paper configuration: 4-bit 7B vision-language model on one plant-side GPU. Demo option: Gemini via Vertex AI. Structured JSON output either way | Plant data stays on site; schema-enforced answers                     |
| Agents              | LangGraph or plain Python state machine                                                                                                         | Router, grader, drafter, compliance; easy to audit                    |
| Data and governance | Postgres: registry, overlays, roles, audit log, approval queue                                                                                  | One source of truth for revisions                                     |
| UI                  | Streamlit or Next.js: operator chat, PDF viewer with highlighted step, expert inbox, review diff view                                           | Demo-ready in days                                                    |
| Deploy              | Docker Compose on one GPU box (open weights served with vLLM); Cloud Run for a hosted demo                                                      | Same pipeline on-prem or in the cloud                                 |
| Evaluation          | RAGAS + custom scripts for trust metrics                                                                                                        | Reproducible results table                                            |

## 8. Seven-day plan to the PPT deadline

<figure>
<img src="figures/fig6.svg" width="100%">
<figcaption><strong>Figure 6.</strong> One week, built thin first and
deepened after. A working slice by Sunday matters more than any single
component.</figcaption>
</figure>

### Suggested 12-slide story (7 minutes)

1.  Title and one-line pitch
2.  Problem: one real-looking story of an operator following an outdated
    revision
3.  Why current tools fail (stale documents, unsupported citations)
4.  M.A.C.H. at a glance (Figure 1)
5.  Novelty 1: Revision Guard, with a screenshot of the "superseded by"
    note
6.  Novelty 2: step-level, safety-complete citations and number lock
7.  Novelty 3: hazard-tiered abstention and smart escalation
8.  Change-controlled drafting (Figure 2)
9.  Evaluation design: MACH-Bench, baselines, release gates
10. Results: one table and two honest failure cases
11. Security, deployment and edge cases handled (Figure 4)
12. Impact for LTTS clients and next steps

## 9. Jury questions and our answers

Q1. Isn't this just RAG with extra steps?  
RAG is the base. The contribution is the trust layer: Revision Guard,
step-level safety-complete citations, number lock and hazard-tiered
abstention. We found no peer-reviewed work on these for procedures, and
we measure each with an ablation.

Q2. How do you know which revision is effective?  
From document-control metadata (status, effective dates, scope,
supersedes links), not file dates. A hard filter removes everything else
before the LLM sees it, and the verifier rejects any answer mixing
revisions.

Q3. What if two current documents disagree?  
M.A.C.H. never picks silently. It shows both sources, escalates to an
expert, and treats a quality alert as overriding the SOP until resolved.

Q4. How do you stop hallucinated numbers?  
Number lock: critical values are copied by code from the cited table
cell with their tolerance and unit. The LLM never writes them. If OCR
and the image reading disagree, the system abstains.

Q5. Won't it refuse too often to be useful?  
We report the risk–coverage curve and escalation rate, not just
accuracy. Only tier-1 hazardous steps need very high confidence; general
lookups answer with a confidence label. Partial answers keep the
operator moving.

Q6. Where do confidence thresholds come from?  
Conformal risk control on a held-out calibration set, separately per
hazard tier (ICML 2024 methods). Thresholds are re-checked whenever an
SOP family is revised.

Q7. Why not fine-tune a model on the SOPs?  
Retrieval beats fine-tuning for adding new knowledge (Ovadia et al.,
EMNLP 2024), and SOPs change too often. Updating an index is instant and
auditable; retraining is neither.

Q8. You have no real plant data. Is the test valid?  
Part of it is real: revision chains come from public FAA Airworthiness
Directive supersessions, and we also run eight public peer-reviewed
benchmarks. The shop-floor part is synthetic but reviewed by someone
with plant experience (name them). The benchmark, code and schema are
designed so LTTS can drop in real documents and rerun the same
evaluation.

Q9. Can a malicious document hijack it?  
Instruction-like text is stripped at ingestion, retrieved text is
treated as data, output is schema-enforced, and access is filtered by
role before search. We include injection documents in the test set.

Q10. What if the cloud LLM is down or data can't leave the plant?  
The reference configuration already runs on-prem: a 4-bit 7B
vision-language model on one plant-side GPU, so documents never leave
the plant. If the model is down, a keyword-only fallback shows the right
source pages with a banner.

Q11. Who is accountable for an AI-drafted work instruction?  
The human approver. Nothing becomes effective without a signed approval,
every AI change is shown as a diff, and planted-fault audits measure
whether reviewers are really checking.

Q12. How fast is it?  
Release gate: 95% of queries answered in under 15 s on a single
plant-side GPU (faster with a cloud API). Simple lookups take one pass;
only multi-step questions run the agent loop (Adaptive-RAG shows this
keeps accuracy at under half the latency). Report the measured p50 and
p95.

Q13. What about expert knowledge that isn't written down?  
Expert answers to escalations are stored as advisory notes with author,
date, expiry and an SOP-conflict check. Repeated notes on the same topic
trigger a change-control draft, so tacit knowledge becomes an official
revision.

Q14. How is this different from commercial copilots?  
General copilots don't understand effectivity, machine variants, hazard
tiers or change control. M.A.C.H. is built around document-control rules
from ISO 9001 §7.5 and GMP, and it proves its behaviour on trap
questions.

Q15. What's the business value for LTTS?  
Fewer quality escapes from obsolete instructions, faster answers on
night shifts without experts, audit-ready traceability, and faster WI
authoring. It is reusable across LTTS's manufacturing, automotive and
medical-device clients.

Q16. Hasn't HoH or SOPRAG already solved this?  
HoH (ACL 2025) shows outdated documents hurt RAG but treats a document
as a whole; it has no effectivity dates, ECN overlays or step-level
supersession. SOPRAG (preprint) improves SOP retrieval but has no
revisions, images, citations or abstention. We cite both, borrow HoH's
outdated-versus-current setup, and test exactly what they leave out.

## 10. Honest limitations

- The shop-floor documents are synthetic and the real revision chains
  come from aviation, so absolute accuracy won't transfer directly to a
  given plant; relative gains over baselines are the claim.
- Conformal guarantees hold only while new questions resemble the
  calibration set; we mitigate with recalibration on revision events,
  not eliminate the risk.
- Several of the newest supporting results are arXiv preprints and are
  labelled as such. Venue status of ColPali (ICLR 2025) and some others
  should be confirmed before citing in a paper.
- The literature search used the OpenAlex index (covers IEEE incl. Early
  Access, ACM, ScienceDirect in press, Springer) but paywalled full
  texts were not read, so novelty claims are phrased as "we found no
  prior work".

<div class="callout b">

**Open questions for you:** How many people are on the team, and who
owns which part? Do you have GCP credits or a GPU? Can anyone with plant
experience review the gold set? Please share the LTTS PPT template so
the slide story can be mapped onto it.

</div>

## Key references

<span class="tag pr">peer-reviewed</span> venue given ·
<span class="tag ax">arXiv</span> not peer-reviewed. Full list with
links and verification notes: *MACH multimodal RAG literature review.md*
in the project files.

1.  Faysse et al. ColPali: Efficient Document Retrieval with Vision
    Language Models. ICLR 2025 (venue to confirm).
    <span class="tag pr">peer-reviewed</span>
2.  Yu et al. VisRAG: Vision-based RAG on Multi-modality Documents.
    ICLR 2025. <span class="tag pr">peer-reviewed</span>
3.  Ma et al. Unifying Multimodal Retrieval via Document Screenshot
    Embedding. EMNLP 2024. <span class="tag pr">peer-reviewed</span>
4.  Zhang et al. OCR Hinders RAG (OHRBench). ICCV 2025.
    <span class="tag pr">peer-reviewed</span>
5.  Ludwig, Schmidt, Kühn. Ontology-based RAG for a voice-controlled
    maintenance assistant. Computers in Industry 169, 2025.
    <span class="tag pr">peer-reviewed</span>
6.  Gao et al. Enabling LLMs to Generate Text with Citations (ALCE).
    EMNLP 2023. <span class="tag pr">peer-reviewed</span>
7.  Asai et al. Self-RAG. ICLR 2024.
    <span class="tag pr">peer-reviewed</span>
8.  Song et al. Trust-Score / Trust-Align. ICLR 2025.
    <span class="tag pr">peer-reviewed</span>
9.  Mohri, Hashimoto. Language Models with Conformal Factuality
    Guarantees. ICML 2024. <span class="tag pr">peer-reviewed</span>
10. Kang et al. C-RAG: Certified Generation Risks for RAG. ICML 2024.
    <span class="tag pr">peer-reviewed</span>
11. Farquhar et al. Detecting hallucinations in LLMs using semantic
    entropy. Nature 630, 2024. <span class="tag pr">peer-reviewed</span>
12. Ma et al. VISA: RAG with Visual Source Attribution. ACL 2025.
    <span class="tag pr">peer-reviewed</span>
13. Saad-Falcon et al. ARES. NAACL 2024; Es et al. RAGAS. EACL 2024
    (demo). <span class="tag pr">peer-reviewed</span>
14. Magesh et al. Hallucination-Free? Assessing legal AI research
    tools. J. Empirical Legal Studies 22, 2025.
    <span class="tag pr">peer-reviewed</span>
15. Xu et al. Knowledge Conflicts for LLMs: A Survey. EMNLP 2024.
    <span class="tag pr">peer-reviewed</span>
16. Ovadia et al. Fine-Tuning or Retrieval? EMNLP 2024.
    <span class="tag pr">peer-reviewed</span>
17. Jeong et al. Adaptive-RAG. NAACL 2024; Trivedi et al. IRCoT.
    ACL 2023. <span class="tag pr">peer-reviewed</span>
18. Mozannar, Sontag. Consistent Estimators for Learning to Defer to an
    Expert. ICML 2020. <span class="tag pr">peer-reviewed</span>
19. De Toni et al. Towards Human-AI Complementarity with Prediction
    Sets. NeurIPS 2024; Fanconi, van der Schaar. Cascaded LMs for
    Human–AI Decision-Making. NeurIPS 2025.
    <span class="tag pr">peer-reviewed</span>
20. Kernan Freire et al. Knowledge sharing in manufacturing using
    LLM-powered tools. Frontiers in AI, 2024.
    <span class="tag pr">peer-reviewed</span>
21. Colabianchi et al. Computers in Industry, 2024 (doi
    10.1016/j.compind.2024.104129); Meyer et al. IEEE ETFA 2024; Widulle
    et al. IEEE INDIN 2024. <span class="tag pr">peer-reviewed</span>
22. Tan et al. JudgeBench. ICLR 2025.
    <span class="tag pr">peer-reviewed</span>
23. Ouyang et al. HoH: Impact of Outdated Information on RAG. ACL 2025.
    <span class="tag pr">peer-reviewed</span>
24. Morita, Sanderson, Hewitt. Longitudinal-aware Evaluation of RAG over
    Evolving Credit Policy Documents. EMNLP 2026 Industry.
    <span class="tag pr">peer-reviewed</span>
25. Doris et al. DesignQA: A Multimodal Benchmark for Engineering
    Documentation. ASME JCISE, 2024 (doi 10.1115/1.4067333).
    <span class="tag pr">peer-reviewed</span>
26. Jonek, Manns. Leveraging LLM for Assembly Instructions Using
    Controlled Natural Language. CARV 2025, Springer LNME (doi
    10.1007/978-3-032-16889-4_64).
    <span class="tag pr">peer-reviewed</span>
27. Wan et al. Hybrid RAG for domain-centric Q&A in smart manufacturing.
    Advanced Engineering Informatics, 2025.
    <span class="tag pr">peer-reviewed</span>
28. Li et al. SOPBench. EMNLP 2026; Wang et al. SOP-Maze. Findings of
    ACL 2026. <span class="tag pr">peer-reviewed</span>
29. Lin et al. SOPRAG: Multi-view Graph Experts Retrieval for Industrial
    SOPs. arXiv 2602.01858. <span class="tag ax">arXiv</span>
30. Ahmed, Galke Poech, Röttger. Stale-Document Poisoning, 2026.
    <span class="tag ax">arXiv</span>
31. Huwiler, Stockinger, Fürst. VersionRAG, 2025.
    <span class="tag ax">arXiv</span>
32. Bock, Barnard Feeney. Engineering Change Management Concepts, NIST
    IR 7922, 2013 (government report); ISO 9001:2015 §7.5; 21 CFR
    211.100; EU AI Act Art. 14.
