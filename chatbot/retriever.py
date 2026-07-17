# Import the Sentence Transformer class
from sentence_transformers import SentenceTransformer
# Import ChromaDB
import chromadb
# Import reranker
from chatbot.reranker import rerank_chunks
# Paths
from chatbot.paths import VECTOR_DB_PATH
import os
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
import re

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# Retrieve more candidates
TOP_K = 15

# Connect to ChromaDB
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_or_create_collection(
    name="employee_handbook"
)
# Load all stored chunks once
all_data = collection.get(
    include=["documents", "metadatas"]
)

ALL_DOCUMENTS = all_data["documents"]
ALL_METADATA = all_data["metadatas"]

# Build BM25 index
tokenized_docs = [
    doc.lower().split()
    for doc in ALL_DOCUMENTS
]

bm25 = BM25Okapi(tokenized_docs)
def detect_document(query):

    query = query.lower()

    results = collection.get(include=["metadatas"])

    sources = {
        meta["source"]
        for meta in results["metadatas"]
    }

    for source in sources:

        clean = (
            source.lower()
            .replace(".pdf", "")
            .replace("_", " ")
        )

        if clean in query:
            return source

    return None

def retrieve_context(query, source=None):
    detected = detect_document(query)

    if detected:
      source = detected
    # Improve semantic retrieval a little
    enhanced_query = (
       query
       .strip()
       .replace("\n", " ")
    )
    query_tokens = re.findall(
       r"\w+",
       enhanced_query.lower()
    )

    keyword_scores = bm25.get_scores(query_tokens)

    top_keyword_ids = sorted(
       range(len(keyword_scores)),
       key=lambda i: keyword_scores[i],
       reverse=True
    )[:10]

    query_embedding = embedding_model.encode(enhanced_query)

    if source is not None:

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=TOP_K,
            where={"source": source},
            include=["documents", "metadatas"]
        )

    else:

        results = collection.query(
           query_embeddings=[query_embedding.tolist()],
           n_results=TOP_K,
           include=[
           "documents",
            "metadatas",
            "distances"
        ]
    )
    retrieved_chunks = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]
    # ----------------------------------------
    # BM25 Results
    # ----------------------------------------

    bm25_chunks = [
        ALL_DOCUMENTS[i]
        for i in top_keyword_ids
    ]

    bm25_metadata = [
       ALL_METADATA[i]
       for i in top_keyword_ids
    ]

    # Merge Vector + BM25 Results
    combined = []
    seen = set()

    # Add vector search results
    for chunk, meta in zip(retrieved_chunks, retrieved_metadata):

       if chunk not in seen:
        combined.append((chunk, meta))
        seen.add(chunk)

    # Add BM25 results
    for chunk, meta in zip(bm25_chunks, bm25_metadata):

       if chunk not in seen:
        combined.append((chunk, meta))
        seen.add(chunk)

    # Cross Encoder scoring

    pairs = [
       (enhanced_query, chunk)
       for chunk, _ in combined
    ]

    scores = reranker_model.predict(pairs)
    best_score = max(scores)
    print(f"Best CrossEncoder Score: {best_score:.3f}")

    print(f"\nBest Retrieval Score: {best_score}\n")
    print("Cross Encoder Scores")

    for (chunk, meta), score in zip(combined, scores):
     print(score, meta)

    scored_results = sorted(
       zip(combined, scores),
       key=lambda x: x[1],
       reverse=True
    )
    print("\nBEST CHUNK")
    print(scored_results[0][0][0][:800])
    print("Score:", scored_results[0][1])
    # If even the best chunk is not relevant,
    # return no context.
    if best_score < 0:

      print("No sufficiently relevant document found.")

      return "", []

    # Reject irrelevant retrievals
    THRESHOLD = 0.35

    ranked_pairs = [
      item[0]
      for item in scored_results
      if item[1] >= THRESHOLD
    ][:5]

    retrieved_chunks = [
    pair[0]
    for pair in ranked_pairs
    ]

    retrieved_metadata = [
    pair[1]
    for pair in ranked_pairs
    ]
    # Remove duplicate citations
    cleaned_metadata = []
    seen = set()

    for item in retrieved_metadata:

        source_name = item.get("source")
        page = item.get("page_label")

        key = (source_name, page)

        if key not in seen:
            seen.add(key)

            cleaned_metadata.append(
                {
                    "source": source_name,
                    "page": page
                }
            )

    if not ranked_pairs:

       print("No relevant chunks after reranking.")

       return "", []

    formatted_chunks = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

       formatted_chunks.append(
          f"""
    ==================== DOCUMENT {index} ====================

    {chunk}

    ----------------------------------------------------
    """
       )

    context = "\n".join(formatted_chunks)

    print("\n" + "=" * 80)
    print("RETRIEVED CONTEXT")
    print("=" * 80)
    print(context)
    print("=" * 80 + "\n")

    return context, cleaned_metadata