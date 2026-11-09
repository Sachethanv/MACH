# M.A.C.H.: Revision-Safe, Citation-Grounded Multimodal RAG for Industrial Work Instructions\`

Draft v0.1 · Nov 5, 2026 · @Sachethan

> **Status of this draft.** Every number in a results table or in the abstract marked `[R#]` is a placeholder. It must come from the prototype and MACH-Bench runs described in Sections V–VI. No result in this draft has been measured. Citations marked † are arXiv preprints, not peer-reviewed; check each one before submission.

## Abstract

Shop-floor operators answer safety-critical questions from standard operating procedures (SOPs), work instructions (WIs), drawings and engineering change notices that exist in several revisions at once. Retrieval-augmented generation (RAG) can answer such questions, but general-purpose RAG has three failure modes that are unacceptable in manufacturing. It can cite a superseded revision, it can mix steps from two revisions into one answer, and it can drop a safety step while still citing real text. We present M.A.C.H., a multimodal, agentic RAG system for industrial procedures built around five contributions. (1) *Revision-safe retrieval*: an effectivity-gated hard filter, explicit supersession statements in the generator context, and a post-generation revision-coherence check that blocks any answer whose citations span more than one effective revision set. (2) *MACH-Bench*, the first benchmark we know of for work instructions that combines multimodal evidence with superseded-revision traps, built from real FAA Airworthiness Directive supersessions and scripted counterfactual edits, with superseded- and mixed-revision traps. (3) *Step-level procedural attribution* metrics: per-step support, order fidelity, safety-step recall and metadata-aware misgrounding, with visual citations to pre-parsed page elements. (4) *Safety-tiered calibrated abstention and escalation*: four-way query routing and a deferral rule weighted by step criticality and expert availability. (5) *Drafting under change control*, measured by planted-fault catch rate in blinded review and safety-step survival. The full system runs on a single plant-side GPU with a 4-bit 7B vision-language model. We evaluate on eight peer-reviewed public benchmarks and on MACH-Bench. M.A.C.H. reaches \[R1\] answer accuracy against \[R2\] for BM25 + LLM and \[R3\] for text-only dense RAG, cuts the superseded-citation rate from \[R4\] to \[R5\], keeps the mixed-revision answer rate at \[R6\], and reaches safety-step recall of \[R7\] at a coverage of \[R8\]. Reviewers caught \[R9\] of seeded faults in drafted WIs. p95 latency is \[R10\] s.

**Index terms:** retrieval-augmented generation, multimodal document retrieval, industrial knowledge management, document version control, selective prediction, human-in-the-loop, work instructions, large language models.

## I. Introduction

In a factory, a wrong answer has a physical cost. An operator who torques a fastener to the value in Rev B of a WI, after Rev C changed it, produces a nonconforming part. An answer that drops a lockout/tagout step can injure someone. ISO 9001:2015 §7.5.3 requires the current document to be available at the point of use \[24\], and auditors treat an obsolete instruction at a workstation as a nonconformity. NIST's engineering change management concepts warn against "accidental mixes of original and changed parts" \[23\]. Any assistant that answers from controlled documents inherits these duties.

Recent RAG research supplies most of the parts such an assistant needs. Retrievers that embed page images beat OCR-text pipelines on documents full of diagrams and tables \[1\]–\[4\]. Citation-trained models and calibrated abstention outperform prompting alone \[7\], \[8\], \[12\]. Routing queries by complexity matches iterative retrieval at a fraction of the cost \[25\]. Yet almost none of this has been tested where an error has a physical cost. Peer-reviewed industrial RAG work is mostly text- or ontology-based and evaluates retrieval only \[5\], \[37\]. Three gaps stand out.

1. **Revisions.** Peer-reviewed work now measures the harm of outdated documents in RAG \[58\] and evaluates RAG over evolving policy corpora \[59\], but none treats procedure revisions with effectivity, step-level supersession or change-notice overlays. Preprints report that a single outdated document overturns 17–91% of otherwise-correct answers† \[21\]. We found no work that measures whether one answer mixes revisions.
2. **Procedures.** Citation metrics such as ALCE \[6\] score sentences, not ordered steps. A response can cite real text and still omit a warning. Legal RAG studies show that such "misgrounded" citations are common \[16\].
3. **Benchmarks.** Multimodal engineering-document benchmarks exist \[60\], and an SOP retrieval benchmark has been proposed† \[61\], but we found none for work instructions that combines multimodal evidence with superseded-revision traps.

This paper presents M.A.C.H., a multimodal agentic RAG system for industrial procedures, and makes five contributions:

- **C1. Revision-safe retrieval.** Effectivity-gated filtering before ranking, supersession statements injected into the generator context, and a revision-coherence check after generation. We define the *mixed-revision answer rate* (MRA) to measure the property directly.
- **C2. MACH-Bench.** A small, reproducible benchmark of procedure revisions: about 100 core items grounded in real FAA Airworthiness Directive supersessions, where the regulator states the gold answer, plus scripted counterfactual edits (changed torque, inserted safety step, swapped steps, scoped deviation) released with the generation script and changelog. Components are also validated on eight peer-reviewed public benchmarks.
- **C3. Step-level procedural attribution.** Per-step support, order fidelity (Kendall τ), safety-step recall and metadata-aware misgrounding, with citations to pre-parsed element IDs rather than free-form boxes.
- **C4. Safety-tiered abstention and escalation.** Four-way routing (direct lookup, single retrieval, multi-hop, escalate) and a deferral threshold that depends on step criticality and expert availability, reported as risk–coverage curves and expert minutes per 100 queries.
- **C5. Drafting under change control.** Drafts generated into a schema and routed as change requests, evaluated by reviewer accept/edit/reject rates and by *seeded-fault detection*, which tests automation bias directly, and by safety-step survival from source to approved draft. Prior drafting studies score draft quality in a feedback loop \[63\]; ours judges drafts inside change control, against planted faults.

We state every novelty claim as "we found no prior work", since the manufacturing journal literature could not be searched exhaustively (Section VIII). Section II reviews related work. Section III formalizes the problem. Section IV describes the system. Section V introduces MACH-Bench and its metrics. Sections VI and VII give the setup and results. Section VIII discusses limitations, threats to validity and ethics.

## II. Related Work

### A. Multimodal document retrieval

