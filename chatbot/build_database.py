# Import the PdfReader class
from pypdf import PdfReader
# Import the text splitter from LangChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Import the Sentence Transformer class
from sentence_transformers import SentenceTransformer
# Import the ChromaDB client
import chromadb

#document loader and reader for the PDF file
#path to the PDF file
pdf_path="data/Employee_Handbook.pdf"
# Create a PdfReader object
reader=PdfReader(pdf_path)
# Get all the pages from the PDF
pages = reader.pages

#Extracting text
# Store the complete document text
document_text = ""
# Read every page in the PDF
for page_number, page in enumerate(pages, start=1):
    #Display the current page number
    print(f"\n========== Page {page_number} ==========\n")
    # Extract text
    text = page.extract_text()
    # Add page text to the complete document
    document_text += text + "\n"
    print(text)
# Display the complete document
#print(document_text)

# Number of characters in each chunk
#chunk_size = 200
# Number of overlapping characters between consecutive chunks
#chunk_overlap = 50
# Store all chunks
#chunks = []
# Create chunks from the complete document
#for i in range(0, len(document_text), chunk_size):
    # Create one chunk from the document using string slicing
    #chunk = document_text[i : i + chunk_size]
    # Add the current chunk to the list of chunks
    #chunks.append(chunk)
# Display all the chunks
#print(chunks)
# Create a text splitter object

#Chunking
# Number of characters in each chunk
chunk_size = 200
# Number of overlapping characters between consecutive chunks
chunk_overlap = 50
# Create a text splitter object
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
# Split the complete document into chunks
chunks = text_splitter.split_text(document_text)
# Display the total number of chunks created
print(len(chunks))
# Display each chunk separately
for chunk_number, chunk in enumerate(chunks, start=1):
    # Display the chunk number
    print(f"\n========== Chunk {chunk_number} ==========\n")
    # Display the chunk
    print(chunk)

# Load the sentence transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# Convert all chunks into embedding vectors
embeddings = embedding_model.encode(chunks)
# Display the number of embedding vectors
print(f"\nTotal Embeddings Created: {len(embeddings)}")
# Display the dimension of one embedding vector
print(f"Embedding Dimension: {len(embeddings[0])}")
# Display the first embedding vector
#print(embeddings[0])

# Create a ChromaDB client
client = chromadb.PersistentClient(path="vector_db")
# Delete the existing collection if it already exists
try:
    client.delete_collection(name="employee_handbook")
    print("Existing collection deleted.")
except:
    pass
# Create a new collection
collection = client.get_or_create_collection(
    name="employee_handbook"
)
# Store the chunks and embeddings in the collection
collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist()
)
# Display a success message
print("\nEmbeddings successfully stored in ChromaDB!")