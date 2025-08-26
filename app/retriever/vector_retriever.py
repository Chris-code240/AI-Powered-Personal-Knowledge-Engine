from typing import List, Dict, Optional
from chromadb import Client
from chromadb.utils import embedding_functions
from ..db.vector_store import client, embedding_fn
from ..db.models import Data
from ..db.connection import session_connection


class VectorRetriever:
    def __init__(self, collection_name: str = "data_chunks", embedding_model: str = "all-MiniLM-L6-v2"):
        self.client: Client = client
        self.embedding_fn = embedding_fn
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(
        self, 
        chunks: List[str], 
        metadatas: Optional[List[Dict]] = None, 
        ids: Optional[List[str]] = None
    ):
        """Add chunks to the vector store."""
        self.collection.add(
            documents=chunks, 
            metadatas=metadatas or [{} for _ in chunks], 
            ids=ids
        )

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve the most relevant documents based on semantic similarity."""
        results = self.collection.query(query_texts=[query], n_results=top_k)
        r = []
        with session_connection() as session:
            for doc, score, meta in zip(
                    results["documents"][0],
                    results["distances"][0],
                    results["metadatas"][0]
                ):
                meta = meta or {'data_id':-1}
                data = session.query(Data).filter(
                        Data.id == meta.get('data_id')
                ).first()
                r.append({
                    "text": doc,
                    "score": score,
                    "metadata": meta,
                    "data_path":data.data_path if data is not None else ""
                })
            return r

q = VectorRetriever(collection_name="data_chunks")

print(q.retrieve("What is recursion"))