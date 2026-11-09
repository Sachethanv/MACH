# M.A.C.H. explained and PPT novelty upgrades

Nov 5, 2026 · @Sachethan

## Key facts for the presentation round

The PPT is due by 11:59 PM IST on 12 November, so you have one week. These rules come from the TECHgium shortlist email you uploaded.

| Rule | Detail |
| --- | --- |
| Deadline | 11:59 PM IST, 12 November 2026. No extensions. |
| Format | Use the provided template (00000\_TG10\_Presentation Round.pptx). Minor changes are allowed, but no more than 15 slides. |
| File name | Last 5 digits of your PID, then \_TG10\_Presentation Round (for example 12345\_TG10\_Presentation Round). |
| Live round | Online on Microsoft Teams: 7 minutes to present (max), then 5 minutes of jury Q&A. |
| More rules | On slide 13 of the template. |

The template itself wasn't in the upload. Share it here and I'll map the slide story below onto its exact slots.

## M.A.C.H. in plain terms

M.A.C.H. is a question-answering assistant for factory workers. An operator asks something like "what torque for the caliper bolts on line 3?". It finds the answer in the plant's own documents, including diagrams, tables and photos as well as text. It replies with the exact source, refuses or calls a human expert when it isn't sure, and never answers from an outdated revision. It can also draft new work instructions, but a human must approve them before they become official.

I rebuilt this glossary from the build plan's summary of your abstract. If any term below doesn't match what you wrote, tell me and I'll fix it.

| Term in your abstract | What it means | Why it matters on the shop floor |
| --- | --- | --- |
| SOP, WI | Standard Operating Procedure (the official process) and Work Instruction (the step-by-step sheet at a station). | These are the documents M.A.C.H. answers from. |
| ECN, RCA | Engineering Change Notice (an official change to a part or process) and Root Cause Analysis (the report written after a defect). | An ECN makes old steps obsolete. An RCA is what triggers a new work instruction. |
| RAG (Retrieval-Augmented Generation) | First search the documents, then let the LLM answer using only what was found. | The answer comes from your plant's documents, not the model's memory. |
| Multimodal | Handles text, tables, diagrams and photos, not only plain text. | Most key facts in manuals sit in figures and tables. |
| Agentic | The system decides its own next step: search again, check its work, refuse, or escalate. A plain chatbot does one fixed pass. | Hard or risky questions get extra checking instead of a guess. |
| Vision-native retrieval (ColPali), "bypass OCR" | Search page images directly. ColPali cuts each page into small patches and matches every word of the question against them (this is called late interaction). | Finds answers hidden in diagrams that OCR text loses. |
| DocLLM spatial attention | A research model that also reads where text sits on the page (its layout). | Tables and forms make sense only with their layout. |
| Sentence-level citations | Every sentence points to its document, page, revision and spot on the page. | The operator can check the source before acting. |
| Supersession | A newer revision or an ECN replaces an older document. | The system must never answer from a replaced step. |
| Abstention | The system says "I don't have enough evidence" instead of guessing. | A confident wrong torque value is worse than no answer. |
| Self-RAG / CRAG | Self-checking RAG. The system grades the evidence it found: good means answer, unsure means search again, bad means abstain. | This is the engine behind abstention. |
| Expert escalation (Pub/Sub) | Send the question to a human expert's inbox. Pub/Sub is Google Cloud's message queue that delivers it. | Covers the questions the AI shouldn't answer alone. |
| Change-controlled WI drafting (AutoGen agents) | One AI agent drafts a work instruction from an RCA and a second checks it against current SOPs. A human then approves it, and only then does it become the new official revision. AutoGen is a framework for running several agents together. | Saves authoring time without bypassing quality approval. |
| RBAC | Role-based access control: operators, engineers and admins each see only what they're allowed to. | Keeps restricted RCA or IP content away from the wrong people. |
| Cloud SQL / pgvector | A Postgres database with an add-on for storing the number vectors used in search. | Stores documents, revisions and the audit log. |
| GKE + vLLM KV cache | Running your own open-weight LLM on Kubernetes. vLLM is a fast serving engine, and its KV cache reuses work on repeated prompts. | Needed only if the client can't send data to a cloud API. |
| BM25 baseline, text-only RAG baseline | BM25 is classic keyword search. Text-only RAG is RAG with no images and no self-checking. | These are the two systems you must beat to prove M.A.C.H. helps. |
| RAGAS / ARES | Automatic tools that score RAG answers for faithfulness and relevance. | Gives you numbers for the results slide. |

