# 09 · Novelty, safe claims and jury Q&A

Sources: [`research/brief/MACH project brief.md`](../research/brief/MACH%20project%20brief.md) §4 and §9,
[`research/planning_docs/03_explainer_and_novelty.md`](../research/planning_docs/03_explainer_and_novelty.md),
literature review addendum.

**Positioning:** a *trust layer for safety-critical SOPs*. Page-image retrieval (VisRAG/ColPali, ICLR 2025)
and self-checking RAG (Self-RAG ICLR 2024, CRAG, Adaptive-RAG NAACL 2024) are table stakes.

**Wording rule:** "we found no prior work on X", never "world first" — IEEE/Elsevier full texts were checked via
the OpenAlex index, not read in full.

## 17 novelty ideas (ranks 1–7 = PPT headline set)

| # | Idea | Gap it fills | Effort |
|---|---|---|---|
| 1 | **Revision Guard** — hard effectivity filter, "superseded by" statements, one-revision-per-answer check | Stale docs flip 17–91% of answers (arXiv); HoH (ACL 2025), Morita et al. (EMNLP 2026 Industry) treat whole documents — none on step-level supersession, ECN overlays or mixed-revision answers | Low |
| 2 | **Step-level, safety-complete citations** with figure/step IDs | ALCE scores sentences, not step order or missing safety steps; visual box citation only 54–68% even fine-tuned (VISA, ACL 2025) | Low–Med |
| 3 | **Hazard-tiered abstention** with partial answers | Conformal guarantees exist (ICML 2024); none calibrated per hazard class or returning certified step subsets | Med |
| 4 | **Smart escalation + expert memory** with expiry and conflict checks | Prediction sets help humans (NeurIPS 2024); the one factory loop (Frontiers in AI 2024) has no expiry/SOP-conflict control | Med |
| 5 | **MACH-Bench** — multimodal WIs + revision traps + unsafe asks | DesignQA (ASME JCISE), SOPRAG (arXiv), VersionQA (software only) — none combines WIs, images and revision traps | Med |
| 6 | **Planted-fault reviewer test** for AI drafts | Becker et al. (Procedia CIRP 2026) evaluate GPT-4o drafts with human feedback but no change control, citations, safety checks or planted faults; EU AI Act Art. 14 automation bias | Low |
| 7 | **Adaptive routing** by complexity | Adaptive-RAG: same F1 as IRCoT at 1.46× vs 3.33× time | Low |
| 8 | **Context lock** — answers scoped to machine variant | "Misgrounded" citations (JELS 2025) never applied to machine variants | Low |
| 9 | **Deviation overlays** on individual steps with expiry | 21 CFR 211.100(b); no RAG work models step-level time-limited patches | Med |
| 10 | **"What changed?"** across revisions incl. tables/figures | Multimodal diffing listed as open | Med |
| 11 | **Cross-reference following** ("see Fig. 3, step 4") | No benchmark/system evaluates it | Med |
| 12 | **Exact-ID search lane** with tuned fusion | Naive fusion hurts 8–21% of queries (arXiv) | Low |
| 13 | **Number lock** for critical values and units | LLM judges near random on expert correctness (JudgeBench, ICLR 2025) | Low |
| 14 | **Query by photo** of a part/panel | No paper found (inference) | Med |
| 15 | **Shift-aware escalation** | Assistant most valuable on night shifts (Frontiers in AI 2024) | Low |
| 16 | **Recalibrate on every revision** | Conformal guarantees break under shift; none tied to document control | Low |
| 17 | **STE check** on drafts | Builds on Jonek & Manns (CARV 2025: compliance 50→85%, edit time ~20→12 min); ours = under change control with planted faults | Low |

Extra slide lines (inference, no paper): hands-free voice for gloved hands; answers in Hindi/local language while
citations stay in the English SOP.

## Narrowed claims (after the IEEE/ACM/ScienceDirect pass)

- **Supersession:** HoH and Morita et al. already study outdated docs in RAG → ours is *step-level supersession
  in procedures, ECN overlays and blocking mixed-revision answers*.
- **Benchmark:** "the first benchmark **we know of** for work instructions that combines multimodal evidence with
  superseded-revision traps."
- **Drafting:** don't claim "evaluating LLM-drafted WIs" (Becker et al. did) → claim *drafting under change
  control*, measured by planted-fault catch rate and safety-step survival; reuse Becker's 4 criteria as the rubric.
- Zennir et al. (GAST 2026, IEEE) — multimodal RAG for electrical-concept education — minor related work only.

## Claims to soften from the abstract

| Abstract | Say instead |
|---|---|
| "Bypass OCR" entirely | Hybrid: page images for retrieval, extracted text for citation, BM25 and checks |
| DocLLM spatial attention | Layout-aware parsing (Docling/PyMuPDF with bboxes) |
| Self-RAG | Self-RAG/CRAG-style evidence grading (prompted, no fine-tuned reflection tokens) |
| ColPali embeddings in Cloud SQL | Qdrant for multi-vector; Postgres for metadata/audit |
| GKE + vLLM | vLLM on one on-prem box; GKE = scale-out option in the deployment report |
| ARES | RAGAS + custom metrics; ARES-style statistical correction |
| "Saves X% expert time" | Timed study: 3–5 people × 10 questions, keyword search vs M.A.C.H. |

## Jury Q&A (short answers; full versions in the brief §9)

1. *Just RAG with extra steps?* — RAG is the base; the contribution is the trust layer, each part ablated.
2. *Which revision is effective?* — Document-control metadata, hard filter before the LLM, verifier rejects mixes.
3. *Two current docs disagree?* — Never picks silently; shows both, escalates; quality alert outranks SOP.
4. *Hallucinated numbers?* — Number lock; OCR vs image mismatch → abstain.
5. *Refuses too often?* — Risk–coverage curve + escalation rate; only tier-1 needs very high confidence; partial answers.
6. *Where do thresholds come from?* — Conformal risk control per tier; re-checked on revision.
7. *Why not fine-tune?* — Retrieval beats fine-tuning for new knowledge (Ovadia et al., EMNLP 2024); SOPs change too often.
8. *No real plant data?* — FAA AD real chains + 8 public peer-reviewed benchmarks; drop-in for LTTS docs.
9. *Malicious document?* — Stripped at ingestion, data-not-instructions, schema-enforced, role-filtered; injection docs in tests.
10. *Cloud down / data can't leave?* — Reference config is on-prem; keyword fallback with banner.
11. *Who's accountable for AI WIs?* — The signed human approver; diffs + planted-fault audits.
12. *How fast?* — Gate: 95% < 15 s on one plant GPU; report measured p50/p95.
13. *Tacit knowledge?* — Expert notes with expiry + conflict check; repeated notes trigger a change-control draft.
14. *vs commercial copilots?* — They don't understand effectivity, variants, hazard tiers or change control.
15. *Value for LTTS?* — Fewer quality escapes, night-shift answers, audit-ready traceability, faster WI authoring.
16. *Hasn't HoH/SOPRAG solved this?* — HoH is whole-document, no effectivity/ECN/step level; SOPRAG has no revisions, images, citations or abstention.

## Honest limitations

Synthetic shop-floor docs + aviation revision chains (relative gains are the claim); conformal guarantees only
under similar distributions; several newest results are arXiv preprints (labelled); paywalled full texts not read.
