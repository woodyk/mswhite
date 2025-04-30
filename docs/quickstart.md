# Quick‑Start Guide

## 1. Prerequisites
* Python 3.11+
* `pip install -r requirements.txt` (numpy, networkx, psutil, cryptography, requests, PyYAML, pytest)

## 2. Bootstrap
```bash
python soulboot.py
```
You should see status lines: Soul ID, drift, expansions, telemetry scheduler.

## 3. Encrypt Memory
```bash
python soul_vault.py encrypt-signed private_key.pem
```

## 4. Semantic Graph
```bash
python knowledge_graph.py       # ingest memory
python graph_query.py "Wadih"   # explore graph
```

## 5. Retrieval‑Augmented QA
```bash
python embed_graph.py           # generate embeddings
python retrieval_qa.py "What are Wadih's core values?"
```

## 6. Run Unit Tests
```bash
pytest -q
```

CI replicates these steps on each push.