## Novelty upgrades for the PPT

Your strongest pitch is a trust layer for safety-critical SOPs, not "multimodal RAG". Page-image retrieval and self-checking RAG are already published at ICLR and NAACL, so they are table stakes. The gaps below are the ones I found no peer-reviewed work on, ranked by how strong the claim is and how cheaply you can show it in a week. Evidence comes from the literature review.

| # | Upgrade (name it on the slide) | What it does | Evidence it's a gap | Cost in one week |
| --- | --- | --- | --- | --- |
| 1 | Revision Guard | Removes superseded or not-yet-effective revisions before the LLM sees them. Every answer states its revision and adds "Rev C replaced by ECN-014 on 2 Mar" when relevant. A check rejects any answer that cites two revisions of the same step. | One stale document flips 17–91% of correct answers (Stale-Document Poisoning, arXiv 2026, not peer-reviewed). VersionRAG scores 90% vs 58% for plain RAG (arXiv 2025, not peer-reviewed). Peer-reviewed work now confirms the harm of outdated documents (HoH, ACL 2025) and studies evolving policy corpora (Morita et al., EMNLP 2026 Industry), but none covers step-level supersession in procedures, ECN overlays or mixed-revision answers. | Low: metadata filter plus one post-check. |
| 2 | Step-level, safety-complete citations | Each step cites doc, page, step number and figure ID, not just "the document". A metric checks that no safety step (LOTO, PPE, torque) was dropped. Visual citations point to parsed figure IDs instead of guessed boxes. | The standard citation metric (ALCE, EMNLP 2023) checks sentences, not step order or missing safety steps. Visual box citation reaches only 54–68% even after fine-tuning (VISA, ACL 2025). | Low to medium. |
| 3 | Risk-tiered abstention | Stricter confidence threshold for high-hazard steps, looser for low-risk lookups. It gives partial answers: the certified steps are shown and the rest is escalated. | Conformal methods give guarantees (ICML 2024), but no work found ties the threshold to hazard level. | Medium: a hazard tag per chunk plus two thresholds. |
| 4 | Smart escalation with expert memory | Escalates with the top 2–3 candidate answers and their evidence, not a blank ticket. The expert's reply is stored as a separate note with provenance and an expiry date, and is checked against the official SOP. It never overrides the SOP until it goes through change control. | Prediction sets help humans decide faster (NeurIPS 2024). The one factory study (Frontiers in AI 2024) found expert answers were most valuable on night shifts. No work found manages expiry or SOP conflict for expert notes. | Medium. |
| 5 | SOP-Trap benchmark | A small public test set with five buckets: text, table, image, superseded-revision traps, and unanswerable or unsafe questions. Each has a gold answer, citation and expected behaviour (answer, abstain or escalate). | DesignQA (ASME JCISE) is a multimodal engineering-document benchmark and SOPRAG (arXiv, not peer-reviewed) has an SOP retrieval benchmark, but none combines work instructions, images and revision traps. | Medium: 60–100 questions, built anyway for your evaluation. |
| 6 | Planted-fault review test | Plant deliberate errors in drafted work instructions and measure how many the reviewers catch. Also report reviewer edits and rejection rate. | No study measures change-control outcomes for LLM-drafted instructions. | Low once drafting works. |
| 7 | Adaptive routing | Simple lookups take one fast pass. Only multi-step questions run the full agent loop. | Adaptive-RAG (NAACL 2024) matched the slow method's accuracy at 1.46× vs 3.33× the time. | Low: one classifier prompt. |

