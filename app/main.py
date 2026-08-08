from indexer import build_vector_store
from chatbot import chat


def main():

    vector_store = build_vector_store()

    chat(vector_store)


if __name__ == "__main__":
    main()