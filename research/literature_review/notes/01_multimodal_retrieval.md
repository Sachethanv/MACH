# Multimodal Retrieval and RAG over Industrial and Technical Documents (for M.A.C.H.)

> **How these sources were checked:** The OpenAlex-backed reference tools (`search_works`, `verify_reference`) could not be used in this session. Every call returned "Tunnel connection failed: 403 Forbidden". Each paper below was found instead through WebSearch or alphaXiv, and its metadata was read from the publisher, proceedings, ACL Anthology, CVF or arXiv/alphaXiv page. Peer-review status is given only where a venue page confirmed it. If a venue is only claimed in arXiv metadata, the entry says so. Every arXiv-only item is labelled **[arXiv, not peer-reviewed]**.

## Source register (all papers cited)

| # | Authors | Year | Title | Venue | DOI / URL | Status | Key finding (one line) |
|---|---|---|---|---|---|---|---|
| P1 | Faysse, Sibille, Wu, Omrani, Viaud, Hudelot, Colombo | 2024/2025 | ColPali: Efficient Document Retrieval with Vision Language Models | Usually cited as ICLR 2025. The arXiv page fetched here names no venue. | https://arxiv.org/abs/2407.01449 | Venue not confirmed by a fetched page. Treat as arXiv until checked. | Late-interaction retrieval over page images scores 81.3 avg nDCG@5 on ViDoRe, against 65.5 for OCR+BM25 and 67.0 for captioning+BGE-M3, and indexes at 0.39 s/page against 7.22 s/page. |
| P2 | Yu, Tang, Xu, Cui, Ran, Yan, Liu, Wang, Han, Liu, Sun | 2025 | VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents | ICLR 2025 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/3640a1997a4c9571cea9db2c82e1fc35-Abstract-Conference.html | Peer-reviewed | Embeds and generates from page images. Reports a 20–40% end-to-end gain over text-based RAG. |
| P3 | Ma, Lin, Li, Chen, Lin | 2024 | Unifying Multimodal Retrieval via Document Screenshot Embedding (DSE) | EMNLP 2024 (main) | https://doi.org/10.18653/v1/2024.emnlp-main.373 | Peer-reviewed | Screenshot embedding beats BM25 by 17 points top-1 on Wiki-SS (1.3M pages) and beats OCR text retrieval by more than 15 nDCG@10 on slides. |
| P4 | Zhang, Zhang, Wang, Ouyang, Wen, Li, Chow, He, Zhang | 2025 | OCR Hinders RAG: Evaluating the Cascading Impact of OCR on Retrieval-Augmented Generation (OHRBench) | ICCV 2025, pp. 17443–17453 | https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html | Peer-reviewed | 8,561 page images and 8,498 QA pairs from 7 domains. No OCR solution tested was adequate for a high-quality RAG knowledge base. |
| P5 | Dong, Chang, Goh, Li, Tang, Liu (Huawei) | 2025 | MMDocIR: Benchmarking Multimodal Retrieval for Long Documents | arXiv; no venue on the fetched page | https://arxiv.org/abs/2501.08828 | [arXiv, not peer-reviewed] (venue unconfirmed) | 313 documents (avg 65.1 pages), 1,658 questions, 10 domains including "Admin & Industry". Visual retrievers beat text retrievers: ColPali R@5 about 80.8 against about 72.3. |
| P6 | Cho, Mahata, Irsoy, He, Bansal | 2024 | M3DocRAG: Multi-modal Retrieval is What You Need for Multi-page Multi-document Understanding | arXiv | https://arxiv.org/abs/2411.04952 | [arXiv, not peer-reviewed] (venue unconfirmed) | ColPali + Qwen2-VL 7B. Introduces M3DocVQA (>3,000 PDFs, >40,000 pages) and reaches SOTA on MP-DocVQA. |
| P7 | Loison, Macé, Edy, Xing, Balough, Moreira, Liu, Faysse, Hudelot, Viaud | 2026 | ViDoRe V3: A Comprehensive Evaluation of RAG in Complex Real-World Scenarios | arXiv | https://www.alphaxiv.org/abs/2601.08620 | [arXiv, not peer-reviewed] | About 26k pages, 3,099 human-verified queries in 6 languages. Visual beats text at equal model size, and visual+text hybrid is the most robust. VLM evidence-localisation F1 is 0.089 against 0.602 for humans. |
| P8 | Shin, Park, Park, Seo, Lim | 2025 | MultiDocFusion: Hierarchical and Multimodal Chunking Pipeline for Enhanced RAG on Long Industrial Documents | EMNLP 2025 (main), according to the DOI in the alphaXiv metadata | https://doi.org/10.18653/v1/2025.emnlp-main.1062 ; https://www.alphaxiv.org/abs/2604.12352 | Probably peer-reviewed. The DOI was not resolved in this session. | Pipeline of layout detection, OCR, LLM section-hierarchy parsing (DSHP-LLM) and DFS hierarchical chunks. Reports +8–15% retrieval precision and +2–3% ANLS on industrial documents. |
| P9 | Ludwig, Schmidt, Kühn | 2025 | An ontology-based retrieval augmented generation procedure for a voice-controlled maintenance assistant | Computers in Industry 169, 104289 | https://doi.org/10.1016/j.compind.2025.104289 | Peer-reviewed | Fusing exact and vector matching (Majority merge) gives F1 0.611 / F2 0.704, against 0.45 / 0.511 for the best single method. Vector-only matching had precision of about 0.006. |
| P10 | Heredia Álvaro, Barreda | 2025 | An advanced retrieval-augmented generation system for manufacturing quality control | Advanced Engineering Informatics 64, 103007 | https://doi.org/10.1016/j.aei.2024.103007 | Peer-reviewed | A RAG system for manufacturing quality control. The abstract and results could not be retrieved (open access at https://hdl.handle.net/10234/713500). |
| P11 | Ha, Islam, Nanda, Lercel | 2026 | Reducing Technician Search Burden: A Multimodal RAG for Cessna 172 Maintenance Manual | arXiv | https://www.alphaxiv.org/abs/2608.18465 | [arXiv, not peer-reviewed] | Page-image multimodal retriever plus VLM over an aircraft maintenance manual. Recall@5 93.37%, answer semantic similarity 87.20%, $0.0091/query, but 11.93 s retrieval latency. |
| P12 | Seefried, Eldegaway, Das, Blanchard, Ghosal (ORNL) | 2026 | BLUEPRINT: Rebuilding a Legacy: Multimodal Retrieval for Complex Engineering Drawings and Documents | arXiv | https://www.alphaxiv.org/abs/2602.13345 | [arXiv, not peer-reviewed] | Pipeline of a CLIP router, YOLOv8 title-block/parts-list detection, VLM-OCR on crops, and BM25+dense hybrid with region rerank over about 770k legacy files. nDCG@3 0.626 against 0.527 for the best VLM baseline. |
| P13 | Akarsu, Karaman, Mierbach | 2026 | From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents | arXiv | https://www.alphaxiv.org/abs/2604.01733 | [arXiv, not peer-reviewed] | R@5: BM25 0.644 beats dense (text-embedding-3-large) 0.587. Hybrid RRF 0.695. Hybrid + Cohere rerank 0.816. |
| P14 | (Fusion Tax authors; names not retrieved) | 2026 | The Fusion Tax: A Diagnostic Analysis of When Hybrid Retrieval Hurts | arXiv. Metadata lists DOI 10.1109/ACCESS.2026.3743502 (IEEE Access). | https://www.alphaxiv.org/abs/2610.30612 | Possibly peer-reviewed (IEEE Access DOI not resolved). Treat as arXiv. | On 7 BEIR corpora, hybrid beats dense in aggregate but ranks relevant docs below dense-only on 8–21% of queries. RRF only helps when sparse and dense are balanced. |
| P15 | Sun, Dexian, Huang, Zhang, Jia, Cheng, Zhang (Qihoo 360) | 2026 | When Good OCR Is Not Enough: Benchmarking OCR Robustness for Retrieval-Augmented Generation (InduOCRBench) | arXiv | https://www.alphaxiv.org/abs/2605.00911 | [arXiv, not peer-reviewed] | 11 hard industrial document types. Low WER/CER does not predict good RAG retrieval, because structural and semantic OCR errors still cause failures. |
| P16 | Multiple (found via alphaXiv, abstract only) | 2026 | Beyond Maintenance Manual Multimodal RAG: Suggesting What Tool (Purdue/Clemson) | arXiv | https://www.alphaxiv.org/abs/2609.05116 | [arXiv, not peer-reviewed] | Extends maintenance-manual MRAG to recommending tools. No numbers were retrieved. |
| P17 | Multiple (abstract only) | 2026 | FactoryLLM: A Safe and Open-Source AI Playground for Evaluating LLMs in Smart Factories | arXiv | https://www.alphaxiv.org/abs/2606.14119 | [arXiv, not peer-reviewed] | Fault-diagnosis evaluation where the evidence is spread across manuals of interconnected machines. No numbers were retrieved. |
| P18 | Multiple (abstract only) | 2026 | M3DocDep: Multi-modal, Multi-page, Multi-document Dependency Chunking with LVLMs | arXiv | https://www.alphaxiv.org/abs/2605.18774 | [arXiv, not peer-reviewed] | Chunks long industrial documents by following true structure and cross-page dependencies. No numbers were retrieved. |
| P19 | Multiple (abstract only) | 2026 | GEMS-RAG: Graph-grounded Engineering Multimodal Standards RAG (Texas A&M) | arXiv | https://www.alphaxiv.org/abs/2610.33277 | [arXiv, not peer-reviewed] | Builds a graph over engineering standards' figures, tables and cross-references. No numbers were retrieved. |
| P20 | Multiple (abstract only) | 2026 | MM-BizRAG: Rethinking Multimodal RAG for General Purpose Enterprise Q&A | arXiv | https://www.alphaxiv.org/abs/2606.04231 | [arXiv, not peer-reviewed] | Questions the trend toward minimal parsing with page-image-only MM-RAG for enterprise documents. No numbers were retrieved. |
| P21 | Multiple (abstract only) | 2026 | Evaluating Modern RAG: Textual, Multimodal, Dense, and Late Interaction Pipelines | arXiv | https://www.alphaxiv.org/abs/2608.23176 | [arXiv, not peer-reviewed] | Compares textual, multimodal, dense and late-interaction RAG pipelines head to head. No numbers were retrieved. |
| P22 | Multiple (abstract only) | 2026 | MIDR: Enrichment-Augmented Indexing for Multimodal Document Retrieval (Bloomberg) | arXiv | https://www.alphaxiv.org/abs/2609.01316 | [arXiv, not peer-reviewed] | Argues that OCR linearises, corrupts or drops table, chart and layout content. Enriches the index beyond ColPali-style embeddings. |
| P23 | Multiple (abstract only) | 2026 | Industrial-Instruction: Building Instruction-Tuning and Benchmark Datasets from Industrial Technical Reports | arXiv | https://www.alphaxiv.org/abs/2608.22817 | [arXiv, not peer-reviewed] | A pipeline for turning industrial technical reports (maintenance, troubleshooting, specifications, tables) into QA benchmarks. |
| P24 | Multiple (abstract only) | 2026 | RAG-Based Auto-Configuration for Industrial Fieldbus Devices | arXiv | https://www.alphaxiv.org/abs/2608.08618 | [arXiv, not peer-reviewed] | Extracts parameters from heterogeneous PDF device manuals. |
| P25 | Multiple (abstract only) | 2026 | BM25 Wins at Scale: A Scaling Study of RAG Paradigms | arXiv | https://www.alphaxiv.org/abs/2607.26497 | [arXiv, not peer-reviewed] | Title and abstract claim BM25 holds up against dense, graph and agentic RAG as corpus size grows. No numbers were retrieved. |

