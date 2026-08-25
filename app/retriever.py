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

    # Retrieve a wider set of candidates first
    retriever = vector_store.as_retriever(
        search_type=settings["search_type"],
        search_kwargs={
            "k": settings["k"],
            "fetch_k": settings["fetch_k"]
        }
    )

    documents = retriever.invoke(question)

    # Display which files were retrieved
    print("\nRetrieved document sources:")

    seen_sources = set()

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        if source not in seen_sources:
            print(f"- {source}")
            seen_sources.add(source)

    return documents