import chromadb

PERSIST_DIR = "./vectorstore"

client = chromadb.PersistentClient(path=PERSIST_DIR)

collection = client.get_or_create_collection(
    name="medical_papers",
    metadata={"hnsw:space": "cosine"}
)


def add_chunks(chunks, embeddings, metadatas, ids):
    """
    Add chunks to ChromaDB
    """

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def query_store(query_text, n_results=5):
    """
    Search ChromaDB using query text.
    """

    return collection.query(
        query_texts=[query_text],
        n_results=n_results
    )


def collection_stats():
    return {
        "documents": collection.count(),
        "name": collection.name
    }


if __name__ == "__main__":
    print(collection_stats())