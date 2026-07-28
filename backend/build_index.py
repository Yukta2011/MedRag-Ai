from pmc_loader import load_pmc_articles
from pubmed_loader import load_pubmed_abstracts
from chunker import chunk_text
from embedder import embed
from vector_store import add_chunks

import uuid


def build_index():

    print("Loading PMC articles...")
    pmc_articles = load_pmc_articles(
        query="artificial intelligence healthcare",
        max_results=500
    )

    print("Loading PubMed abstracts...")
    pubmed_articles = load_pubmed_abstracts(
        query="artificial intelligence healthcare",
        max_results=200
    )

    articles = pmc_articles + pubmed_articles

    print(f"\nTotal Articles: {len(articles)}")

    total_chunks = 0

    for article in articles:

        text = article.get("text", "")

        if len(text) < 100:
            continue

        chunks = chunk_text(text)

        if not chunks:
            continue

        embeddings = embed(chunks)

        metadatas = []

        ids = []

        for i, chunk in enumerate(chunks):

            metadata = {
                "title": article.get("title", "Unknown Title"),
                "authors": ", ".join(article.get("authors", [])),
                "journal": article.get("journal", ""),
                "year": article.get("year", ""),
                "pmc_id": article.get("pmc_id", ""),
                "pmid": article.get("pmid", ""),
                "url": article.get(
                    "url",
                    f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{article.get('pmc_id','')}/"
                    if article.get("pmc_id")
                    else f"https://pubmed.ncbi.nlm.nih.gov/{article.get('pmid','')}/"
                )
            }

            metadatas.append(metadata)

            ids.append(str(uuid.uuid4()))

        add_chunks(
            chunks,
            embeddings,
            metadatas,
            ids
        )

        total_chunks += len(chunks)

        print(
            f"Indexed: {article.get('title','Unknown')[:60]}"
            f" ({len(chunks)} chunks)"
        )

    print("\n====================================")
    print("Index Complete")
    print("====================================")
    print(f"Articles : {len(articles)}")
    print(f"Chunks   : {total_chunks}")


if __name__ == "__main__":
    build_index()