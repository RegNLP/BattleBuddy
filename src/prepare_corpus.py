# 2️⃣ `src/prepare_corpus.py`

import json
import os
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_text_from_html(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    # Remove script / style tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Normalize whitespace
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def extract_text_from_txt(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages_text = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        pages_text.append(page_text)
    text = "\n".join(pages_text)
    # Basic cleanup
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def chunk_text(
    text: str,
    max_chars: int,
    overlap_chars: int,
    min_chars: int,
):
    """
    Very simple character-based chunking with overlap.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + max_chars, length)
        chunk = text[start:end].strip()
        if len(chunk) >= min_chars:
            chunks.append(chunk)
        if end == length:
            break
        start = end - overlap_chars  # overlap for continuity
        if start < 0:
            start = 0

    return chunks


def infer_category_from_path(path: Path, raw_dir: Path) -> str:
    """
    Infer category ('lore', 'rules', 'army_guide', 'rules_update', etc.)
    from folder structure, assuming `raw_dir/category/...`.
    """
    try:
        rel = path.relative_to(raw_dir)
    except ValueError:
        # Not under raw_dir, fallback
        return "unknown"

    parts = rel.parts
    if len(parts) < 2:
        return "unknown"
    # Example: lore/stormcast_eternals.html -> 'lore'
    return parts[0]


def build_title_from_filename(path: Path) -> str:
    """
    Turn 'stormcast_eternals.html' into 'Stormcast Eternals'
    """
    stem = path.stem
    stem = stem.replace("-", " ").replace("_", " ")
    return stem.title()


def main():
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config" / "corpus_config.yaml"
    cfg = load_config(config_path)

    raw_dir = project_root / cfg["paths"]["raw_dir"]
    processed_corpus_path = project_root / cfg["paths"]["processed_corpus"]

    max_chars = cfg["chunking"]["max_chars"]
    min_chars = cfg["chunking"]["min_chars"]
    overlap_chars = cfg["chunking"]["overlap_chars"]

    print(f"[prepare_corpus] Raw dir: {raw_dir}")
    print(f"[prepare_corpus] Output: {processed_corpus_path}")

    all_chunks = []
    doc_id_counter = 0

    # Walk through all files under raw_dir
    for root, dirs, files in os.walk(raw_dir):
        root_path = Path(root)

        for fname in files:
            path = root_path / fname
            suffix = path.suffix.lower()

            # Skip hidden files etc.
            if fname.startswith("."):
                continue

            # Extract category from folder structure
            category = infer_category_from_path(path, raw_dir)

            print(f"\n[prepare_corpus] Processing file: {path} (category={category})")

            # Extract text depending on file type
            if suffix in [".html", ".htm"]:
                text = extract_text_from_html(path)
            elif suffix in [".txt"]:
                text = extract_text_from_txt(path)
            elif suffix in [".pdf"]:
                text = extract_text_from_pdf(path)
            else:
                print(f"[prepare_corpus] Skipping unsupported file type: {path}")
                continue

            if not text.strip():
                print(f"[prepare_corpus] WARNING: Empty text extracted from {path}")
                continue

            # Chunking
            chunks = chunk_text(text, max_chars=max_chars, overlap_chars=overlap_chars, min_chars=min_chars)
            print(f"[prepare_corpus] -> {len(chunks)} chunks")

            title = build_title_from_filename(path)

            for i, chunk in enumerate(chunks):
                doc_id = f"aos_{category}_{path.stem}_{i:03d}"

                item = {
                    "id": doc_id,
                    "title": title,
                    "text": chunk,
                    "source": "unknown",
                    "url": None,
                    "category": category,
                    "faction": None,
                    "date": None,
                    "edition": None,
                }
                all_chunks.append(item)
                doc_id_counter += 1

    # Ensure output directory exists
    processed_corpus_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSONL
    with open(processed_corpus_path, "w", encoding="utf-8") as f:
        for item in all_chunks:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\n[prepare_corpus] Done. Wrote {len(all_chunks)} chunks to {processed_corpus_path}")


if __name__ == "__main__":
    main()
