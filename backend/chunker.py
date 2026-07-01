import re


def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks"""
    if not text or len(text) < 50:
        return []

    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.5:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks


if __name__ == "__main__":
    test = "This is a test. " * 50
    chunks = chunk_text(test)
    print(f"Created {len(chunks)} chunks")