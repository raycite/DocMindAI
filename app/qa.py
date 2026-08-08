from pathlib import Path


def generate_answer(llm, documents, question):
    """
    Generate an answer using retrieved documents as context.
    """

    context = ""
    sources = []

    for i, doc in enumerate(documents, start=1):

        page = doc.metadata.get("page")

        if page is not None:
            page = page + 1
        else:
            page = "Unknown"

        source = Path(
            doc.metadata.get("source", "Unknown")
        ).name

        context += f"""
Source {i}:
File: {source}
Page: {page}

Content:
{doc.page_content}

---------------------
"""

        # Collect unique sources
        source_info = {
            "file": source,
            "page": page
        }

        if source_info not in sources:
            sources.append(source_info)

    prompt = f"""
You are an intelligent AI assistant working with retrieved documents.

Your task is to answer the user's question using ONLY the information
contained in the provided context.

IMPORTANT RULES:

1. Use all relevant information from the provided context.
2. Combine information across multiple sources when necessary.
3. Do not rely on only the first or most relevant-looking source.
4. For questions asking for a list, identify ALL distinct items that
   are explicitly supported by the context.
5. Do not invent, assume, or add information that is not in the context.
6. If the context does not contain enough information to answer the
   question, say:
   "I couldn't find that information in the document."
7. Do not mention sources, chunks, pages, scores, or metadata in your answer.
8. Answer clearly and directly.
9. For summary questions, combine the important information available
   across the retrieved context rather than focusing on one chunk.

Context:

{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response,
        "sources": sources
    }