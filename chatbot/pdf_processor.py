# Load PDF files
from langchain_community.document_loaders import PyPDFLoader
# Split long text into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Create embeddings for text
from langchain_openai import OpenAIEmbeddings
# Store embeddings in ChromaDB
from langchain_chroma import Chroma

# Create embedding model
def create_embeddings():
    # Create OpenAI embedding model
    embeddings = OpenAIEmbeddings()
    # Return embedding model
    return embeddings

# Create ChromaDB vector database
def create_vector_store(chunks):
    # Create embedding model
    embeddings = create_embeddings()
    # Create ChromaDB and store the chunks
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    # Return the vector database
    return vector_store

# Complete PDF processing pipeline
def ingest_pdf(pdf_path):
    # Load and split the PDF into chunks
    chunks = process_pdf(pdf_path)
    # Create ChromaDB vector store
    vector_store = create_vector_store(chunks)
    # Return the vector store
    return vector_store

# Load PDF and return LangChain documents
def load_pdf(pdf_path):
    # Create a PDF loader
    loader = PyPDFLoader(pdf_path)
    # Read the PDF
    documents = loader.load()
    return documents

# Split documents into smaller chunks
def split_documents(documents):
    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    # Return chunks
    return chunks

# Process PDF and return chunks
def process_pdf(pdf_path):
    # Load the PDF
    documents = load_pdf(pdf_path)
    # Split the documents into chunks
    chunks = split_documents(documents)
    # Return chunks
    return chunks