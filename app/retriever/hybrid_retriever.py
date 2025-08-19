from typing import List, Dict
from sqlalchemy.orm import Session
from ..db.connection import session_connection
from ..db.models import Chunk, Tag

class HybridRetriever:
    def __init__(self):
        self.conn = session_connection()

    def add_chunks(self, chunks: List[str], data_id: int):
        with self.conn as session:
            for c in chunks:
                session.add(Chunk(data_id=data_id, text=c))
            session.commit()

    def add_tags(self, tags: List[Dict], data_id: int):
        """tags: list of dicts with {name, label}"""
        with self.conn as session:
            for t in tags:
                session.add(Tag(data_id=data_id, name=t["name"], label=t["label"]))
            session.commit()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Hybrid retrieval:
        1. Tag match (NER style, e.g. PERSON, ORG)
        2. Keyword text match in chunks
        (later we can extend with embeddings)
        """
        with self.conn as session:
            # Step 1: match tags
            tag_matches = (
                session.query(Tag)
                .filter(Tag.name.ilike(f"%{query}%"))
                .all()
            )

            # Step 2: match chunk text
            chunk_matches = (
                session.query(Chunk)
                .filter(Chunk.text.ilike(f"%{query}%"))
                .all()
            )

            # Merge results (prioritize tags, then chunks)
            results = []

            for t in tag_matches:
                results.append({"source": "tag", **t.get()})

            for c in chunk_matches:
                results.append({"source": "chunk", **c.get()})

            # Return top_k (naive ordering: tags first, then chunks)
            return results[:top_k]
