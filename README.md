# DocMindAI 📄🤖

DocMindAI is an AI-powered document question-answering application that allows users to upload PDF documents and ask questions about their content. It uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from documents and generate context-based answers.

## Features

* Upload and process PDF documents
* Automatically split documents into searchable chunks
* Generate document embeddings using Hugging Face models
* Store and retrieve embeddings with ChromaDB
* Ask natural-language questions about uploaded documents
* Retrieve relevant document sections using semantic search
* Generate answers using a locally running LLM through Ollama
* Display source documents and page references for retrieved information

## Tech Stack

* **Python**
* **Streamlit** – User interface
* **LangChain** – RAG pipeline and document processing
* **ChromaDB** – Vector database
* **Hugging Face Sentence Transformers** – Document embeddings
* **Ollama / Llama 3.1** – Local language model
* **PyPDFLoader** – PDF processing

## How It Works

1. A user uploads a PDF document.
2. The document is loaded and divided into smaller text chunks.
3. Embeddings are generated for the chunks.
4. The embeddings are stored in ChromaDB.
5. When a question is asked, relevant chunks are retrieved using semantic search.
6. The retrieved context is passed to the LLM to generate an answer based on the document.

## Run Locally

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Make sure **Ollama** is installed and pull the model:

```bash
ollama pull llama3.1
```

Run the application:

```bash
streamlit run streamlit_app.py
```

## Project Goal

DocMindAI was developed as a practical exploration of **Generative AI, Retrieval-Augmented Generation, semantic search, vector databases, and local Large Language Models**. The goal is to make it easier to interact with and extract useful information from documents using natural-language questions.
