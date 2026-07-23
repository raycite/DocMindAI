from retriever import retrieve_documents
from llm import get_llm
from qa import generate_answer


def chat(vector_store):
    """
    Ask the user a question
    and generate an answer.
    """

    llm = get_llm()

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        documents = retrieve_documents(
            vector_store,
            question
        )

        print("\nRetrieved Documents:\n")

        for i, doc in enumerate(documents, start=1):
            print(f"----- Chunk {i} -----")
            print(doc.page_content)
            print()

        response = generate_answer(
            llm,
            documents,
            question
        )

        print("\nAnswer:\n")
        print(response["answer"])

        print("\nSources:")

        for source in response["sources"]:
            print(
                f"- {source['file']} (Page {source['page']})"
            )