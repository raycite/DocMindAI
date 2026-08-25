import streamlit as st
from pathlib import Path
import shutil

from indexer import build_vector_store
from retriever import retrieve_documents
from llm import get_llm
from qa import generate_answer


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="DocMindAI",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

UPLOADS_FOLDER = Path("uploads")
VECTOR_STORE_FOLDER = Path("vector_store")

UPLOADS_FOLDER.mkdir(exist_ok=True)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "uploader_version" not in st.session_state:
    st.session_state.uploader_version = 0

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def get_uploaded_documents():
    """Return all PDF files currently in the uploads folder."""

    return sorted(
        [
            file
            for file in UPLOADS_FOLDER.iterdir()
            if file.is_file() and file.suffix.lower() == ".pdf"
        ],
        key=lambda x: x.name.lower()
    )


def delete_document(file_path):
    """Delete a document from the uploads folder."""

    if file_path.exists():
        file_path.unlink()


def clear_vector_store():
    """Remove the existing vector database."""

    if VECTOR_STORE_FOLDER.exists():
        shutil.rmtree(VECTOR_STORE_FOLDER)


def rebuild_vector_store():
    """Build a fresh vector database from current uploads."""

    with st.spinner(
        "Processing documents and rebuilding the vector database..."
    ):

        vector_store = build_vector_store()

        st.session_state.vector_store = vector_store
        st.session_state.llm = get_llm()
        st.session_state.documents_processed = True


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📄 DocMindAI")
st.subheader("AI Document Intelligence Assistant")

st.write(
    "Upload your documents and ask questions about their content."
)


# --------------------------------------------------
# Current documents
# --------------------------------------------------

current_documents = get_uploaded_documents()

st.subheader("📚 Your Documents")

if current_documents:

    st.write(
        f"You currently have **{len(current_documents)}/5 documents**."
    )

    for document in current_documents:

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"📄 {document.name}")

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{document.name}"
            ):

                delete_document(document)

                # The vector database is now outdated
                st.session_state.vector_store = None
                st.session_state.documents_processed = False

                # Force a fresh uploader widget
                st.session_state.uploader_version += 1

                st.success(
                    f"{document.name} deleted successfully."
                )

                st.rerun()

else:

    st.info(
        "No documents uploaded yet. Upload up to 5 PDF documents below."
    )


# --------------------------------------------------
# Upload documents
# --------------------------------------------------

st.divider()

st.subheader("📤 Add Documents")

remaining_slots = 5 - len(current_documents)

if remaining_slots > 0:

    uploaded_files = st.file_uploader(
        f"Upload PDF documents ({remaining_slots} slot(s) available)",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.uploader_version}"
    )

    if uploaded_files:

        # Prevent uploading more than available spaces
        if len(uploaded_files) > remaining_slots:

            st.error(
                f"You can only add {remaining_slots} more document(s)."
            )

        else:

            # --------------------------------------------------
            # First real user upload
            #
            # Remove old development/test documents.
            # A marker file prevents this from happening again.
            # --------------------------------------------------

            marker_file = UPLOADS_FOLDER / ".user_documents_initialized"

            if not marker_file.exists():

                # Remove existing PDFs
                for old_file in UPLOADS_FOLDER.glob("*.pdf"):
                    old_file.unlink()

                # Create marker
                marker_file.touch()

                current_documents = []


            # --------------------------------------------------
            # Save new documents
            # --------------------------------------------------

            saved_count = 0

            for file in uploaded_files:

                file_path = UPLOADS_FOLDER / file.name

                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                saved_count += 1


            if saved_count > 0:

                st.success(
                    f"{saved_count} document(s) added successfully."
                )

                # Vector database is now outdated
                st.session_state.vector_store = None
                st.session_state.documents_processed = False

                # Refresh uploader
                st.session_state.uploader_version += 1

                st.rerun()

else:

    st.warning(
        "You have reached the maximum of 5 documents. "
        "Delete a document before adding another."
    )


# --------------------------------------------------
# Process Documents
# --------------------------------------------------

st.divider()

st.subheader("⚙️ Document Processing")

current_documents = get_uploaded_documents()

if current_documents:

    if st.button(
        "🔄 Process / Rebuild Documents",
        use_container_width=True
    ):

        try:

            rebuild_vector_store()

            st.success(
                "Documents processed successfully! "
                "DocMindAI is ready for questions."
            )

        except Exception as e:

            st.error(
                f"An error occurred while processing documents: {e}"
            )

else:

    st.info(
        "Upload at least one document before processing."
    )


# --------------------------------------------------
# Question section
# --------------------------------------------------

st.divider()

st.subheader("💬 Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="e.g. What are this person's research interests?"
)


if st.button("🔎 Ask Question", use_container_width=True):

    if not current_documents:

        st.warning(
            "Please upload and process your documents first."
        )

    elif st.session_state.vector_store is None:

        st.warning(
            "Your documents have changed. "
            "Please click 'Process / Rebuild Documents' first."
        )

    elif st.session_state.llm is None:

        st.warning(
            "The AI model is not ready. "
            "Please process the documents again."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                # ------------------------------------------
                # Retrieve relevant documents
                # ------------------------------------------

                documents = retrieve_documents(
                    st.session_state.vector_store,
                    question
                )


                # ------------------------------------------
                # Generate answer
                # ------------------------------------------

                response = generate_answer(
                    st.session_state.llm,
                    documents,
                    question
                )


                # ------------------------------------------
                # Answer
                # ------------------------------------------

                st.subheader("Answer")

                st.write(
                    response["answer"]
                )


                # ------------------------------------------
                # Sources
                # ------------------------------------------

                st.subheader("Sources")

                if response["sources"]:

                    for source in response["sources"]:

                        st.write(
                            f"- {source['file']} "
                            f"(Page {source['page']})"
                        )

                else:

                    st.write(
                        "No specific sources were returned."
                    )


            except Exception as e:

                st.error(
                    f"An error occurred while answering: {e}"
                )