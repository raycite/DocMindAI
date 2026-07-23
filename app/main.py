from indexer import build_vector_store
from chatbot import chat


def main():

    pdf_path = "uploads/sample.pdf"

    vector_store = build_vector_store(pdf_path)

    chat(vector_store)


if __name__ == "__main__":
    main()