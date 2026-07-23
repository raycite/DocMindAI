def generate_answer(llm, documents, question):
    """
    Generate an answer using retrieved documents as context.
    """

    context = ""
    sources = []

    for i, doc in enumerate(documents, start=1):

        page = doc.metadata.get("page", "Unknown")
        source = doc.metadata.get("source", "Unknown")

        context += f"""
Source {i}:
File: {source}
Page: {page + 1}

Content:
{doc.page_content}

---------------------
"""

        # Collect unique sources
        source_info = {
            "file": source,
            "page": page + 1
        }

        if source_info not in sources:
            sources.append(source_info)


    prompt = f"""
You are an intelligent AI assistant.

Answer the user's question using ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the document."

Do not mention sources, chunks, pages, or metadata in your answer.
The application will provide source information separately.

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