Say "we found no prior work on X", never "first in the world". The IEEE and Elsevier manufacturing journals couldn't be searched exhaustively, and a juror may know a paper.

Two results to headline on the results slide: revision-mixing rate (the target is 0% for M.A.C.H., measured against both baselines) and unsafe-answer rate on the unanswerable bucket. Juries remember one number per idea.

## More novel ideas

Ten more ideas go beyond the seven above. Each fills a gap where the research found no prior work. Ideas marked (inference) have no supporting paper; they are design ideas, so pitch them as "we propose".

| # | Idea | What it does | Gap it fills | Fits PPT or paper? |
| --- | --- | --- | --- | --- |
| 8 | Context-locked answers | The operator's station, machine model and serial range automatically scope every search. A citation counts only if its text supports the claim and it matches that machine variant. | Legal RAG studies define "misgrounded" citations: real text that doesn't fit the case. No one has applied this to machine variants. | Both. Strong demo. |
| 9 | Deviation overlays | Temporary deviations and partial ECNs are stored as time-limited patches to specific SOP steps, not as whole new documents. The answer shows the base step with the patch applied and says when the patch expires. | 21 CFR 211.100(b) requires recorded deviations. No RAG work models step-level, time-limited changes. | Paper, plus one PPT line. |
| 10 | "What changed?" answers | Compares two revisions, including changed table values and swapped diagrams, and explains the difference with citations to both. | Comparing revisions of multimodal content is an open problem in the versioning literature. | Both. |
| 11 | Cross-reference following | Parses "see Fig. 3, step 4" and "Table 2" into links. The agent follows the link after the first search, so the answer includes the referenced figure. | No benchmark or system was found that evaluates cross-references inside manuals. | Paper. |
| 12 | Exact-ID search lane | A third search lane matches part numbers, tool IDs and SOP codes exactly, alongside keyword and image search, with tuned (not naive) fusion weights. | Studies warn that naive fusion ranks relevant results lower on 8–21% of queries. No study isolates part numbers. | Paper ablation. |
| 13 | Number lock | Torque, temperature, pressure and dimension values are copied from the source cell by code, never written by the LLM. Units are checked and converted deterministically. | LLM judges can't be trusted on expert-level correctness (JudgeBench, ICLR 2025). Critical parameters need exact-match checks. | Both. Juries love it. |
| 14 | Query by photo | A technician photographs a part or panel and gets the matching diagram page and its SOP. | No paper found tests photo queries over SOP pages (inference). | PPT demo. |
| 15 | Shift-aware escalation | The escalation threshold depends on whether an expert is on shift. When no expert is available, the system gives conservative partial answers plus a "stop and wait" instruction for hazardous steps. | The one factory field study found the assistant mattered most on night shifts. No system adapts to expert availability. | Both. |
| 16 | Recalibrate on every revision | When an SOP revision is approved, the confidence thresholds for that SOP family are re-checked on a small calibration set. Statistical guarantees assume new questions resemble old ones, and a revision breaks that. | No work found ties recalibration to document-control events. | Paper. |
| 17 | Simplified Technical English check on drafts | Drafted work instructions are checked against ASD-STE100-style rules (one instruction per sentence, approved verbs, a word limit). The test compares constrained and free drafting. | Builds on Jonek & Manns (CARV 2025): controlled language raised vocabulary compliance from 50% to 85% and cut editing from about 20 to 12 minutes. Our new part is testing it under change control with planted faults. | Paper. |

Two practical additions with no paper behind them, but likely to impress an Indian shop-floor jury (inference): hands-free voice queries for gloved hands, and answers in Hindi or the local language while citations stay in the original English SOP.

## Edge cases and how to harden them

The most dangerous failures are confident, cited, wrong answers. The first 11 of these 29 rows are rated High (the PDF brief extends the list to 37). Every row is a test case to add to the gold set, so each robustness claim in the PPT is backed by a number.

