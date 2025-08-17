import chromadb
from chromadb.utils import embedding_functions

# Init Chroma client (persistent mode saves in ./chroma_db)
client = chromadb.PersistentClient(path="./chroma_db")

# Use sentence-transformers as embedding model
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or get a collection
collection = client.get_or_create_collection(
    name="data_chunks",
    embedding_function=embedding_fn
)

def add_chunks(data_id: str, chunks: list[str]):
    """
    Store chunks with embeddings into Chroma
    """
    collection.add(
        ids=[f"{data_id}_{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[{"data_id": data_id, "chunk_index": i} for i in range(len(chunks))]
    )

def query_chunks(query: str, n_results=5):
    """
    Semantic search over stored chunks
    """
    results = collection.query(query_texts=[query], n_results=n_results)
    return results
