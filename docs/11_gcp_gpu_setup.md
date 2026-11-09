# 11 · GCP GPU VM setup (dev + demo)

Decision D16: the GPU box is a **GCP Compute Engine `g2-standard-8` with 1 × NVIDIA L4 (24 GB)**, paid from GCP
credits. It runs the same `docker-compose.yml` as the plant server would. Commands below are a starting point:
image family names and regional GPU availability change, so check each `list` command's output first.

## 0. Before you start (one-time)

1. **Billing:** GPUs are not available on a free-trial account. Upgrade to a paid billing account. Remaining
   credits still apply after the upgrade.
2. **Quota:** new projects usually have 0 GPU quota. In *IAM & Admin → Quotas*, request
   `NVIDIA L4 GPUs` = 1 in your region, and `GPUs (all regions)` = 1. Approval can take minutes to a day, so
   request it now.
3. **Region:** prefer Mumbai `asia-south1`. Check where L4 is offered:
   ```bash
   gcloud compute accelerator-types list --filter="name=nvidia-l4" --format="value(zone)"
   ```
   If Mumbai has no L4 or no capacity, use `asia-southeast1` (Singapore).
4. Install the Google Cloud CLI on the PC, then run `gcloud init` and `gcloud auth login`.
5. **Budget alert:** set one at e.g. 50% and 90% of your credits (*Billing → Budgets & alerts*).

## 1. Create the VM

Use a Deep Learning VM image, which comes with the NVIDIA driver and Docker:

```bash
gcloud compute images list --project=deeplearning-platform-release --filter="family~cu12 AND family~ubuntu" --format="value(family)" | sort -u
```

```bash
gcloud compute instances create mach-gpu \
  --zone=asia-south1-a \
  --machine-type=g2-standard-8 \
  --accelerator=type=nvidia-l4,count=1 \
  --maintenance-policy=TERMINATE \
  --image-project=deeplearning-platform-release \
  --image-family=<family from the list above> \
  --boot-disk-size=200GB --boot-disk-type=pd-balanced \
  --metadata=install-nvidia-driver=True \
  --tags=mach-gpu
```

- The 200 GB disk holds model weights (~25 GB), indexes and Docker images, and it survives stop/start.
- *Optional:* add `--provisioning-model=SPOT` for a much lower price. The VM can be pre-empted, so don't use
  Spot on demo day.

## 2. First login and checks

```bash
gcloud compute ssh mach-gpu --zone=asia-south1-a
nvidia-smi                         # should show the L4
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

Then clone the repo from GitHub, copy `.env.example` to `.env`, and add your `HF_TOKEN`:

```bash
git clone https://github.com/<you>/mach-framework.git && cd mach-framework
docker compose --profile gpu up -d     # postgres, qdrant, vllm
curl localhost:8000/v1/models          # vLLM is up once the model has downloaded
```

## 3. Work from the PC (Antigravity + Claude Code)

- **Remote-SSH:** open the repo on the VM directly from Antigravity, or
- **Port forward** and keep the code local:
  ```bash
  gcloud compute ssh mach-gpu --zone=asia-south1-a -- -L 8000:localhost:8000 -L 8501:localhost:8501 -L 8080:localhost:8080
  ```
  Then `http://localhost:8501` on the PC is the Streamlit UI and `localhost:8000` is vLLM.
- **Never** open Postgres (5432), Qdrant (6333) or vLLM (8000) in the firewall. Use SSH tunnels only.
  For a shared demo link, expose only the UI, either through an HTTPS reverse proxy with a password or
  with Cloud Run in front of the API.

## 4. Save credits

```bash
gcloud compute instances stop mach-gpu --zone=asia-south1-a    # after every session
gcloud compute instances start mach-gpu --zone=asia-south1-a
```

A stopped VM only bills for its disk. Optionally, set an instance schedule that stops it every night.

## 5. Rules

- Only public or synthetic documents go on this VM, never real LTTS documents.
- Pin the model version, and record the VM type and GPU next to every latency number
  ("measured on one NVIDIA L4 24 GB, g2-standard-8").
- For the 7B-vs-32B comparison, create a second, temporary VM with a 48 GB GPU (check quota and availability,
  e.g. `g2-standard-24` with 2 × L4, or an A100 40 GB / L40S-class option), run it, then delete it.
