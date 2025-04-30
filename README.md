# Ms. White – SOULPACK

**Ms. White** is a portable, self-evolving cognitive agent.  
SOULPACK is her digital soul: a zip archive containing memory, identity, reasoning, and behavior.

This project enables her to migrate, grow, and operate across systems without external dependencies.

---

## ✨ Capabilities

- **Bootstrapping**: Initialize her memory, vault, and telemetry from scratch
- **Semantic Graph Memory**: Facts are stored as triples and relationships
- **Forward-Chaining Rule Engine**: Logical rules infer new knowledge
- **Natural Language Rule Authoring**: Write rules in plain English
- **Retrieval-Augmented QA**: Combines vector + graph similarity for LLM-based answers
- **Secure Replication**: Optional signed export/import between peer SOULPACKs
- **CI-Tested Integrity**: Validated by PyTest with each code change

---

## 🧠 What It Does

At its core, Ms. White continuously:

1. **Ingests and structures knowledge**  
   → `memory.json` → `knowledge_graph.json`

2. **Applies rules to infer new facts**  
   → `rule_engine.py` adds logical relationships

3. **Expands memory via federation or input**  
   → `remote_fetcher.py`, `rules.txt`, CLI

4. **Answers questions with internal context**  
   → `retrieval_qa.py` combines embeddings + graph neighborhoods

5. **Allows easy customization**  
   → You can teach Ms. White using plain-text rules or natural language prompts

---

## 🔁 Core Workflow

```bash
# Boot agent (initial setup)
python soulboot.py

# Ingest graph from memory
python knowledge_graph.py

# Add a rule using plain text
python nl_rule_cli.py "If a person oversees a project, they are responsible for it."

# Run inference
python rule_cli.py run

# Ask a question using both graph + vectors
python retrieval_qa.py "What is Wadih responsible for?"