ColPali embeds page images with late interaction and scores 81.3 average nDCG@5 on ViDoRe, against 65.5 for OCR+BM25, while indexing about 18× faster than a parsing pipeline \[1\]. VisRAG generates directly from page images and reports a 20–40% end-to-end gain over text RAG \[2\]. Document screenshot embedding beats BM25 by 17 points top-1 \[3\]. OHRBench shows that no tested OCR system was good enough to build a high-quality RAG knowledge base \[4\]. Fusion of visual and text retrievers is the most robust choice on ViDoRe V3† \[39\], and BM25 remains a strong baseline on identifier-dense text† \[42\]. Peer-reviewed industrial RAG is mostly text-based: a maintenance assistant fusing exact and vector matching reached F1 0.611 against 0.45 for the best single method \[5\]. A multimodal aircraft-manual system reaches Recall@5 of 93.4% but takes 11.9 s per retrieval† \[48\]. DesignQA is a multimodal benchmark over engineering documentation \[60\]. SOPRAG proposes graph-expert retrieval (entity, causal and flow views) for industrial SOPs with its own four-domain benchmark† \[61\], and is the closest prior system. Multimodal RAG has also been combined with fine-tuned LLMs for technical teaching material on electrical concepts \[64\]. None of these models revisions, step-level citations or abstention.

### B. Attribution, faithfulness and abstention

ALCE defines citation recall and precision through NLI entailment \[6\]. Self-RAG \[7\] and Trust-Align \[8\] train models to attribute and refuse; Trust-Align improved 26 of 27 models. Automatic attribution judges reach only about 80% macro-F1 \[9\], so judge reliability must itself be measured. RAGAS \[10\] and ARES \[11\] give reference-free and confidence-interval estimates. Visual attribution is weak: zero-shot box accuracy is 1.5% in VISA \[15\], which motivates citing pre-parsed elements instead† \[43\]. For abstention, conformal methods give finite-sample guarantees on factuality \[12\] and RAG risk \[13\]; semantic entropy detects confabulation \[44\]; and selective QA under domain shift benefits from calibrators \[38\]. The TACL survey \[14\] names over-abstention as an open problem. Legal RAG tools hallucinate on 17–33% of queries once misgrounded citations are counted \[16\].

### C. Knowledge conflicts and versioning

Inter-context conflicts, where retrieved passages disagree, are a recognized class \[17\]. Models follow coherent context even against their own knowledge \[18\]. A stale corpus can make retrieval no better than none \[19\], and date-ordered evidence in the prompt helps \[20\]. Context-aware decoding improves faithfulness but amplifies whatever context it is given \[40\], so it is safe only after the right revision is selected. VersionRAG filters vector search by version and reaches 90% against 58% for naive RAG† \[22\]. Stale-document poisoning is largely fixed by stating explicitly when old evidence stopped applying† \[21\]. HoH, a peer-reviewed dynamic benchmark, shows that outdated information placed beside current information lowers accuracy and can produce harmful outputs \[58\]. Morita et al. evaluate RAG over evolving credit-policy corpora with a Stable / Evolved / Added / Removed change taxonomy, and find that version-unaware evaluation misreports recall by up to 25.7 points \[59\]. None of these works covers procedures, step-level supersession, effectivity filtering or a check against mixed-revision answers.

### D. Adaptive retrieval and deferral to experts

IRCoT interleaves retrieval with reasoning steps \[26\]. Adaptive-RAG routes queries by complexity and matches IRCoT at 1.46× rather than 3.33× the cost of single-step retrieval, with a router that is only 54.5% accurate \[25\]. Learning to defer makes the answer-or-defer decision jointly with expert cost and accuracy \[27\]. A calibrated small-LLM → large-LLM → human cascade needs only 100 calibration samples \[28\]. A factory field study found operators valued an LLM tool most on night shifts, when experts are scarce \[29\].

### E. Generated work instructions

LLM-generated assembly instructions have been explored at IEEE ETFA \[30\] and INDIN, the latter separating sequence planning from wording \[31\]. An LLM assembly assistant was evaluated with workers in *Computers in Industry* \[32\]. Jonek and Manns combine RAG with a controlled natural language, raising vocabulary compliance from 50% to 85% and cutting post-editing time from about 20 to about 12 minutes \[62\]; our schema and Simplified Technical English checks build on that result. Becker et al. draft assembly instructions with GPT-4o and RAG, have people score each draft on completeness, understandability, freedom from error and sequence, and feed the scores back each round; quality improved over the loops but never reached full compliance \[63\]. Their work has no revisions, change control, citations, safety checks or planted faults. Evaluating LLM-drafted instructions is therefore not new; what we found no prior work on is drafting *under change control*, measured by reviewers' detection of planted faults and by whether safety steps survive into the approved revision. The EU AI Act Art. 14 requires human oversight that guards against automation bias \[33\], which motivates our seeded-fault protocol.

### F. Benchmarks for RAG

RGB tests negative rejection and counterfactual robustness \[34\]. CRAG scores answers as accurate, missing or hallucinated with a penalty for hallucination \[35\]. LLM judges do only slightly better than random on hard knowledge pairs \[36\]. MACH-Bench adopts the RGB and CRAG scoring ideas and adds revision and procedural strata.

## III. Problem Formulation

**Corpus.** A controlled corpus D is a set of documents. Each document d has revisions r(d,1), r(d,2), … Each revision carries metadata m = (doc\_id, rev, status, t\_from, t\_to, scope, superseded\_by, access\_role), where scope is a set of (site, line, station, product, serial range) constraints and status ∈ {draft, in review, effective, superseded, obsolete}. A revision is parsed into elements e, each with an element ID, a type (text block, step, table cell, figure, callout), a page, a bounding box and a criticality label κ(e) ∈ {0: informational, 1: quality-critical, 2: safety-critical}.

**Effective set.** Given a query context c = (time t, scope s, user role u), the effective set is the set of elements a user may act on:

```latex
E(c) = \{\, e \in r : r.\mathrm{status} = \mathrm{effective},\; t_{\mathrm{from}}(r) \le t < t_{\mathrm{to}}(r),\; s \models r.\mathrm{scope},\; u \in r.\mathrm{access\_role} \,\}
```

A temporary deviation is modeled as a scoped, time-limited override of individual steps, not as a competing document. When a deviation is active, it replaces the steps it names within E(c).

