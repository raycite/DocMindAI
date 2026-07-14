from loaders import load_pdf
from chunker import split_documents
from embeddings import get_embedding_model
from vector_store import create_vector_store


pdf_path = "uploads/sample.pdf"


# 1. Load document
documents = load_pdf(pdf_path)

print("Original pages:", len(documents))


# 2. Split document into chunks
chunks = split_documents(documents)

print("Number of chunks:", len(chunks))


# 3. Load embedding model
print("Loading embedding model...")

embedding_model = get_embedding_model()


# 4. Create vector database
print("Creating vector database...")

vector_store = create_vector_store(
    chunks,
    embedding_model
)


print("Vector database created successfully!")