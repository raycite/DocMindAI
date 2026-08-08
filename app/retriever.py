from planner import plan_retrieval


def retrieve_documents(vector_store, question):

    total_chunks = vector_store._collection.count()

    settings = plan_retrieval(
        question,
        total_chunks
    )

    print(
        f"\nRetrieval settings: "
        f"k={settings['k']}, "
        f"fetch_k={settings['fetch_k']}, "
        f"strategy={settings['search_type']}"
    )

    retriever = vector_store.as_retriever(
        search_type=settings["search_type"],
        search_kwargs={
            "k": settings["k"],
            "fetch_k": settings["fetch_k"]
        }
    )

    documents = retriever.invoke(question)

    return documents