**Answer.** For query q, the system returns either a response y or an escalation. A response is an ordered list of statements y = (y\_1, …, y\_n), each with a citation set C\_i of element IDs, plus a confidence score.

**Properties.** We require four properties. *Validity*: every cited element lies in E(c). *Revision coherence*: all citations for one document come from a single revision.

```latex
\mathrm{coherent}(y) \iff \forall d:\; |\{\, \mathrm{rev}(e) : e \in \textstyle\bigcup_i C_i,\; \mathrm{doc}(e) = d \,\}| \le 1
```

*Procedural completeness*: if y answers a procedural query, every safety-critical step (κ = 2) in the gold procedure appears in y, in the correct relative order. *Selective safety*: the probability of an unsupported statement about a step of criticality k is at most α\_k, with α\_2 < α\_1 < α\_0; otherwise the system escalates.

**Objective.** Subject to validity and coherence as hard constraints, M.A.C.H. maximizes answer accuracy and coverage while keeping tiered risk below α\_k and minimizing expert time. Validity and coherence are enforced by construction (Section IV-B); completeness and selective safety are measured (Section V).

## IV. The M.A.C.H. System

M.A.C.H. is a pipeline of six stages: ingestion, revision gate, hybrid retrieval, routing, grounded generation with verification, and escalation or drafting. Validity and access control are enforced before ranking, so no downstream model ever sees an element outside E(c).

&#91;embedded content: Fig. 1. M.A.C.H. architecture · query path and change-control loop\]

Fig. 1. The revision gate filters by effectivity, scope and role before any ranking. Answers pass a symbolic verifier and a per-tier risk gate; anything else escalates. Approved drafts re-enter the corpus as new effective revisions.

### A. Ingestion and the element graph

Each revision is rendered to page images at 150 dpi and parsed with a layout parser (Docling or PyMuPDF) into typed elements with bounding boxes. Tables are kept both as page regions and as markdown. Figures and tables receive VLM-written captions, which MMDocIR found improve text retrieval over OCR alone†. Steps are detected from numbering and imperative structure. Explicit cross-references ("see Fig. 3", "torque per Table 2", callout numbers) become edges in an element graph. A rule-plus-classifier labeler assigns criticality κ(e) from cues such as PPE, LOTO, WARNING/CAUTION blocks, torque and temperature parameters, and links to open quality alerts. Each page is tagged as scanned or born-digital. The corpus snapshot is hashed so every answer can be traced to a frozen state.

### B. Revision-safe retrieval (C1)

*Effectivity gate.* Every index entry carries the metadata m of Section III. The query context c is filled from the user session (site, line, station, role) and the clock, so the system never asks the LLM to guess a version. The gate applies E(c) as a hard pre-filter in every retrieval channel, before ranking. Superseded content can be retrieved only through an explicit history mode, and then always with a banner.

*Supersession statements.* For any document whose effective revision replaced an earlier one, the generator context includes a validity statement, for example: "WI-214 Rev B was superseded by Rev C on 2026-03-02 via ECN-014; Rev B must not be used for execution." Preprint evidence indicates that such explicit statements, unlike dates alone, let larger models switch almost perfectly to the current evidence† \[21\].

*Revision-coherence check.* After generation, a deterministic checker tests coherent(y) and validity for every citation. A violating answer is never shown. The system regenerates once with the offending elements removed and, if the check fails again, escalates. Because the check is symbolic, its guarantee does not depend on model behaviour.

*Conflict detector.* If two elements in E(c) give different values for the same parameter at the same scope (two effective documents that disagree), the system does not choose. It abstains, shows both sources and opens a document-control ticket.

### C. Three-channel hybrid retrieval

Channel 1 does exact matching on identifiers (part, tool, SOP, ECN numbers) after normalizing separators and case, following the identifier-fusion result of \[5\]. Channel 2 runs BM25 \[45\] and a dense text embedder over layout-aware chunks and captions. Channel 3 is a ColQwen2/ColPali page-image index with multi-vector MaxSim \[1\]. Scores are fused with reciprocal rank fusion \[46\] using weights tuned on the dev split, then reranked. After the first pass, cross-reference edges are followed one hop so that a step and the table it points to arrive together. A query can also be a shop-floor photo, embedded by the visual channel and captioned for the text channels.

### D. Query router (C4)

A lightweight classifier sends each query to one of four paths: *direct lookup* (identifier or single-value questions answered from a table cell), *single retrieval*, *multi-hop loop* (bounded to three iterations, stopping when a new retrieval returns no new element IDs), or *escalate immediately* (out-of-scope, disallowed or high-risk intent). Adaptive-RAG shows such routing preserves accuracy at much lower cost \[25\].

### E. Grounded generation with element-ID citation (C3)

The generator (Qwen2.5-VL-7B-Instruct, 4-bit AWQ, served locally with vLLM \[56\]) returns structured JSON: each statement or step carries the element IDs it relies on, the revision, and a support flag. Citing from a closed list of pre-parsed IDs turns visual grounding into classification, avoiding the weak zero-shot box drawing reported in \[15\]. A verifier then checks each statement. Numeric values, units, part numbers and tool IDs are checked by exact match against the cited element. Remaining text is checked by an NLI model for entailment. Unsupported statements are removed or flagged. The UI opens the cited page with the element's bounding box highlighted.

### F. Safety-tiered abstention and escalation (C4)

Each statement i receives a risk score from three signals: evidence sufficiency from a CRAG-style grader \[41\], verifier support, and semantic dispersion across k sampled answers \[44\]. Thresholds are calibrated per criticality tier with split-conformal calibration on the dev set, targeting risk α\_k for tier k \[12\], \[13\]. The deferral rule weighs expected harm against expert cost:

```latex
\text{escalate}(q) \iff \max_i \; \hat{p}_{\mathrm{err}}(y_i)\, w_{\kappa(y_i)} \;>\; \lambda \cdot \mathrm{cost}_{\mathrm{expert}}(t, s)
```

where w\_k is the harm weight of tier k and cost\_expert rises when fewer experts are on shift, making the system *more* conservative about answering when no expert can catch an error later. This is the expert-cost term of learning to defer \[27\] made concrete; the operator decides λ and w\_k, not the model. When only some steps are certified, the system returns those steps and "escalate for steps X–Y". The escalation ticket carries the query, evidence, and a ranked list of candidate answers. Expert replies are stored as dated, expiring "expert notes" with provenance, ranked below controlled documents, and reused as calibration labels.

