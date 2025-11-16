import json
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import yaml

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config" / "corpus_config.yaml"
    cfg = load_config(config_path)

    corpus_path = project_root / cfg["paths"]["processed_corpus"]

    print(f"[build_index] Loading corpus from: {corpus_path}")
    docs = []
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            docs.append(json.loads(line))

    print(f"[build_index] Loaded {len(docs)} chunks")

    # Sentence-transformers model
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"[build_index] Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    # Chroma persistent client
    db_dir = project_root / "data" / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir), settings=Settings(anonymized_telemetry=False))

    collection_name = "battlebuddy_aos"
    # Drop old collection if needed
    try:
        client.delete_collection(collection_name)
        print(f"[build_index] Deleted existing collection '{collection_name}'")
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    # Prepare data
    ids = [d["id"] for d in docs]
    texts = [d["text"] for d in docs]
    metadatas = [
        {
            "title": d.get("title"),
            "category": d.get("category"),
        }
        for d in docs
    ]

    print("[build_index] Computing embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    print("[build_index] Adding to Chroma collection...")
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print(f"[build_index] Done. Collection '{collection_name}' stored in {db_dir}")


if __name__ == "__main__":
    main()
