from vector_store import query_store

SIMILARITY_THRESHOLD = 1.2


def retrieve(query, k=5):

    # ----------------------------------------
    # Clean the query for keyword matching
    # ----------------------------------------

    query_lower = query.lower()

    for phrase in [
        "what is",
        "what are",
        "define",
        "meaning of",
        "tell me about",
        "explain",
    ]:
        query_lower = query_lower.replace(phrase, "")

    query_lower = query_lower.replace("?", "").strip()

    # ----------------------------------------
    # Retrieve more candidates
    # ----------------------------------------

    results = query_store(query, n_results=15)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    filtered_docs = []
    filtered_meta = []
    filtered_distances = []

    # ----------------------------------------
    # Filter results
    # ----------------------------------------

    for doc, meta, dist in zip(documents, metadatas, distances):

        title = meta.get("title", "").lower()
        journal = meta.get("journal", "").lower()
        authors = meta.get("authors", "").lower()

        keyword_match = (
            query_lower in doc.lower()
            or query_lower in title
            or query_lower in journal
            or query_lower in authors
        )

        if dist <= SIMILARITY_THRESHOLD or keyword_match:

            meta["score"] = round(1 - dist, 3)

            if meta.get("pmc_id"):
                meta["url"] = (
                    f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{meta['pmc_id']}/"
                )
            else:
                meta["url"] = ""

            filtered_docs.append(doc)
            filtered_meta.append(meta)
            filtered_distances.append(dist)

    # ----------------------------------------
    # Sort by similarity (smallest distance first)
    # ----------------------------------------

    combined = list(
        zip(filtered_distances, filtered_docs, filtered_meta)
    )

    combined.sort(key=lambda x: x[0])

    filtered_distances = [x[0] for x in combined][:k]
    filtered_docs = [x[1] for x in combined][:k]
    filtered_meta = [x[2] for x in combined][:k]

    # ----------------------------------------
    # Return
    # ----------------------------------------

    return {
        "documents": filtered_docs,
        "metadatas": filtered_meta,
        "distances": filtered_distances,
        "retrieval_found": len(filtered_docs) > 0,
    }


if __name__ == "__main__":

    result = retrieve("What is heart disease?")

    print(result)