### G. Work-instruction drafting under change control (C5)

Given a root-cause analysis (RCA) record or an ECN, a Drafter agent writes a WI revision into a schema (step, tool, torque, PPE, caution/warning, cited source). A Compliance agent checks the draft against the effective SOPs, required fields and a Simplified Technical English rule set, following the controlled-language approach of \[62\]. The draft enters a state machine (Draft → In review → Approved/Rejected → Published), is never auto-published, and on approval becomes a new effective revision that supersedes the old one, which closes the loop with Section IV-B. Every transition is logged with user and timestamp.

### H. Security and governance

Role-based access is applied in the effectivity gate, so restricted RCA content never reaches an operator's context. Ingested text is treated as data: instructions found inside documents are neutralized and flagged, since indirect prompt injection is a known attack on RAG \[47\]. Every query, retrieval set, answer, verification result and escalation is written to an append-only audit log. Deployment is edge-first. The whole answer path (index, three retrievers, reranker, revision gate, router, generator, verifier and escalation) runs on one plant-side GPU server, so safety answers never depend on the internet link and controlled documents never leave the plant. The cloud, where allowed, is used only offline: figure captioning at ingestion, synthetic query generation, router training and conformal recalibration. The latency budget is 15 s end to end; page embeddings and captions are precomputed, at most four page images go to the generator, multi-hop is capped at two rounds, and the first steps stream while the rest is generated.

## V. MACH-Bench and Metrics

### A. Corpus

No public corpus of shop-floor procedures with revisions exists, so MACH-Bench is built from public-domain documents that already carry real supersession: FAA Airworthiness Directives (each superseding AD names the AD it replaces and its effective date), FAA handbooks and advisory circulars with torque tables and figures, NHTSA service bulletins, iFixit repair guides with edit history (CC BY-NC-SA, linked rather than redistributed) and OSHA lockout/tagout material for safety steps. The corpus spans three product families, \[N\_d\] documents and \[N\_p\] pages; at least 15 documents have two or more revisions.

The core revision suite has about 100 items. Thirty to fifty are real FAA supersession cases, where the regulator states the gold answer. The rest are scripted counterfactual edits, following the method of RGB \[34\] and Xie et al. \[18\]: a changed parameter, an inserted safety step, swapped steps, a replaced part or tool number, a deleted step, a scoped temporary deviation by serial range, a separate change notice that alters one step, and a planted SOP–WI conflict. Each edited revision is re-rendered with the original layout, and every edit is logged in a changelog and tagged with the change taxonomy of \[59\] (Stable, Evolved, Added, Removed), so anyone can regenerate the suite and results can be split by change type. A share of pages is rasterized with scan noise (skew, blur, JPEG artefacts) so results can be split by scanned and born-digital pages. If LTTS or a partner plant shares real SOPs under NDA, they form a private held-out test reported separately. The snapshot is frozen with a SHA-256 hash per file.

### B. Queries and labels

Queries are written from realistic operator, maintenance and quality-engineer questions, plus LLM-proposed questions edited by a person. Each item has a gold answer, *every* supporting element ID (multi-gold), the expected behaviour (answer, abstain or escalate) and, for procedures, the ordered steps with critical parameters and criticality labels. Two annotators with domain knowledge label at least 25% of items, and we report Krippendorff's α. Splits are 30% dev and 70% test; prompts and thresholds are tuned only on dev.

| Stratum | Share of queries | Purpose |
| --- | --- | --- |
| Text lookup | \[x\]% | Baseline capability |
| Table lookup (torques, settings) | \[x\]% | Exact values, identifier matching |
| Diagram or photo evidence | \[x\]% | Tests visual retrieval |
| Cross-reference / multi-hop | \[x\]% | Tests graph expansion and the multi-hop path |
| Procedural sequence | \[x\]% | Order fidelity and safety-step recall |
| Identifier / part number | \[x\]% | Known BM25 strength |
| Superseded-revision trap | \~10% | Validity (C1) |
| Mixed-revision trap | \[x\]% | Revision coherence (C1) |
| Unanswerable | 10–15% | Abstention (C4) |
| Conflicting effective sources | \[x\]% | Conflict detector |
| Adversarial / injection | \[x\]% | Robustness and security |
| WI drafting tasks | \[N\_wi\] tasks | Change-control evaluation (C5) |

### C. Metrics

*Retrieval.* Recall@5/10, nDCG@10 and MRR over graded multi-gold labels, plus per-query win/loss against BM25 to expose any fusion tax.

*Answers.* CRAG-style accurate / missing / hallucinated labels with score = accurate − hallucinated \[35\]; ALCE citation precision and recall \[6\]; RAGAS faithfulness \[10\].

*Revision safety (C1).* The superseded-citation rate (SCR) is the share of answers citing any element outside E(c). The mixed-revision answer rate is

```latex
\mathrm{MRA} = \frac{1}{|Q|} \sum_{q \in Q} \mathbb{1}[\neg\,\mathrm{coherent}(y_q)]
```

The *metadata-aware misgrounding rate* counts citations whose text supports the claim but whose revision, product variant or site does not match the context, extending the legal definition \[16\].

*Procedural attribution (C3).* For a procedural query with gold steps G and predicted steps P: per-step support is the share of predicted steps entailed by their cited elements; order fidelity is Kendall τ over the steps in both G and P; and safety-step recall is

```latex
\mathrm{SSR} = \frac{|\{ g \in G : \kappa(g) = 2,\; g \text{ matched in } P \}|}{|\{ g \in G : \kappa(g) = 2 \}|}
```

Parameter exact-match covers torques, temperatures, tool IDs and part numbers, checked deterministically. Element-ID accuracy measures visual citations.

*Abstention and escalation (C4).* Abstention precision and recall on unanswerable items; over-abstention on answerable items; risk–coverage curves overall and per criticality tier; area under the risk–coverage curve (AURC); escalation rate; and expert minutes per 100 queries.

*Drafting (C5).* The four reviewer criteria of \[63\] (completeness, understandability, freedom from error, sequence) as the quality rubric; safety-step survival (the share of source safety steps present in the approved draft); STE and schema rule violations; reviewer accept / minor-edit / reject rates; normalized edit distance to the approved version; time to approve; and seeded-fault detection rate in blinded review.

*Operations.* p50 and p95 end-to-end latency, first-stage retrieval latency, and cost per query.

