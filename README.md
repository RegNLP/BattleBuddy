# BattleBuddy: An Age of Sigmar LLM Assistant for Players

BattleBuddy is an end-to-end LLM / GenAI assistant designed for **Warhammer: Age of Sigmar (AoS)** players.

It is not just a toy chatbot: the project is built as a realistic, portfolio-ready example of how to design, implement, and deploy a modern LLM system using **RAG, multi-agent orchestration, vector databases, and cloud-native tooling**.

---

## Project Overview

BattleBuddy helps AoS players with three main types of questions:

- **Lore** – Mortal Realms, factions, gods, key characters and events.  
- **Rules & mechanics** – turn structure, phases, saves, wards, command abilities, and other core concepts.  
- **Army-building** – beginner-friendly list ideas, faction playstyles, unit roles, and (optionally) basic meta insights.

Under the hood, BattleBuddy combines:

- **Retrieval-Augmented Generation (RAG)** over a curated AoS corpus,  
- **Vector databases & embeddings** for semantic search,  
- **Multi-agent orchestration** (via LangGraph) to route queries to specialized AoS “agents”,  
- **LLM tools / function calling** for structured unit and faction lookups,  
- **Containerization and deployment** to simulate a production-style GenAI workflow.

The domain is Age of Sigmar, but the design is intended to transfer directly to real-world, domain-specific assistants (e.g., legal, financial, regulatory).

---

## Goals & Learning Objectives

### Main goals

- **Build an end-to-end GenAI system** that covers the full stack:  
  data ingestion → retrieval → LLM reasoning → API → UI.
- **Gain hands-on experience** with LangChain, LangGraph, vector databases, and LLM tool / function calling in a realistic project.
- **Work with modern foundation models** (OpenAI and/or open-source) inside a controlled RAG setup focused on grounding and reduced hallucination.
- **Containerize and deploy BattleBuddy** using Docker and a simple cloud environment to simulate a production-style workflow.
- *(Stretch)* **Implement LLM evaluation and a small RLHF-style preference loop** to experiment with aligning answer style and quality.

### Secondary goals

- **Practice clean software design and documentation** so that the project can be easily showcased in CVs, portfolios, and interviews.
- **Explore multi-agent patterns and orchestration** in a rich, real-world domain (Age of Sigmar), including routing, specialization, and coordination between agents.

---

## High-Level System Design

At a high level, BattleBuddy will consist of:

- A curated **Age of Sigmar knowledge corpus**, including:
  - Lore wikis (Realms, factions, events),
  - Core rules explanations and FAQs/errata,
  - Beginner guides and (optionally) metagame analysis,
  - Internal synthetic notes (faction summaries, example lists).
- A **RAG pipeline** that:
  - Embeds questions and documents using sentence-transformer models,
  - Retrieves relevant chunks from a vector database,
  - Feeds retrieved context into an LLM with a grounded prompt.
- A **multi-agent layer** that routes queries to:
  - `LoreAgent` (setting, narrative),
  - `RulesAgent` (rules, interactions, updates),
  - `ArmyBuilderAgent` (playstyle, lists, meta – if enabled).
- A **backend API** (FastAPI) that exposes a `/chat` endpoint.
- A simple **frontend UI** (Streamlit or React) to interact with the assistant.
- **Dockerized services** to run the API, vector DB, and UI in a reproducible way.
- Basic **evaluation scripts** and (optionally) a small RLHF-style experiment.

Detailed architecture (LLM choices, embedding models, categories, agent design, etc.) is described in the phase-specific docs.

---

## Project Phases (High-Level Roadmap)

Each phase will have its own markdown file (e.g., `docs/phase_0.md`, `docs/phase_1.md`) describing detailed steps and implementation notes.

### Phase 0 – Project Setup & Corpus Definition

- Initialize the repository, folder structure, and configuration files.  
- Define the **document schema** (JSONL format, categories, metadata).  
- Collect a small, representative AoS corpus in `data/raw/` (lore, rules, guides, FAQs).  
- Document data layout and schema for later phases.

**Details:** see `docs/phase_0.md`.

---

### Phase 1 – Core RAG MVP (Plain Python)

- Implement a simple **RAG pipeline** in plain Python:  
  embeddings → vector DB → retrieval → single LLM call.
- Build a minimal **CLI interface** (e.g., `python ask.py "Who are the Stormcast Eternals?"`).  
- Validate that BattleBuddy can answer basic AoS questions using retrieved context only.

**Details:** see `docs/phase_1.md`.

---

### Phase 2 – LangChain & LangGraph Multi-Agent Assistant

- Rebuild the retrieval and QA pipeline using **LangChain** abstractions.  
- Introduce a **multi-agent workflow** with LangGraph:
  - `LoreAgent`, `RulesAgent`, and `ArmyBuilderAgent`.  
- Add **tools / function calling** (e.g., `get_unit_summary`, `suggest_basic_army`).  
- Start logging interactions for debugging and evaluation.

**Details:** see `docs/phase_2.md`.

---

### Phase 3 – API, UI, Logging & Docker

- Wrap the LangGraph pipeline inside a **FastAPI** backend with a `/chat` endpoint.  
- Build a simple **web UI** (Streamlit or React) for players to chat with BattleBuddy.  
- Add basic **logging / observability** (queries, agent routing decisions, retrieved docs).  
- Create **Docker** and `docker-compose` configs and deploy to a small cloud instance.

**Details:** see `docs/phase_3.md`.

---

### Phase 4 – Evaluation & RLHF-style Experiments (Stretch)

- Construct a small **evaluation set** of AoS questions (lore, rules, army-building).  
- Implement **retrieval metrics** (e.g., Recall@k, nDCG@k) and simple **answer quality checks**.  
- *(Optional)* Collect preference data (Answer A vs. Answer B) and run a small  
  **RLHF-style experiment** (DPO/ORPO or reward model) to tune answer style and helpfulness.

**Details:** see `docs/phase_4.md`.

---

## Status

> **Current status:** Designing the project and setting up Phase 0 (repository structure, config, and corpus schema).

As the project evolves, this section can be updated with milestones, screenshots, and links to demos.

---

## License

This is a personal / hobby project for learning and experimentation with LLM systems.  
Any reuse of proprietary AoS content should comply with the original IP holders’ terms and relevant site ToS.
