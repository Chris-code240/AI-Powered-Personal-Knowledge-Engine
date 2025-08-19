from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, create_engine, JSON, Boolean
)
import os
from sqlalchemy.orm import relationship, declarative_base
import datetime
import dotenv

dotenv.load_dotenv()
engine = create_engine(os.getenv("DB_URI"))

Base = declarative_base()

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)   # pdf, audio, video, etc.
    data_path = Column(String(500), nullable=True)  # path or URL
    value = Column(Text, nullable=True)  # extracted raw text
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    metadata_ = Column(JSON, default = {})
    has_been_indexed = Column(Boolean, default = False)
    chunks = relationship("Chunk", back_populates="data", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="data", cascade="all, delete-orphan")

    def get(self):
        return {"id":self.id, "type":self.type, "data_path":self.data_path, "chunks":self.chunks, "tags":self.tags, "created_at":self.created_at}


class Chunk(Base):
    __tablename__ = "chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(Integer, ForeignKey("data.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)

    data = relationship("Data", back_populates="chunks")

    def get(self):
        return {"id":self.id,"text":self.text, "data_id":self.data_id}



class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(Integer, ForeignKey("data.id", ondelete="CASCADE"))
    name = Column(String(200), nullable=False)   # entity text
    label = Column(String(100), nullable=False)  # entity type (PERSON, ORG, etc.)

    data = relationship("Data", back_populates="tags")

    def get(self):
        return {"id":self.id,"name":self.name,"label":self.label ,"data_id":self.data_id}