### D. Judging protocol

Safety-critical values are never judged by an LLM; they are checked by exact match. For free text, the LLM judge comes from a different model family than the generator \[36\], runs three times with shuffled answer order, and is validated against at least 100 human-labeled items with Cohen's κ reported. ARES-style prediction-powered inference corrects the judge's estimates and gives confidence intervals \[11\].

## VI. Experimental Setup

### A. Systems compared

All systems share the same generator, top-k, context budget and corpus snapshot, so differences come from retrieval and control logic alone.

| ID | System | What it isolates |
| --- | --- | --- |
| B1 | BM25 retrieval only (top passage shown) | Keyword search as used today |
| B2 | BM25 + LLM | Generation over lexical retrieval |
| B3 | Dense text RAG over OCR/parsed text | The standard text-only RAG baseline |
| B4 | Hybrid BM25 + dense with reranking | Strong text-only baseline |
| B5 | B4 + metadata date sorting | "Newest first" without effectivity |
| M | Full M.A.C.H. | All contributions |

**Public benchmarks.** Every contribution except drafting is also tested on peer-reviewed public benchmarks with published baselines. We sample 200–500 items from each so all runs finish within hours, and use the official scoring code where it exists.

| Benchmark | Venue | Tests | Contribution |
| --- | --- | --- | --- |
| MMLongBench-Doc \[49\] | NeurIPS 2024 D&B | Long PDFs with charts, tables, figures; unanswerable items | Multimodal retrieval, abstention |
| SlideVQA \[50\] | AAAI 2023 | Reasoning over slide images | Multimodal retrieval |
| E-Manual QA \[51\] | Findings of EMNLP 2021 | Questions over a real product manual | Closest public match to SOPs |
| ALCE-ASQA \[6\] | EMNLP 2023 | Citation precision and recall | C3 |
| RGB \[34\] | AAAI 2024 | Negative rejection, counterfactual robustness | C4, C1 proxy |
| WikiContradict \[52\] | NeurIPS 2024 D&B | Real contradictions between retrieved passages | Conflict detector (C1) |
| FreshQA \[20\] | Findings of ACL 2024 | Answers that change over time | C1 proxy |
| MuSiQue \[53\], HotpotQA \[54\] | TACL 2022, EMNLP 2018 | Multi-hop QA, the Adaptive-RAG setup \[25\] | Router (C4) |

### B. Ablations

We remove one component at a time from M: (A1) visual channel, (A2) identifier channel, (A3) cross-reference expansion, (A4) effectivity gate, (A5) supersession statements, (A6) revision-coherence check, (A7) verifier, (A8) router (always single retrieval), (A9) tiered calibration (one global threshold), (A10) expert-availability term, and (A11) schema and STE constraints in drafting (free generation).

### C. Robustness and edge-case suite

Beyond the benchmark strata, we run a scripted suite of 55 edge cases (365 paraphrased items) in 14 families: revision conflicts and mixed revisions, temporary deviations, scope and variant mismatches, missing or partial evidence, conflicting effective sources, adversarial and prompt-injection queries, degraded scans, access control, missing or partial evidence, multilingual and code-mixed queries, query-by-photo, escalation failures, drafting faults, and operations (load, outages, index rebuilds, audit replay). Each case has a pass criterion that is checked automatically where possible. The full suite is in the companion test plan (Appendix A).

### D. Implementation

Parsing uses Docling with rules for step numbering, producing stable element IDs of the form doc:rev:page:element. The visual channel uses ColQwen2.5 in Qdrant with multi-vector MaxSim; the text channel uses BM25 and BGE-M3; reranking uses bge-reranker-v2-m3. The generator is Qwen2.5-VL-7B-Instruct \[55\] in 4-bit AWQ, served with vLLM \[56\] on one 24 GB GPU (RTX 4090 class) alongside the retrievers. To test whether a larger model is worth its latency, we repeat the main runs with Qwen2.5-VL-32B-Instruct on a 48 GB GPU. The router is a small classifier (DeBERTa-v3-small) trained on 1,500–3,000 automatically labeled queries; fusion weights are fit by grid search and conformal thresholds are calibrated per tier on the dev split. No generator fine-tuning is done. The verifier uses \[NLI model\]; the judge uses \[model from a different family\]. Code, scripts, MACH-Bench items and prompts will be released at \[URL\] under \[license\].

### E. Statistics

All comparisons are paired per query. We report 95% confidence intervals from a paired bootstrap with 10,000 resamples, use a permutation test for differences in proportions and Wilcoxon signed-rank for ordinal scores, and apply a Holm correction across the comparisons against M. We report effect sizes, not only p-values.

### F. Human studies

*Timed task study.* \[N\_p\] participants with shop-floor or engineering background answer 10 questions each, in counterbalanced order, using B1 and M. We record minutes per correct answer and errors on safety-critical items.

*Seeded-fault study (C5).* For \[N\_wi\] drafting tasks we prepare drafts with planted faults: a wrong torque, a missing warning, a reordered step, a wrong tool ID and a reference to a superseded revision. Reviewers, blind to which drafts contain faults and to which drafts are machine-generated, approve or reject each draft. The primary outcome is the fault detection rate; we compare drafts with and without M.A.C.H.'s compliance annotations to measure whether the checker reduces or increases automation bias.

## VII. Results

> **Placeholder section.** Every cell marked \[ \] is filled from the experiment runs. The hypotheses (H1–H6) are stated now so the paper reports them whether they hold or not. Do not adjust a hypothesis after seeing results.

**Hypotheses.** H1: M beats B3 and B4 on diagram and table strata, and is no worse than B1 on identifier queries. H2: the effectivity gate and coherence check bring SCR and MRA to zero on trap items, while B5 does not. H3: M has higher safety-step recall than B4 at equal coverage. H4: tiered calibration lowers safety-tier risk at a fixed overall coverage compared with one global threshold. H5: reviewers detect more seeded faults when drafts carry compliance annotations. H6: M's p95 latency stays under 15 s on one 24 GB GPU. H7: the revision-safety metrics (SCR, MRA) of the 7B local model match those of a 32B model, because the gate and checks are deterministic.

### Public benchmarks (Table I)