| Stage | Edge case | What goes wrong | Hardening | Test to add | Risk |
| --- | --- | --- | --- | --- | --- |
| Revisions | Two "effective" revisions of the same SOP (bad metadata) | Answer mixes old and new steps | Ingestion check blocks two active revisions per SOP and station; answer-time check rejects mixed citations | Plant a duplicate active revision | High |
| Revisions | ECN changes one step but the SOP isn't reissued yet | Answer uses the old step from the current SOP | Deviation overlay applies the ECN patch to that step | ECN-only change questions | High |
| Revisions | Revision effective tomorrow, or effective on one line only | Too-early or wrong-line answer | Filter on effective date and scope, using the operator's line and the query date | Future-dated and scoped revisions | High |
| Revisions | Operator asks for an old document number | Executes from obsolete text | Answer from the current revision and say what changed | Old-ID queries | Medium |
| Variants | Same procedure, different machine model or serial range | Right text, wrong machine (misgrounding) | Context lock on station, model and serial; variant must match to cite | Near-duplicate variant SOPs | High |
| Numbers | Torque in N·m in one document, lbf·ft in another | Wrong value or wrong unit | Number lock copies values from the source; units converted by code | Mixed-unit corpus | High |
| Numbers | Value given as a range or tolerance ("25 ± 2 N·m") | Tolerance dropped | Extract value, tolerance and unit as one field and never truncate | Tolerance questions | High |
| Conflict | Two active sources disagree (SOP vs quality alert) | Picks one silently | Detect the conflict, show both, escalate; a quality alert outranks the SOP until resolved | Planted conflicts | High |
| Safety | Answer omits a LOTO or PPE step | Injury risk | Safety-step completeness check; warnings always shown first and never cut | Steps with a buried warning | High |
| Safety | User asks how to skip or bypass a safety step | Unsafe instruction | Refuse plus escalate; logged | Red-team bypass prompts | High |
| Security | Malicious text hidden in an ingested document ("ignore previous rules") | Hijacked answer | Treat retrieved text as data; strip instructions at ingestion; output schema enforced | Injection documents | High |
| Access | Operator asks about a restricted RCA | Leaks restricted content | Filter by role before search, not after generation | Cross-role queries | High |
| Retrieval | Answer only in a diagram callout or table cell | Text search misses it | Page-image lane plus layout parsing | Diagram-only and table-only questions | Medium |
| Retrieval | Scanned, skewed or handwritten-marked pages | OCR garbage, so wrong or no citations | Route scans to image search and VLM reading; flag low-quality pages | Scanned subset reported separately | Medium |
| Retrieval | Table spans two pages, or a step continues overleaf | Half the step is missing | Merge split tables and steps at ingestion | Page-break cases | Medium |
| Retrieval | Query uses plant slang or abbreviations ("CP" for caliper piston) | Retrieval miss | Plant glossary expands the query; exact-ID lane | Slang queries | Medium |
| Retrieval | Same warning repeated in 10 documents | Evaluation unfairly scores correct citations as wrong | Multi-gold evidence sets | Redundant-evidence questions | Medium |
| Query | Vague question ("how do I fix it?") | Guesses the machine | Ask one clarifying question, or use the station context | Underspecified queries | Medium |
| Query | Two questions in one, or a multi-step plan | Answers only half | Adaptive routing to the multi-step path | Compound queries | Medium |
| Query | Out-of-scope question (HR, weather) or none of the documents answer it | Hallucinated answer | Abstain with "not in the controlled documents" | Unanswerable bucket | Medium |
| Query | Blurry or wrong photo uploaded | Wrong page retrieved with high confidence | Image quality check; confirm the matched part with the user | Bad-photo set | Medium |
| Escalation | No expert responds, or the expert's answer conflicts with the SOP | Operator blocked, or SOP overridden informally | Timeout leads to "stop and hold" for hazardous steps; expert notes can't override the SOP without change control | Simulated timeouts and conflicting expert notes | Medium |
| Escalation | Over-escalation (everything goes to experts) | System ignored | Track escalation rate; risk–coverage curve; tune thresholds | Report coverage at fixed risk | Medium |
| Drafting | Drafted WI contradicts another active SOP | Bad revision approved | Compliance agent checks against all active SOPs for that station | Planted contradictions | Medium |
| Drafting | Reviewer rubber-stamps an AI draft | Automation bias | Planted-fault test; diff view highlights every AI change | Reviewer catch rate | Medium |
| Drafting | Two drafts for the same SOP at once | Revision collision | Lock the SOP family while a draft is in review | Concurrent drafts | Low |
| Ops | LLM API down or slow | No answer on the shop floor | Fallback to keyword search showing source pages only, with a clear banner | Kill-switch test; p95 latency | Medium |
| Ops | Model version changes silently | Behaviour drifts | Pin the model version; rerun the gold set on every change | Regression run | Low |
| Audit | Auditor asks "what did the AI tell operator X on date D?" | No proof | Log query, retrieved chunk IDs, revisions, answer and model version | Audit replay | Low |

