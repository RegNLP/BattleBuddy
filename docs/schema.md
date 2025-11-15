# BattleBuddy Document Schema

Each document in `data/processed/corpus.jsonl` is a single JSON object
representing a chunk of text from an Age of Sigmar source.

## Required fields

- `id` (string)  
  Unique identifier for the chunk. Recommended format:
  `<domain>_<category>_<slug>_<index>`, e.g.
  `aos_lore_stormcast_01`.

- `title` (string)  
  Human-readable title of the source section or page.

- `text` (string)  
  The actual chunked text content used for retrieval.

- `source` (string)  
  High-level source label, e.g.:
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
  Original URL for web-based sources (if available).

- `faction` (string)  
  Faction name if the chunk is strongly tied to a specific faction
  (e.g. `Stormcast Eternals`, `Nighthaunt`).

- `date` (string, ISO format `YYYY-MM-DD`)  
  Relevant for rules updates, FAQs, battlescrolls. Used to prioritize
  newer chunks when answering rules questions.

- `edition` (string)  
  Game edition or rules context if needed, e.g. `"3rd"`.

## Example

```json
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

This file is something you can even link in your CV / portfolio (“Documented a reusable corpus schema for RAG experiments”).

### 0.6 Populate Raw Data Folders

For Phase 0 you don’t need to parse anything yet; just **collect and drop** files into `data/raw`:

- `data/raw/lore/`
  - A few `.html` or `.txt` files with lore pages (Mortal Realms, Stormcast, Nighthaunt, etc.)
- `data/raw/rules/`
  - A few `.html` / `.txt` files describing core rules and phases.
- `data/raw/guides/`
  - 2–3 intro or beginner guides saved as `.html` / `.txt`.
- `data/raw/rules_update/`
  - 1–2 FAQ / Battlescroll PDFs.

Optionally add a tiny `data/README.md`:

```markdown
# Data Layout

- `data/raw/` contains raw source files (HTML, text, PDFs).
- `data/processed/` will contain normalized JSONL chunks used for RAG.

Subfolders under `data/raw/`:

- `lore/`         – AoS lore pages (Realms, factions, events)
- `rules/`        – core rules explanations
- `guides/`       – beginner guides / faction intros
- `rules_update/` – official FAQs, errata, battlescrolls (PDFs)
