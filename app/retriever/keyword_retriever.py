###########################
# I wwant to let only the  #
# Vector Retriver to handle#
#  the job
###########################
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..db.connection import session_connection
from ..db.models import Chunk, Tag


class KeywordRetriever:
    def __init__(self):
        self.conn = session_connection()

    def add_chunks(self, chunks: List[str], data_id: int):
        with self.conn as session:
            for c in chunks:
                session.add(Chunk(data_id=data_id, text=c))
            session.commit()

    def add_tags(self, tags: List[Dict], data_id: int):
        """
        tags = [{"name": "Chris", "label": "PERSON"}, {"name": "USA", "label": "ORG"}]
        """
        with self.conn as session:
            for t in tags:
                session.add(Tag(data_id=data_id, name=t["name"], label=t["label"]))
            session.commit()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """ 
        Retrieve chunks if query matches chunk text or related tag name/label 
        """
        with self.conn as session:
            # match against chunk text
            chunk_matches = session.query(Chunk).filter(
                Chunk.text.ilike(f"%{query}%")
            ).limit(top_k).all()

            # match against tags
            tag_matches = session.query(Tag).filter(
                or_(
                    Tag.name.ilike(f"%{query}%"),
                    Tag.label.ilike(f"%{query}%")
                )
            ).limit(top_k).all()

            results = []

            for c in chunk_matches:
                try:
                    results.append({
                        "id": c.id,
                        "text": c.text,
                        "data_id": c.data_id,
                        "match_type": "chunk",
                        "data_path":c.data.data_path
                    })
                except Exception:
                    continue

            for t in tag_matches:
                try:
                    results.append({
                        "id": t.id,
                        "name": t.name,
                        "label": t.label,
                        "data_id": t.data_id,
                        "match_type": "tag",
                        "data_path":t.data.data_path
                    })
                except Exception as e:
                    continue

            return results[:top_k]
        

