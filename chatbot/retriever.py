# Import the Sentence Transformer class
from sentence_transformers import SentenceTransformer
# Import the ChromaDB client
import chromadb

# Load the same embedding model used while building the database
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# Number of most relevant chunks to retrieve
TOP_K = 2
# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(path="vector_db")
# Open the existing collection
collection = client.get_collection(
    name="employee_handbook"
)

# main function app.py will call this function to retrieve relevant context for a user query
# Retrieve relevant context for a user query
def retrieve_context(query, source=None):
    # Convert the user question into an embedding vector
    query_embedding = embedding_model.encode(query)
    # Check whether the user has selected a specific PDF
    #FILTERING METADATA BASED ON SOURCE
    if source is not None:
        # Search the vector database using the query embedding
        results = collection.query(
        # Convert the query embedding from a NumPy array into a Python list
        # and send it to ChromaDB for similarity search
        query_embeddings=[query_embedding.tolist()],
        # Retrieve only the TOP_K most relevant chunks
        n_results=TOP_K,
        # Filter the search so that only chunks whose metadata
        # contains the selected PDF name are searched
        where={"source": source},
        # Return both the retrieved document chunks and their metadata
        include=["documents", "metadatas"]
    )
    # If no specific PDF is selected
    else:
        # Search across all PDFs stored in the vector database
        results = collection.query(
        # Convert the query embedding into a Python list
        query_embeddings=[query_embedding.tolist()],
        # Retrieve only the TOP_K most relevant chunks
        n_results=TOP_K,
        # Return both the retrieved document chunks
        # and their corresponding metadata
        include=["documents", "metadatas"]
    )
    
    # Extract the retrieved chunks
    retrieved_chunks = results["documents"][0]
    # Extract the metadata of the retrieved chunks
    retrieved_metadata = results["metadatas"][0]
    # Combine all chunks into one context
    context = "\n".join(retrieved_chunks)
    # Return both the context and metadata
    return context, retrieved_metadata