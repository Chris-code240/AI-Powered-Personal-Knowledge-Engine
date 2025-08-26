from typing import List, Dict
from sqlalchemy.orm import Session
from ..db.connection import session_connection
from ..db.models import Chunk, Tag
from .vector_retriever import VectorRetriever

class HybridRetriever:
    def __init__(self, collection_name: str = "default_collection"):
        self.conn = session_connection()
        self.vector_retriever = VectorRetriever(collection_name=collection_name)

    def add_chunks(self, chunks: List[str], data_id: int, metadatas: List[Dict] = None, ids: List[str] = None):
        """Add chunks to both SQL DB and vector DB."""
        with self.conn as session:
            for c in chunks:
                session.add(Chunk(data_id=data_id, text=c))
            session.commit()
        self.vector_retriever.add_chunks(chunks, metadatas=metadatas, ids=ids)

    def add_tags(self, tags: List[Dict], data_id: int):
        """tags: list of dicts with {name, label}"""
        with self.conn as session:
            for t in tags:
                session.add(Tag(data_id=data_id, name=t["name"], label=t["label"]))
            session.commit()

    def retrieve(self, query: str, top_k: int = 5, vector_weight: float = 0.6, keyword_weight: float = 0.3, tag_weight: float = 0.1) -> List[Dict]:
        """
        Hybrid retrieval:
        1. Tag match (tag_weight)
        2. Keyword text match in chunks (keyword_weight)
        3. Vector similarity search (vector_weight)
        Weighted combination for ranking.
        """
        with self.conn as session:
            # Step 1: match tags
            tag_matches = session.query(Tag).filter(Tag.name.ilike(f"%{query}%")).all()
            tag_results = [{"source": t.data.data_path or "", "text": t.name, "score": tag_weight, **t.get()} for t in tag_matches]

            # Step 2: match keyword in chunks
            chunk_matches = session.query(Chunk).filter(Chunk.text.ilike(f"%{query}%")).all()
            chunk_results = [{"source": c.data.data_path or "", "text": c.text, "score": keyword_weight, **c.get()} for c in chunk_matches]

            # Step 3: vector search
            vector_results = self.vector_retriever.retrieve(query, top_k=top_k)
            for v in vector_results:
                v["source"] = "vector"
                v["score"] = (1 - v["score"]) * vector_weight  # invert distance into similarity

            # Combine all results
            combined = tag_results + chunk_results + vector_results

            # Sort by score (descending)
            combined.sort(key=lambda x: x["score"], reverse=True)

            return combined[:top_k]
