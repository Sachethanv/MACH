# Supersession, Versioning, Temporal Validity and Conflicting Knowledge in RAG (for M.A.C.H.)

> Method note: the OpenAlex-backed reference tools (search_works / verify_reference) returned "Tunnel connection failed: 403 Forbidden" for every call in this session, so **no entry below was verified through OpenAlex**. Papers were found through WebSearch, ACL Anthology / NeurIPS / publisher pages (WebFetch), and alphaXiv. The venue and authors given are those shown on the fetched landing page or PDF. Where I saw only a search-result title, the entry says "title/venue from search result only; details not read". arXiv-only items are labelled **[arXiv, not peer-reviewed]**. Search date: 2026-11-05.

## Q1. How do LLMs behave when retrieved passages conflict or are outdated, and which mitigations work?

### Takeaway
Peer-reviewed work agrees on four points. LLMs readily follow coherent retrieved context, even when it contradicts what they already know. They show confirmation bias when the evidence is mixed. They fall back on stale parametric answers when retrieval is insufficient. Decoding- and prompt-level mitigations help only modestly. The newest (2026, arXiv) results are the most relevant to M.A.C.H.: a single outdated document overturns 17–91% of otherwise-correct answers, and telling the model *explicitly when old evidence stops applying* almost fully fixes this in larger models. Validity metadata, not just recency, is therefore the key lever.

### Cited Findings

