# 05 · Edge vs cloud decision

**Decision: hybrid, edge-first.** Everything on the answer path runs on one on-premise GPU server in the plant.
The cloud is used only for offline, non-critical jobs. The user confirmed: *use a local model, powerful enough
for the whole RAG, inference under 15 seconds.*

## Demo setup (decided 9 Nov 2026)

The dev PC has an **NPU, no NVIDIA GPU**, so vLLM can't run locally. For development and the TECHgium demo we
**rent one cloud GPU VM** and run the exact same Docker Compose stack on it. The VM stands in for the
"plant-side server": the architecture, the paper claim and the measured latency stay edge-first, because the
whole answer path still runs on one self-hosted GPU box with open weights (no cloud LLM API on the answer path).

| Option | GPU | Notes |
|---|---|---|
| GCP Compute Engine `g2-standard-8` | 1 × NVIDIA L4, 24 GB | Fits Qwen2.5-VL-7B AWQ + ColQwen2.5 + reranker; GCP credits may apply; Mumbai region (asia-south1) |
| RunPod / Vast.ai / Lambda | RTX 4090 / A10 / L4, 24 GB | Cheapest per hour, quick start with a Docker template |
| Same providers, 48 GB (L40S / A6000) | 48 GB | Only for the 7B-vs-32B comparison run |

Rules: start the VM only when working or demoing (stop it after, pay per hour); keep model weights on a
persistent disk so restarts are fast; expose only the UI/API through HTTPS or an SSH tunnel, never Postgres,
Qdrant or vLLM ports; use public/synthetic documents only, never real LTTS documents, on a rented GPU.
Latency numbers in the paper are reported as "measured on one 24 GB L4/4090-class GPU".

Local PC (NPU) is used for editing code, running unit tests, the Streamlit UI against the remote API, and
optionally small models via Ollama/OpenVINO for offline tinkering.

## Why

The deciding factors are **privacy and availability**, not cost:

- A shop floor needs an answer when the internet link is down (night shifts included).
- SOPs, drawings and RCA logs are proprietary and possibly export-controlled; they never leave the plant.
- Plant OT networks (IEC 62443 zones) usually forbid inbound internet; only the central IT zone talks to the cloud.
- "Never cite a superseded revision" is easiest to audit when index, filter and model all sit inside the plant's
  change-controlled environment.

## Comparison

| Factor | Edge (on-prem) | Cloud | Hybrid, edge-first |
|---|---|---|---|
| Latency | No WAN round trip; 7B 4-bit VLM ≈ few s/answer (to measure) | Fast big models + WAN latency | Answer path local |
| Availability | Works offline | Fails with the link | Safety answers never depend on the link |
| Privacy / IP | Stays in plant | Leaves site | Only redacted/non-sensitive data, offline only |
| Answer quality | Limited by 7–8B | Best models | Local for answers, cloud for drafting/data generation where allowed |
| Cost | One-time server + power | Per-query, grows with users/shifts and image tokens | Capex + small offline bills |
| Ops | Plant maintains a GPU box | Vendor maintains | Cloud part non-critical |

## Split

| Plant server (online) | Cloud / central DC (offline only) |
|---|---|
| Document index, all 4 retrievers, reranker, Revision Guard, router, 7B VLM generator, verifier, abstention, escalation tickets, audit log | Bulk figure captioning at ingestion, synthetic question generation, router + LoRA training, conformal recalibration when SOPs change, (optionally) WI drafting |

## Hardware tiers

| Tier | Hardware | Use |
|---|---|---|
| TECHgium demo | 1 workstation, **24 GB GPU (RTX 4090 class)** | ColQwen2.5 + reranker + Qwen2.5-VL-7B AWQ together |
| Plant pilot | 1 rack server, 48 GB GPU (L40S class) or 2 × 24 GB | One line/plant with concurrency headroom; allows Qwen2.5-VL-32B AWQ or Qwen3-VL-30B-A3B (MoE, ~3B active) |
| Line-side embedded | Jetson AGX Orin 64 GB class | Possible for one station, slower; not the main server |

Operators use tablets / line-side terminals as thin clients over the plant network.

## Make it a measured result

Run the identical pipeline twice on the MACH-Bench test split — **local 7B vs local 32B** (and optionally a
cloud frontier model as generator). Report accuracy, superseded-citation rate, safety-step recall and p50/p95
latency. The deterministic gates (Revision Guard, access, coherence, atomic index swap) should pass identically
for both, which is direct evidence for edge-first deployment.

## Cost (for the deployment report, not the PPT)

Don't quote prices from memory. Break-even: monthly cloud cost = queries/day × 30 × tokens/query × price/token,
vs server cost over 3 years + power. Image-heavy retrieval means thousands of input tokens per query.

## Where the abstract's GCP pieces now live

| Abstract | Now |
|---|---|
| Cloud Run | Hosted demo only |
| Vertex AI / Gemini | Offline jobs + hosted demo option, behind the same generator interface |
| Pub/Sub | Swap-in for the Postgres escalation queue if deployed on GCP |
| GKE + vLLM KV cache | vLLM is used on-prem (single box, Docker Compose); GKE is the scale-out option in the deployment report |
| Cloud SQL | Postgres (same engine) for registry/audit; vectors in Qdrant because pgvector lacks native multi-vector MaxSim |
