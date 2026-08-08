from langchain_chroma import Chroma
import shutil
import os


def create_vector_store(chunks, embedding_model):

    persist_directory = "vector_store"

    # Remove old database if it exists
    if os.path.exists(persist_directory):
        print("Removing old vector database...")
        shutil.rmtree(persist_directory)

    print("Creating new vector database...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    return vector_store