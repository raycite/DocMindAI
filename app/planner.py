def plan_retrieval(question, total_chunks, chunk_size=500):
    """
    Decide how many chunks to retrieve and which
    retrieval strategy to use.
    """

    question_length = len(question.split())

    # Very small document collection
    if total_chunks <= 20:
        k = min(3, total_chunks)
        fetch_k = min(6, total_chunks)

    # Medium document collection
    elif total_chunks <= 100:
        k = 3
        fetch_k = 10

    # Large document collection
    else:
        k = 5
        fetch_k = 15

    # Longer questions usually require broader context
    if question_length > 12:
        k += 2
        fetch_k += 5

    # Never retrieve more chunks than actually exist
    k = min(k, total_chunks)
    fetch_k = min(fetch_k, total_chunks)

    return {
        "k": k,
        "fetch_k": fetch_k,
        "search_type": "mmr"
    }