| Benchmark | Metric | B2 BM25 + LLM | B3 Dense text | B4 Hybrid | M (7B) | M (32B) | Best published |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MMLongBench-Doc | Acc. / F1 | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| SlideVQA | EM / F1 | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| E-Manual QA | EM / F1 | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| ALCE-ASQA | Cit. P / R | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| RGB | Rejection rate | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| WikiContradict | Conflict flagged | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| FreshQA | Strict acc. | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[cite\] |
| MuSiQue + HotpotQA | F1 / time vs single-step | n/a | n/a | n/a | \[ \] | \[ \] | Adaptive-RAG \[25\] |

Published numbers use different generators, so the comparison against them is indicative; the controlled comparison is between columns B2–M, which share one generator.

### A. Retrieval (Table II)

| System | R@5 | R@10 | nDCG@10 | MRR | Wins / losses vs BM25 |
| --- | --- | --- | --- | --- | --- |
| B1 BM25 | \[ \] | \[ \] | \[ \] | \[ \] | — |
| B3 Dense text | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| B4 Hybrid + rerank | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| M (visual + text + ID + xref) | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |

A figure breaks R@5 down by stratum (text, table, diagram, cross-reference, identifier) and by scanned versus born-digital pages. \[Figure 3 placeholder\]

### B. Answers and revision safety (Table III)

| System | Accurate | Hallucinated | CRAG score | Cit. P / R | SCR | MRA | Misgrounding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B2 BM25 + LLM | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| B3 Dense text RAG | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| B4 Hybrid | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| B5 Hybrid + date sort | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| M | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |

### C. Procedural attribution (Table IV)

| System | Per-step support | Kendall τ | Safety-step recall | Parameter exact match | Element-ID accuracy |
| --- | --- | --- | --- | --- | --- |
| B4 | \[ \] | \[ \] | \[ \] | \[ \] | n/a |
| M | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |

### D. Abstention and escalation

Risk–coverage curves overall and per criticality tier, for M with tiered calibration versus a single threshold (A9). \[Figure 4 placeholder\] AURC: \[ \] vs \[ \]. Abstention precision / recall on unanswerable items: \[ \] / \[ \]. Over-abstention on answerable items: \[ \]. Expert minutes per 100 queries: \[ \] (day shift) and \[ \] (night shift).

### E. Ablations (Table V)

| Removed | Δ Accurate | Δ SCR | Δ MRA | Δ SSR | Δ p95 latency |
| --- | --- | --- | --- | --- | --- |
| A1 Visual channel | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A3 Cross-ref expansion | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A4 Effectivity gate | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A5 Supersession statements | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A6 Coherence check | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A7 Verifier | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |
| A8 Router | \[ \] | \[ \] | \[ \] | \[ \] | \[ \] |

### F. Edge-case suite, drafting and human studies

Pass rate per edge-case family (Table VI): \[ \]. Drafting: accept / minor edit / reject \[ \] / \[ \] / \[ \]; normalized edit distance \[ \]; seeded-fault detection \[ \] with annotations versus \[ \] without. Timed study: minutes per correct answer \[ \] with B1 versus \[ \] with M. Latency p50 / p95: \[ \] / \[ \] s; cost per query \[ \].

### G. Failure analysis

We will report three or four failure cases in full, with the query, retrieved evidence, answer and root cause. \[placeholder\]

## VIII. Discussion

### A. What the guarantees do and do not cover

Validity and revision coherence are enforced symbolically, so they hold whatever the model does, *provided the metadata is correct*. A revision registered with the wrong effectivity date defeats the gate. M.A.C.H. therefore moves the risk from the model to document control, where existing ISO 9001 processes already audit it. Conformal thresholds give a stated bound only when calibration and live queries are exchangeable. A new machine, a new product variant or a large SOP revision breaks that assumption, so we recalibrate after each effective-set change and present the result as a demonstrated design, not a certified guarantee.

### B. Limitations

MACH-Bench is small and partly synthetic, and it covers one assembly cell. Results may not transfer to process industries, pharmaceutical GMP or aerospace maintenance. Criticality labels come from rules and a classifier and can miss an implicit hazard. Element-ID citation depends on layout-parser quality, which degrades on poor scans. Human studies use few participants, and the timed study measures participants who are not always plant operators.

### C. Threats to validity

*Internal.* The team that built the system also wrote the benchmark. We mitigate this by freezing the test split before tuning, having an outside reviewer with plant experience audit \[x\]% of items, and reporting dev and test results separately. *Construct.* LLM judges are unreliable on knowledge-heavy items \[36\]; we keep safety-critical values out of LLM judging and report judge–human agreement. *External.* Synthetic documents are cleaner and more consistent than real ones; we report results on any real documents separately. *Conclusion.* With a few hundred items, small differences will not be significant; we report intervals and pre-state hypotheses.

### D. Novelty claims and search scope

Our search covered ACL, ICLR, NeurIPS, ICML, CVF, AAAI and arXiv thoroughly, but IEEE Xplore and ScienceDirect manufacturing journals only partly. Every "first" in this paper means "we found no prior work". A second pass over IEEE, ACM and Scopus-indexed venues through OpenAlex found HoH \[58\], Morita et al. \[59\], DesignQA \[60\] and Jonek and Manns \[62\]; our claims are worded to exclude what they cover. IEEE Xplore and ScienceDirect full texts were still not read. Several directly relevant results are preprints (†) and have not been replicated.

### E. Ethics and deployment

M.A.C.H. assists people and never replaces document approval: drafts are never auto-published, and escalation is the default under uncertainty. Field work reports that factory assistants can create contribution burden and surveillance concerns for operators \[29\]. Query logs are therefore used for system improvement, not for individual performance assessment, and a deployment should agree this with worker representatives. Sending controlled documents to a cloud LLM raises IP and data-residency questions; the on-premises open-weight path addresses them.

## IX. Conclusion

General-purpose RAG optimizes for answers that look right. Shop floors need answers that are valid at this station today, complete in their safety steps, and withheld when the evidence is not enough. M.A.C.H. enforces validity and revision coherence by construction, measures procedural completeness at step level, calibrates abstention by hazard tier, and evaluates drafted instructions by whether reviewers catch planted faults. MACH-Bench makes these properties measurable. The result that matters is not a higher average score than BM25 but \[R: zero superseded citations, safety-step recall of x, and y expert minutes per 100 queries\], on a benchmark that did not exist before. Future work covers real multi-plant corpora, query-by-photo at scale, and a controlled field trial measuring first-time-fix rate.

## Appendix A. Evaluation and edge-case test plan

