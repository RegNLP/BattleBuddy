Phase 0 – Project Setup & Corpus Definition

Goal:  
Set up the BattleBuddy repository, define the document schema and configuration, and prepare the raw Age of Sigmar corpus folders for later preprocessing and indexing.

🔍 Important: Phase 0 is about structure and data collection only.  
The actual preprocessing / chunking logic (e.g. prepare_corpus.py) will be implemented in Phase 1.

0.1 Repository & Folder Layout

Create a new repository, e.g. battlebuddy-aos, with the following base structure:

```text
battlebuddy-aos/
  config/
    corpus_config.yaml
  data/
    raw/
      lore/
      rules/
      guides/
      rules_update/
      # (optional later) metagame/
      # (optional later) youtube/
    processed/
      .gitkeep
  docs/
    schema.md
    phase_0.md
    phase_1.md        # (placeholder)
    phase_2.md        # (placeholder)
    phase_3.md        # (placeholder)
    phase_4.md        # (placeholder)
  notebooks/
    00_corpus_sanity_check.md
  src/
    __init__.py
    # (preprocessing / RAG code will be added in later phases)
  .gitignore
  README.md
  requirements.txt
```


You can add / rename folders later, but this gives a clear separation between:

config – project-wide settings
data – raw and processed corpora
docs – design & phase specifications
notebooks – quick analyses and sanity checks
src – library / application code


0.2 Python Environment & Requirements (Phase 0)

At this stage you only need basic utilities for fetching, parsing and organizing data.

Create a requirements.txt with:
``` txt
beautifulsoup4
requests
pypdf
tqdm
python-dotenv
pyyaml
```

Later phases will add LLM- and API-related packages (LangChain, LangGraph, sentence-transformers, chromadb, fastapi, streamlit, etc.).

0.3 .gitignore

Add a minimal .gitignore to keep the repo clean:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
.eggs/

# Environments
.venv/
venv/
.env
.env.*

