from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def embed(texts):
    """Embed texts using SentenceTransformer"""
    if isinstance(texts, str):
        texts = [texts]
    return model.encode(texts, show_progress_bar=True).tolist()


if __name__ == "__main__":
    embeddings = embed(["test sentence", "another test"])
    print(f"Embeddings shape: {len(embeddings)} x {len(embeddings[0])}")