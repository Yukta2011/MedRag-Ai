from embedder import embed
from vector_store import collection


def retrieve(question, k=5):
    """Retrieve relevant documents"""
    query_embedding = embed(question)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    return {
        "documents": results["documents"][0] if results["documents"] else [],
        "metadatas": results["metadatas"][0] if results["metadatas"] else [],
        "distances": results["distances"][0] if results["distances"] else []
    }


if __name__ == "__main__":
    result = retrieve("What is diabetes?")
    print(f"Retrieved {len(result['documents'])} documents")
    for i, doc in enumerate(result["documents"][:2]):
        print(f"--- Chunk {i+1} ---")
        print(doc[:200])