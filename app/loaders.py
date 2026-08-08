from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):
    """
    Load all PDF documents from a folder.
    """

    documents = []

    pdf_files = Path(folder_path).glob("*.pdf")

    for pdf in pdf_files:

        print(f"Loading {pdf.name}...")

        loader = PyPDFLoader(str(pdf))

        docs = loader.load()

        documents.extend(docs)

    return documents