from retriever import retrieve
from local_llm import ask_local_model
from cloud_llm import ask_cloud_model
from router import route_question


# =====================================================
# Format Sources
# =====================================================

def format_sources(metadata):

    papers = {}

    for meta in metadata:

        pmc = meta.get("pmc_id")

        if pmc not in papers:

            papers[pmc] = {
                "title": meta.get("title"),
                "authors": meta.get("authors"),
                "journal": meta.get("journal"),
                "year": meta.get("year"),
                "pmc_id": pmc,
                "url": meta.get(
                    "url",
                    f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc}/"
                ),
            }

    return list(papers.values())


# =====================================================
# Prompt for Retrieved Papers
# =====================================================

def build_rag_prompt(question, context):

    return f"""
You are MedRAG AI, an evidence-based medical assistant.

Use the retrieved medical papers ONLY if they are relevant.

If the retrieved papers are directly related to the user's question:

- Answer using the research.
- Mention important findings.

If the retrieved papers are NOT directly related:

- Say the retrieved papers are not directly relevant.
- Then answer using established medical knowledge.
- Do NOT invent research findings.

Finally include:

Research Evidence:
- Summarize whether the retrieved papers support the answer.

==========================
MEDICAL RESEARCH
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""


# =====================================================
# Prompt without Retrieval
# =====================================================

def build_general_prompt(question):

    return f"""
You are an expert medical AI assistant.

No relevant indexed medical research was found.

Answer using established medical knowledge.

If appropriate, recommend consulting a healthcare professional.

Question:

{question}

Answer:
"""


# =====================================================
# Main RAG Function
# =====================================================

def ask_rag(question):

    definition_words = [
        "what is",
        "what are",
        "define",
        "meaning of",
        "tell me about",
        "explain",
    ]

    is_definition = any(
        question.lower().startswith(word)
        for word in definition_words
    )

    docs = retrieve(question, k=5)

    documents = docs["documents"]
    metadata = docs["metadatas"]
    distances = docs["distances"]

    # ------------------------------------
    # Better filtering for definition questions
    # ------------------------------------

    if is_definition:

        keyword = (
            question.lower()
            .replace("what is", "")
            .replace("what are", "")
            .replace("define", "")
            .replace("meaning of", "")
            .replace("tell me about", "")
            .replace("explain", "")
            .replace("?", "")
            .strip()
        )

        filtered_docs = []
        filtered_meta = []
        filtered_distances = []

        for doc, meta, dist in zip(documents, metadata, distances):

            title = meta.get("title", "").lower()

            if keyword in title or keyword in doc.lower():

                filtered_docs.append(doc)
                filtered_meta.append(meta)
                filtered_distances.append(dist)

        if filtered_docs:

            documents = filtered_docs
            metadata = filtered_meta
            distances = filtered_distances

    retrieval_found = len(documents) > 0

    route = route_question(question)

    # ------------------------------------
    # Build Prompt
    # ------------------------------------

    if retrieval_found:

        context = "\n\n".join(documents)

        prompt = build_rag_prompt(
            question,
            context,
        )

    else:

        prompt = build_general_prompt(question)

    # ------------------------------------
    # Choose Model
    # ------------------------------------

    if route == "local":

        answer = ask_local_model(prompt)
        model_used = "Mistral"

    else:

        answer = ask_cloud_model(prompt)
        model_used = "Gemini"

        if (
            "429" in answer
            or "503" in answer
            or "RESOURCE_EXHAUSTED" in answer
            or "Error" in answer
        ):

            print("Cloud failed. Falling back to local...")

            answer = ask_local_model(prompt)

            model_used = "Mistral (Fallback)"
            route = "local"

    # ------------------------------------
    # Return
    # ------------------------------------

    return {

        "question": question,

        "answer": answer,

        "route": route,

        "model_used": model_used,

        "retrieval": retrieval_found,

        "sources": format_sources(metadata) if retrieval_found else [],

        "distances": distances if retrieval_found else [],

        "chunks_retrieved": len(documents),

        "fallback": not retrieval_found,
    }


# =====================================================
# CLI Test
# =====================================================

if __name__ == "__main__":

    while True:

        q = input("\nAsk Medical Question: ")

        if q.lower() == "exit":
            break

        result = ask_rag(q)

        print("\n===========================")
        print("ANSWER")
        print("===========================\n")

        print(result["answer"])

        print("\nModel:", result["model_used"])
        print("Retrieval:", result["retrieval"])
        print("Chunks:", result["chunks_retrieved"])

        print("\nSources:\n")

        for src in result["sources"]:
            print(src)