# Evaluation

- `metrics/` trust metrics (SCR, MRA, safety-step recall, exact critical values, abstention P/R), retrieval and citation metrics
- `benchmarks/` loaders for MMLongBench-Doc, SlideVQA, E-Manual QA, ALCE, RGB, WikiContradict, FreshQA, MuSiQue/HotpotQA
- `mach_bench/` corpus builder (FAA ADs, scripted counterfactual edits + changelog), questions, splits (30% dev / 70% test)
- `edge_cases/fixtures/` YAML fixtures for the 55 cases; `edge_cases/test_edge_cases.py` harness

Never tune on test splits. See docs/06.
