# 03 · Agentic design

The abstract says "AutoGen-inspired multi-agent architecture". The plan keeps the multi-agent idea but builds
it as an **auditable state graph** (LangGraph, or a plain Python state machine) rather than free-chatting
agents. Reason: every decision must be logged and replayable, and the safety-critical checks (Revision Guard,
access, number lock, coherence) must be deterministic code, not agent judgement.

Rule of thumb: **LLM nodes propose, code nodes decide.**

## Agents / nodes

| Node | Type | Input → Output | Notes |
|---|---|---|---|
| **ContextLock** | code | session → `Context(time, site, line, station, model, serial, role, shift)` | Role comes from the session only ("I'm the QE" in a prompt changes nothing) |
| **Router** | small classifier | query → `direct` / `single` / `multihop` / `escalate` | DeBERTa-v3-small or LR on embeddings; trained on 1.5–3k auto-labelled queries. Adaptive-RAG (NAACL 2024) setup. Also refuses bypass/unsafe intents |
| **Retriever** | code | query + `E(c)` → ranked elements | 4 lanes, all pre-filtered by Revision Guard; RRF + rerank + cross-ref hop |
| **RevisionGuard** | code | context → effective set, supersession statements; post-hoc coherence check | Never an LLM |
| **Grader** (CRAG-style) | LLM prompt | query + evidence → relevant / ambiguous / irrelevant + sufficiency score | Ambiguous → re-retrieve (≤ 2 rounds total for latency) |
| **ConflictDetector** | code (+LLM extraction of parameter/value pairs) | evidence → conflicts | Same parameter, same scope, different value → escalate |
| **Generator** | VLM | evidence (≤ 4 page images + text) → JSON `{steps:[{text, element_ids, revision, support}], confidence}` | Cites only from a closed list of element IDs |
| **NumberLock** | code | answer + cited elements → answer with values replaced from source | Units/tolerances copied as one field |
| **Verifier** | code + NLI | answer → per-statement verdicts | Validity ∈ E(c), coherence, entailment, variant match, safety-step completeness |
| **RiskGate** | code | verdicts + grader + dispersion → answer / partial / abstain | Per-tier conformal thresholds; shift-aware cost |
| **Escalation** | code + LLM summary | query, evidence, top-3 candidate answers → expert ticket | Timeout on tier-1 → "stop and hold" + supervisor alert |
| **ExpertMemory** | code | expert reply → expert note (author, date, expiry, conflict-checked) | Advisory, ranked below controlled docs; repeated notes trigger a draft; replies reused as calibration labels |
| **Drafter** | LLM | RCA/ECN + current SOP → WI draft in schema (step, tool, torque, PPE, caution/warning, cited source) | Uses STE rules (Jonek & Manns, CARV 2025) |
| **Compliance** | code + LLM | draft → issues | Checks all effective SOPs for that station, required fields, STE rules, safety-step survival |
| **ChangeControl** | code | draft → state machine | Draft → In review → Approved/Rejected → Published; SOP family locked during review; signed approval; diff view |
| **Auditor** | code | everything → append-only log | Enables replay |

## Answer graph (online)

```
ContextLock → Router
  ├─ escalate ─────────────────────────────────────────────▶ Escalation
  ├─ direct   → Retriever(ID lane) → NumberLock → Verifier → RiskGate
  ├─ single   → Retriever → Grader ─┬─ relevant  → ConflictDetector → Generator → NumberLock → Verifier → RiskGate
  │                                  ├─ ambiguous → Retriever (round 2) → Grader
  │                                  └─ irrelevant → Abstain
  └─ multihop → [Retriever → Grader → sub-answer] × ≤2 (stop when no new element IDs) → Generator → …
RiskGate ─┬─ pass    → Answer
          ├─ partial → Answer(certified steps) + Escalation(rest)
          └─ fail    → Abstain + Escalation
Verifier failure (coherence/validity) → regenerate once without offending elements → else Escalation
All nodes → Auditor
```

## Drafting graph (offline / on demand)

```
RCA or ECN → Drafter → Compliance ─ issues → Drafter (≤ N loops)
                        └─ clean → ChangeControl(In review) → human reviewer (diff view; planted-fault audits)
                                    ├─ reject → Drafter / closed
                                    └─ approve (signed) → Published → new effective revision → Ingestion
```

Becker et al. (Procedia CIRP 2026) four criteria — **completeness, understandability, free of error,
sequence** — are the drafting rubric. Our measured extras: planted-fault catch rate and safety-step survival.

## Shared state (sketch)

```python
class MachState(TypedDict):
    query: str
    image: bytes | None
    language: str
    context: Context              # from session, immutable
    route: Literal["direct", "single", "multihop", "escalate"]
    effective_snapshot: str       # corpus snapshot hash
    evidence: list[Element]       # all within E(context)
    grade: Literal["relevant", "ambiguous", "irrelevant"]
    rounds: int                   # ≤ 2
    conflicts: list[Conflict]
    draft_answer: AnswerJSON | None
    verdicts: list[StatementVerdict]
    decision: Literal["answer", "partial", "abstain", "escalate"]
    trace: list[AuditEvent]
```

## Why not free-form AutoGen chat

- Non-deterministic agent conversations are hard to audit (ISO 9001 §7.5, EU AI Act Art. 14 human oversight).
- Latency: each agent turn costs seconds; the 15 s budget allows ~1 generator call + checks.
- We keep the vocabulary ("Drafter agent", "Compliance agent") for the pitch; the implementation is a graph.
