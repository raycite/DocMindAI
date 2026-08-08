from loaders import load_documents
from chunker import split_documents
from embeddings import get_embedding_model
from vector_store import create_vector_store


def build_vector_store():
    """
    Load PDFs from the uploads folder, split them into chunks,
    generate embeddings, and create/load the vector database.
    """

    print("Loading document...")

    documents = load_documents("uploads")

    print(f"Original pages: {len(documents)}")

    print("Splitting document...")

    chunks = split_documents(documents)

    print(f"Number of chunks: {len(chunks)}")

    print("Loading embedding model...")

    embedding_model = get_embedding_model()

    print("Creating vector database...")

    vector_store = create_vector_store(
        chunks,
        embedding_model
    )

    print("Vector database ready!")

    return vector_store