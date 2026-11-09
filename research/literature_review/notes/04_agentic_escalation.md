# Agentic RAG, Human-in-the-Loop Expert Escalation, and Industrial Knowledge Assistants (for M.A.C.H.)

> **Method note.** The OpenAlex reference tools (`search_works` / `verify_reference`) could not be used in this session: the cloud call was blocked by the proxy (403) and the device-side call timed out. Papers were found and checked with WebSearch, alphaXiv discovery and WebFetch of publisher, ACL Anthology or arXiv landing pages. Peer-review status comes from the venue page I found. Where I could not confirm a venue, the entry says so. Items marked **[arXiv, not peer-reviewed]** are preprints. Their numbers are author-reported and have not been independently replicated.

---

## Q1. Which peer-reviewed agentic RAG designs give the best accuracy/latency trade-off for multi-hop technical questions?

### Takeaway
The best-documented peer-reviewed trade-off is **complexity-routed adaptive retrieval (Adaptive-RAG, NAACL 2024)**:
- It gets within about 0.2–0.7 points of fully iterative IRCoT.
- It runs at about 44% of IRCoT's per-query time (1.46× vs 3.33× single-step).

Always-on iterative retrieval (IRCoT) gives the highest accuracy, at roughly 3× the latency. 2026 preprints suggest that a full LLM agent doing every RAG step costs about 1.5× the latency and 3.3× the input tokens of a well-built fixed pipeline, for mixed gains. The practical recommendation is a hybrid: route by query complexity first, and use agentic loops only for hard (multi-hop) queries.

### Cited Findings