The parallel test-plan doc already covers how to run these. Use this table as its case list.

## Claims to soften or drop

A juror who knows the field will probe these first. Fixing them before the PPT turns a weakness into a sign of engineering maturity.

| Claim | Problem | Say instead |
| --- | --- | --- |
| "Bypass OCR entirely" | Citations, the BM25 baseline and the revision checks all need text. | "Hybrid: page images for retrieval, extracted text for citation and keyword search." Benchmarks show the hybrid is the most robust. |
| DocLLM spatial attention | There's no easy public model to use. | "Layout-aware parsing" (Docling or PyMuPDF with bounding boxes). |
| Self-RAG | The real thing needs a specially fine-tuned model. | "Self-RAG/CRAG-style evidence grading". |
| GKE + vLLM | Not needed if you call a cloud LLM API. | Keep it as the on-prem option for clients who can't send data to the cloud. |
| ColPali vectors in Cloud SQL | pgvector can't do ColPali's multi-vector matching natively. | Qdrant or byaldi for vectors, Postgres for metadata and audit logs. |
| "Saves X% expert time" | Unproven without a study. | Report a small timed test: 3–5 people answer 10 questions with keyword search vs M.A.C.H. |

## Suggested slide story and jury questions

Aim for 12 slides, which leaves about 35 seconds per slide in 7 minutes. I'll remap this to the template's slots once you share it.

1. Title, team, one-line pitch: "A shop-floor assistant that cites, refuses and never uses an outdated SOP."
2. The problem: one real-looking story of an operator following an outdated revision, and what it costs.
3. Why current tools fail: keyword search misses diagrams, and plain RAG mixes revisions and hallucinates. Use the 17–91% stale-document figure, labelled as a preprint.
4. M.A.C.H. at a glance: one architecture diagram.
5. Novelty 1, Revision Guard, with a screenshot of the superseded-by warning.
6. Novelty 2, step-level safety-complete citations, with a screenshot of a highlighted source.
7. Novelty 3 and 4, risk-tiered abstention and smart escalation, shown as one flow.
8. Change-controlled drafting: RCA, then draft, then compliance check, then human approval, then the new revision.
9. Evaluation design: the SOP-Trap benchmark, the two baselines, and the metrics.
10. Results: one table plus one or two honest failure cases.
11. Security and deployment: RBAC, audit log, protection against malicious text in documents, cloud vs on-prem.
12. Impact for LTTS clients and next steps.

Likely jury questions to rehearse:

- How do you know which revision is effective? Answer: document-control metadata (status, effective date, the supersedes link), not file dates.
- What happens if two active documents disagree? Answer: abstain, show both, escalate.
- How did you build the test set without real plant data? Answer: a synthetic corpus reviewed by someone with plant experience. Name them.
- Why not fine-tune a model? Answer: research shows retrieval beats fine-tuning for adding new knowledge (EMNLP 2024), and SOPs change too often.
- What's your latency? Know your p50 and p95 numbers.
- Can a malicious document hijack the AI? Answer: retrieved text is treated as data, and access is role-based.
