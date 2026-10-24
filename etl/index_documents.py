"""Build the optional, local policy search index; no model downloads or API keys."""

from app.data import DOCUMENTS
from app.documents import INDEX, COLLECTION, embed


def build_index():
    import chromadb

    files = sorted(DOCUMENTS.glob("*.txt"))
    if not files:
        raise ValueError("No policy text files found.")
    ids, documents, metadata = [], [], []
    for path in files:
        text = path.read_text().strip()
        for offset in range(0, len(text), 1000):
            chunk = text[offset : offset + 1200]
            if not chunk.strip():
                continue
            ids.append(f"{path.stem}:{offset}")
            documents.append(chunk)
            metadata.append(
                {
                    "doc_id": path.stem,
                    "title": path.stem.split("_", 1)[1].replace("_", " "),
                    "filename": path.name,
                }
            )
    INDEX.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX))
    existing = {c.name for c in client.list_collections()}
    if COLLECTION in existing:
        client.delete_collection(COLLECTION)
    collection = client.create_collection(
        COLLECTION, embedding_function=None, metadata={"hnsw:space": "cosine"}
    )
    collection.add(
        ids=ids, documents=documents, metadatas=metadata, embeddings=[embed(d) for d in documents]
    )
    return len(files), collection.count()


if __name__ == "__main__":
    files, chunks = build_index()
    print(f"Indexed {files} policies, {chunks} chunks")
