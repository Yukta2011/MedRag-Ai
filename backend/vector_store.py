import chromadb
import os

PERSIST_DIR = "./vectorstore"

client = chromadb.PersistentClient(path=PERSIST_DIR)

collection = client.get_or_create_collection(
    name="medical_papers",
    metadata={"hnsw:space": "cosine"}
)


def add_chunks(chunks, embeddings, metadatas, ids):
    """Add chunks to vector store"""
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def query_store(query_embedding, n_results=5):
    """Query vector store"""
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )


if __name__ == "__main__":
    print(f"Collection count: {collection.count()}")