# LLM-Generated Work Instructions under Change Control, and RAG Evaluation Methodology (for M.A.C.H.)

Scope note: this covers (A) using LLMs to write manufacturing work instructions and procedures, and (B) how to evaluate RAG systems, including comparisons against BM25 and text-only RAG. Tool conditions this session: the OpenAlex lookup ran through the cloud proxy and failed every time (403). The device-side OpenAlex lookup worked for 4 queries, then hit HTTP 429 rate limits. The other papers were found through WebSearch result pages (ACL Anthology, AAAI OJS, NeurIPS/ICLR proceedings, ScienceDirect, Springer) or alphaXiv. Each entry says how it was located. A one-line finding comes from the abstract or venue page I saw, or from well-established knowledge of a canonical paper. Where I could not read a paper's results in this session, the entry says so.

Peer-review labels: **[PR]** = peer-reviewed venue confirmed via tool. **[arXiv, not peer-reviewed]** = preprint only, as far as located.

---

## Q1. What peer-reviewed work generates manufacturing work instructions or procedures with LLMs, and how was quality judged?

### Takeaway
Peer-reviewed work on LLM-*generated* manufacturing work instructions is small and new (2024–2026). Most of it is conference papers (IEEE ETFA/INDIN, Springer proceedings, Procedia). These papers judge quality with small expert reviews, task-execution user studies, or rubric checks. None uses a standard benchmark. A larger and more mature body of work covers LLM/RAG *assistants* that retrieve and explain existing procedures (Computers in Industry 2024–2025). Controlled language is starting to appear as a way to constrain generation (CNL for assembly instructions, 2025/26). I found no peer-reviewed study of ASD-STE100 combined with LLMs. I also found no study of LLM-drafted instructions going through a formal change-control approval workflow.

