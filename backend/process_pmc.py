from pmc_loader import load_pmc_articles
from chunker import chunk_text
from embedder import embed
from vector_store import add_chunks
import time


def process_and_store(query="artificial intelligence healthcare", max_results=500):
    """Load PMC articles, chunk them, embed, and store in vector DB"""
    print("="*60)
    print("PMC Article Processing Pipeline")
    print("="*60)

    # Load articles
    articles = load_pmc_articles(query=query, max_results=max_results)

    if not articles:
        print("No articles loaded!")
        return

    all_chunks = []
    all_metadatas = []
    all_ids = []
    chunk_counter = 0

    print("" + "-"*60)
    print("Chunking and embedding...")
    print("-"*60)

    for idx, article in enumerate(articles):
        text = article.get("text", "")
        if not text or len(text) < 100:
            continue

        chunks = chunk_text(text)

        for chunk_idx, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "pmc_id": article.get("pmc_id", "unknown"),
                "title": article.get("title", "Unknown Title"),
                "authors": ", ".join(article.get("authors", [])),
                "journal": article.get("journal", "Unknown Journal"),
                "year": article.get("year", "N/A"),
                "chunk_index": chunk_idx
            })
            all_ids.append(f"pmc_{article.get('pmc_id', 'unknown')}_chunk_{chunk_idx}")
            chunk_counter += 1

        if (idx + 1) % 10 == 0:
            print(f"  Processed {idx+1}/{len(articles)} articles, {chunk_counter} total chunks")

    print(f"Total chunks to embed: {len(all_chunks)}")

    # Embed in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        batch_metas = all_metadatas[i:i+batch_size]
        batch_ids = all_ids[i:i+batch_size]

        print(f"Embedding batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}...")
        embeddings = embed(batch_chunks)

        add_chunks(batch_chunks, embeddings, batch_metas, batch_ids)

        if i + batch_size < len(all_chunks):
            time.sleep(0.5)

    print("" + "="*60)
    print(f"✅ Done! Stored {len(all_chunks)} chunks from {len(articles)} articles")
    print("="*60)


if __name__ == "__main__":
    process_and_store()