# Data
data/processed/*
!data/processed/.gitkeep

# Notebooks
.ipynb_checkpoints/
```

Note: data/processed/* is ignored by default.
You can later decide whether a specific processed corpus should be versioned.

0.4 Corpus Configuration

Create config/corpus_config.yaml with basic paths, chunking defaults, and categories.
These will be consumed in later phases by preprocessing / RAG code.
```
paths:
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  processed_corpus: "data/processed/corpus.jsonl"

chunking:
  # Initial defaults – can be tuned later
  max_chars: 1200        # approximate target chunk size
  min_chars: 300
  overlap_chars: 150

categories:
  lore:
    raw_subdir: "lore"
  rules:
    raw_subdir: "rules"
  army_guide:
    raw_subdir: "guides"
  rules_update:
    raw_subdir: "rules_update"
  # optional / advanced (Phase 2+):
  # metagame:
  #   raw_subdir: "metagame"
  # youtube:
  #   raw_subdir: "youtube"

metadata_defaults:
  source: "unknown"
  edition: "unspecified"
```

This keeps path and chunking logic out of the code and makes the project feel more “production-like”.

0.5 Document Schema Specification

Define the JSONL schema once, then stick to it for all processed documents.

Create docs/schema.md:

# BattleBuddy Document Schema

Each entry in `data/processed/corpus.jsonl` is a single JSON object
representing a chunk of text from an Age of Sigmar source.

## Required fields
```
- `id` (string)  
  Unique identifier for the chunk. Recommended format:
  `<domain>_<category>_<slug>_<index>`, e.g.
  `aos_lore_stormcast_01`.

- `title` (string)  
  Human-readable title of the source page or section.

- `text` (string)  
  The chunked text content used for retrieval and LLM context.

- `source` (string)  
  High-level source label, for example:
  - `lexicanum_aos`
  - `warhammer_community`
  - `wahapedia_aos`
  - `internal_notes`

- `category` (string)  
  Coarse topic/category of the chunk, one of:
  - `lore`
  - `rules`
  - `army_guide`
  - `rules_update`
  - `metagame` (optional / advanced)

## Optional fields

- `url` (string)  
  Original URL for web-based sources, if available.

- `faction` (string)  
  Faction name if the chunk is tied to a specific faction
  (e.g. `Stormcast Eternals`, `Nighthaunt`).

- `date` (string, ISO `YYYY-MM-DD`)  
  Relevant for rules updates, FAQs, and battlescrolls.
  Used to prioritise newer chunks for rules questions.

- `edition` (string)  
  Game edition or rules context, e.g. `"3rd"`.
```
## Example

``` json
{
  "id": "aos_lore_stormcast_01",
  "title": "Stormcast Eternals - Overview",
  "text": "The Stormcast Eternals are mortal heroes reforged by Sigmar in the Realm of Azyr...",
  "source": "lexicanum_aos",
  "url": "https://example.com/...",
  "category": "lore",
  "faction": "Stormcast Eternals",
  "date": "2024-01-01",
  "edition": "3rd"
}
```

This schema document is what you can later point to in CV / portfolio as “corpus design”.

0.6 Raw Data Layout & Collection

Phase 0 only requires you to collect and organise AoS content into data/raw/.  
Parsing, cleaning and chunking will happen in Phase 1.

Create (or confirm) the following subfolders:
```
data/raw/
  lore/
  rules/
  guides/
  rules_update/
  # metagame/    (optional – Phase 2+)
  # youtube/     (optional – Phase 2+)
```

Then:

Lore (data/raw/lore/)
Collect a small, representative set, for example:

2–3 pages describing the Mortal Realms and major events (Realmgate Wars, Soul Wars).

2–3 pages for key factions (e.g. Stormcast Eternals, Nighthaunt).

Save as .html or .txt files (one per page).

Rules (data/raw/rules/)
Collect:

3–5 pages that explain:

Turn / battle round structure,

Phases (Hero, Movement, Shooting, Charge, Combat, Battleshock),

Common concepts like armour saves, wards, command abilities.

Again, save them as .html or .txt.

Beginner Guides (data/raw/guides/)
Collect:

2–3 introductory or “how to start” faction guides (e.g. “Getting started with Nighthaunt”).

Save them as .html/.txt for now.

Rules Updates (data/raw/rules_update/)
Collect:

1–2 recent official AoS FAQ / Battlescroll PDFs from Warhammer Community (Age of Sigmar downloads).

Save them directly as .pdf.
They’ll be parsed in Phase 1 using a PDF library.

(Optional) Metagame and YouTube transcript folders can be created but don’t need to be populated in Phase 0.

0.7 Data README & Sanity Notebook

To make the project more self-documenting:

data/README.md
Add a short description of the data layout:

# Data Layout

- `data/raw/` contains raw source files (HTML, text, PDFs).
- `data/processed/` will contain normalized JSONL chunks used for retrieval.

Subfolders under `data/raw/`:

- `lore/`         – AoS lore pages (Realms, factions, events)
- `rules/`        – core rules explanations
- `guides/`       – beginner guides / faction intros
- `rules_update/` – official FAQs, errata, battlescrolls (PDFs)

Optional (later):

- `metagame/`     – tournament reports, advanced tactics
- `youtube/`      – exported transcripts from AoS channels


notebooks/00_corpus_sanity_check.md
Create a simple markdown stub to be- filled later:

# 00 – Corpus Sanity Check

This notebook will be used after Phase 1 to:

1. Count documents per category.
2. Inspect a few example chunks from `corpus.jsonl`.
3. Check average and max chunk lengths.
4. Verify metadata fields (category, faction, date, edition).


0.8 Exit Criteria for Phase 0

Phase 0 is considered complete when:

The repository battlebuddy-aos exists with:

Base folder structure,

.gitignore and requirements.txt,

config/corpus_config.yaml,

docs/schema.md,

docs/phase_0.md (this file) and placeholders for later phases.

Raw AoS content is collected and stored in:

data/raw/lore/,

data/raw/rules/,

data/raw/guides/,

data/raw/rules_update/.

The document schema and corpus configuration are clearly defined and ready to be used by preprocessing code in Phase 1.

At this point, you can move on to docs/phase_1.md, where the first RAG pipeline and the actual prepare_corpus.py (or equivalent) will be introduced.