### Cited Findings — LLM generation of assembly / work instructions
- **Meyer, F., Freitag, L., Hinrichsen, S., Niggemann, O. (2024). "Potentials of Large Language Models for Generating Assembly Instructions." IEEE ETFA 2024. DOI 10.1109/etfa61755.2024.10710806 [PR]**. Located through the device-side OpenAlex lookup; repository record at TH-OWL. This is one of the first peer-reviewed tests of whether LLMs can generate assembly instructions. Its detailed evaluation results were not retrieved in this session. — [DOI](https://doi.org/10.1109/etfa61755.2024.10710806); [TH-OWL record](https://www.th-owl.de/elsa/record/11330)
- **Widulle, N., Meyer, F., Niggemann, O. (2024). "Generating Assembly Instructions Using Reinforcement Learning in Combination with Large Language Models." IEEE INDIN 2024. DOI 10.1109/indin58382.2024.10774545 [PR]**. RL handles the assembly *sequence* and the LLM turns it into natural-language instructions. This split (a symbolic or optimised planner for order, an LLM for wording) is directly relevant to keeping step order correct. Evaluation details were not retrieved. — [DOI](https://doi.org/10.1109/indin58382.2024.10774545)
- **Leder, R., Lütjen, M., Freitag, M. (2026). "Towards Large Language Model-Driven Personalization of Assembly Work Instructions." Procedia Computer Science. DOI 10.1016/j.procs.2026.02.035 [PR, conference proceedings]**. Uses an LLM to adapt the same work instruction to individual workers. — [DOI](https://doi.org/10.1016/j.procs.2026.02.035)
- **"Leveraging LLM for Assembly Instructions Using Controlled Natural Language" (Springer chapter, 2025/26; authors not retrieved) [PR, proceedings]**. Constrains LLM output to a controlled natural language (CNL) for assembly instructions. It is the closest peer-reviewed analogue to using ASD-STE100 with an LLM. Authors, venue name and metrics need verifying before citation. — [Springer](https://link.springer.com/chapter/10.1007/978-3-032-16889-4_64)
- **"AIssembly: Generating Assembly Work Instructions from 3D-CAD Models Using Artificial Intelligence" (Springer chapter, 2025; authors not retrieved) [PR, proceedings]**. Generates work instructions from CAD geometry, a multimodal input. Authors and metrics were not retrieved. — [Springer](https://link.springer.com/chapter/10.1007/978-3-032-09700-2_20)
- **"Automated Assembly Instruction Generation from CAD Models Using Grounded Large Language Models: A Human-in-the-Loop Framework" (2026) [arXiv, not peer-reviewed]**. A grounded LLM with human-in-the-loop review, the same design pattern as M.A.C.H.'s draft-then-approve flow. — [arXiv](https://arxiv.org/html/2610.11896)
- **"Prompt-to-Parts: Generative AI for Physical Assembly and Scalable Instructions" (2025) [arXiv, not peer-reviewed]**. — [arXiv](https://arxiv.org/abs/2512.15743v1)

### Cited Findings — LLM/RAG assistants for shop-floor procedures (retrieval and explanation of existing SOPs)
- **Colabianchi, S., Costantino, F., Sabetta, N. (2024). "Assessment of a large language model based digital intelligent assistant in assembly manufacturing." Computers in Industry, 104129. DOI 10.1016/j.compind.2024.104129 [PR, journal]**. Located through OpenAlex (71 citations). It evaluates an LLM digital intelligent assistant used by people doing assembly work, a human-centred task evaluation rather than text metrics. Exact measures were not retrieved. — [DOI](https://doi.org/10.1016/j.compind.2024.104129); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0166361524000575)
- **Ludwig, H., Schmidt, T., Kühn, M. (2025). "An ontology-based retrieval augmented generation procedure for a voice-controlled maintenance assistant." Computers in Industry, 104289. DOI 10.1016/j.compind.2025.104289 [PR, journal]**. Grounds maintenance-procedure RAG in an ontology, a structured alternative to plain chunk retrieval. — [DOI](https://doi.org/10.1016/j.compind.2025.104289)
- **Bensch, O., Bensch, L., Nilsson, T., et al. (2024). "AI Assistants for Spaceflight Procedures: Combining GPT and RAG on Knowledge Graphs With Augmented Reality Cues." arXiv:2409.14206 [arXiv, not peer-reviewed as located]**. Procedure assistant built on KG-RAG with AR cues. — [arXiv](http://arxiv.org/abs/2409.14206)
- "A Generative AI Framework for Smart Maintenance: Utilizing RAG Systems and LLMs to Assist Manufacturing Operations" (Springer chapter, 2025) [PR, proceedings; authors not retrieved]. — [Springer](https://link.springer.com/chapter/10.1007/978-3-032-03725-1_13)
- "Industrial Maintenance Optimization Based on the Integration of LLM and AR" (Springer chapter, 2025) [PR, proceedings; authors not retrieved]. — [Springer](https://link.springer.com/chapter/10.1007/978-3-031-86489-6_20)
- "FactoryLLM: A Safe and Open-Source AI Playground for Evaluating LLMs in Smart Factories" (2026) [arXiv, not peer-reviewed]. — [arXiv](https://arxiv.org/html/2606.14119v1)

### Cited Findings — Surveys / context
- **Li, Y., Zhao, H., Jiang, H., et al. (2026). "Large Language Models for manufacturing." Journal of Manufacturing Systems. DOI 10.1016/j.jmsy.2026.02.014 [PR, journal survey]**. — [DOI](https://doi.org/10.1016/j.jmsy.2026.02.014)
- **Ouerghemmi, C., Ertz, M. (2025). "Integrating Large Language Models into Digital Manufacturing: A Systematic Review and Research Agenda." Computers (MDPI) 14(8):318. DOI 10.3390/computers14080318 [PR, journal]**. — [DOI](https://doi.org/10.3390/computers14080318)
- Makatura et al., "How Can Large Language Models Help Humans in Design and Manufacturing?" Harvard Data Science Review special issue (Parts 1–2) [PR, journal]. Covers the end-to-end LLM design-to-manufacturing workflow. — [HDSR Part 1](https://hdsr.mitpress.mit.edu/pub/15nqmdzl/release/2); [Part 2 (ResearchGate)](https://www.researchgate.net/publication/380943277_How_Can_Large_Language_Models_Help_Humans_in_Design_And_Manufacturing_Part_2_Synthesizing_an_End-To-End_LLM-Enabled_Design_and_Manufacturing_Workflow)

### Cited Findings — Controlled language and compliance
- ASD-STE100 Simplified Technical English is a controlled-language standard from aerospace maintenance documentation. It limits the dictionary and sets writing rules (e.g., short sentences, one instruction per sentence, active voice). — [Wikipedia overview](https://en.wikipedia.org/wiki/Simplified_Technical_English)
- The sources this session found on ASD-STE100 combined with LLMs are **all grey literature**: blogs and GitHub "skills" that prompt LLMs to write in STE. One claims "cuts slop 72.9%", which is unverified marketing. No peer-reviewed evaluation was found. — [explainx blog (unverified claim)](https://www.explainx.ai/blog/asd-ste100-simplified-technical-english-ai-skill-2026); [GitHub asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill); [kgolubic.com](https://kgolubic.com/posts/asd-ste100-and-llms/)
- EU AI Act Article 14 (human oversight) requires high-risk AI systems to be designed so natural persons can oversee them effectively. That includes being able to understand the system's limits, staying aware of automation bias, and being able to disregard, override or reverse its output. — [Art. 14 text (euaiact.com)](https://euaiact.com/article/14); legal analysis: [SSRN "Human Oversight under Article 14 of the EU AI Act"](https://papers.ssrn.com/abstract=5147196) [legal working paper, not peer-reviewed as located]
- ISO 9001 clause 7.5 (documented information) requires approval of documents for adequacy before issue, plus control of changes, versions and distribution. The standard's text was not retrieved this session, so the clause wording needs checking against ISO 9001:2015. GMP equivalents (EU GMP Ch. 4, 21 CFR 211.100) were not retrieved either; see Gaps.

### Inferences
- Peer-reviewed generation papers seem to rely on expert judgement and small user studies. None I found reports inter-annotator agreement or step-level error taxonomies. M.A.C.H. can stand out by reporting both.
- The split of RL or planner for ordering plus an LLM for wording (Widulle et al.), and CNL-constrained output, both suggest one design: a **template/schema-constrained generator** (fields for step, tool, torque, PPE, caution/warning) whose output is checked against STE-style rules. This is defensible, but its effect on quality has not been tested empirically.
- M.A.C.H.'s rule "never auto-published; goes through change control" fits EU AI Act Art. 14 (override/disregard) and ISO 9001 document approval. Evaluation should show that reviewers can *detect* errors. Showing that drafts are good is not enough, because automation bias is a named Art. 14 risk.

### Gaps
- I found no peer-reviewed study measuring whether ASD-STE100 constraints improve LLM-generated procedure accuracy or comprehension.
- I found no peer-reviewed study of LLM drafts inside a formal document change-control/approval workflow. Reviewer edit distance, rejection rate and time-to-approve are all unmeasured in the literature.
- The detailed metrics of Meyer 2024, Widulle 2024, the CNL chapter, AIssembly and Colabianchi 2024 were not retrieved here. Read the full texts before citing specific numbers.
- GMP (EU GMP Annex 11, Chapter 4; FDA 21 CFR Part 11/211) primary texts were not retrieved.

---

## Q2. What evaluation design would reviewers accept as rigorous for comparing M.A.C.H. to BM25 and text-only RAG?

### Takeaway
The accepted design scores **retrieval** and **generation** separately. Retrieval gets graded-relevance metrics (Recall@k, nDCG@10, MRR) against qrels made by humans or LLMs. Generation gets faithfulness/groundedness, answer correctness and citation precision/recall, measured on a domain test set with stratified question types: text-only, table, figure/diagram, multi-hop, unanswerable, and superseded-version. Systems are compared with paired significance tests, and ablations isolate each component. Prior work sets the baselines to beat: BM25 is a strong zero-shot baseline (BEIR), and visual page retrieval beats OCR-text pipelines on visually rich documents (ColPali, VisRAG).

### Cited Findings — Benchmarks and frameworks
- **Es, S., James, J., Espinosa-Anke, L., Schockaert, S. (2024). "RAGAs: Automated Evaluation of Retrieval Augmented Generation." EACL 2024 System Demonstrations [PR, demo track]**. Reference-free LLM-based metrics: faithfulness (are the answer's claims entailed by the context), answer relevance, and context relevance. — [ACL Anthology](https://aclanthology.org/2024.eacl-demo.16.pdf)
- **Saad-Falcon, J., Khattab, O., Potts, C., Zaharia, M. (2024). "ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems." NAACL 2024 (long) [PR]**. Fine-tunes lightweight LM judges on synthetic data. It then uses prediction-powered inference with a small human-annotated set (a few hundred points) to put confidence intervals on context relevance, faithfulness and answer relevance. This gives a template for pairing LLM judges with a small human set. — [ACL Anthology](https://aclanthology.org/2024.naacl-long.20.pdf)
- **Gao, T., Yen, H., Yu, J., Chen, D. (2023). "Enabling Large Language Models to Generate Text with Citations" (ALCE). EMNLP 2023 [PR]**. Defines NLI-based **citation recall** (is each statement fully supported by its citations) and **citation precision** (is each citation needed). Even the best models of the time often lacked full citation support. — [ACL Anthology](https://aclanthology.org/2023.emnlp-main.398.pdf)
- **Chen, J., Lin, H., Han, X., Sun, L. (2024). "Benchmarking Large Language Models in Retrieval-Augmented Generation" (RGB). AAAI 2024 [PR]**. Tests four RAG abilities: noise robustness, negative rejection, information integration and counterfactual robustness. LLMs were weak at rejecting questions when the retrieved context lacked the answer, and at handling counterfactual or erroneous context. This maps directly onto the abstention and outdated-SOP cases. — [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/29728/31250)
- **Yang, X., et al. (2024). "CRAG — Comprehensive RAG Benchmark." NeurIPS 2024 Datasets & Benchmarks [PR]**. Includes question types such as multi-hop, comparison and false-premise, and scores answers as accurate, missing (abstain) or hallucinated, with hallucinations penalised. — [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/file/1435d2d0fca85a84d83ddcb754f58c29-Paper-Datasets_and_Benchmarks_Track.pdf)
- **CRUD-RAG (Lyu et al., 2024) — arXiv:2401.17043**. Chinese RAG benchmark across Create/Read/Update/Delete task types. The "Update" category is relevant to revising SOPs. Located via WebSearch as an arXiv entry. The ACM TOIS journal version was **not confirmed by a tool this session**. — [arXiv](https://arxiv.org/abs/2401.17043v3)
- **BEIR (Thakur et al., NeurIPS 2021 D&B)** and **KILT (Petroni et al., NAACL 2021)**: no tool located these this session, so they are not formally cited here. They are canonical (BEIR established BM25 as a hard-to-beat zero-shot baseline across 18 datasets). Verify before citing.
- A NeurIPS 2024 D&B "Benchmark Suite for Retrieval Augmented Generation in ..." also came up; the title was truncated, so it is not cited. — [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/7c06759d1a8567f087b02e8589454917-Paper-Datasets_and_Benchmarks_Track.pdf)
- Survey/index of RAG evaluation work: "Evaluation of Retrieval-Augmented Generation: A Survey" repo. — [GitHub](https://github.com/yhpeter/awesome-rag-evaluation)

### Cited Findings — Multimodal document retrieval and text-only vs visual comparisons
- **Faysse, M., et al. (2025). "ColPali: Efficient Document Retrieval with Vision Language Models." ICLR 2025 [PR]**. ICLR 2025 slides found; also arXiv:2407.01449. Introduced the ViDoRe benchmark. Late-interaction retrieval over page images beat OCR/caption text pipelines on visually rich documents and was simpler to index. — [ICLR 2025 slides](https://www.iclr.cc/media/iclr-2025/Slides/27679_RMItJE2.pdf); [arXiv](https://arxiv.org/abs/2407.01449)
- **Yu, S., et al. (2024). "VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents." arXiv:2410.10594 [arXiv; I believe it appeared at ICLR 2025 but this session did not confirm it]**. Retrieves and generates over page images directly instead of parsed text, and reports end-to-end gains over text-based RAG. — [alphaXiv](https://www.alphaxiv.org/abs/2410.10594)
- **Cho, J., et al. (2024). "M3DocRAG: Multi-modal Retrieval is What You Need for Multi-page Multi-document Understanding." arXiv:2411.04952 [arXiv, not peer-reviewed as located]**. — [alphaXiv](https://www.alphaxiv.org/abs/2411.04952)
- **ViDoRe V3 (2026). "A Comprehensive Evaluation of RAG in Complex Real-World Scenarios." arXiv:2601.08620 [arXiv, not peer-reviewed]**. Extends ViDoRe to end-to-end RAG with visual elements and multi-document synthesis. — [alphaXiv](https://www.alphaxiv.org/abs/2601.08620)
- **"Comparison of Text-Based and Image-Based Retrieval in Multimodal RAG LLM Systems" (2025). arXiv:2511.16654 [arXiv, not peer-reviewed]**. A direct text-vs-image retrieval comparison, the M.A.C.H. vs text-only RAG question. — [alphaXiv](https://www.alphaxiv.org/abs/2511.16654)
- **"Evaluating Modern RAG: Textual, Multimodal, Dense, and Late Interaction Pipelines" (2026). arXiv:2608.23176 [arXiv, not peer-reviewed]**. — [alphaXiv](https://www.alphaxiv.org/abs/2608.23176)
- **"From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents" (2026). arXiv:2604.01733 [arXiv, not peer-reviewed]**. Compares BM25, dense, hybrid and corrective RAG on mixed text/table documents. — [arXiv](https://arxiv.org/html/2604.01733v1)
- **"MMLongBench-Doc-V2: A Corrected-Annotation, Semantics-Aware Revision of MMLongBench-Doc" (2026). arXiv:2608.03397 [arXiv, not peer-reviewed]**. Says the original MMLongBench-Doc (1,082 questions over 135 PDFs) has annotation errors and a reference metric that distorts scores. The lesson: audit your own gold labels. — [alphaXiv](https://www.alphaxiv.org/abs/2608.03397)
- **"One Fact, Many Places: Redundant Evidence in Long Visual Documents Breaks Single-Gold Evaluation of Retrieval, Citation and Attribution" (2026). arXiv:2610.26401 [arXiv, not peer-reviewed]**. Single-gold evidence labels under-credit correct retrieval and citations when a fact appears in several places. This is highly relevant to SOP corpora, where safety warnings repeat across documents and revisions. — [alphaXiv](https://www.alphaxiv.org/abs/2610.26401)
- **"VisR-RAG-Fin" (2026), arXiv:2610.24822 [arXiv, not peer-reviewed]**. A domain-specific multimodal RAG benchmark (finance). An example of how to build a vertical test set. — [alphaXiv](https://www.alphaxiv.org/abs/2610.24822)

### Inferences — what reviewers will expect
- **Baselines** (all on the same corpus, chunking and generator):
  1. BM25 alone, with no generation: return top-k passages.
  2. BM25 + LLM (sparse RAG).
  3. Dense text RAG over OCR/parsed text, the "text-only RAG" baseline.
  4. Hybrid BM25 + dense with RRF.
  5. M.A.C.H.: multimodal page/figure retrieval + agentic loop + citations + abstention.
- **Ablations**: remove visual retrieval; remove the agentic re-query; remove the reranker; remove version/supersession filtering; remove abstention; remove the template constraint and STE rules (for the drafting task).
- **Metrics**:
  - Retrieval: Recall@{5,10}, nDCG@10, MRR, with graded qrels and multi-gold evidence sets (because of the redundancy issue above).
  - Generation: answer correctness against a reference; faithfulness (RAGAS-style claim entailment); citation precision/recall (ALCE-style); CRAG-style accurate/missing/hallucinated rates with a penalty for hallucination.
  - Procedure-specific: step-order correctness (Kendall tau or exact sequence match), parameter fidelity (torque, temperature and tool IDs exactly correct), and safety-warning recall.
- **Statistics**: paired tests per query (paired randomisation/permutation or bootstrap; Wilcoxon signed-rank). Report effect sizes with 95% bootstrap confidence intervals, and apply a multiple-comparison correction such as Holm across baselines. The canonical IR significance-testing papers (Smucker et al., CIKM 2007; Dror et al., ACL 2018) were **not located by a tool this session**; verify before citing.
- **Test-set size**: a few hundred queries, stratified by modality and question type, is in the range of ARES's human-annotation budget. Hold out a dev split so prompts are not tuned on the test set.

### Gaps
- I found no peer-reviewed benchmark of multimodal RAG on manufacturing SOPs or work instructions specifically. The domain multimodal benchmarks I found are in finance and general documents, and mostly arXiv.
- Peer-reviewed head-to-head studies of BM25 vs dense vs hybrid in *technical/industrial* domains were not found this session. The results came back as arXiv preprints, blogs and an IJERT paper of low credibility.

---

## Q3. How reliable is LLM-as-judge versus human judgment for faithfulness and procedural correctness?

### Takeaway
LLM judges agree with humans about as well as humans agree with each other on general preference and relevance tasks. They are biased (position, verbosity, self-preference), inconsistent across repeated runs, and close to random on hard, knowledge-heavy pairs. For procedural correctness in a specialist domain, nothing validates them yet. They should therefore be *calibrated against a human-annotated subset* (ARES-style), not trusted on their own.

### Cited Findings
- **Zheng, L., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." NeurIPS 2023 Datasets & Benchmarks [PR]**. GPT-4 as judge agreed with humans at over 80%, about the same as human–human agreement. The paper documents position, verbosity and self-enhancement biases. Located by title; the OpenAlex search failed (403). — Canonical; [LLM-judge discussion page (SIGIR 2025 perspective, Balog et al.)](https://krisztianbalog.com/files/sigir2025-llms.pdf). *Note: the Zheng URL itself was not retrieved this session. Confirm the DOI/URL before final citation.*
- **Tan, S., et al. (2025). "JudgeBench: A Benchmark for Evaluating LLM-Based Judges." ICLR 2025 [PR]**. On challenging response pairs across knowledge, reasoning, math and coding, strong models (e.g., GPT-4o) did only slightly better than random. Judges are weak exactly where correctness needs expertise, as procedural correctness does. — [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/file/9e720fce64f91114c49cfd640d821da3-Paper-Conference.pdf)
- **Thomas, P., Spielman, S., Craswell, N., Mitra, B. (2024). "Large Language Models can Accurately Predict Searcher Preferences." SIGIR 2024 [PR]**. In Bing, LLM relevance labels with a well-designed prompt matched or exceeded third-party human labellers. This supports LLM-generated qrels for retrieval metrics. — [Microsoft Research](https://microsoft.com/en-us/research/publication/large-language-models-can-accurately-predict-searcher-preferences); [arXiv](https://arxiv.org/abs/2309.10621)
- **"Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards." EMNLP 2025 Industry Track [PR]**. Builds a faithfulness and hallucination judging approach for RAG, checked against human annotation. — [ACL Anthology](https://aclanthology.org/2025.emnlp-industry.54/)
- **"Rating Roulette: Self-Inconsistency in LLM-As-A-Judge..." Findings of EMNLP 2025 [PR]**. LLM judges give different ratings to the same item across runs, so report judge variance and use repeated or majority judgments. — [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1361.pdf)
- **"Evaluating Alignment and Vulnerabilities in LLMs-as-Judges." GEM Workshop 2025 [PR, workshop]**. Judges can be manipulated, and they agree with humans less than headline numbers suggest. — [ACL Anthology](https://aclanthology.org/2025.gem-1.33.pdf)
- **"LLMs-as-Judges in Automatic Evaluation of Free-Form QA." WiNLP 2025 [PR, workshop]**. — [ACL Anthology](https://aclanthology.org/2025.winlp-main.37.pdf)
- **Balog, K., et al. (2025). "Rankers, Judges, and Assistants: Towards Understanding the Interplay of LLMs in Information Retrieval Evaluation." SIGIR 2025 perspective [PR]**. Warns about circularity when the same or similar LLMs both rank and judge, which inflates LLM-based systems' scores. — [PDF](https://krisztianbalog.com/files/sigir2025-llms.pdf)
- "Judge's Verdict: A Comprehensive Analysis of LLM Judge Capability Through Human Agreement" (2025), arXiv:2510.09738 [arXiv, not peer-reviewed]. — [arXiv](https://arxiv.org/abs/2510.09738)
- ARES (above) shows a statistical remedy: prediction-powered inference that combines many LLM judgments with a small human-labelled set and yields valid confidence intervals. — [ACL Anthology](https://aclanthology.org/2024.naacl-long.20.pdf)

### Inferences
- For M.A.C.H.:
  - Use LLM judges for scale, but use a judge from a **different model family** than the generator, to avoid Balog et al.'s circularity concern.
  - Double-annotate a stratified human subset of at least 100–200 items with process/quality engineers, and report Cohen's or Krippendorff's κ between humans and between humans and the judge.
  - Run the judge several times (Rating Roulette), randomise answer order (Zheng et al.), and correct estimates with PPI (ARES).
- Safety-critical fields (torques, part numbers, warnings) should be checked **deterministically** by exact match against source values. An LLM judge should not decide them; JudgeBench shows judges are weakest on knowledge-heavy correctness.

### Gaps
- I found no study validating LLM judges for *procedural* correctness (step order, missing preconditions, safety warnings) in manufacturing.
- I found no study of LLM judges on multimodal (figure-grounded) faithfulness in technical documents.

---

## Q4. What gaps exist? Gaps and novelty opportunities for M.A.C.H., plus recommended evaluation protocol

### Takeaway
The open space is the intersection of: (1) **multimodal** retrieval over SOPs with figures, tables and drawings; (2) **version-aware** retrieval (superseded revisions); (3) LLM **drafting of revisions** under **controlled language and templates**; and (4) **human change-control review** measured as the outcome. Each piece exists separately, mostly as preprints or conference papers. I found no peer-reviewed system or benchmark that combines them.

### Cited Findings (supporting the gap claims)
- Peer-reviewed generation of assembly instructions exists, but it is limited to conference papers and has no shared benchmark — [Meyer et al. 2024](https://doi.org/10.1109/etfa61755.2024.10710806); [Widulle et al. 2024](https://doi.org/10.1109/indin58382.2024.10774545); [Leder et al. 2026](https://doi.org/10.1016/j.procs.2026.02.035)
- Manufacturing RAG assistants are evaluated as assistants, not as document authors — [Colabianchi et al. 2024](https://doi.org/10.1016/j.compind.2024.104129); [Ludwig et al. 2025](https://doi.org/10.1016/j.compind.2025.104289)
- Multimodal page retrieval beats text pipelines on visually rich documents in general benchmarks, but no SOP benchmark exists — [ColPali, ICLR 2025](https://www.iclr.cc/media/iclr-2025/Slides/27679_RMItJE2.pdf); [VisRAG](https://www.alphaxiv.org/abs/2410.10594)
- Negative rejection and counterfactual robustness are weak spots for RAG, which relates to outdated or conflicting SOP revisions — [RGB, AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29728/31250)
- Single-gold evaluation breaks when evidence is redundant — [arXiv:2610.26401](https://www.alphaxiv.org/abs/2610.26401)
- LLM judges are unreliable on expert-level correctness — [JudgeBench, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/9e720fce64f91114c49cfd640d821da3-Paper-Conference.pdf)
- Human oversight must allow override and address automation bias — [EU AI Act Art. 14](https://euaiact.com/article/14)

### Inferences — Novelty opportunities
1. **The first SOP-specific multimodal RAG test set (a "MACH-Bench")**. Questions are stratified by evidence modality (text, table, figure/diagram, cross-page), by type (lookup, multi-hop, procedural-sequence, unanswerable, superseded-revision trap), and come with multi-gold evidence sets.
2. **A version-aware robustness test**. Inject superseded SOP revisions as counterfactual distractors, in the style of RGB counterfactual robustness, and measure how often the system cites an obsolete revision.
3. **Change-control outcome metrics for generated drafts**:
   - reviewer accept / minor-edit / reject rate;
   - normalised edit distance from draft to approved version;
   - time to approve;
   - **error-detection rate on seeded faults**, which tests whether reviewers catch planted wrong torques or missing warnings. This directly measures automation bias under Art. 14.
4. **An empirical test of ASD-STE100 or template constraints** (constrained vs free generation), measuring STE-rule violations, readability, step-level correctness and reviewer edit effort. No peer-reviewed evidence exists, so even a small controlled ablation is novel.
5. **A validated judge for procedural correctness**. Report human–judge κ for step order, preconditions and warnings, with PPI-corrected estimates.

### Inferences — Recommended evaluation protocol (hackathon-feasible, reviewer-defensible)
**Corpus**: the target plant's SOPs, WIs, drawings and maintenance manuals, including at least 2 revisions for a subset so supersession can be tested. Freeze the corpus snapshot and hash it.

**Test set (about 200–300 queries, plus 20–40 drafting tasks)**:
- Write queries from real shop-floor questions (operators, quality engineers), and add LLM-proposed questions that a human has edited. Tag each query with modality, type and difficulty.
- Include 10–15% unanswerable queries and 10% supersession traps.
- Make a dev/test split of about 30/70. Tune prompts only on dev.
- Gold labels: answer, all supporting evidence locations (multi-gold), and for procedure questions the ordered step list and the critical parameters.
- Have two domain annotators label a subset of at least 25%; report κ and adjudicate disagreements.

**Systems**:
1. BM25 alone (retrieval only).
2. BM25 + LLM.
3. Dense text RAG over OCR text.
4. Hybrid (RRF).
5. M.A.C.H. in full.
6. Ablations: no visual retrieval, no agentic loop, no reranker, no version filter, no abstention, no template/STE.

Hold the generator LLM, top-k and context budget constant across systems.

**Metrics**:
- Retrieval: Recall@5/10, nDCG@10, MRR (multi-gold, graded).
- Answer: correctness (human, or a calibrated judge), CRAG-style accurate/missing/hallucinated with a hallucination penalty, faithfulness (RAGAS-style), citation precision/recall (ALCE-style).
- Procedure: Kendall τ on step order; exact-match rate on critical parameters; safety-warning recall.
- Robustness: superseded-citation rate; abstention precision/recall on unanswerable queries.
- Drafting: STE/template rule violations (automated checker), reviewer accept/edit/reject rate, normalised edit distance, time to approve, seeded-fault detection rate.
- Operational: latency (p50/p95) and cost per query.

**Judging**:
- The LLM judge comes from a different family than the generator and runs 3 times with order randomisation.
- Validate it against human labels on a subset of at least 100 items and report κ.
- Apply ARES-style PPI to report corrected confidence intervals.
- Check critical parameters deterministically.

**Statistics**:
- Per-query paired comparisons of M.A.C.H. vs each baseline: paired bootstrap (10k resamples) or a permutation test; Wilcoxon for ordinal scores.
- Holm correction across comparisons; effect sizes with 95% confidence intervals.
- Break results down by modality stratum to show *where* multimodality helps.

**Human evaluation protocol (drafting)**:
- Blinded review: reviewers do not know whether a draft came from M.A.C.H. or a baseline/human author, and the order is randomised.
- Use a structured rubric: technical correctness, completeness, safety, clarity/STE compliance, and conformance to the template.
- Report seeded-fault catch rates as evidence of oversight effectiveness.

### Gaps
- No tool located primary GMP texts (EU GMP Annex 11 / Chapter 4, 21 CFR 211/Part 11) or the ISO 9001:2015 clause 7.5 text. Cite them from the standards themselves.
- No tool confirmed citations for BEIR, KILT, CRUD-RAG (TOIS version), MMLongBench-Doc (original venue), DocVQA, Smucker et al. 2007 or Dror et al. 2018 this session. Verify them before including.
- Authors and detailed results for several Springer chapters (CNL assembly instructions, AIssembly, smart-maintenance RAG) were not retrieved.
