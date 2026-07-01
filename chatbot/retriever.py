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
def retrieve_context(query):
    # Convert the user question into an embedding vector
    query_embedding = embedding_model.encode(query)
    # Search for the most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=TOP_K
    )
    # Extract the retrieved chunks
    retrieved_chunks = results["documents"][0]
    # Combine all chunks into one context
    context = "\n".join(retrieved_chunks)
    # Return the final context
    return context