**Taxonomy / surveys**
- Xu, Qi, Guo, Wang, Wang, Zhang, Xu (2024), "Knowledge Conflicts for LLMs: A Survey," *EMNLP 2024* (Main), pp. 8541–8565, DOI 10.18653/v1/2024.emnlp-main.486. Peer-reviewed. Sorts conflicts into three types: **context–memory** (retrieved text vs parametric knowledge), **inter-context** (retrieved passages disagree with each other; for M.A.C.H. this is Rev B vs Rev C, or SOP vs deviation), and **intra-memory**. It covers causes, model behaviour, and solutions, with misinformation and noise as drivers. — [ACL Anthology](https://aclanthology.org/2024.emnlp-main.486/); companion repo [GitHub](https://github.com/pillowsofwind/Knowledge-Conflicts-Survey)

**Behaviour under conflict**
- Xie, Zhang, Chen, Lou, Su (2024), "Adaptive Chameleon or Stubborn Sloth: Revealing the Behavior of Large Language Models in Knowledge Conflicts," *ICLR 2024* (arXiv 2305.13300). Peer-reviewed (ICLR 2024, per [chatpaper listing](https://chatpaper.com/paper/5828)). LLMs are highly receptive to coherent, convincing external evidence that contradicts their memory. When the evidence is mixed (some supporting memory, some not), they show strong **confirmation bias** toward their parametric belief. — [arXiv](https://arxiv.org/abs/2305.13300v4)
- Kasai, Sakaguchi, Takahashi, Le Bras, Asai, Yu, Radev, Smith, Choi, Inui (2023), "RealTime QA: What's the Answer Right Now?", *NeurIPS 2023* (Datasets & Benchmarks). Peer-reviewed. Covers June 2022–June 2023:
  - Open-book GPT-3 with up-to-date Google search: **66.5%** multiple-choice accuracy and **34.6 EM** on generation.
  - Closed-book GPT-3: 44.9% / 15.3 EM.
  - GPT-3 with Wikipedia DPR retrieval (a stale corpus): 43.9% / 13.3, i.e. no better than closed-book.
  - When retrieved docs are insufficient, GPT-3 **falls back to outdated answers** (e.g. it answered "Andrew Cuomo" when the correct answer was "Boris Johnson").
  - Error analysis: 52% correct, **34% retrieval errors**, 13% reading errors, so retrieval is the bottleneck.
  - [PDF](https://keisuke-sakaguchi.github.io/assets/pdf/2023_neurips_realtimeqa.pdf)
- Vu, Iyyer, Wang, Constant, Wei, Wei, Tar, Sung, Zhou, Le, Luong (2024), "FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation," *Findings of ACL 2024*, pp. 13697–13720. Peer-reviewed. Introduces **FreshQA** (600 questions: fast-changing, never-changing and false-premise). With **FreshPrompt** (dated search evidence ordered by date in the prompt):
  - GPT-4 reaches 77.6% (STRICT) / 79.0% (RELAXED). The paper reports the gain over vanilla GPT-4 as +47 / +31.4 points in §4.3 but as +49.0% / +32.6% in the introduction; the two sets of numbers are inconsistent within the paper.
  - GPT-3.5 goes from 26.0% to 56.0% (STRICT), beating Self-Ask (41.6%) and Perplexity.ai (52.2%).
  - [PDF](https://aclanthology.org/2024.findings-acl.813.pdf)

**Mitigations (peer-reviewed)**
- Shi, Han, Lewis, Tsvetkov, Zettlemoyer, Yih (2024), "Trusting Your Evidence: Hallucinate Less with Context-aware Decoding," *NAACL 2024* (short), DOI 10.18653/v1/2024.naacl-short.69. Peer-reviewed. CAD is a contrastive decoding method that amplifies the difference between output with context and output without it. It gives a **+14.3% factuality gain for LLaMA** on summarization and "substantial improvements" on knowledge-conflict tasks, with no training. Caveat for M.A.C.H.: CAD pushes the model toward *whatever* is in context, so it helps only if the context has already been filtered to the effective revision. — [ACL Anthology](https://aclanthology.org/2024.naacl-short.69/)
- Peer-reviewed follow-ups located by search (title/venue from the search result only; details not read):
  - "AdaCAD: Adaptively Decoding to Balance Conflicts…" (NAACL 2025) — [PDF](https://aclanthology.org/2025.naacl-long.581.pdf)
  - "Discerning and Resolving Knowledge Conflicts through…" (Findings of ACL 2024) — [PDF](https://aclanthology.org/2024.findings-acl.234.pdf)
  - "Conflict-Aware Soft Prompting for Retrieval-Augmented…" (EMNLP 2025) — [PDF](https://aclanthology.org/2025.emnlp-main.1371.pdf)

**Newest work on outdated or superseded evidence [arXiv, not peer-reviewed]**
- Ahmed, Galke Poech, Röttger (2026), "Stale-Document Poisoning: When Outdated Retrieval Overrides Correct Model Answers," arXiv 2609.31342 **[arXiv, not peer-reviewed]**. Builds a benchmark of 317 verified knowledge reversals (medicine, law, software, policy) from dated official sources, tested on 12 models.
  - Outdated retrieval flips **30% (Llama) / 37% (Qwen)** of otherwise-correct answers. "Follow the document" instructions raise this to **66% / 75%**.
  - Across domains, poisoning ranges **17–91%**, while matched up-to-date evidence is followed in **97–100%** of trials.
  - Giving dates alone produces only modest adaptation. *Explicitly stating when the old evidence stops applying* makes larger models switch "almost perfectly."
  - A recency-aware hybrid re-ranker cuts poisoning by only **4.6–10.0 points**, and only when the date metadata is accurate.
  - [alphaXiv](https://www.alphaxiv.org/abs/2609.31342)
- Other 2025–2026 arXiv work found via alphaXiv discovery, abstract snippets only — [alphaXiv search results](https://www.alphaxiv.org/abs/2506.08500):
  - "DRAGged into Conflicts: Detecting and Addressing Conflicting Sources in Search-Augmented LLMs" (Google Research / Bar-Ilan, 2025). Proposes a taxonomy of conflict types plus a benchmark. [arXiv, not peer-reviewed]
  - "Retrieved but Not Read" (Imperial, 2026, arXiv 2610.21731). Search-augmented LLMs give outdated answers even when the up-to-date evidence was retrieved. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2610.21731)
  - "Where and Why Search-Augmented LLMs Fail When Reasoning over Rapidly Evolving Knowledge" (Aarhus / MSR / TU Darmstadt, 2026, arXiv 2610.25323). [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2610.25323)
  - "EvoTrustRAG: Evolution-Aware Conflict Attribution…" (2026, arXiv 2608.07933). Separates *evolutionary* conflicts (outdated vs updated) from adversarial ones. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2608.07933)
  - "Does RAG Know When Retrieval Is Wrong? Diagnosing Context Compliance under Knowledge Conflict" (GaTech / CMU / UCSD, 2026, arXiv 2605.14473). [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2605.14473)
  - "Contradictions in Context: Challenges for RAG in Healthcare" (Deakin / RMIT, 2025, arXiv 2511.06668). An example of a high-stakes domain. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2511.06668)

### Inferences
- For M.A.C.H., "old revision" conflicts are *non-adversarial inter-context conflicts*: the outdated document is genuine, well-written and was authoritative when issued. That is exactly the case where Xie et al. show models are most persuadable, and where Ahmed et al. show the worst failure rates. Prompting the model to "use the latest document" is therefore not enough.
- Evidence points to fixing conflicts **before generation**: filter by effective status, or inject explicit "valid-until / superseded-by" statements into context. Ahmed et al. show the explicit statement works far better than raw dates. Decoding-level tricks such as CAD come second.
- RealTime QA's 34% retrieval-error share suggests that most of the gain comes from retrieving the correct revision, not from reasoning over a mix of revisions.

### Gaps
- No peer-reviewed knowledge-conflict benchmark uses *procedural* documents (step sequences, parameters, safety interlocks). All the benchmarks above are factoid or entity QA.
- I did not read the full numbers for AdaCAD, the Findings ACL 2024 "Discerning and Resolving" paper, or the EMNLP 2025 conflict-aware soft-prompting paper. Only titles and venues were confirmed.
- PoisonedRAG / misinformation-pollution papers (adversarial misinformation) were not located with a tool this session, so they are not cited.

## Q2. Methods and benchmarks for version-aware or time-aware retrieval

### Takeaway
Time-sensitive QA benchmarks (TimeQA, SituatedQA, RealTime QA, FreshQA) exist and show large gaps between models and humans. All of them model time as *real-world dates attached to facts*, not *document revisions with effectivity*. The only work found that explicitly targets versioned documents is VersionRAG (2025, arXiv). It shows naive RAG reaches 58% and GraphRAG 64% on version questions, versus 90% with an explicit version graph plus metadata filtering. That is the closest analogue to M.A.C.H.

### Cited Findings

**Temporal / time-sensitive QA benchmarks (peer-reviewed)**
- Chen, Wang, Wang (2021), "A Dataset for Answering Time-Sensitive Questions" (TimeQA), *NeurIPS 2021 Datasets & Benchmarks*. Peer-reviewed. The best model (FiD fine-tuned on NQ+TimeQA) scores **60.5 EM easy / 46.8 EM hard**, versus humans at 89.0 / 87.0. Models lose about 15 points from easy to hard, while humans lose about 2. — [PDF](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/1f0e3dad99908345f7439f8ffabdffc4-Paper-round2.pdf)
- RealTime QA (NeurIPS 2023) and FreshQA (Findings ACL 2024): see Q1 for numbers. RealTime QA performance stayed high for about 24 h after questions were released, then **degraded substantially**. This is a quantitative freshness half-life for a news corpus. — [RealTime QA PDF](https://keisuke-sakaguchi.github.io/assets/pdf/2023_neurips_realtimeqa.pdf)
- Peer-reviewed temporal QA methods (title/venue from search results only; details not read):
  - "Time-Aware Representation Learning for Time-Sensitive Question Answering" (Findings EMNLP 2023) — [ACL Anthology](https://aclanthology.org/2023.findings-emnlp.6/)
  - "Question Answering as Programming for Solving Time-Sensitive Questions" (EMNLP 2023) — [PDF](https://aclanthology.org/2023.emnlp-main.787.pdf)
  - "UnSeenTimeQA" (ACL 2025) — [PDF](https://aclanthology.org/2025.acl-long.94.pdf)

**Version-aware RAG**
- Huwiler, Stockinger, Fürst (2025), "VersionRAG: Version-Aware Retrieval-Augmented Generation for Evolving Documents," arXiv 2510.08109 (ZHAW) **[arXiv, not peer-reviewed]**.
  - Architecture: a hierarchical graph (Category → Document → Version → Content, plus Change nodes). Versions are linked by temporal edges. Explicit changes come from changelogs; implicit changes come from DeepDiff line diffs interpreted by an LLM.
  - Retrieval: an LLM query router classifies each query as content, version-listing or change. Vector search is restricted to the requested version's chunks through graph-based filtering.
  - Dataset: VersionQA, 100 QA pairs over 34 versioned technical documents (more than 700 pages).
  - Overall accuracy: **90% (DeepSeek-R1-70B) vs 58% naive RAG vs 64% GraphRAG**.
  - By query type:
    - Version-specific content: 100% vs 55% (naive RAG).
    - Version listing: 100% vs 35% (naive RAG) / 80% (GraphRAG).
    - Explicit changes: 80–90% vs 50–60%.
    - Implicit changes: 60% vs 0–10%.
  - Cost: indexing used **97% fewer tokens** than GraphRAG (186K vs 2.97M), about $0.17 vs $6.67, and 25 min vs 5.2 h.
  - Errors: 8% of the 10% error comes from query misclassification. Accuracy scales with router quality (Llama-3-8B 55%, GPT-4o-mini 79%).
  - [alphaXiv](https://www.alphaxiv.org/abs/2510.08109)
- 2026 temporal / version-RAG preprints found via alphaXiv (abstract snippets only) — [alphaXiv results](https://www.alphaxiv.org/abs/2609.11572):
  - "TimelyRAG: Semantic-Temporal Hybrid Retrieval for Time-Critical QA in Overlapping-Evolving Documents" (KAIST et al., arXiv 2609.11572). Targets documents that evolve through *amendments*. [arXiv, not peer-reviewed]
  - "IA-RAG: Interval-Algebra-Driven Temporal Reasoning for Dynamic Knowledge Retrieval" (ECNU / Shanghai AI Lab, arXiv 2606.06044). Uses Allen-style interval reasoning over validity periods in RAG and GraphRAG. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2606.06044)
  - "FRESCO: Benchmarking and Optimizing Re-rankers for Evolving Semantic Conflict in RAG" (Meta / UCLA, arXiv 2604.14227). Re-rankers versus stale passages. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2604.14227)
  - "Asking For An Old Friend: Temporal Failure Modes in LLM-based Statutory QA" (TUM, arXiv 2605.23497). Amended laws are the closest legal analogue to superseded SOPs. [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2605.23497)
  - "TEMPS: Temporal Sentence Embeddings for Temporal IR" (arXiv 2609.28048). [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2609.28048)
  - "CALM: Conflict-Aware Lifecycle Memory Governance" (HIT / Meituan, arXiv 2610.38573). Argues that a memory can be outdated for present-day reasoning yet still needed to reconstruct the past, which maps onto "answer from current revision, but keep the history auditable." [arXiv, not peer-reviewed] — [alphaXiv](https://www.alphaxiv.org/abs/2610.38573)

**Knowledge editing vs retrieval for updates**
- Ovadia, Brief, Mishaeli, Elisha (2024), "Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs," *EMNLP 2024*, DOI 10.18653/v1/2024.emnlp-main.15. Peer-reviewed. **RAG consistently outperforms unsupervised fine-tuning** for both previously seen and entirely new knowledge. LLMs struggle to learn new facts through fine-tuning; exposing them to many paraphrases of a fact partly helps. — [ACL Anthology](https://aclanthology.org/2024.emnlp-main.15/)

### Inferences
- For a shop floor where SOP revisions arrive weekly, editing weights (fine-tuning or model editing) is the wrong update path. Ovadia et al. show RAG wins even for new facts, and editing offers no rollback or audit trail. Updates should happen in the index and its metadata.
- VersionRAG's main lesson is that **a structured version layer (graph plus filters) beats both naive RAG and generic GraphRAG, at about 3% of GraphRAG's indexing cost.** For M.A.C.H., a lightweight "Document → Revision → Chunk" graph with SUPERSEDES / AMENDED_BY / DEVIATION_OF edges is likely a better choice than full entity-level GraphRAG.
- The weakest link in VersionRAG is query-intent routing (8 of 10 error points). Shop-floor queries rarely name a revision, so M.A.C.H. should default to "effective now at this site/line" rather than asking the LLM to infer the version.

### Gaps
- VersionQA is small (100 QA pairs) and software-only. There is no public benchmark of manufacturing SOP revisions, deviations or ECNs.
- None of the time-aware benchmarks models *effectivity* (valid from / valid to, scoped by site, line, part number or serial range), *temporary deviations* that override an SOP for a limited window, or *partial supersession* (an ECN that changes one step).
- Peer-reviewed knowledge-editing benchmarks (e.g. MQuAKE, ripple-effect evaluations) were not located with a tool this session, so they are not cited.

## Q3. How has engineering change management / document control been modelled computationally in manufacturing literature?

### Takeaway
ECM has a mature conceptual base: NIST formalised change requests, change orders, effectivity, configuration management, and the difference between versions and variants. Knowledge graphs are an established manufacturing research topic (Journal of Manufacturing Systems reviews 2023–2024). Specific KG/ontology work on *engineering change propagation* exists, but much of what I found is either preprint or only partly accessible. Industry document-control rules (ISO 9001 §7.5, 21 CFR 211.100) define exactly the behaviour M.A.C.H. must enforce, but I found no peer-reviewed work linking them to RAG.

### Cited Findings

**ECM concepts**
- Bock & Barnard Feeney (2013), "Engineering Change Management Concepts for Systems Modeling," **NIST IR 7922**. A government technical report, not a journal paper. It defines:
  - **change requests** (describe the situation, not the fix);
  - **change orders** (proposed specification changes, including when they take effect);
  - **urgency** classes and **impact / propagation analysis**;
  - a four-step process: evaluate urgency → develop change orders → determine impact → plan production, including effectivity;
  - **effectivity**, the period during which products are built to a given specification, which must be refined "so that products aren't built from accidental mixes of original and changed parts";
  - **configuration management**;
  - **versions** (successive, with earlier ones phased out) as distinct from **variants** (parallel options).
  - [NIST PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913323)

**ECM modelling papers (title/venue from search results only; details not read)**
- "Requirement-driven engineering change management in product design," *Computers & Industrial Engineering* (2022). Peer-reviewed. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0360835222001231)
- Yin, Sun, Lu, "Hierarchical Discovery of Engineering Change Propagation Paths on an Engineering Change Knowledge Graph: A Dual-Agent Reinforcement Learning Framework." **SSRN preprint, not peer-reviewed.** A direct example of an ECM knowledge graph. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6036374)
- "Change Propagation Analysis for System Modeling using Semantic Web technology." Venue not confirmed. — [ResearchGate](https://www.researchgate.net/publication/321849666_Change_Propagation_Analysis_for_System_Modeling_using_Semantic_Web_technology)
- "Towards a Universal Model of Engineering Change Management," *Journal of the Knowledge Economy* (Springer, 2023), DOI 10.1007/s13132-023-01576-3. Peer-reviewed. — [Springer](https://link.springer.com/article/10.1007/s13132-023-01576-3)

**Manufacturing knowledge-graph work (peer-reviewed; title/venue from search results only)**
- "Knowledge graph-based manufacturing process planning: A state-of-the-art review," *Journal of Manufacturing Systems* (2023). — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0278612523001577)
- "Making knowledge graphs work for smart manufacturing: Research topics, applications and prospects," *Journal of Manufacturing Systems* (2024). — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0278612524001572); [ResearchGate](https://www.researchgate.net/publication/382918442_Making_knowledge_graphs_work_for_smart_manufacturing_Research_topics_applications_and_prospects)
- "Ontology-based knowledge representation of industrial production workflow," *Advanced Engineering Informatics* (2023). Relevant for modelling SOP steps as ontology entities. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1474034623003130)
- "An ontology change management approach for facility management," *Computers in Industry* (2015). Seminal work on versioning the ontology itself. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0166361514001419)
- "An LLM-based knowledge and function-augmented approach for optimal design of remanufacturing process," *Advanced Engineering Informatics* (2025). LLM plus a manufacturing knowledge base. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1474034625000990)
- "Evolving to multi-modal knowledge graphs for engineering design: state-of-the-art and future challenges." Venue not confirmed. — [Semantic Scholar](https://www.semanticscholar.org/paper/Evolving-to-multi-modal-knowledge-graphs-for-and-Pan-Li/d7fb3fcc1897065b50ebdc0c01977d2dbda78d6e)

**Industry document control (normative requirements)**
- **ISO 9001:2015 §7.5.2** requires, when creating or updating documented information, identification (title, date, author, reference number), format, and review and approval before use. **§7.5.3** requires documented information to be "available and suitable for use where and when needed," with control of distribution, access, retrieval, use, storage, *control of changes (version control)*, and retention / disposition. External documents must also be controlled.
  - Audit practice: a correct master list does **not** satisfy the requirement if an obsolete work instruction is posted at a workstation. This is a common nonconformity against 7.5.3.1.
  - The summary is from a study guide, not the standard text. — [Open Exam Prep study guide](https://open-exam-prep.com/study-guides/cqi-irca-qms-lead-auditor/clauses-6-7/clause-7-documented-info); see also [Smithers summary](https://prd-b4f.smithers.com/resources/2026/february/smithers-summarizes-iso-9001-document-control)
- **21 CFR 211.100 (US cGMP)**
  - (a) "There shall be written procedures for production and process control." Changes must be drafted, reviewed and approved by the appropriate units and by the quality control unit.
  - (b) Procedures must be followed and documented at the time of performance; "Any deviation from the written procedures shall be recorded and justified."
  - [Cornell LII](https://www.law.cornell.edu/cfr/text/21/211.100)
- 21 CFR Part 11 (electronic records and signatures: audit trails, versioned records). I did not fetch the primary text this session. It is listed here for completeness only; cite it from eCFR in the final report.

### Inferences
- The regulatory "point-of-use" test in ISO 9001 7.5.3 is the requirement M.A.C.H. must meet: if the assistant cites an obsolete revision to an operator, that is equivalent to an obsolete paper copy at the workstation, which auditors treat as a nonconformity. The design requirement therefore comes from regulation, not only from accuracy.
- NIST's *effectivity* concept (start and end of production to a specification, and avoiding "accidental mixes" of original and changed parts) maps directly onto the hackathon requirement to "never mix old and new procedures." M.A.C.H. could represent effectivity as metadata on each chunk (`effective_from`, `effective_to`, `scope`, `superseded_by`) and filter on it before ranking.
- 21 CFR 211.100(b) makes deviations first-class records that must be justified. A RAG system should model a deviation as a *time- and scope-bounded override* of a specific SOP step, not as a competing document.

### Gaps
- I found **no peer-reviewed paper that connects PLM/ECM data (ECR/ECO/ECN) to a RAG or LLM assistant** for shop-floor procedures. The closest are the KG-based ECM propagation preprint (SSRN) and generic manufacturing-KG reviews.
- I could not read the full text of the JMS / AEI / C&IE papers above (ScienceDirect fetch failed), so their quantitative results are not reported.
- Jarratt et al.'s and Hamraz et al.'s ECM reviews (*Research in Engineering Design*) are well known but were not located with a tool this session, so they are not cited.

## Q4. What gaps exist specifically on supersession in procedural documents? (Gaps and novelty opportunities for M.A.C.H.)

### Takeaway
Everything found so far treats temporal validity at the level of documents or facts, in software, news, medicine and law. Nothing addresses *procedural supersession*: step-level changes, scoped deviations, ECN-driven partial revisions, and the safety-critical rule against mixing revisions inside one answer. That leaves clear room for novelty for M.A.C.H.

### Cited Findings
- The closest system (VersionRAG) is evaluated only on software documentation (Spark, Bootstrap, Node.js). Its authors list legal and medical domains as future work, and implicit-change detection is still only 60% accurate. — [alphaXiv](https://www.alphaxiv.org/abs/2510.08109)
- Stale-document poisoning is severe (17–91%). It is largely solved when the model is told *when* old evidence stops applying, but date-only re-ranking gives only 4.6–10 points of improvement and depends on accurate metadata. — [alphaXiv](https://www.alphaxiv.org/abs/2609.31342)
- Regulators require point-of-use availability of the current revision only, and justified deviations. — [ISO 9001 §7.5 study guide](https://open-exam-prep.com/study-guides/cqi-irca-qms-lead-auditor/clauses-6-7/clause-7-documented-info); [21 CFR 211.100](https://www.law.cornell.edu/cfr/text/21/211.100)
- ECM theory defines effectivity and warns against mixing original and changed specifications. — [NIST IR 7922](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913323)

### Inferences — Gaps and novelty opportunities for M.A.C.H.
1. **Effectivity-gated retrieval as a hard filter, not a soft re-rank.** Store `doc_id`, `revision`, `status` (draft / effective / superseded / obsolete), `effective_from` / `effective_to`, scope (site, line, product, serial range) and `superseded_by` on every chunk. Filter before vector search, following VersionRAG's version-filtered search. This turns the ISO 9001 7.5.3 "point-of-use" rule into a retrieval invariant.
2. **Supersession-statement injection.** When an older revision is retrieved (for example for a "what changed?" question), prepend an explicit line: "Rev B was superseded by Rev C on DATE via ECN-123; do not use for execution." Ahmed et al. show explicit validity cut-offs, not dates alone, make models switch almost perfectly.
3. **Revision-coherence check on answers ("never mix").** Verify after generation that every citation in an answer resolves to the same effective revision set, and block or flag mixed answers. No paper found evaluates *intra-answer revision consistency*; this is a novel metric M.A.C.H. could define.
4. **Deviation / temporary-change overlays.** Model deviations and ECNs as scoped, time-bounded patches to specific SOP *steps* (step-level graph edges such as OVERRIDES / AMENDS), rather than as whole documents. This is unaddressed in the RAG literature and follows 21 CFR 211.100(b).
5. **Lightweight lineage graph rather than full GraphRAG.** Document → Revision → Step/Chunk, plus Change nodes derived from diffs between revisions (VersionRAG-style, with about 97% lower indexing cost than GraphRAG). Diffs of multimodal content, such as changed torque values in tables or swapped images, are an open problem.
6. **"Superseded citation" UX flag.** Always show revision ID and status next to each citation. If the user references an old document number, answer from the current one and state what changed. This is aligned with ISO auditor expectations, but no system was found that evaluates it.
7. **A small procedural-supersession benchmark as a contribution.** Example: 30–50 SOP families with 2–4 revisions, deviations and ECNs, with questions in four categories:
   - current procedure;
   - "what changed";
   - "which revision applies to line X on date D";
   - adversarial queries that try to pull up the old revision.
   No such benchmark exists; VersionQA is software-only and has 100 items.
8. **No weight editing.** Handle updates in the index, which matches Ovadia et al.'s finding that RAG beats fine-tuning for injecting new knowledge, and keeps an auditable trail (the spirit of 21 CFR Part 11).

### Gaps
- No peer-reviewed evidence was found on LLM behaviour with **multimodal** superseded content (outdated diagrams, photos, CAD views).
- No quantitative study was found on how often shop-floor errors trace to obsolete SOPs. Industry claims exist only in vendor blogs, which were excluded.
- Because OpenAlex verification was unavailable, the report writer should treat entries marked "title/venue from search result only" as needing confirmation before formal citation.