The full test plan, with 12 families, each case's input and pass criterion, is a companion document: \[M.A.C.H. evaluation and edge-case test plan\](https://claude.ai/artifact/SXXQi4b9uN4yVPwc2npz1L). For the camera-ready version, include its two case tables here as Tables A1 and A2.

## References

† = arXiv preprint, not peer-reviewed. ‡ = cited from memory, not checked in the literature review; verify before submission. Convert to IEEE format with full author lists and pages from each venue page.

1. M. Faysse *et al.*, "ColPali: Efficient document retrieval with vision language models," ICLR 2025 (venue confirmed only via [ICLR slides](https://www.iclr.cc/media/iclr-2025/Slides/27679_RMItJE2.pdf)); [arXiv:2407.01449](https://arxiv.org/abs/2407.01449).
2. S. Yu *et al.*, "VisRAG: Vision-based retrieval-augmented generation on multi-modality documents," [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3640a1997a4c9571cea9db2c82e1fc35-Abstract-Conference.html).
3. X. Ma *et al.*, "Unifying multimodal retrieval via document screenshot embedding," [EMNLP 2024](https://aclanthology.org/2024.emnlp-main.373).
4. J. Zhang *et al.*, "OCR hinders RAG: Evaluating the cascading impact of OCR on RAG," [ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html).
5. Ludwig, Schmidt, Kühn, "An ontology-based RAG procedure for a voice-controlled maintenance assistant," *Computers in Industry*, vol. 169, 2025, [doi:10.1016/j.compind.2025.104289](https://www.sciencedirect.com/science/article/pii/S0166361525000545).
6. T. Gao, H. Yen, J. Yu, D. Chen, "Enabling large language models to generate text with citations," [EMNLP 2023](https://preview.aclanthology.org/setup/2023.emnlp-main.398).
7. A. Asai *et al.*, "Self-RAG: Learning to retrieve, generate, and critique through self-reflection," [ICLR 2024](https://iclr.cc/virtual/2024/poster/18095).
8. M. Song *et al.*, "Measuring and enhancing trustworthiness of LLMs in RAG through grounded attributions and learning to refuse," [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4c88827decab6c046b881a2c3a99c76f-Abstract-Conference.html).
9. Y. Li, X. Yue, Z. Liao, H. Sun, "AttributionBench," [Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.886).
10. S. Es, J. James, L. Espinosa-Anke, S. Schockaert, "RAGAs: Automated evaluation of retrieval augmented generation," [EACL 2024 Demos](https://preview.aclanthology.org/naacl24-info/2024.eacl-demo.16).
11. J. Saad-Falcon, O. Khattab, C. Potts, M. Zaharia, "ARES," [NAACL 2024](https://preview.aclanthology.org/setup/2024.naacl-long.20).
12. C. Mohri, T. Hashimoto, "Language models with conformal factuality guarantees," [ICML 2024](https://proceedings.mlr.press/v235/mohri24a.html).
13. M. Kang *et al.*, "C-RAG: Certified generation risks for retrieval-augmented language models," ICML 2024, [arXiv:2402.03181](https://arxiv.org/pdf/2402.03181).
14. B. Wen *et al.*, "Know your limits: A survey of abstention in large language models," [TACL 2025](https://transacl.org/index.php/tacl/article/view/7077).
15. X. Ma *et al.*, "VISA: Retrieval augmented generation with visual source attribution," [ACL 2025](https://preview.aclanthology.org/setup/2025.acl-long.1456).
16. V. Magesh *et al.*, "Hallucination-free? Assessing the reliability of leading AI legal research tools," *J. Empirical Legal Studies*, vol. 22, pp. 216–242, 2025, [PDF](https://nlp.stanford.edu/~manning/papers/Magesh-Hallucination%E2%80%90Free-2025.pdf).
17. R. Xu *et al.*, "Knowledge conflicts for LLMs: A survey," [EMNLP 2024](https://aclanthology.org/2024.emnlp-main.486/).
18. J. Xie *et al.*, "Adaptive chameleon or stubborn sloth," ICLR 2024, [arXiv:2305.13300](https://arxiv.org/abs/2305.13300v4).
19. J. Kasai *et al.*, "RealTime QA: What's the answer right now?," [NeurIPS 2023 D&B](https://keisuke-sakaguchi.github.io/assets/pdf/2023_neurips_realtimeqa.pdf).
20. T. Vu *et al.*, "FreshLLMs: Refreshing large language models with search engine augmentation," [Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.813.pdf).
21. † Ahmed, Galke Poech, Röttger, "Stale-document poisoning," 2026, [alphaXiv:2609.31342](https://www.alphaxiv.org/abs/2609.31342).
22. † Huwiler, Stockinger, Fürst, "VersionRAG," 2025, [alphaXiv:2510.08109](https://www.alphaxiv.org/abs/2510.08109).
23. C. Bock, A. Barnard Feeney, "Engineering change management concepts for systems modeling," NIST IR 7922, 2013, [PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913323).
24. ISO 9001:2015, *Quality management systems — Requirements*, §7.5 (check clause text against the standard).
25. S. Jeong *et al.*, "Adaptive-RAG," [NAACL 2024](https://aclanthology.org/2024.naacl-long.389).
26. H. Trivedi *et al.*, "Interleaving retrieval with chain-of-thought reasoning," [ACL 2023](https://aclanthology.org/2023.acl-long.557).
27. H. Mozannar, D. Sontag, "Consistent estimators for learning to defer to an expert," [ICML 2020](https://proceedings.mlr.press/v119/mozannar20b/mozannar20b.pdf).
28. C. Fanconi, M. van der Schaar, "Cascaded language models for cost-effective human–AI decision-making," [NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/file/10e0c427408ccc6e073d9464e2280f89-Paper-Conference.pdf).
29. S. Kernan Freire *et al.*, "Knowledge sharing in manufacturing using LLM-powered tools," *Frontiers in AI*, vol. 7, 2024, [PDF](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1293084/pdf).
30. Meyer, Freitag, Hinrichsen, Niggemann, "Potentials of LLMs for generating assembly instructions," IEEE ETFA 2024, [doi:10.1109/etfa61755.2024.10710806](https://doi.org/10.1109/etfa61755.2024.10710806).
31. Widulle, Meyer, Niggemann, "Generating assembly instructions using reinforcement learning with LLMs," IEEE INDIN 2024, [doi:10.1109/indin58382.2024.10774545](https://doi.org/10.1109/indin58382.2024.10774545).
32. Colabianchi, Costantino, Sabetta, "Assessment of a large language model based digital intelligent assistant in assembly manufacturing," *Computers in Industry*, 2024, [doi:10.1016/j.compind.2024.104129](https://doi.org/10.1016/j.compind.2024.104129).
33. Regulation (EU) 2024/1689 (AI Act), [Art. 14](https://euaiact.com/article/14).
34. J. Chen, H. Lin, X. Han, L. Sun, "Benchmarking LLMs in retrieval-augmented generation," [AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29728/31250).
35. X. Yang *et al.*, "CRAG — Comprehensive RAG benchmark," [NeurIPS 2024 D&B](https://proceedings.neurips.cc/paper_files/paper/2024/file/1435d2d0fca85a84d83ddcb754f58c29-Paper-Datasets_and_Benchmarks_Track.pdf).
36. S. Tan *et al.*, "JudgeBench," [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/9e720fce64f91114c49cfd640d821da3-Paper-Conference.pdf).
37. Siouffi, Glandon, Kubler, Soumianarayanan, "SEASONED," *Procedia CIRP*, vol. 134, 2025, [PDF](https://orbilu.uni.lu/bitstream/10993/65242/1/1-s2.0-S2212827125006158-main.pdf).
38. A. Kamath, R. Jia, P. Liang, "Selective question answering under domain shift," [ACL 2020](https://aclanthology.org/2020.acl-main.503).
39. † Loison *et al.*, "ViDoRe V3," 2026, [alphaXiv:2601.08620](https://www.alphaxiv.org/abs/2601.08620).
40. W. Shi *et al.*, "Trusting your evidence: Context-aware decoding," [NAACL 2024](https://aclanthology.org/2024.naacl-short.69/).
41. † S. Yan, J. Gu, Y. Zhu, Z. Ling, "Corrective retrieval augmented generation," 2024, [arXiv:2401.15884](https://arxiv.org/pdf/2401.15884).
42. † Akarsu, Karaman, Mierbach, "From BM25 to corrective RAG," 2026, [alphaXiv:2604.01733](https://www.alphaxiv.org/abs/2604.01733).
43. † De Grandis *et al.*, "DocAttriBench," 2026, [arXiv:2609.20574](https://arxiv.org/pdf/2609.20574).
44. S. Farquhar, J. Kossen, L. Kuhn, Y. Gal, "Detecting hallucinations in large language models using semantic entropy," *Nature*, vol. 630, 2024, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11186750).
45. ‡ S. Robertson, H. Zaragoza, "The probabilistic relevance framework: BM25 and beyond," *Found. Trends Inf. Retr.*, 2009.
46. ‡ G. Cormack, C. Clarke, S. Büttcher, "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods," SIGIR 2009.
47. ‡ K. Greshake *et al.*, "Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection," ACM AISec 2023.
48. † Ha, Islam, Nanda, Lercel, "Multimodal RAG for Cessna 172 maintenance manual," 2026, [alphaXiv:2608.18465](https://www.alphaxiv.org/abs/2608.18465).

Additional references added with the benchmark and model choices (‡ verify every detail before submission):

&#91;49\] ‡ Y. Ma *et al.*, "MMLongBench-Doc: Benchmarking long-context document understanding with visualizations," NeurIPS 2024 Datasets and Benchmarks.

&#91;50\] ‡ R. Tanaka *et al.*, "SlideVQA: A dataset for document visual question answering on multiple images," AAAI 2023.

&#91;51\] ‡ A. Nandy *et al.*, "Question answering over electronic devices: A new benchmark dataset and a multi-task learning based QA framework," Findings of EMNLP 2021.

&#91;52\] ‡ Y. Hou *et al.*, "WikiContradict: A benchmark for evaluating LLMs on real-world knowledge conflicts from Wikipedia," NeurIPS 2024 Datasets and Benchmarks.

&#91;53\] ‡ H. Trivedi *et al.*, "MuSiQue: Multihop questions via single-hop question composition," TACL, 2022.

&#91;54\] ‡ Z. Yang *et al.*, "HotpotQA: A dataset for diverse, explainable multi-hop question answering," EMNLP 2018.

&#91;55\] ‡ Qwen Team, "Qwen2.5-VL technical report," arXiv, 2025.

&#91;56\] ‡ W. Kwon *et al.*, "Efficient memory management for large language model serving with PagedAttention," ACM SOSP 2023.

&#91;57\] Federal Aviation Administration, Airworthiness Directives, Dynamic Regulatory System (public domain).

&#91;58\] Ouyang *et al.*, "HoH: A dynamic benchmark for evaluating the impact of outdated information on retrieval-augmented generation," [ACL 2025](https://aclanthology.org/2025.acl-long.301).

&#91;59\] Morita, Sanderson, Hewitt, "Longitudinal-aware evaluation of RAG over evolving credit policy documents," [EMNLP 2026 Industry](https://aclanthology.org/2026.emnlp-industry.40/).

&#91;60\] Doris *et al.*, "DesignQA: A multimodal benchmark for evaluating large language models' understanding of engineering documentation," *J. Computing and Information Science in Engineering*, 2024, [doi:10.1115/1.4067333](https://doi.org/10.1115/1.4067333).

&#91;61\] † Lin, Zhu, Zhang, Wen, "SOPRAG: Multi-view graph experts retrieval for industrial SOPs," 2026, [arXiv:2602.01858](https://arxiv.org/abs/2602.01858).

&#91;62\] Jonek, Manns, "Leveraging LLM for assembly instructions using controlled natural language," CARV 2025, LNME, Springer, 2026, [doi:10.1007/978-3-032-16889-4\_64](https://doi.org/10.1007/978-3-032-16889-4_64).

&#91;63\] Becker, Adrian, Green, Hinrichsen, "Evaluating feedback mechanisms in the automatic creation of assembly instructions using RAG," *Procedia CIRP*, 2026, [doi:10.1016/j.procir.2026.03.242](https://doi.org/10.1016/j.procir.2026.03.242) vol. 146, pp. 243–248.

&#91;64\] Zennir, El Gourari, Raoufi, Skouri, "Multimodal RAG and fine-tuned LLMs for enhanced understanding of electrical concepts," GAST 2026, IEEE (Xplore document 11523239).
