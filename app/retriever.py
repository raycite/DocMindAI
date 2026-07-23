from langchain_core.documents import Document



def retrieve_documents(vector_store, question, k=3):

    results = vector_store.max_marginal_relevance_search(
        query=question,
        k=k,
        fetch_k=10
    )

    return results