**Seminal / peer-reviewed designs**
- **IRCoT**: Trivedi, Balasubramanian, Khot, Sabharwal (2023).
  - Paper: "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions," ACL 2023 (long), [ACL Anthology 2023.acl-long.557](https://aclanthology.org/2023.acl-long.557). Peer-reviewed.
  - Design: each chain-of-thought sentence becomes the next retrieval query.
  - Results: up to **+21 points retrieval** and **+15 points downstream QA** with GPT-3 on HotpotQA, 2WikiMultihopQA, MuSiQue and IIRC. The authors also report fewer hallucinations. ([arXiv abstract](https://arxiv.org/abs/2212.10509v2))
- **FLARE (Active Retrieval Augmented Generation)**: Jiang et al. (2023), EMNLP 2023 main, [ACL Anthology 2023.emnlp-main.495](https://preview.aclanthology.org/setup/2023.emnlp-main.495) / [arXiv 2305.06983](https://arxiv.org/abs/2305.06983). Peer-reviewed.
  - Design: the model writes a draft of the next sentence and retrieves again only when that draft contains low-confidence tokens. Retrieval is driven by uncertainty, not run at every step.
- **Self-RAG**: Asai et al. (2024).
  - Paper: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," ICLR 2024, [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html). Peer-reviewed.
  - Design: trained "reflection tokens" decide when to retrieve and grade relevance and support. The critique signal is built in and could be reused as a confidence or escalation signal.
- **Adaptive-RAG**: Jeong, Baek, Cho, Hwang, Park (2024).
  - Paper: "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity," NAACL 2024, DOI [10.18653/v1/2024.naacl-long.389](https://aclanthology.org/2024.naacl-long.389). Peer-reviewed.
  - Design: a small T5 classifier routes each query to no retrieval, single-step retrieval, or iterative (IRCoT-style) retrieval.
  - Results with GPT-3.5 ([Table 1, arXiv PDF](https://arxiv.org/pdf/2403.14403)). Time is relative to single-step (= 1.00).

    | Method | EM | F1 | Acc | Retrieval steps | Time |
    |---|---|---|---|---|---|
    | No retrieval | 35.77 | 48.56 | 44.27 | 0 | 0.71 |
    | Single-step | 34.73 | 46.99 | 45.27 | 1.00 | 1.00 |
    | IRCoT (multi-step) | 38.13 | 50.87 | 49.70 | 2.81 | 3.33 |
    | **Adaptive-RAG** | **37.97** | **50.91** | **48.97** | **1.03** | **1.46** |

  - The complexity classifier itself is only **54.5% accurate**. Even a weak router therefore recovers most of the gain from iterative retrieval, and a better router has clear headroom. ([arXiv PDF](https://arxiv.org/pdf/2403.14403))
  - The Self-RAG row in the same table (EM 10.87; time 1.50) uses a LLaMA2 backbone and is not directly comparable. ([arXiv PDF](https://arxiv.org/pdf/2403.14403))

**Agentic vs. "enhanced" pipeline RAG (newest evidence)**
- Ferrazzi, Cvjeticanin, Piraccini, Giannuzzi (2026), "Is Agentic RAG worth it? An experimental comparison of RAG approaches" (Fondazione Bruno Kessler). **[arXiv 2601.07711, not peer-reviewed]** [alphaXiv](https://www.alphaxiv.org/abs/2601.07711)
  - **Cost and latency:** agentic RAG used on average **3.3× input tokens, 1.9× output tokens and 1.5× end-to-end latency** compared with an enhanced pipeline.
  - **Intent routing (F1):**
    - Agentic RAG did better on FIQA (98.8 vs 95.7) and CQADupStack (99.8 vs 96.6).
    - It collapsed on FEVER (49.3 vs 87.9 for a semantic router).
  - **Query rewriting:** agentic rewriting beat HyDE by +2.8 NDCG@10 on average (+7.8 on NQ).
  - **Re-retrieval:** agentic re-retrieval was mostly wasted. In 53% of cases the second retrieval returned identical results. A dedicated ELECTRA reranker in the pipeline helped more.
  - **Authors' recommendation:** a hybrid, with the agent doing intent classification and query rewriting and a fixed pipeline doing retrieval and reranking.

**Other 2026 preprints on adaptive or agentic RAG** (all **[arXiv, not peer-reviewed]**, found via alphaXiv; abstract-level only)
- PAR²-RAG, "Planned Active Retrieval and Reasoning for Multi-Hop QA" (Oracle AI, 2026): planning plus active retrieval for multi-hop QA. [2603.29085](https://www.alphaxiv.org/abs/2603.29085)
- "When Should Active RAG Retrieve? A Budget-Aware Evaluation of Utility, Calibration, and Cost" (CMU / Glasgow / Georgia Tech, 2026): evaluates active-RAG retrieval decisions under budgets. [2607.24010](https://www.alphaxiv.org/abs/2607.24010)
- AutoSearch (CAS / Meituan, 2026): reinforcement learning sets an adaptive search depth to cut multi-step cost. [2604.17337](https://www.alphaxiv.org/abs/2604.17337)
- A²RAG (UNSW et al., 2026): cost-aware adaptive agentic Graph-RAG. [2601.21162](https://www.alphaxiv.org/abs/2601.21162)
- "Quantifying the Accuracy and Cost Impact of Design Decisions in Budget-Constrained Agentic LLM Search" (2026). [2603.08877](https://www.alphaxiv.org/abs/2603.08877)
- "Do We Still Need GraphRAG? Benchmarking RAG and GraphRAG for Agentic Search Systems" (NYU Shanghai, 2026). [2604.09666](https://www.alphaxiv.org/abs/2604.09666)
- A-RAG (USTC, 2026): hierarchical retrieval interfaces exposed to the agent as tools. [2602.03442](https://www.alphaxiv.org/abs/2602.03442)
- DeFT-RAG (UT Dallas, 2026): breaks a question into self-contained sub-questions whose answers can be reused. [2610.37826](https://www.alphaxiv.org/abs/2610.37826)
- ConCise (2026): training-free compression of the reasoning-chain state to cut multi-step RAG serving cost. [2606.28361](https://www.alphaxiv.org/abs/2606.28361)
- "Dynamic Retriever and Generator Selection for RAG" (Adobe / Glasgow, 2026): per-query choice of retriever and generator. [2609.17709](https://www.alphaxiv.org/abs/2609.17709)
- "Adaptive Retrieval, Selective Answers: Evaluating Conformal Factuality in Agentic RAG" (Georgia State, 2026): claim-level conformal filtering applied to multi-step agentic RAG, which links directly to escalation. [2610.34872](https://www.alphaxiv.org/abs/2610.34872)
- "Bayesian Uncertainty Propagation for Agentic RAG Pipelines" (Univ. of Hull, 2026): estimates when multi-stage pipelines will fail. [2607.00972](https://www.alphaxiv.org/abs/2607.00972)

### Inferences
- For M.A.C.H., the evidence favours a **router-first design**:
  - A cheap classifier or LLM call labels each query as direct lookup (one SOP step), single retrieval, or multi-hop (e.g., fault → cause → procedure → torque spec).
  - IRCoT- or FLARE-style loops run only on the multi-hop branch.
  - In the peer-reviewed Adaptive-RAG numbers, this keeps latency near 1.5× single-step instead of about 3.3×.
- Uncertainty signals already inside these methods (FLARE's low-confidence tokens, Self-RAG's support and relevance tokens) can **serve as escalation triggers**, so the system does not need a separate confidence model.
- The 53% wasted re-retrieval finding suggests capping agent loops and checking whether new evidence differs from what was already retrieved, which reduces shop-floor latency.

### Gaps
- **ReAct** (Yao et al., ICLR 2023) and **multi-agent RAG** frameworks were not located with a tool in this session. They are left out rather than cited from memory, and need a follow-up search.
- No peer-reviewed benchmark was found that tests agentic RAG on **manufacturing or technical multi-hop questions**. All numbers above are open-domain Wikipedia QA, and transfer to SOP corpora is not established.
- Latency figures are relative (normalised to single-step), not wall-clock on edge hardware.

---

## Q2. What does the learning-to-defer / selective-prediction literature say about when to route to a human, and how should the combined human+AI system be evaluated?

### Takeaway
Learning-to-defer (L2D) treats "answer vs. defer" as a decision learned **jointly with the expert's accuracy**. The system defers when the expected loss of answering is higher than the expected loss of the expert plus the cost of consulting them, not simply when its confidence is low.

The combined system should be evaluated on:
- **System-level accuracy against deferral rate (coverage)**: risk–coverage curves, AURCC, and accuracy at a fixed coverage.
- **Total cost**, including expert time.
- **Complementarity**: the combined team should beat both the AI alone and the human alone.

Recent LLM work uses cascades (small model → large model → human) with thresholds that are calibrated and then updated online from expert labels.

### Cited Findings
- **Mozannar & Sontag (2020)**, "Consistent Estimators for Learning to Defer to an Expert," ICML 2020 (PMLR v119), [PMLR PDF](https://proceedings.mlr.press/v119/mozannar20b/mozannar20b.pdf). Peer-reviewed.
  - This is the foundational L2D paper.
  - It gives a consistent surrogate loss for learning the classifier and the rejector together, so the deferral decision depends on how good the expert is.
  - Code: [clinicalml/learn-to-defer](https://github.com/clinicalml/learn-to-defer).
- **Mao, Mohri et al.**, "Principled Approaches for Learning to Defer with Multiple Experts," [NYU PDF](https://cs.nyu.edu/~mohri/pub/def.pdf).
  - Extends L2D to **several experts**, which matches routing to different SMEs (electrical, mechanical, quality).
  - The venue was not confirmed via tool.
- **"Consistent Learning-to-Defer with Expert-Conditional Advice"** (2026). **[arXiv 2603.14324, not peer-reviewed]** [arXiv PDF](https://arxiv.org/pdf/2603.14324)
- **Kamath, Jia, Liang (2020)**, "Selective Question Answering under Domain Shift," ACL 2020, [2020.acl-main.503](https://aclanthology.org/2020.acl-main.503). Peer-reviewed.
  - Establishes selective QA: the model answers only above a confidence threshold, and calibrators help when the input distribution shifts.
  - This matters for M.A.C.H. because new machines and new SOPs are exactly that kind of shift.
- **Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang**, "Know Your Limits: A Survey of Abstention in Large Language Models," [arXiv 2407.18418v3](https://arxiv.org/html/2407.18418v3). The tool did not confirm a peer-reviewed venue (the landing page lists arXiv only, v3 Feb 2025).
  - The system should abstain if **any** of three views says to abstain: query answerability, model confidence, or alignment with human values. Otherwise it can abstain partially. Abstention is described as a spectrum of behaviours, not a yes/no choice.
  - Metrics: coverage and abstention rate, accuracy on answered questions (R-Acc), Effective Reliability, coverage at a fixed accuracy (C@Acc), AUACC, **AURCC** (area under the risk–coverage curve; lower is better), and AUROC for the uncertainty scores.
  - Inference-time methods: probing internal states, calibration, consistency across samples, self-evaluation, and multi-LLM collaboration.
- **Fanconi & van der Schaar (2025)**, "Cascaded Language Models for Cost-Effective Human–AI Decision-Making," NeurIPS 2025, [NeurIPS PDF](https://papers.neurips.cc/paper_files/paper/2025/file/10e0c427408ccc6e073d9464e2280f89-Paper-Conference.pdf). Peer-reviewed.
  - **Three tiers:** a small LLM answers first; it defers to a larger LLM when calibrated confidence is low; the system escalates to a **human** when predictive uncertainty (posterior std) is high.
  - **Calibration:** Bayesian Platt scaling fitted on only **100 calibration samples**.
  - **Online updates:** thresholds are updated with Adam on a system-risk objective, using expert labels collected whenever the system abstains.
  - **Benefit per cost (ΔIBC):** large on ARC-Easy (~243) and ARC-Challenge (~89); **not significant on MedQA/MedMCQA**.
  - **Regret:** lower cumulative regret than single models on 4 of 5 datasets.
  - **Human side:** the "human" is a **simulated oracle**. A label-flipping experiment shows regret rises as expert labels get noisier.
- **De Toni et al. (2024)**, "Towards Human-AI Complementarity with Prediction Sets," NeurIPS 2024, [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/37d4d4413b7c7558cc27a6d3d42ea998-Paper-Conference.pdf). Peer-reviewed.
  - Instead of a hard defer, the AI gives the human a **set of candidate answers** built to maximise the accuracy of the human+AI team.
  - This suits M.A.C.H.: show the expert the top candidate procedures rather than a blank ticket.
- "Toward Human-AI Complementarity Across Diverse Tasks" (2026). **[arXiv 2605.04070, not peer-reviewed]** [alphaXiv](https://www.alphaxiv.org/abs/2605.04070)
- "Incremental Retrieval-Augmented Generation for Human-in-the-Loop Decision Support" (iRAG, ISTI-CNR, 2026). **[arXiv 2610.12666, not peer-reviewed]** [alphaXiv](https://www.alphaxiv.org/abs/2610.12666)
  - Combines RAG with hybrid human/AI decision-making and updates the knowledge base incrementally instead of keeping it static.

### Inferences
- **Escalation rule for M.A.C.H.:** escalate when **(calibrated retrieval/answer uncertainty) × (safety criticality of the SOP step)** is above a threshold, rather than on a confidence threshold alone.
  - L2D says the threshold should depend on the expert's availability and accuracy. For example, it should be lower on night shifts when experts are scarce but the cost of an error is higher.
- **Evaluate the combined system** with:
  - a risk–coverage curve: answered-correctly rate against escalation rate;
  - expert minutes per 100 queries;
  - time-to-resolution;
  - whether the human+AI team beats AI-only and expert-only baselines.
- The Fanconi & van der Schaar design (calibrate on about 100 labelled queries, then tune thresholds online from expert answers) is a demo-ready template. It also closes the loop: every escalation produces a label.

### Gaps
- No L2D paper was found evaluated with **real** (non-simulated) industrial experts or with RAG-style free-text answers. Almost all L2D work is classification with simulated or crowd experts.
- No source was found that compares calibration methods for **RAG-grounded** confidence (retrieval score vs. verbalised confidence vs. sampling consistency) on technical corpora.

---

## Q3. Which peer-reviewed studies deploy LLM/RAG assistants in real factories or maintenance settings, and what did they find?

### Takeaway
Real-factory, peer-reviewed evidence is **thin and mostly qualitative**. The best-documented case is a detergent-factory RAG tool (Kernan Freire et al., Frontiers in AI 2024):
- Its benchmark showed GPT-4 at **97.5% factuality and 0% hallucination**.
- Its user study found **operators often prefer asking a nearby colleague**. The tool's value was highest on **night shifts** when no expert is present.
- Its failure modes were missing answers, unreliable answers to overly specific questions, and hallucination framed as a **safety risk**.

A two-year longitudinal follow-up (preprint) adds two concerns: the **burden of contributing knowledge**, and **surveillance and manager–operator tension**.

### Cited Findings

**Kernan Freire, Wang, Foosherian, Wellsandt, Ruiz-Arenas, Niforatos (2024)**, "Knowledge sharing in manufacturing using LLM-powered tools: user study and model benchmarking," *Frontiers in Artificial Intelligence* 7:1293084, DOI [10.3389/frai.2024.1293084](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1293084/pdf). Peer-reviewed.

- **Setting and system:**
  - Detergent factory; 9 participants (4 managers, 5 operators).
  - RAG built on LlamaIndex: about 400-token chunks, ada-002 embeddings, top-K retrieval. Manuals and issue reports are queried separately.
- **Benchmark:** 7 LLMs on 20 questions, scored out of 100.

  | Model | Factuality | Completeness | Hallucination |
  |---|---|---|---|
  | GPT-4 | 97.5 | 95 | 0 |
  | StableBeluga2 | 95 | 92.5 | 7.5 |
  | Mixtral 8x7B | 92.5 | 92.5 | 2.5 |
  | GPT-3.5 | 90 | 90 | 5 |
  | Llama 2 | 77.5 | 82.5 | 13 |
  | Guanaco 33B | 27.5 | 27.5 | 65.6 |

- **Qualitative findings:**
  - Quick access to information was valued.
  - Users lost time when the answer was not in the corpus.
  - Overly specific questions produced answers users found unreliable.
  - A manager warned: "if the responses are not adequate, you risk safety."
  - "Faster and easier to ask an expert colleague working near me."
- **Adoption barriers:** awareness, training, acceptance, and a generational divide.
- **Limitations:** a single coder scored responses, only 20 questions, and no production-line evaluation.

**Other deployments and systems**
- **Kernan Freire, He, Wang, Niforatos, Bozzon (2024)**, "Factory Operators' Perspectives on Cognitive Assistants for Knowledge Sharing: Challenges, Risks, and Impact on Work." **[arXiv 2409.20192, not peer-reviewed]** (no venue on the landing page) [arXiv](https://arxiv.org/abs/2409.20192v1)
  - Two-year longitudinal study of smartphone voice assistants and LLM chatbots in factories.
  - The assistants fall short of human-to-human knowledge sharing.
  - Contributing knowledge is a burden.
  - It is unclear which kinds of knowledge can be shared this way.
  - Operators raised surveillance and privacy concerns, and the study found tension between operators and managers.
- **Operator 4.0 framing:** Thorvald, Fasth Berglund, Romero (2021), "The cognitive operator 4.0," Proc. ICMR 2021, *Advances in Transdisciplinary Engineering* 15:3–8, DOI 10.3233/ATDE210003, [Chalmers record](https://research.chalmers.se/en/publication/526558). Peer-reviewed conference.
  - Industry 4.0 treats the operator as a knowledge worker.
  - Of the eight Operator 4.0 scenarios (XR, real-time data access, augmentation, etc.), some impose higher cognitive demands than others.
- **"Leveraging large language models for Human-Machine collaborative troubleshooting of complex industrial equipment faults"** (2025), *Advanced Engineering Informatics*, DOI [10.1016/j.aei.2025.103235](https://dl.acm.org/doi/10.1016/j.aei.2025.103235) / [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1474034625001284). Peer-reviewed journal.
  - Located, but the page fetch failed, so authors and results were **not retrieved**. Needs follow-up.
- **"Probing a novel machine tool fault reasoning and maintenance service recommendation approach through data-knowledge empowered LLMs integrated with AR-assisted maintenance guidance"** (2025), *Advanced Engineering Informatics*, [ScienceDirect S1474034625003532](https://www.sciencedirect.com/science/article/abs/pii/S1474034625003532). Peer-reviewed. Abstract not retrieved.
- **"A Generative AI Framework for Smart Maintenance: Utilizing RAG Systems and LLMs to Assist Manufacturing Operations"**, Springer book chapter (2025), [Springer](https://link.springer.com/chapter/10.1007/978-3-032-03725-1_13). Peer-reviewed proceedings chapter. Details not retrieved.
- **"Industrial Maintenance Optimization Based on the Integration of LLM and Augmented Reality"**, Springer chapter (2025), [Springer](https://link.springer.com/chapter/10.1007/978-3-031-86489-6_20). Details not retrieved.
- **Reviews and positioning papers (peer-reviewed; useful framing, no deployments):**
  - "AI Agents and Agentic AI – navigating a plethora of concepts for future manufacturing," *Journal of Manufacturing Systems* (2025). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S027861252500216X)
  - "Leveraging large language models in next generation intelligent manufacturing: Retrospect and prospect," *J. Manufacturing Systems* (2025). [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0278612525001943)
  - "Hybrid Agentic AI and Multi-Agent Systems in Smart Manufacturing," *J. Manufacturing Systems* (2026), DOI 10.1016/j.jmsy.2026.04.002. [ResearchGate](https://www.researchgate.net/publication/397934623_Hybrid_Agentic_AI_and_Multi-Agent_Systems_in_Smart_Manufacturing_Full_Paper_published_in_Journal_of_Manufacturing_Systems_httpsdoiorg101016jjmsy202604002)
  - "Generative AI for Predictive Maintenance for Manufacturing: A Survey," Procedia CIRP (2025). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2212827125009643)
  - "Integrating LLMs into Digital Manufacturing: A Systematic Review and Research Agenda," *Computers* (MDPI) 14(8):318 (2025). [MDPI](https://www.mdpi.com/2073-431X/14/8/318)
  - Curated list of agentic-AI manufacturing papers (not a paper): [awesome-agentic-manufacturing](https://github.com/Nastaran95/awesome-agentic-manufacturing)
- **Workplace GenAI copilot acceptance:** "Extended technology acceptance of workplace GenAI copilots: Evidence from PLS-SEM" (2026). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S3051051126000039) This is a survey-based acceptance model and not specific to manufacturing. Details not retrieved.
- **Newer industrial and operations RAG systems** (all **[arXiv, not peer-reviewed]**):
  - FactoryLLM (2026): an open-source sandbox for testing LLMs on fault diagnosis and recovery across interconnected machine manuals. [2606.14119](https://www.alphaxiv.org/abs/2606.14119)
  - "A corrective agentic hybrid RAG and an operations-grounded evaluation for a scientific facility" (2026): covers logbooks, wikis, operations chat and maintenance records, and is evaluated against real operations. [2607.24663](https://www.alphaxiv.org/abs/2607.24663)
  - "Integration of RAG for Knowledge Access in the ELBE Accelerator Control System" (HZDR, 2026): covers logbooks and interlock reports. [2609.27579](https://www.alphaxiv.org/abs/2609.27579)
  - "Reducing Technician Search Burden: A Multimodal RAG for Cessna 172 Maintenance Manual" (2026): a multimodal manual with diagrams, cautions and specifications, which closely matches M.A.C.H. [2608.18465](https://www.alphaxiv.org/abs/2608.18465)
  - IndustryAssetEQA (2026): neurosymbolic embodied question answering for asset maintenance. [2604.23446](https://www.alphaxiv.org/abs/2604.23446)
  - "Plant Memory" (IIT Jodhpur, 2026): technical language processing plus a verified maintenance ontology over SAP PM work orders, so agents can access failure knowledge. [2610.19131](https://www.alphaxiv.org/abs/2610.19131)
  - "Bridging Industrial Expertise and XR with LLM-Powered Conversational Agents" (2025). [arXiv 2504.05527](https://arxiv.org/html/2504.05527v1)

### Inferences
- The strongest adoption lesson: **an assistant competes with the colleague standing next to the operator.** M.A.C.H. should present escalation as "get the expert faster, with context already attached," not as a replacement for asking people.
- **Safety-critical SOP steps need conservative abstention.** Users explicitly linked hallucination to safety.
- Open models (Mixtral, StableBeluga2) came within about 5 points of GPT-4 on factuality, which supports on-premise deployment where factory data privacy matters.

### Gaps
- No peer-reviewed **controlled field trial** was found that reports task time, error rate or first-time-fix rate with versus without an LLM/RAG assistant on a real line.
- Results for the two *Advanced Engineering Informatics* papers and the Springer chapters could not be retrieved.
- No peer-reviewed study was found that measures **calibrated trust** (over- or under-reliance) of operators on a RAG assistant.

---

## Q4. How is expert feedback captured and reused (KB update, feedback loops), and what are the risks?

### Takeaway
The documented pattern is a **gated loop**:
1. The operator or the system drafts knowledge, for example a five-why issue report or an escalated Q&A.
2. The LLM checks it for consistency.
3. An expert reviews it.
4. The approved item goes into the KB and is indexed separately from the official manuals.

Main risks:
- **Contribution burden** on experts.
- **Unverified or erroneous expert input contaminating the KB.** Simulations show deferral systems degrade with noisy expert labels.
- **Provenance loss.**
- **Surveillance and labour-relations concerns.**

2026 preprints explore elicitation that goes beyond Q&A capture: logic-augmented generation, active inference, and ontology-grounded expansion of a knowledge graph.

### Cited Findings
- **Gated capture in a real factory.** In Kernan Freire et al. (2024):
  - Operators file issue reports with the **five-why** root-cause method.
  - The LLM checks each report for logical inconsistencies.
  - **Expert operators review** reports before they enter the KB.
  - Manuals and issue reports are indexed and queried **separately**.
  - Source: [Frontiers in AI, DOI 10.3389/frai.2024.1293084](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1293084/pdf). Peer-reviewed.
- **Contribution burden and social risks.** Over two years, operators reported the burden of contributing knowledge, uncertainty about which knowledge is shareable, surveillance and privacy fears, and operator–manager tension. ([arXiv 2409.20192, not peer-reviewed](https://arxiv.org/abs/2409.20192v1))
- **Noisy experts.** In the NeurIPS 2025 cascade, flipping expert labels raised regret: online threshold learning from expert answers is sensitive to expert error. Sparse or noisy feedback is listed as a limitation. ([Fanconi & van der Schaar, NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/file/10e0c427408ccc6e073d9464e2280f89-Paper-Conference.pdf))
- **Tacit knowledge literature:**
  - "Large Language Models for Tacit Knowledge Elicitation in Industry 5.0: A Literature Review" (FAU). [FAU CRIS](https://cris.fau.de/publications/353231146/) Peer-reviewed status and venue not confirmed.
  - "Unlocking Tacit Knowledge in Industrial Production: Exploring Barriers…" (HICSS proceedings). [ScholarSpace](https://scholarspace.manoa.hawaii.edu/bitstreams/5f84bbf5-399a-4bd3-92fa-8529a1c94e36/download) Peer-reviewed conference; findings not retrieved.
  - "Capturing Tacit Design for Manufacturing Knowledge from Unstructured Discourse" (McGowan et al., ASME IDETC). [Berkeley CoDesign](https://codesign.berkeley.edu/papers/mcgowan-kg-idetc/) Builds a knowledge graph from expert discussions.
  - "Tacit Domain Knowledge Extraction and AI-Driven Learning Framework for Optimization of Factory Operations" (2026). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2213846326002166) Peer-reviewed journal; details not retrieved.
- **Newer capture mechanisms** (all **[arXiv, not peer-reviewed]**):
  - "Tacit Knowledge Extraction via Logic Augmented Generation and Active Inference" (CNR-ISTC / Bologna / Consorzio MUSP, 2026): targets procedural manufacturing domains. [2605.07639](https://www.alphaxiv.org/abs/2605.07639)
  - GRACE, "Graph-Grounded Reflective Agent Copilot Engine for Expert-in-the-Loop Knowledge Expansion" (2026): experts confirm graph-grounded claims before the knowledge graph is extended. [2609.04442](https://www.alphaxiv.org/abs/2609.04442)
  - KUPAS MASTER (Tongji / Kupas, 2026): distils master practitioners' cues, rationale and actions into experience corpora agents can use. [2609.37673](https://www.alphaxiv.org/abs/2609.37673)
  - AquiLLM (2026): an architecture for capturing tacit knowledge in research groups. [2608.08883](https://www.alphaxiv.org/abs/2608.08883)
  - "Contestable Agents for Data Governance: Recording Human Stewardship of AI-Generated Metadata" (MongoDB / Trane, 2026): provenance records of human approvals and edits for industrial data. [2610.31553](https://www.alphaxiv.org/abs/2610.31553)
  - iRAG (ISTI-CNR, 2026): the KB is updated incrementally from human-in-the-loop decisions. [2610.12666](https://www.alphaxiv.org/abs/2610.12666)
  - "LLMs Can Explain Experts Better Than Experts Themselves" (2026). [arXiv 2608.07488](https://arxiv.org/html/2608.07488)

### Inferences
- **Proposed M.A.C.H. loop:**
  1. On escalation, send the SME the query, the retrieved evidence, the draft answer and its confidence (prediction-set style).
  2. Capture the expert's answer as a structured "expert note" with machine ID, SOP reference, author, timestamp, an expiry or review date, and its safety class.
  3. Have the LLM check the note for consistency against the official SOP.
  4. Get a second-expert or QA sign-off for safety-critical notes.
  5. Index the note in a separate "expert-note" collection with lower retrieval priority than the official SOP and a visible provenance badge.
  6. Use the escalation outcome as a calibration label for the escalation threshold.
- **Risks to mitigate:**
  - **KB poisoning** from expert errors or outdated tips.
  - **Conflict with controlled SOP documents**, where ISO 9001 document control requires approval.
  - **Expert fatigue** from too many escalations.
  - **Privacy and surveillance** perceptions, so log queries without operator-level performance tracking.
  - **Feedback loops** that drop the escalation threshold too fast after a run of easy cases.

### Gaps
- No peer-reviewed study was found that **measures KB quality drift** or error propagation after expert-answer ingestion in an industrial RAG.
- No quantitative data was found on expert time per escalation or on how willing experts are to contribute in manufacturing.

---

## Gaps and novelty opportunities for M.A.C.H.

1. **Calibrated escalation for multimodal SOP RAG.** No peer-reviewed work combines Adaptive-RAG-style routing with L2D-style human deferral on technical or multimodal manuals. M.A.C.H. could route each query to one of four paths: no retrieval, single retrieval, multi-hop, or **escalate to SME**. It can then report a risk–coverage curve and expert minutes per 100 queries. This is new as a systems contribution.
2. **Safety-weighted deferral.** L2D losses treat all errors as equal. Weighting deferral by SOP step criticality (e.g., lockout/tagout or torque specs versus cosmetic steps) is unexplored in the RAG literature.
3. **Shift-aware routing.** Field evidence says the assistant matters most on night shifts with no expert nearby (Kernan Freire 2024). Making the deferral threshold depend on whether an expert is available (the expert cost in L2D) is a direct and demo-able idea.
4. **Expert-answer capture with provenance and conflict detection.** The only real-factory loop found (five-why, LLM check, expert review) has no versioning, expiry, or conflict detection against controlled SOPs. M.A.C.H. could add these and show how they reduce KB contamination.
5. **Prediction-set escalation.** Hand the SME a short ranked list of candidate SOP passages and answers (De Toni et al., NeurIPS 2024) instead of a blank ticket, to cut expert effort. This has not been tested in manufacturing.
6. **Escalations as online calibration data.** Fanconi & van der Schaar showed online threshold learning with *simulated* experts. M.A.C.H. could be the first to log real SME decisions and report how the thresholds converge.
7. **Evaluation gap.** No public benchmark exists for multi-hop, multimodal shop-floor SOP QA with answerability labels. A small labelled set (answerable / needs expert / unsafe to answer) would itself be a contribution.
8. **Human factors.** Design for low contribution burden (one-tap confirm or edit of the AI draft) and privacy (no per-operator performance analytics). These address the specific risks raised by the longitudinal factory study.
