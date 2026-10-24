"""Optional ChromaDB retrieval with local hashed token vectors, not an LLM."""

import hashlib
import math
import re
from app.data import DATA

INDEX = DATA / "generated/chroma"
COLLECTION = "payroll_policies_v1"


def embed(text):
    vector = [0.0] * 512
    for token in re.findall(r"[a-z]{2,}", text.lower()):
        slot = int.from_bytes(hashlib.sha256(token.encode()).digest()[:4], "big") % len(vector)
        vector[slot] += 1
    norm = math.sqrt(sum(x * x for x in vector)) or 1
    return [x / norm for x in vector]


class PolicyIndex:
    def __init__(self, collection):
        self.collection = collection

    def count(self):
        return self.collection.count()

    def query(self, query_texts, n_results=3):
        return self.collection.query(
            query_embeddings=[embed(q) for q in query_texts], n_results=min(n_results, self.count())
        )


def open_index():
    if not INDEX.exists():
        return None
    try:
        import chromadb
    except ImportError as exc:
        raise ImportError(
            "Policy index exists, but ChromaDB is missing. Install requirements-rag.txt."
        ) from exc
    try:
        client = chromadb.PersistentClient(path=str(INDEX))
        return PolicyIndex(client.get_collection(COLLECTION, embedding_function=None))
    except Exception as exc:
        raise RuntimeError(
            "Policy index cannot be opened. Run python -m etl.index_documents to rebuild it."
        ) from exc
