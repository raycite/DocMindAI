from langchain_chroma import Chroma
import os


def create_vector_store(chunks, embedding_model):

    persist_directory = "vector_store"

    if os.path.exists(persist_directory):
        print("Loading existing vector database...")

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model
        )

    else:
        print("Creating new vector database...")

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=persist_directory
        )

    return vector_store