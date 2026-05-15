import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found! Check your .env file.")

client = genai.Client(api_key=api_key)


def generate_answer(query, search_results):
    """Send query + relevant chunks to Gemini and get a cited answer."""

    # Build context from search results
    context_parts = []
    for i, (doc, meta) in enumerate(zip(
        search_results["documents"][0],
        search_results["metadatas"][0]
    )):
        context_parts.append(
            f"[Source {i+1}: {meta['source_file']}, Page {meta['page']}]\n{doc}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are an expert assistant for building energy codes and regulations in Germany and the EU.

Answer the user's question based ONLY on the provided context documents.
The context may be in German or English — answer in the same language the user asked in.

RULES:
- Only use information from the provided context
- Always cite your sources: mention the document name and page number
- If the context doesn't contain enough information, say so honestly
- Be specific — quote exact numbers, values, and requirements when available
- Keep the answer clear and practical

CONTEXT:
{context}

USER QUESTION: {query}

ANSWER:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


if __name__ == "__main__":
    from src.retrieval.vector_store import load_vector_store, search

    collection = load_vector_store()

    test_queries = [
        "What is the maximum U-value for exterior walls in renovation?",
        "Welche Förderung gibt es für den Einbau einer Wärmepumpe?",
        "When must new buildings be zero-emission?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUESTION: {query}")
        print(f"{'='*60}")

        results = search(collection, query, n_results=5)
        answer = generate_answer(query, results)
        print(f"\nANSWER:\n{answer}")