# Grounded Answer Generation with Citations, Faithfulness/Hallucination Detection, and Abstention for RAG (for M.A.C.H.)

> Scope: 2023–2026, peer-reviewed first. Every paper below was located with WebSearch or WebFetch during this session. The OpenAlex/arXiv reference-lookup tools (search_works, verify_reference) could not run: the proxy blocked them with "Tunnel connection failed: 403", so no DOI/metadata was cross-checked through OpenAlex. Venues come from ACL Anthology, PMLR, ICLR proceedings, Nature/Wiley/TACL landing pages that turned up in search results. **Number provenance:** figures marked (F) were read from the fetched paper/page this session. Figures marked (R) are well-known headline numbers from the paper, recalled but not re-fetched. The report writer should treat (R) figures as "verify before quoting verbatim".

## Paper registry (quick reference)

| # | Authors, year | Title | Venue | Link | Peer-reviewed? | One-line key finding |
|---|---|---|---|---|---|---|
| 1 | Gao, Yen, Yu, Chen, 2023 | Enabling Large Language Models to Generate Text with Citations (ALCE) | EMNLP 2023 (main) | https://preview.aclanthology.org/setup/2023.emnlp-main.398 ; arXiv 2305.14627 | Yes | First reproducible citation benchmark; NLI-based citation recall/precision; best models lack full citation support ~50% of the time on ELI5 (R) |
| 2 | Asai, Wu, Wang, Sil, Hajishirzi, 2024 | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | ICLR 2024 | https://iclr.cc/virtual/2024/poster/18095 ; https://arxiv.org/html/2310.11511 | Yes | Reflection tokens (Retrieve/IsRel/IsSup/IsUse) give on-demand retrieval + self-critique; beats ChatGPT on ASQA citation precision (R) |
| 3 | Yan, Gu, Zhu, Ling, 2024 | Corrective Retrieval Augmented Generation (CRAG) | arXiv 2401.15884 | https://arxiv.org/pdf/2401.15884 | [arXiv, not peer-reviewed] (no venue version found in this session) | Lightweight retrieval evaluator labels retrieval Correct/Incorrect/Ambiguous and triggers refinement or web-search fallback; plug-in over RAG/Self-RAG |
| 4 | Es, James, Espinosa-Anke, Schockaert, 2024 | RAGAs: Automated Evaluation of Retrieval Augmented Generation | EACL 2024 System Demonstrations | https://preview.aclanthology.org/naacl24-info/2024.eacl-demo.16 | Yes (demo track) | Reference-free LLM-judged faithfulness, answer relevance, context relevance |
| 5 | Saad-Falcon, Khattab, Potts, Zaharia, 2024 | ARES: An Automated Evaluation Framework for RAG Systems | NAACL 2024 (long) | https://preview.aclanthology.org/setup/2024.naacl-long.20 | Yes | Fine-tuned lightweight LM judges + prediction-powered inference (PPI) give confidence intervals from a small human-labelled set |
| 6 | Li, Yue, Liao, Sun, 2024 | AttributionBench: How Hard is Automatic Attribution Evaluation? | Findings of ACL 2024 | https://aclanthology.org/2024.findings-acl.886 | Yes | Even fine-tuned GPT-3.5 reaches only ~80% macro-F1 at judging attribution (F) |
| 7 | Min et al., 2023 | FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation | EMNLP 2023 | (located via search for ALCE-line work; ACL Anthology 2023.emnlp-main) | Yes | Atomic-fact decomposition + retrieval verification; ChatGPT biographies ~58% FActScore (R) |
| 8 | Niu et al., 2024 | RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models | ACL 2024 (long) | https://aclanthology.org/2024.acl-long.585 | Yes | Word/span-level hallucination labels on ~18k RAG responses; fine-tuned small detectors are competitive with GPT-4 prompting (R) |
| 9 | Farquhar, Kossen, Kuhn, Gal, 2024 | Detecting hallucinations in large language models using semantic entropy | Nature 630 (2024) | https://oatml.cs.ox.ac.uk/publications/202406_FarquharKossenKuhn_HallucinatingLLMs.html ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11186750 | Yes | Entropy over meaning-clusters of sampled answers detects confabulations; AUROC ≈0.79 vs ≈0.69–0.70 for baselines on average (R) |
| 10 | Mohri & Hashimoto, 2024 | Language Models with Conformal Factuality Guarantees | ICML 2024 (PMLR 235) | https://proceedings.mlr.press/v235/mohri24a.html | Yes | Conformal "back-off": drop low-confidence sub-claims until a user-set correctness level (e.g. 80–90%) is guaranteed (R) |
| 11 | Kang, Gürel, Yu, Xu, Li, 2024 | C-RAG: Certified Generation Risks for Retrieval-Augmented Language Models | ICML 2024 | https://arxiv.org/pdf/2402.03181 ; https://openreview.net/pdf/c57b645c75b0ba2f777be4c7cae7a4484ae4da27.pdf | Yes | Conformal upper bounds on RAG generation risk; proves RAG gets a lower certified risk than no-retrieval under conditions (R) |
| 12 | Abbasi-Yadkori, Kuzborskij, Stutz, et al. (Google DeepMind), 2024 | Mitigating LLM Hallucinations via Conformal Abstention | arXiv 2405.01563 (NeurIPS 2024 virtual listing found: https://neurips.cc/virtual/2024/105548, likely workshop) | https://arxiv.org/pdf/2405.01563 | [arXiv, not peer-reviewed]; venue status unclear | Self-consistency "match count" score + conformal risk control bounds hallucination rate ≤ α with less abstention than log-prob scores (F) |
| 13 | Li et al., 2023 | TRAC: Trustworthy Retrieval Augmented Chatbot | arXiv 2307.04642 | https://arxiv.org/html/2307.04642v1 | [arXiv, not peer-reviewed] | Conformal prediction on both retrieval and generation yields answer sets with coverage guarantees |
| 14 | Song, Sim, Bhardwaj, Chieu, Majumder, Poria, 2025 | Measuring and Enhancing Trustworthiness of LLMs in RAG through Grounded Attributions and Learning to Refuse (Trust-Score / Trust-Align) | ICLR 2025 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/4c88827decab6c046b881a2c3a99c76f-Abstract-Conference.html | Yes | Joint metric for grounded answers, citations, and correct refusal; alignment gives 26/27 models large gains (F) |
| 15 | Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang, 2025 | Know Your Limits: A Survey of Abstention in Large Language Models | TACL 2025 (doi 10.1162/tacl_a_00754) | https://transacl.org/index.php/tacl/article/view/7077 ; https://arxiv.org/abs/2407.18418 | Yes | Taxonomy of abstention by query, model, and human-value perspectives; covers methods across the LLM lifecycle and abstention metrics |
| 16 | Zhang et al. (THUDM), 2024 | LongCite: Enabling LLMs to Generate Fine-grained Citations in Long-context QA | arXiv 2409.02897; author page found in ACL Anthology (venue version likely 2025, unconfirmed) | https://arxiv.org/abs/2409.02897 | Treat as [arXiv, not peer-reviewed] unless venue confirmed | Sentence-level citations from long context; LongCite-8B/9B beat GPT-4o on citation F1 in LongBench-Cite (R) |
| 17 | Ma, Zhuang, Koopman, Zuccon, Chen, Lin, 2025 | VISA: Retrieval Augmented Generation with Visual Source Attribution | ACL 2025 (long) | https://preview.aclanthology.org/setup/2025.acl-long.1456 ; https://arxiv.org/html/2412.14457v1 | Yes | VLM answers and draws a bounding box on the source page screenshot; zero-shot 1.5% box accuracy → 54–68% after fine-tuning (F) |
| 18 | De Grandis, Cappelletti, Raccagni, Cornia, Baraldi, Cucchiara, 2026 | DocAttriBench: Benchmarking Answer Grounding in Document VQA | arXiv 2609.20574 | https://arxiv.org/pdf/2609.20574 | [arXiv, not peer-reviewed] | Layout-element grounding; zero-shot Box F1 <40% even for >30B MLLMs (F) |
| 19 | Ma, Li, Wang, et al. (PKU / Shanghai AI Lab), 2026 | CiteVQA: Benchmarking Evidence Attribution for Trustworthy Document Intelligence | arXiv 2605.12882 | https://arxiv.org/html/2605.12882 | [arXiv, not peer-reviewed] | "Attribution hallucination": answer accuracy far exceeds strict attributed accuracy (GPT-5.4 87.1 vs 59.0) (F) |
| 20 | Magesh, Surani, Dahl, Suzgun, Manning, Ho, 2025 | Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools | Journal of Empirical Legal Studies 22:216–242, doi 10.1111/jels.12413 | https://nlp.stanford.edu/~manning/papers/Magesh-Hallucination%E2%80%90Free-2025.pdf | Yes | Commercial legal RAG tools hallucinate on 17–33% of queries, counting "misgrounded" citations (F) |
| 21 | Wu, Wu, … Zou et al., 2025 | An Automated Framework for Assessing How Well LLMs Cite Relevant Medical References (SourceCheckup) | Nature Communications 2025 (arXiv 2402.02008) | https://law.stanford.edu/publications/an-automated-framework-for-assessing-how-well-llms-cite-relevant-medical-references/ ; https://arxiv.org/abs/2402.02008 | Yes | 50–90% of LLM medical responses not fully supported by their cited sources; even GPT-4o with web search ~30% unsupported statements (R) |
| 22 | Siouffi, Glandon, Kubler, Soumianarayanan, 2025 | LLM-based Contrastive Representation Learning for Enhanced Maintenance Work Order Retrieval (SEASONED) | Procedia CIRP 134:981–986 (CIRP CMS 2025), doi 10.1016/j.procir.2025.02.230 | https://orbilu.uni.lu/bitstream/10993/65242/1/1-s2.0-S2212827125006158-main.pdf | Yes (conference proceedings journal) | Industrial maintenance retrieval MRR 0.80 vs 0.64 for Ada-002; no generation/hallucination measured (F) |

---

## Q1. Which peer-reviewed methods give the most reliable citations, and how are citation precision and recall measured?

### Takeaway
The de-facto measurement standard is **ALCE-style NLI-based citation recall and precision**, often computed with an NLI model such as TRUE/T5-11B or an LLM judge. Within peer-reviewed work, the most reliable citations come from **models trained for attribution**: Self-RAG (ICLR 2024), Trust-Align (ICLR 2025), and fine-grained or sentence-level citation training such as LongCite. Prompt-only citing is less reliable. Automatic attribution judges are themselves only about 80% accurate (AttributionBench), so verification is a noisy signal, not ground truth.

### Cited Findings
**Benchmarks and metric definitions**
- ALCE introduced the first reproducible benchmark for LLM generation with citations, spanning ASQA, QAMPARI and ELI5, and scores fluency, correctness, and citation quality automatically — [ACL Anthology, EMNLP 2023](https://preview.aclanthology.org/setup/2023.emnlp-main.398); [arXiv 2305.14627](https://arxiv.org/abs/2305.14627v2); [code](https://github.com/fallcat/ALCE)
  - **Citation recall:** a statement counts as supported when the concatenation of its cited passages entails it, as judged by an NLI model.
  - **Citation precision:** a citation counts as irrelevant when it neither supports the statement alone nor is needed for the full set of citations to support it.
  - Reported finding (R): even the best models lacked complete citation support about 50% of the time on ELI5.
- Self-RAG trains one LM to emit reflection tokens: Retrieve, IsREL (passage relevance), IsSUP (fully, partially, or not supported) and IsUSE. Generation is then a segment-level beam search weighted by these critique scores. The paper reports higher citation precision than ChatGPT on ASQA. — [ICLR 2024](https://iclr.cc/virtual/2024/poster/18095); [arXiv](https://arxiv.org/html/2310.11511); [mlanthology](https://mlanthology.org/iclr/2024/asai2024iclr-selfrag)
  - (R) Self-RAG 13B: about 70 citation precision and 71 citation recall on ASQA. ChatGPT: about 65 precision and 77 recall. Self-RAG favours precision, ChatGPT favours recall.
- Trust-Score (ICLR 2025) is a holistic RAG trustworthiness metric. It jointly measures grounded answer correctness, citation quality, and whether the model correctly refuses when documents do not contain the answer. — [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4c88827decab6c046b881a2c3a99c76f-Abstract-Conference.html)
  - (F) Trust-Align improved 26 of 27 aligned models over competitive baselines on ASQA, QAMPARI and ELI5.
  - (F) LLaMA-3-8B gained +12.56 on ASQA, +36.04 on QAMPARI and +17.69 on ELI5 over the FRONT baseline, alongside better refusal and citation quality. — [arXiv 2409.11242](https://arxiv.org/abs/2409.11242v3)

**Fine-grained citation (not peer-reviewed)**
- LongCite moves from passage-level citations to sentence-level citations inside long contexts, using the LongBench-Cite benchmark and a CoF ("coarse-to-fine") data pipeline. (R) Its 8B/9B models outperform GPT-4o on citation F1. [arXiv, not peer-reviewed / venue unconfirmed] — [arXiv 2409.02897](https://arxiv.org/abs/2409.02897)
- Follow-ups located in search but not read in depth, all [arXiv, not peer-reviewed]:
  - Factual-consistency-model-guided citation learning — [arXiv 2406.13124](https://arxiv.org/pdf/2406.13124)
  - "Learning Fine-Grained Grounded Citations for Attributed LLMs" — [arXiv 2408.04568](https://arxiv.org/pdf/2408.04568)
  - FineRef, fine-grained error reflection and correction for citations, 2026 — [arXiv 2602.18437](https://arxiv.org/pdf/2602.18437)

**Faithfulness evaluators and their reliability**
- RAGAS defines three reference-free metrics:
  - **Faithfulness:** the fraction of answer statements an LLM can infer from the context.
  - **Answer relevance.**
  - **Context relevance.**
  - (R) On its WikiEval set, RAGAS faithfulness agreed with humans far better than direct GPT-3.5 scoring, about 0.95 vs 0.72.
  - [EACL 2024 demo](https://preview.aclanthology.org/naacl24-info/2024.eacl-demo.16); [Cardiff ORCA](https://orca.cardiff.ac.uk/166780)
- ARES fine-tunes small LM judges on synthetic data for context relevance, answer faithfulness, and answer relevance. It applies prediction-powered inference (PPI) to a small human-annotated validation set, about a few hundred items, to produce **confidence intervals** on system scores. — [NAACL 2024](https://preview.aclanthology.org/setup/2024.naacl-long.20); [bib](https://aclanthology.org/2024.naacl-long.20.bib)
- FActScore splits long-form output into atomic facts and checks each against a knowledge source. (R) ChatGPT scored about 58% on biographies, and the automated estimator came within about 2% of human FActScore. — EMNLP 2023 (found in this search space; ACL Anthology entry)
- AttributionBench combines 7 attribution datasets into a test of whether an answer is supported by its cited evidence. (F) Even a fine-tuned GPT-3.5 reaches only about 80% macro-F1 in binary classification. An analysis of more than 300 errors blames:
  - difficulty with nuanced information;
  - a gap between what the model sees and what annotators used.
  - Sources: [Findings ACL 2024](https://aclanthology.org/2024.findings-acl.886); [arXiv 2402.15089](https://arxiv.org/abs/2402.15089)
- RAGTruth provides span-level hallucination annotations for responses from several LLMs on RAG tasks: QA, data-to-text and summarization. It supports training hallucination detectors, and (R) a fine-tuned Llama-2-13B detector is competitive with GPT-4-prompted detection. — [ACL 2024](https://aclanthology.org/2024.acl-long.585)

### Inferences
- For M.A.C.H., "reliable citations" should be operationalised as ALCE recall/precision at the **SOP step level**, not the passage level. Steps are atomic, ordered and safety-tagged, which makes entailment checking much more tractable than open-ended ELI5 answers.
- Because automatic judges reach only about 80% (AttributionBench), a production system should combine:
  - (a) constrained generation, where the model can only quote or point to retrieved step IDs;
  - (b) an independent NLI/LLM verifier;
  - (c) a human-labelled calibration set, à la ARES/PPI, to report confidence intervals instead of point scores.
- Self-RAG's precision-over-recall behaviour is the right bias for a safety setting: fewer, correct citations beat many loose ones.

### Gaps
- No peer-reviewed study found reports citation precision/recall on **procedural/SOP documents** specifically.
- No head-to-head peer-reviewed comparison of RAGAS vs ARES vs NLI checkers on the same industrial data was found.
- The exact numeric tables for ALCE, Self-RAG, RAGAS and FActScore were not re-fetched this session (marked R).

---

## Q2. What are the best methods to decide when a RAG system should abstain, and which give statistical guarantees (conformal)?

### Takeaway
There are three families:
1. **Learned or self-reflective gating:** Self-RAG IsSUP tokens, CRAG retrieval evaluator, Trust-Align refusal training.
2. **Sampling-based uncertainty:** semantic entropy (Nature 2024), self-consistency match counts.
3. **Conformal and risk-control wrappers:** conformal factuality (ICML 2024), C-RAG (ICML 2024), conformal abstention, TRAC.

Only family 3 gives **finite-sample, distribution-free guarantees**, such as "hallucination risk ≤ α", and only under exchangeability between calibration and deployment data. The best practical recipe stacks a strong uncertainty score from family 2 inside a conformal calibrator from family 3.

### Cited Findings
**Sampling-based uncertainty**
- Semantic entropy samples several answers, clusters them by bidirectional entailment, and computes entropy over meaning clusters. This detects "confabulations" (arbitrary, wrong generations) without task-specific training, across datasets and models. — [Nature 2024, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11186750); [OATML](https://oatml.cs.ox.ac.uk/publications/202406_FarquharKossenKuhn_HallucinatingLLMs.html)
  - (R) Average AUROC is about 0.79, against about 0.69–0.70 for naive entropy and P(True).
  - It also improves accuracy when used to refuse the most uncertain questions.

**Conformal and risk-control methods**
- Conformal factuality maps conformal prediction onto LLM outputs. It decomposes an output into sub-claims, then removes the least-confident claims until the remaining output is entailed with probability ≥ 1−α, i.e. it "backs off" to a less specific but correct answer. (R) Tested on QA and math with 80–90% target correctness while keeping most content. — [PMLR v235, ICML 2024](https://proceedings.mlr.press/v235/mohri24a.html); [ICML poster](https://icml.cc/virtual/2024/poster/32822)
- C-RAG provides conformal-risk-control certificates (upper bounds) on RAG generation risk. It also shows theoretically and empirically that RAG achieves lower certified risk than the bare LLM when retrieval quality is adequate, including under some distribution shift. — [arXiv 2402.03181](https://arxiv.org/pdf/2402.03181); [OpenReview PDF](https://openreview.net/pdf/c57b645c75b0ba2f777be4c7cae7a4484ae4da27.pdf)
- Conformal abstention (DeepMind) works in four steps:
  1. Sample several responses.
  2. Score their pairwise agreement with the LLM itself ("match count" / "expected match count").
  3. Calibrate an abstention threshold with conformal risk control (CRC), which guarantees expected hallucination risk ≤ α. RCPS variants give high-probability bounds instead.
  4. Calibrate the match function separately.
  - (F) On Temporal Sequences (long answers) at α=0.1 and n=3200, test loss was 0.065 for CRC with match count vs 0.084 for CRC with log-probabilities, with less abstention.
  - (F) On TriviaQA (short answers), log-prob scores were competitive.
  - [arXiv, not peer-reviewed; a NeurIPS 2024 virtual page exists, likely a workshop] — [arXiv 2405.01563](https://arxiv.org/pdf/2405.01563); [NeurIPS listing](https://neurips.cc/virtual/2024/105548)
- TRAC applies conformal prediction to both the retriever and the generator, giving answer sets with a coverage guarantee. [arXiv, not peer-reviewed] — [arXiv 2307.04642](https://arxiv.org/html/2307.04642v1)

**Learned or self-reflective gating**
- CRAG uses a lightweight retrieval evaluator (T5-large) that grades retrieved documents. The grade triggers one of three actions:
  - **Correct:** decompose-then-recompose knowledge refinement.
  - **Incorrect:** discard and fall back to web search.
  - **Ambiguous:** combine both.
  - It is plug-and-play over standard RAG and Self-RAG. [arXiv, not peer-reviewed] — [arXiv 2401.15884](https://arxiv.org/pdf/2401.15884); [code](https://github.com/HuskyInSalt/CRAG)
- Trust-Align explicitly trains refusal when retrieved documents do not contain the answer. Trust-Score rewards correct refusals and penalises over-refusal. — [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4c88827decab6c046b881a2c3a99c76f-Abstract-Conference.html)

**Survey**
- The TACL 2025 abstention survey organises abstention by three perspectives:
  - **Query:** answerable, ambiguous, or harmful.
  - **Model:** knowledge or confidence.
  - **Human values:** safety.
  - It reviews methods across pretraining, alignment and inference, plus abstention benchmarks and metrics such as abstention precision/recall and risk-coverage curves. It notes that over-abstention and evaluation inconsistency remain open. — [TACL](https://transacl.org/index.php/tacl/article/view/7077); [arXiv 2407.18418](https://arxiv.org/abs/2407.18418); [doi 10.1162/tacl_a_00754](https://api.crossref.org/works/10.1162%2FTACL_A_00754)

### Inferences
- **Recommended M.A.C.H. abstention stack**, each step a gate:
  1. **Retrieval sufficiency gate:** CRAG-style evaluator. If no SOP chunk for the right machine, model, or revision, then escalate. Do not fall back to the web, which is unsafe on a shop floor.
  2. **Support gate:** NLI/IsSUP check for every generated step against its cited step.
  3. **Uncertainty gate:** semantic entropy or match-count across about 5 samples.
  4. **Conformal threshold:** CRC calibrated on a labelled set of shop-floor Q&A, giving a stated guarantee such as "≤5% unsupported instructions among answered queries".
  5. **Conformal-factuality back-off:** drop uncertain sub-steps and tell the operator which part is missing, rather than abstaining wholesale.
- The conformal guarantee is **marginal and needs exchangeability**. A new machine, an SOP revision, or a new operator phrasing breaks it, so recalibration must be tied to document version control.
- Per-hazard-class risk levels (α lower for LOTO or energy-isolation steps than for cleaning steps) would need class-conditional (Mondrian) conformal calibration. None of the located papers did this for RAG.

### Gaps
- No located paper gives conformal guarantees for **multimodal** (figure/table) RAG answers.
- No located paper studies abstention calibration under SOP document drift or versioning.
- Semantic entropy's cost (multiple samples plus entailment clustering) for real-time shop-floor latency was not quantified in the sources read.

---

## Q3. How do these methods perform with multimodal evidence (figures, tables), and is there work on visual citation or grounding?

### Takeaway
Visual citation is an emerging but **weak** capability:
- Zero-shot VLMs barely localise evidence. Qwen2-VL-72B reaches 1.5% bounding-box accuracy on VISA, and models over 30B stay below 40% Box F1 on DocAttriBench.
- Fine-tuning helps substantially but not reliably: 54–68% on VISA and about 62–68% F1 on DocAttriBench.
- Even frontier models answer far better than they cite. CiteVQA calls this "attribution hallucination".

The only peer-reviewed anchor found is VISA (ACL 2025); the newer benchmarks are arXiv-only.

### Cited Findings
- **VISA (ACL 2025).** A VLM answers a question over retrieved page screenshots and draws a bounding box around the supporting region.
  - Datasets: Wiki-VISA (from NQ, about 87k train / 3k test) and Paper-VISA (from PubLayNet, about 100k train / 2.16k test).
  - (F) Zero-shot Qwen2-VL-72B: 1.5% box accuracy on both datasets.
  - (F) Fine-tuned VISA-7B: 54.2% on Wiki-VISA and 68.2% on Paper-VISA with a single oracle page, dropping to 37.7% and 59.9% in the multi-candidate setting.
  - (F) Cross-domain transfer is poor: Paper→Wiki 0.2%, Wiki→Paper 27.8%.
  - Sources: [ACL Anthology](https://preview.aclanthology.org/setup/2025.acl-long.1456); [arXiv 2412.14457](https://arxiv.org/html/2412.14457v1)
- **DocAttriBench (2026)** covers about 237k documents and 296k QA pairs, grounding answers to layout elements (text blocks, tables, images) with Box F1 at IoU 0.5. It defines three tasks: grounded answer generation, post-hoc grounding, and answer-locating. Labels come from "MAPPET": elements are ranked by how much masking them increases answer perplexity. [arXiv, not peer-reviewed] — [arXiv 2609.20574](https://arxiv.org/pdf/2609.20574)
  - (F) Zero-shot Box F1: below 40% for models over 30B, below 20% for 7–8B models, below 10% for 2–3B models.
  - (F) Best zero-shot model, Qwen3-VL-32B: about 44% answer-locating F1 and about 47% post-hoc F1.
  - (F) Fine-tuned MAPPET-I-8B: about 62% and 68%.
  - (F) Overall answer+grounding correctness is only about 37% for the best fine-tuned model, about 25% for the best zero-shot model, and 24% for VISA-7B.
- **CiteVQA (2026)** has 1,897 questions over 711 long PDFs (about 40.6 pages each), 7 domains and 2 languages. Its metric, Strict Attributed Accuracy (SAA), requires both a correct answer and correct element-level bounding-box evidence. [arXiv, not peer-reviewed] — [arXiv 2605.12882](https://arxiv.org/html/2605.12882)
  - (F) Gemini-3.1-Pro-Preview: SAA 76.0 (answer 86.1, recall 66.0).
  - (F) Best open model, Qwen3-VL-235B-A22B: SAA 22.5.
  - (F) GPT-5.4: answer 87.1 vs SAA 59.0. Gemini-3-Flash: answer 84.5 vs SAA 65.4.
  - (F) Recall falls from 68.9 to 55.3 when evidence spans multiple documents.

### Inferences
- For M.A.C.H., a figure or diagram citation (e.g. "torque pattern in Fig. 4, p. 12") must be treated as **lower-confidence than a text-step citation**. Even the best systems mis-localise visual evidence 25–45% of the time, and open-weight models do much worse.
- Practical mitigation: cite at the **page + figure-ID** level, using layout-parsed figure captions or IDs produced by the document parser, rather than relying on free VLM bounding boxes. Ask the VLM only to pick among pre-segmented layout elements, which turns grounding into classification. This mirrors DocAttriBench's layout-element formulation.
- VISA's near-zero cross-domain transfer suggests any visual-grounding model must be fine-tuned on in-domain SOP layouts: exploded views, P&IDs, wiring diagrams, torque tables.

### Gaps
- No located work evaluates visual citation on engineering drawings, exploded assembly views, or SOP photos.
- No located work combines visual grounding with conformal abstention.
- No peer-reviewed table-cell-level citation benchmark was located in this session. Tables appear only as layout elements in DocAttriBench/CiteVQA.

---

## Q4. What do safety-critical domain studies show about hallucination rates, and what are the gaps for safety-critical industrial use?

### Takeaway
Domain studies show that **RAG with citations does not eliminate hallucination**:
- Commercial legal RAG tools hallucinate on 17–33% of queries when misgrounded citations are counted (JELS 2025).
- In medicine, 50–90% of LLM responses are not fully supported by their own cited sources (Nature Communications 2025).

Peer-reviewed industrial/manufacturing work found so far evaluates **retrieval only**, not grounded generation or abstention. That is the core gap M.A.C.H. can address.

### Cited Findings
- **Legal (JELS 2025).** Magesh et al. tested Lexis+ AI, Westlaw AI-Assisted Research and Ask Practical Law AI. (F)
  - Lexis+ AI and Ask Practical Law AI hallucinated on more than 1 in 6 queries (about 17%).
  - Westlaw AI-Assisted Research hallucinated on about 1 in 3 queries.
  - The legal tools hallucinate less than GPT-4, but far from the "hallucination-free" marketing.
  - The definition counts as hallucination any response that is incorrect **or "misgrounded"**, meaning a citation that does not support the claim or is inapplicable.
  - Sources: [Stanford NLP PDF](https://nlp.stanford.edu/~manning/papers/Magesh-Hallucination%E2%80%90Free-2025.pdf); [Stanford Law](https://law.stanford.edu/publications/hallucination-free/); [RePEc](https://econpapers.repec.org/RePEc:wly:empleg:v:22:y:2025:i:2:p:216-242)
- **Medical (Nature Communications 2025).** SourceCheckup is an automated pipeline that checks whether the URLs and sources LLMs cite actually support their medical statements. (R) 50–90% of responses were not fully supported, and even GPT-4o with web search (a RAG setting) left about 30% of individual statements unsupported. — [Stanford Law listing](https://law.stanford.edu/publications/an-automated-framework-for-assessing-how-well-llms-cite-relevant-medical-references/); [arXiv 2402.02008](https://arxiv.org/abs/2402.02008); PMC full text located at [PMC12003634](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003634/) (the fetch was blocked by reCAPTCHA, so the numbers are R)
- **Industrial (Procedia CIRP 2025).** SEASONED fine-tunes a BERT retriever (TSDAE + triplet loss) on maintenance work orders.
  - (F) Proprietary Plansee data: MRR 0.80 / accuracy 0.76, vs Ada-002 at 0.64/0.55 and BM25 at 0.36/0.30.
  - (F) Open TechQA: only MRR 0.22.
  - (F) No hallucination or generation evaluation. The reported improvement percentages are internally inconsistent: the abstract claims 28–58%, the conclusion 21–27%.
  - Source: [Procedia CIRP 134, doi 10.1016/j.procir.2025.02.230](https://orbilu.uni.lu/bitstream/10993/65242/1/1-s2.0-S2212827125006158-main.pdf)
- **Industrial, not read.** An arXiv paper, "FactoryLLM: A Safe and Open-Source AI Playground for Evaluating LLMs in Smart Factories" (2026), was located but not read, so no claims are made about it. [arXiv, not peer-reviewed] — [arXiv 2606.14119](https://arxiv.org/pdf/2606.14119)

### Inferences
- The legal "misgrounded citation" category is exactly the failure mode M.A.C.H. must measure. A step cited to the wrong SOP revision or wrong machine variant is a hallucination even when the cited text exists.
- Medical and legal error rates (17–33% and up to about 30% unsupported statements, with RAG) are **orders of magnitude above** what a shop-floor instruction system can tolerate. Accuracy alone is therefore insufficient: an abstention-plus-escalation layer with a stated, calibrated risk bound is required.

### Gaps
- No peer-reviewed study reporting **hallucination rates of generative RAG on manufacturing SOPs or work instructions** was found in this session.
- No study links LLM hallucination to physical-safety outcomes (near-misses, scrap) in factories.
- The GPT-4 baseline numbers in the legal study were not extractable from the fetched text.

---

## Gaps and novelty opportunities for M.A.C.H.

These are inferences drawn from the gaps above.

1. **Step-level procedural attribution metric.** Extend ALCE citation recall/precision to *ordered* procedures. Score:
   - per-step support (entailment by the cited SOP step);
   - **order fidelity** (steps not reordered or skipped);
   - **safety-step completeness** (every PPE, LOTO, or warning step in the source appears in the answer).
   - No located benchmark measures omission of safety-critical steps.
2. **Version- and variant-aware "misgrounding" checks.** Adopt the JELS legal definition of misgrounded citation and add metadata constraints: machine model, SOP revision, plant. A citation is valid only when the text entails the claim **and** the metadata matches the operator's context.
3. **Conformal abstention with hazard-tiered risk budgets.** Combine semantic-entropy or match-count scores with conformal risk control (Mohri & Hashimoto; C-RAG; conformal abstention), calibrated **per hazard class** with Mondrian/class-conditional CRC. Report "≤α unsupported instructions among answered queries" with α_LOTO << α_general. No located RAG work does class-conditional, safety-tiered calibration.
4. **Conformal back-off for partial answers.** Instead of a binary abstain, return the certified subset of steps plus an explicit "escalate to supervisor for steps X–Y", following the conformal factuality back-off. This is novel for procedural QA.
5. **Multimodal citation via layout-element selection.** Given 1.5% zero-shot VISA accuracy and below 40% DocAttriBench F1, avoid free-form box prediction:
   - Parse SOPs into figure, table and step elements with IDs.
   - Have the model select element IDs.
   - Verify with a VLM entailment check.
   - Report "page/figure/step" citations with lower confidence for visual evidence.
   - No located work offers conformal guarantees on visual citations, which is an open niche.
6. **Drift-aware recalibration.** Conformal guarantees need exchangeability, so tie recalibration to SOP revision events and add monitoring that flags distribution shift, such as new machines or unseen query clusters. This is not addressed in the located literature.
7. **Evaluation with interval estimates.** Use ARES-style PPI with a small set of expert-labelled shop-floor Q&A, a few hundred items, to report confidence intervals on faithfulness and abstention quality, since automatic attribution judges reach only about 80% (AttributionBench).
8. **Over-abstention cost.** The TACL survey and Trust-Score both penalise needless refusal. M.A.C.H. should measure the *escalation rate* alongside safety, because a system that always escalates gets ignored on the shop floor. A risk-coverage curve is the natural demo artefact.
9. **First generative-RAG hallucination audit on manufacturing SOPs.** The peer-reviewed industrial work found evaluates retrieval only (Procedia CIRP 2025). A small, public, shop-floor-style benchmark that reports citation precision/recall, misgrounding rate, abstention precision/recall and visual-citation accuracy would itself be a novel contribution.