---

## Which methods best retrieve answers from documents whose key content is in diagrams and tables, and what gains over text-only RAG are reported?

### Takeaway
On every major visually rich benchmark found, page-image retrievers (ColPali-style late interaction, or single-vector DSE/VisRAG) beat OCR- or parser-based text retrieval by large margins. Reported gains are about +14 to +16 nDCG over OCR/caption text pipelines, +17 top-1 over BM25, and 20–40% end-to-end over text RAG. The most robust 2026 results combine visual and text retrievers and add reranking. Pure page-image retrieval is not the final answer: evidence localisation within the page remains poor.

### Cited Findings
- **ColPali (late interaction over page-image patches)**:
  - ViDoRe average nDCG@5 was 81.3 for ColPali, 65.5 for Unstructured+OCR+BM25 and 67.0 for Unstructured+captioning+BGE-M3, a gain of about 14–16 points over the best text pipelines. — [Faysse et al., arXiv 2407.01449 (PDF Table 2)](https://arxiv.org/pdf/2407.01449v6)
  - Offline indexing took 0.39 s/page for ColPali against 7.22 s/page for the parsing pipeline (layout 0.81 s, OCR 2.67 s, captioning 3.71 s). — [Faysse et al., Table 5](https://arxiv.org/pdf/2407.01449v6)
- **VisRAG (ICLR 2025)**: embedding the page image with a VLM and generating directly from it, with no parsing, gives "a 20–40% end-to-end performance gain over traditional text-based RAG pipeline". The method beats text RAG in both retrieval and generation. — [Yu et al., ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3640a1997a4c9571cea9db2c82e1fc35-Abstract-Conference.html)
- **DSE (EMNLP 2024)**: a screenshot-embedding retriever beats BM25 by 17 points top-1 on Wiki-SS (1.3M page screenshots, NQ questions). On mixed-modality slide retrieval it beats OCR-text retrieval by more than 15 nDCG@10. — [Ma et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.373)
- **MMDocIR (long documents, avg 65 pages)**:
  - Visual retrievers beat text retrievers at page level. ColPali R@5 (macro) is about 80.8 against about 72.3 for the best text retriever (ColBERT on VLM-generated text). — [Dong et al., arXiv 2501.08828](https://arxiv.org/html/2501.08828v3)
  - Text retrievers do much better on VLM-written descriptions than on OCR text. ColBERT layout-level R@1 rises from 19.8 (OCR) to 31.3 (VLM-text). — [Dong et al.](https://arxiv.org/html/2501.08828v3)
  - Layout-level (region) retrieval is much harder than page-level: about 63 R@10 against about 82 R@5. Token-level (multi-vector) embeddings help R@1 but cost far more storage. Cascading page then layout retrieval helps. — [Dong et al.](https://arxiv.org/html/2501.08828v3)
- **M3DocRAG**: ColPali retrieval with Qwen2-VL-7B generation beats strong baselines on M3DocVQA (>3k PDFs, >40k pages), MMLongBench-Doc and MP-DocVQA, and reaches SOTA on MP-DocVQA. The fetched page gave no numbers. — [Cho et al., arXiv 2411.04952](https://arxiv.org/abs/2411.04952v1)
- **ViDoRe V3 (2026)** [arXiv, not peer-reviewed]: [Loison et al.](https://www.alphaxiv.org/abs/2601.08620)
  - Visual retrievers beat text retrievers at the same parameter scale.
  - Fusing the top-k of visual and textual retrievers was "the most robust approach".
  - Late interaction and textual reranking substantially improve results.
  - On hard queries, generating from page images instead of extracted text added about 3 points of accuracy (Gemini 3 Pro).
- **OCR fragility (why text-only RAG loses on tables and diagrams)**:
  - OHRBench (ICCV 2025) found that no current OCR solution is adequate for building high-quality RAG knowledge bases. It names two kinds of noise, Semantic and Formatting, and finds that RAG performance falls as noise rises. — [Zhang et al., ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html)
  - InduOCRBench [arXiv, not peer-reviewed] covers 11 hard industrial document types (extreme layouts, watermarks, historical scans, tables and formulas). SOTA OCR degrades on them, and low WER/CER does not guarantee good RAG retrieval. — [Sun et al.](https://www.alphaxiv.org/abs/2605.00911)
- **Counterpoint (parse-heavy is not dead)**:
  - MM-BizRAG [arXiv, not peer-reviewed] explicitly questions the shift to "minimal parsing" page-image MM-RAG for enterprise Q&A. — [MM-BizRAG](https://www.alphaxiv.org/abs/2606.04231)
  - MIDR (Bloomberg) [arXiv, not peer-reviewed] enriches the index beyond ColPali-style embeddings. — [MIDR](https://www.alphaxiv.org/abs/2609.01316)
  - MultiDocFusion (EMNLP 2025 per DOI metadata) shows that layout parsing plus hierarchical chunking improves retrieval precision by 8–15% on industrial documents. — [Shin et al.](https://www.alphaxiv.org/abs/2604.12352)

### Inferences
- For M.A.C.H., the strongest evidence-based default is a **dual index**:
  1. a ColPali-family page-image index to recall diagram-, table- and schematic-heavy pages;
  2. a parsed-text index (layout-aware chunks plus VLM captions of figures and tables) with BM25 + dense retrieval;
  3. fusion, then a reranker, with page images (not only OCR text) passed to the generator.
  This matches the ViDoRe V3 hybrid finding and the MMDocIR "VLM-text beats OCR-text" result.
- Evaluating M.A.C.H. against both BM25 and text-only RAG baselines is well matched to the literature. The expected size of the gain on visually rich pages is about +10–20 retrieval points (nDCG/Recall), based on ColPali, DSE and MMDocIR.
- ColPali's indexing cost (0.39 s/page against 7.22 s/page) favours page-image indexing when a hackathon must ingest a large SOP corpus quickly.

### Gaps
- None of these benchmarks is made of manufacturing SOPs or work instructions. ViDoRe/MMDocIR domains include "Admin & Industry", energy and similar, but the industrial share is small or unspecified, so the gains may not transfer to schematics or exploded-view drawings.
- Exact per-domain numbers for VisRAG retrieval, M3DocRAG and OHRBench (OCR-vs-ground-truth gap) were not in the fetched abstracts. Read the full PDFs to get them.
- ColPali's ICLR 2025 venue and MMDocIR's venue were not confirmed by a fetched page, and the OpenAlex verifier was unavailable.

---

## What peer-reviewed work applies RAG or multimodal RAG to manufacturing, maintenance, aerospace, automotive or industrial SOPs, and what datasets and benchmarks exist?

### Takeaway
Peer-reviewed industrial RAG (Computers in Industry, Advanced Engineering Informatics, EMNLP) is mostly **text- or ontology-based**. Truly multimodal RAG over maintenance manuals and engineering drawings appears so far only in 2026 arXiv preprints (Cessna 172 manual, ORNL BLUEPRINT, GEMS-RAG). No public, peer-reviewed multimodal benchmark of shop-floor SOPs was found. This is the clearest novelty opening for M.A.C.H.

### Cited Findings
- **Peer-reviewed, industrial**:
  - Ludwig, Schmidt and Kühn (Computers in Industry 169, 2025) built a voice-controlled maintenance assistant using RAG over an OWL ontology (filter-system example). Combining exact and vector matching (Majority merge) reached F1 0.611 / F2 0.704, against 0.45 / 0.511 for the best single method (exact match). Vector-only matching at threshold 0.1 had recall 0.995 but precision 0.006. — [Ludwig et al., DOI 10.1016/j.compind.2025.104289](https://www.sciencedirect.com/science/article/pii/S0166361525000545)
  - Heredia Álvaro and Barreda (Advanced Engineering Informatics 64, 2025) built "An advanced retrieval-augmented generation system for manufacturing quality control". The metadata is confirmed, but the abstract and results were not retrievable. — [UJI portal](https://portalcientific.uji.es/documentos/675f91d260134444f311f72e?lang=en); [DOI 10.1016/j.aei.2024.103007](https://dl.acm.org/doi/10.1016/j.aei.2024.103007)
  - MultiDocFusion (EMNLP 2025 per DOI metadata) is a hierarchical, multimodal chunking pipeline for long industrial documents: vision-based region detection, OCR, LLM section-hierarchy reconstruction (DSHP-LLM) and DFS-grouped chunks. It reports +8–15% retrieval precision and +2–3% ANLS. — [Shin et al.](https://www.alphaxiv.org/abs/2604.12352)
  - Other Elsevier industrial-RAG papers surfaced by search but **not opened**, so they are listed only as leads:
    - "An LLM-based knowledge and function-augmented approach for optimal design of remanufacturing process" (AEI 2025, DOI 10.1016/j.aei.2025.103206) — [link](https://dl.acm.org/doi/10.1016/j.aei.2025.103206)
    - "Enhancing retrieval-augmented generation for interoperable industrial knowledge representation and inference toward cognitive digital twins" (Computers in Industry, PII S0166361525000958) — [link](https://sciencedirect.com/science/article/pii/S0166361525000958)
    - "Generative AI for Predictive Maintenance for Manufacturing: A Survey" (Procedia CIRP, PII S2212827125009643) — [link](https://www.sciencedirect.com/science/article/pii/S2212827125009643)
- **Aerospace maintenance, multimodal** [arXiv, not peer-reviewed]:
  - Ha et al. (2026) built a multimodal retriever plus VLM for the Cessna 172 Maintenance Manual. It reached Recall@5 93.37%, answer semantic similarity 87.20%, 11.93 s retrieval for 5 pages, 4.95 s generation and $0.0091/query, with heatmap interpretability. The paper notes that prior aircraft-maintenance RAG was text-only. — [Ha et al.](https://www.alphaxiv.org/abs/2608.18465)
  - A follow-up (Purdue/Clemson) goes beyond manual retrieval to suggest which tool to use. — [P16](https://www.alphaxiv.org/abs/2609.05116)
- **Legacy engineering drawings and scans** [arXiv, not peer-reviewed]: BLUEPRINT (ORNL, 2026) — [Seefried et al.](https://www.alphaxiv.org/abs/2602.13345)
  - Routing: a CLIP router separates drawings from text, with 94.5% accuracy and 97.7% recall.
  - Drawing track: YOLOv8-S detects the drawing number, data block, parts list and revision block, and a VLM-OCR reads only those crops.
  - Retrieval and evaluation: BM25+cosine hybrid with region reranking over about 770k files, evaluated on 5k files with 350/375 expert queries.
  - Results: nDCG@3 0.626 / Success@3 0.715 at 9.46 s/file, against 0.527 / 0.614 at 64.36 s/file for Llama-4 Scout. Preferred 72.88% of the time in head-to-head judgments.
- **Other 2026 industrial preprints** [arXiv, not peer-reviewed]:
  - GEMS-RAG builds a graph over engineering standards' figures, tables and cross-references. — [link](https://www.alphaxiv.org/abs/2610.33277)
  - FactoryLLM evaluates fault diagnosis across manuals of interconnected machines. — [link](https://www.alphaxiv.org/abs/2606.14119)
  - M3DocDep does dependency-aware chunking of industrial documents. — [link](https://www.alphaxiv.org/abs/2605.18774)
  - Industrial-Instruction builds QA benchmarks from industrial technical reports. — [link](https://www.alphaxiv.org/abs/2608.22817)
  - Another paper does RAG-based fieldbus device configuration from PDF manuals. — [link](https://www.alphaxiv.org/abs/2608.08618)
- **Benchmarks and datasets that exist**:

  | Benchmark | Status | Size and focus | Source |
  |---|---|---|---|
  | ViDoRe (V1) | arXiv | Page-retrieval nDCG@5 benchmark used to evaluate ColPali | [ColPali](https://arxiv.org/pdf/2407.01449v6) |
  | ViDoRe V2 | arXiv | Follow-up to V1 | [arXiv 2505.17166](https://arxiv.org/pdf/2505.17166) |
  | ViDoRe V3 | arXiv | 26k pages, 3,099 queries, 6 languages, includes energy, finance and pharma | [link](https://www.alphaxiv.org/abs/2601.08620) |
  | MMDocIR | arXiv | 313 docs, 1,658 queries, page and layout labels, includes Admin & Industry | [link](https://arxiv.org/html/2501.08828v3) |
  | M3DocVQA | arXiv | >3k PDFs, >40k pages | [link](https://arxiv.org/abs/2411.04952v1) |
  | Wiki-SS | EMNLP 2024 | 1.3M page screenshots | [link](https://aclanthology.org/2024.emnlp-main.373) |
  | OHRBench | ICCV 2025 | OCR impact on RAG, 7 domains | [link](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html) |
  | InduOCRBench | arXiv | Industrial OCR robustness, 11 hard document types | [link](https://www.alphaxiv.org/abs/2605.00911) |
  | C172-MM synthetic queries | arXiv | Aircraft maintenance manual | [link](https://www.alphaxiv.org/abs/2608.18465) |
  | BLUEPRINT 5k-file benchmark | arXiv | Legacy engineering drawings | [link](https://www.alphaxiv.org/abs/2602.13345) |

### Inferences
- A small, public, expert-verified **multimodal SOP / work-instruction QA set** built by M.A.C.H. would be a contribution. Queries that hinge on diagrams, tables and torque/spec values, with page- and region-level evidence labels in MMDocIR style, would fill a gap no peer-reviewed benchmark covers.
- The industrial pattern is consistent: practical systems use **hybrid exact+semantic matching** (Ludwig et al.; BLUEPRINT) and **layout-specific detectors** for domain regions such as title blocks and parts lists. These are cheap to build and fit an SOP corpus well.

### Gaps
- No peer-reviewed automotive-specific multimodal RAG paper was located in this session.
- The search tools were limited (OpenAlex was down, and IEEE Xplore and ScienceDirect pages often failed to fetch). IEEE TII, IEEE Access, Journal of Manufacturing Systems and RCIM industrial-RAG papers may exist without having been found here.
- Results for the AEI quality-control RAG paper could not be retrieved.

---

## Does hybrid BM25+dense retrieval still beat pure dense on technical jargon and part numbers?

### Takeaway
Usually yes on lexically dense, identifier-heavy corpora, especially once a reranker is added. In the papers found, BM25 alone can beat a strong commercial dense embedder. Hybrid is not a free win, though. Per query it can hurt when dense is clearly stronger, and RRF is the riskiest fusion choice. No paper found isolates part numbers specifically.

### Cited Findings
- **Text-and-table (financial) documents** [arXiv, not peer-reviewed]: — [Akarsu et al.](https://www.alphaxiv.org/abs/2604.01733)

  | Method | R@5 |
  |---|---|
  | BM25 | 0.644 |
  | Dense (OpenAI text-embedding-3-large) | 0.587 |
  | Hybrid RRF | 0.695 |
  | Hybrid + Cohere Rerank v4.0 | 0.816 (MRR@3 0.605) |

  - Recall@5 correlates r=0.980 with end-to-end numeric answer match.
  - The authors attribute BM25's advantage to the lexical density of the text.
- **Maintenance ontology RAG (peer-reviewed)**: exact matching beat vector matching as a single method, and combining them gave the best F1/F2 (0.611 / 0.704). — [Ludwig et al., Computers in Industry 2025](https://www.sciencedirect.com/science/article/pii/S0166361525000545)
- **Engineering drawings** [arXiv, not peer-reviewed]: BLUEPRINT's winning configuration uses BM25+cosine hybrid scoring with a region reranker. — [Seefried et al.](https://www.alphaxiv.org/abs/2602.13345)
- **Caveat ("Fusion Tax", 2026; arXiv with an IEEE Access DOI in its metadata)**: — [Fusion Tax](https://www.alphaxiv.org/abs/2610.30612)
  - On 7 BEIR corpora, dense-weighted score interpolation beats dense-only in aggregate on every corpus.
  - Even so, it ranks relevant docs below dense-only on 8–21% of queries, and below the better component on 13–48%.
  - RRF carries a higher "tax" wherever dense is clearly stronger. A cross-encoder recovers part of it.
  - Recommendation: base the fusion decision on the measured sparse-dense balance of the target corpus. "Do not fuse" is a valid outcome.
- **Scale** [arXiv, not peer-reviewed]: "BM25 Wins at Scale" claims lexical retrieval stays competitive with dense, graph and agentic RAG as corpus size grows. The fetched material had no numbers. — [P25](https://www.alphaxiv.org/abs/2607.26497)
- ViDoRe V3 shows the same complementarity in the visual setting: fusing visual and text retriever outputs is the most robust option. — [Loison et al.](https://www.alphaxiv.org/abs/2601.08620)

### Inferences
- SOPs are full of part numbers, torque specs, tool IDs and error codes. That makes the corpus lexically dense, the regime where BM25 was competitive or better in the papers above.
- For M.A.C.H. this argues for **BM25 + dense (+ ColPali page index) with score interpolation tuned on a dev set, then a cross-encoder or VLM reranker**, instead of naive RRF.
- M.A.C.H. should also report per-query win/loss against the BM25 baseline, not only means, given the fusion-tax result.
- An exact-match or regex channel for identifiers (part numbers, SOP IDs) is cheap and backed by the evidence (Ludwig et al.).

### Gaps
- No peer-reviewed study was found that measures hybrid against dense specifically on **alphanumeric part numbers or identifiers** in manufacturing text. This is an evaluation M.A.C.H. could run itself.
- The well-known seminal hybrid-retrieval papers (e.g., BEIR 2021, SPLADE) were not looked up in this session and are not cited here.

---

## What are the open gaps (cross-modal grounding, spatial references such as "see fig 3 step 4", scanned legacy documents)?

### Takeaway
The 2025–2026 literature agrees on four unsolved problems:
1. **Fine-grained evidence grounding** inside pages (region and layout level).
2. **Cross-references and structure** across figures, tables and steps.
3. **Robustness to scanned and degraded industrial documents**, where OCR metrics mislead.
4. **Latency and storage costs** of multi-vector visual indexes.

### Cited Findings
- **Grounding**:
  - In ViDoRe V3, human evidence-localisation F1 was 0.602 against 0.089 for Qwen3-VL-30B-A3B, a very large gap. — [Loison et al.](https://www.alphaxiv.org/abs/2601.08620)
  - Layout-level retrieval tops out at about 63 R@10, against about 82 R@5 at page level. — [MMDocIR](https://arxiv.org/html/2501.08828v3)
- **Multi-hop and multi-page**: ViDoRe V3 accuracy drops as more pages are needed and on multi-hop or open-ended queries. — [Loison et al.](https://www.alphaxiv.org/abs/2601.08620)
- **Structure and cross-references**:
  - Flattening structured documents into isolated text and image units weakens local text-image logic. — HAM-RAG [arXiv, not peer-reviewed](https://www.alphaxiv.org/abs/2608.14032)
  - Engineering standards are "densely connected through figures, tables, cross-references", which motivates graph grounding. — GEMS-RAG [arXiv, not peer-reviewed](https://www.alphaxiv.org/abs/2610.33277)
  - Chunk boundaries must follow true multi-page structure. — M3DocDep [arXiv, not peer-reviewed](https://www.alphaxiv.org/abs/2605.18774); MultiDocFusion (EMNLP 2025 per DOI)
- **Scanned and legacy documents**:
  - OCR noise propagates into RAG failure. — [OHRBench, ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html)
  - Industrial historical, watermarked and extreme-layout documents defeat SOTA OCR. — [InduOCRBench](https://www.alphaxiv.org/abs/2605.00911)
  - Legacy drawing archives often lack metadata, and end-to-end VLM baselines are slow (21–64 s/file). — [BLUEPRINT](https://www.alphaxiv.org/abs/2602.13345)
- **Cost**:
  - Multi-vector (token-level) embeddings improve R@1 but need much more storage. — [MMDocIR](https://arxiv.org/html/2501.08828v3)
  - The Cessna-manual MRAG takes 11.93 s to retrieve 5 pages, which is too slow for interactive shop-floor use. — [Ha et al.](https://www.alphaxiv.org/abs/2608.18465)

### Inferences
- **Explicit spatial or cross-modal references** inside a document ("see Fig. 3, step 4", "torque per Table 2", callout numbers on an exploded view) are not treated as a first-class retrieval signal in any paper found. Most systems retrieve whole pages or isolated chunks.

### Gaps
- No paper was found that benchmarks resolution of intra-document references (figure/step/callout linking) for RAG.
- No study was found on photos of physical equipment, or on query-by-photo from the shop floor, against SOP pages.
- No study was found on keeping an SOP index current across document revisions, even though BLUEPRINT detects revision blocks.

---

### Gaps and novelty opportunities for M.A.C.H.

> The template above has no top-level section with this name, so it sits here inside the last question's Gaps. Every opportunity below follows from the cited evidence above. The opportunities are inferences, not results.

1. **A multimodal SOP benchmark with evidence labels.** No peer-reviewed multimodal shop-floor SOP or work-instruction QA benchmark exists. Build a small expert-verified set split into text-only, table-dependent, diagram-dependent and cross-reference queries, with page- and region-level gold evidence (MMDocIR-style). Report results by split against BM25, text-only RAG and M.A.C.H.
2. **Resolving cross-references as a retrieval tool for the agent.** Parse "Fig. N", "Step k", "Table M" and callout numbers into a document graph that links steps, figures and tables (in the spirit of GEMS-RAG and HAM-RAG). Let the agent follow those edges after first-stage retrieval. None of the papers found evaluates this.
3. **Tri-channel retrieval with corpus-calibrated fusion.** Combine an exact identifier channel (part, tool and SOP IDs), BM25 + dense over layout-aware chunks with VLM captions, and a ColPali page-image index. Tune the interpolation weights rather than using naive RRF, then rerank. Report per-query win/loss to show there is no fusion tax against BM25.
4. **Region-level grounding in the answer.** Return the cited page with a highlighted region (bounding box from a layout detector, or a patch-similarity heatmap from late-interaction scores). This targets the 0.089-against-0.602 grounding gap in ViDoRe V3 and builds shop-floor trust.
5. **Robustness to scanned and legacy pages.** Route scanned pages to page-image retrieval and VLM reading instead of trusting OCR text, since OHRBench and InduOCRBench show OCR noise and low-CER-but-wrong-structure failures. Report results separately for scanned and born-digital SOPs.
6. **Shop-floor latency budget.** Published maintenance-manual MRAG takes about 12 s to retrieve. Target sub-second first-stage retrieval with single-vector or token-pooled visual embeddings, plus a lexical prefilter, and report latency and cost per query next to accuracy.
7. **Query-by-photo** (an inference; no supporting paper found). Let the technician photograph a part or panel and retrieve the matching SOP diagram page. This is an unexplored cross-modal query direction in this literature.
