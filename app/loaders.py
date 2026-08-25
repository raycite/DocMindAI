from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


MAX_DOCUMENTS = 5


def load_documents(folder_path):
    """
    Load PDF documents from a folder.

    The system allows a maximum of 5 documents.
    """

    documents = []

    pdf_files = sorted(Path(folder_path).glob("*.pdf"))

    if len(pdf_files) == 0:
        print("No PDF documents found.")
        return documents

    if len(pdf_files) > MAX_DOCUMENTS:
        raise ValueError(
            f"Maximum of {MAX_DOCUMENTS} PDF documents allowed. "
            f"Found {len(pdf_files)}."
        )

    for pdf in pdf_files:

        print(f"Loading {pdf.name}...")

        loader = PyPDFLoader(str(pdf))

        docs = loader.load()

        documents.extend(docs)

    return documents