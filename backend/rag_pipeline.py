from retriever import retrieve
from local_llm import ask_local_model
from cloud_llm import ask_cloud_model
from router import route_question


def build_prompt(context, question, sources):
    return f"""You are an expert medical research assistant.

Use ONLY the research context provided below.
If the answer is not contained in the context, say: "The information is not available in the retrieved documents."

=========================
RESEARCH CONTEXT
=========================
{context}

=========================
SOURCES
=========================
{sources}

=========================
QUESTION
=========================
{question}

=========================
ANSWER
=========================
"""


def format_citations(metadata):
    citations = []
    for i, meta in enumerate(metadata, 1):
        if meta:
            title = meta.get('title', 'Unknown Title')
            authors = meta.get('authors', '')[:50] if meta.get('authors') else ''
            journal = meta.get('journal', 'Unknown Journal')
            year = meta.get('year', 'N/A')
            pmc_id = meta.get('pmc_id', 'N/A')
            citations.append(f"[{i}] {title} | {authors} | {journal} ({year}) | PMC:{pmc_id}")
        else:
            citations.append(f"[{i}] Unknown Source")
    return "".join(citations)


def ask_rag(question):
    try:
        docs = retrieve(question, k=5)
        documents = docs["documents"]
        metadata = docs["metadatas"]

        if not documents:
            return {
                "answer": "No relevant medical documents found.",
                "sources": [],
                "route": "none",
                "model_used": "none",
                "chunks_retrieved": 0
            }

        context = " ".join(documents[:5])
        context = context[:4000]
        sources = format_citations(metadata[:5])
        prompt = build_prompt(context, question, sources)

        route = route_question(question)

        # Try primary route
        if route == "local":
            answer = ask_local_model(prompt)
            model_used = "local (Mistral)"
        else:
            answer = ask_cloud_model(prompt)
            model_used = "cloud (Gemini)"

            # FALLBACK: If cloud fails, use local
            if "Error" in answer or "UNAVAILABLE" in answer or "503" in answer:
                print(f"\n⚠️  Cloud failed: {answer[:60]}...")
                print("🔄 Falling back to local Mistral...\n")
                answer = ask_local_model(prompt)
                model_used = "local (Mistral) [cloud fallback]"
                route = "local"
            
        return {
            "answer": answer,
            "sources": sources.split("\n"),
            "route": route,
            "model_used": model_used,
            "chunks_retrieved": len(documents)
        }

    except Exception as e:
        return {
            "answer": f"RAG Error: {str(e)}",
            "sources": [],
            "route": "error",
            "model_used": "none",
            "chunks_retrieved": 0
        }


if __name__ == "__main__":
    question = input("\nAsk Medical Question: ")
    result = ask_rag(question)

    print("\n" + "="*50)
    print(f"ANSWER (via {result['model_used']}):")
    print("="*50)
    print(result["answer"])

    print("\n" + "-"*50)
    print("SOURCES:")
    print("-"*50)
    for src in result["sources"]:
        print(src)

    print(f"\nRoute: {result['route']} | Chunks: {result['chunks_retrieved']}")  