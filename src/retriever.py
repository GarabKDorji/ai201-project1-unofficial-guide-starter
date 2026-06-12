"""Embedding + vector store + retrieval for The Unofficial Guide (Milestone 4).

Takes the chunks produced by chunking.py, turns each chunk's text into an
embedding vector with sentence-transformers/all-MiniLM-L6-v2, stores those
vectors (plus metadata) in ChromaDB, and retrieves the most similar chunks for
a user query.

ChromaDB does the embedding for us: we hand it the raw text and it runs the
SentenceTransformer model under the hood. We never compute vectors by hand.

Run directly to (re)build the store and try a couple of test queries
(run as a module from the project root so the ``src`` imports resolve):

    python -m src.retriever
"""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# Works whether you run from the project root (python -m src.retriever)
# or from inside the src/ folder (python retriever.py).

from chunking import load_and_chunk

# ---------------------------------------------------------------------------
# Configuration (matches the Retrieval Approach section of planning.md)
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # local, lightweight, recommended model
# Anchor the store to the project root (next to documents/) so it lands in the
# same place no matter which folder you run the script from.
CHROMA_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")
COLLECTION_NAME = "unofficial_guide"
TOP_K = 5                              # how many chunks to retrieve per query

# The embedding function and ChromaDB client are created once when this module
# loads. On the very first run sentence-transformers downloads the model
# (~30-60s); after that it uses a local cache.
_embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=_embed_fn,
    metadata={"hnsw:space": "cosine"},   # cosine distance: lower = more similar
)


def get_collection():
    """Return the ChromaDB collection."""
    return _collection


def embed_and_store() -> int:
    """Load all chunks, embed them, and store them in ChromaDB.

    If the collection is already populated, this does nothing (delete the
    ./chroma_db folder to force a rebuild after changing the chunking).
    Returns the number of chunks now in the store.
    """
    if _collection.count() > 0:
        print(f"Store already has {_collection.count()} chunks — skipping. "
              f"Delete {CHROMA_PATH} to rebuild.")
        return _collection.count()

    chunks = load_and_chunk()

    # ChromaDB.add() wants three parallel lists: the texts to embed, one
    # metadata dict per text, and a unique id per text.
    documents = [c.text for c in chunks]
    metadatas = [c.metadata for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    _collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Stored {_collection.count()} chunks in ChromaDB.")
    return _collection.count()


def retrieve(query: str, n_results: int = TOP_K) -> list[dict]:
    """Return the ``n_results`` chunks most similar to ``query``.

    Each result is a dict with the chunk text, its metadata, and the cosine
    distance (lower = closer match).
    """
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    # query() returns nested lists (one per query); we sent one query, so [0].
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []
    for text, meta, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "text": text,
            "metadata": meta,
            "distance": distance,
        })
    return retrieved


# ---------------------------------------------------------------------------
# Manual check: build the store, then run a couple of evaluation questions.
# ---------------------------------------------------------------------------
def _main() -> None:
    embed_and_store()

    test_queries = [
        "What do student reviews say about Daniel Mejia's teaching style?",
        "Do students describe the UTEP CS program as worth it?",
    ]
    for q in test_queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {q}")
        print("=" * 70)
        for r in retrieve(q):
            m = r["metadata"]
            who = m.get("professor") or m.get("title", "?")
            first_line = r["text"].splitlines()[0]
            snippet = r["text"].replace("\n", " ")[:90]
            print(f"\n  dist={r['distance']:.3f}  [{m.get('unit_kind')}] {who}")
            print(f"  {snippet}...")


if __name__ == "__main__":
    _main()
