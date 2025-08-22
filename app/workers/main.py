from celery import shared_task
from ..db.parser import Tag, Data, get_media_type, is_url
from ..nlp.main import get_ner_tags
from ..db.utils import text_to_chunks, clean_text, pdf_to_text
from ..ingest.utils import audio_to_text, transcribe_video
from ..db.vector_store import add_chunks  
from ..db.connection import session_connection
from ..db.models import Data as Data_in_DB, Tag as Tag_in_DB, Chunk as Chunk_in_DB
from ..ingest.web_scrapper import scrape_url
from .celery import app

@app.task
def process_bookmark(data_id: int, url: str):
    """Scrape bookmark content, clean, chunk, tag, and store in DB + vector store."""
    text, metadata = scrape_url(url)
    cleaned_text = clean_text(text)

    # Pipeline
    chunks = text_to_chunks(cleaned_text)
    ner_tags = get_ner_tags(cleaned_text)

    # Build ORM objects
    tag_objs = [Tag_in_DB(data_id=data_id, name=tag['name'], label=tag['label']) for tag in ner_tags]
    chunk_objs = [Chunk_in_DB(data_id=data_id, text=chunk_text) for chunk_text in chunks]

    with session_connection() as session:
        data = session.query(Data_in_DB).filter(Data_in_DB.id == data_id).first()
        if not data:
            raise ValueError(f"No data found with id={data_id}")

        data.value = cleaned_text
        session.add_all(tag_objs)
        session.add_all(chunk_objs)

    # Push chunks to vector store
    add_chunks(data_id=data_id, chunks=chunks)

    return {
        "data_id": data_id,
        "metadata": metadata,
        "tags": [t.name for t in tag_objs],
        "chunks_added": len(chunks),
    }


@app.task
def add_data_task(data_dict):
    """General ingestion task: extract, clean, chunk, tag, embed, and persist data."""
    data = Data(**data_dict)

    # ---- Step 1: Extract raw text depending on type ----
    if data.type == "audio":
        if get_media_type(data.data_path) != "audio":
            raise ValueError("Invalid media type for audio")
        data.value = audio_to_text(data.data_path)

    elif data.type == "pdf":
        if get_media_type(data.data_path) != "document":
            raise ValueError("Invalid media type for PDF")
        data.value = pdf_to_text(data.data_path)

    elif data.type == "video":
        if get_media_type(data.data_path) != "video":
            raise ValueError("Invalid media type for video")
        data.value = transcribe_video(data.data_path)

    elif data.type == "image":
        if get_media_type(data.data_path) != "image":
            raise ValueError("Invalid media type for image")
        data.value = "<text_from_image>"  # TODO: OCR

    elif data.type == "bookmark":
        if not is_url(data.data_path):
            raise ValueError("Invalid URL for bookmark")
        text_, metadata = scrape_url(data.data_path)
        data.value = text_
        data.metadata = metadata

    elif data.type == "code-repo":
        if not is_url(data.data_path):
            raise ValueError("Invalid URL for repo")
        data.value = "<repo_code_and_docs>"  # TODO: implement repo extraction

    else:
        raise ValueError(f"Unsupported data type: {data.type}")

    # ---- Step 2: Clean + chunk ----
    text = clean_text(data.value)
    chunks = text_to_chunks(text)
    data.chunks = chunks

    # ---- Step 3: NER tagging ----
    ner_tags = get_ner_tags(text)
    data.tags = [Tag(name=tag['name'], label=tag['label']) for tag in ner_tags]

    # ---- Step 4: Persist in DB ----
    data_orm = Data_in_DB(
        data_path=data.data_path,
        type=data.type,
        value=data.value,
        metadata=getattr(data, "metadata", {}),
    )

    chunk_objs = [Chunk_in_DB(data_id=data_orm.id, text=chunk) for chunk in chunks]
    tag_objs = [Tag_in_DB(data_id=data_orm.id, name=t.name, label=t.label) for t in data.tags]
    data_id_value = None
    with session_connection() as session:
        session.add(data_orm)
        session.flush()  # ensure `data_orm.id` is available
        data_id_value = data_orm.id
        for obj in chunk_objs + tag_objs:
            obj.data_id = data_id_value
        session.add_all(chunk_objs + tag_objs)

    # ---- Step 5: Push to vector store ----
        add_chunks(data_id=data_id_value, chunks=chunks)

    return {
        "data_id": str(data_id_value),
        "chunks_added": len(chunks),
        "tags": [t.name for t in data.tags],
    }



# print(type(data.model_dump()))

