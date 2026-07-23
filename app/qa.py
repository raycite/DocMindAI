from langchain_core.documents import Document


def generate_answer(llm, documents, question):
    """
    Generate an answer using the retrieved documents as context.
    """

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = f"""
You are an intelligent AI assistant.

Answer the user's question using ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response