from typing import List, Dict
from chromadb import Client
from chromadb.utils import embedding_functions
from ..db.vector_store import client,embedding_fn, collection
class VectorRetriever:
    def __init__(self, collection_name: str, embedding_model: str = "all-MiniLM-L6-v2"):
        self.client = client
        self.embedding_fn = embedding_fn
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
        self.collection.add(documents=chunks, metadatas=metadatas, ids=ids)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return [
            {"text": doc, "score": score, "metadata": meta}
            for doc, score, meta in zip(results["documents"][0], results["distances"][0], results["metadatas"][0])
        ]
