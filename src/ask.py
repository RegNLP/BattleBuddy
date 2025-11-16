import os
import sys
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from openai import OpenAI


os.environ["TOKENIZERS_PARALLELISM"] = "false"



def load_chroma_collection(project_root: Path, collection_name: str = "battlebuddy_aos"):
    db_dir = project_root / "data" / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir), settings=Settings(anonymized_telemetry=False))
    return client.get_collection(collection_name)


def build_prompt(question: str, contexts):
    context_text = "\n\n---\n\n".join(contexts)
    prompt = f"""You are BattleBuddy, an Age of Sigmar (AoS) assistant.

Use only the provided context to answer the user's question about AoS lore, rules, and beginner army-building.
If the answer is not clearly supported by the context, say that you don't know based on the current information.

Preserve original names of factions, units, rules, and places.

Context:
{context_text}

Question: {question}

Answer:"""
    return prompt


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m ask \"Your question here\"")
        sys.exit(1)

    question = sys.argv[1]
    project_root = Path(__file__).resolve().parents[0].parent  # src -> project root

    # Load Chroma and embedding model
    collection = load_chroma_collection(project_root)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embed_model = SentenceTransformer(model_name)

    # Embed query and retrieve top-k
    query_embedding = embed_model.encode([question])[0].tolist()
    k = 5
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    print("[ask] Retrieved contexts:")
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        print(f"\n--- Context {i+1} (category={meta.get('category')}, title={meta.get('title')}) ---\n")
        print(doc[:500] + ("..." if len(doc) > 500 else ""))

    # Build prompt
    prompt = build_prompt(question, docs)

    # OpenAI client
    client = OpenAI()  # uses OPENAI_API_KEY

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialised in Warhammer: Age of Sigmar."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    answer = completion.choices[0].message.content
    print("\n=== BattleBuddy Answer ===\n")
    print(answer)


if __name__ == "__main__":
    main()
