from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, LargeBinary, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)   # pdf, audio, video, etc.
    data_path = Column(String(500), nullable=True)  # path or URL
    file_content = Column(LargeBinary, nullable=True)  # optional: actual file
    value = Column(Text, nullable=True)  # extracted raw text
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    chunks = relationship("Chunk", back_populates="data", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="data", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(Integer, ForeignKey("data.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)

    data = relationship("Data", back_populates="chunks")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(Integer, ForeignKey("data.id", ondelete="CASCADE"))
    name = Column(String(200), nullable=False)   # entity text
    label = Column(String(100), nullable=False)  # entity type (PERSON, ORG, etc.)

    data = relationship("Data", back_populates="tags")
