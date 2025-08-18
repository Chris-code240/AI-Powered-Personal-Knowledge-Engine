from celery import shared_task
from db.parser import Tag, Data, get_media_type, is_url
from nlp.main import get_ner_tags
from db.utils import text_to_chunks, clean_text, pdf_to_text
from ingest.utils import audio_to_text, transcribe_video
from db.vector_store import add_chunks  # wraps chroma

@shared_task
def add_data_task(data_dict):
    """Background task to process and embed data."""

    try: 
        data = Data(**data_dict)

        # Step 1: Extract raw text depending on type
        if data.type == "audio":
            if get_media_type(data.data_path) != "audio":
                raise ValueError("Invalid media type for audio")
            # TODO: audio_to_text
            data.value = audio_to_text(data.data_path)

        elif data.type == "pdf":
            if get_media_type(data.data_path) != "document":
                raise ValueError("Invalid media type for PDF")
            data.value = pdf_to_text(data.data_path)

        elif data.type == "video":
            if get_media_type(data.data_path) != "video":
                raise ValueError("Invalid media type for video")
            # TODO: extract audio + transcribe
            data.value = transcribe_video(data.data_path)

        elif data.type == "image":
            if get_media_type(data.data_path) != "image":
                raise ValueError("Invalid media type for image")
            # TODO: OCR
            data.value = "<text_from_image>"

        elif data.type == "bookmark":
            if not is_url(data.data_path):
                raise ValueError("Invalid URL for bookmark")
            # TODO: scrape web page
            data.value = "<scraped_webpage_text>"

        elif data.type == "code-repo":
            if not is_url(data.data_path):
                raise ValueError("Invalid URL for repo")
            # TODO: clone repo + extract info
            data.value = "<repo_code_and_docs>"

        else:
            raise ValueError(f"Unsupported data type: {data.type}")

        # Step 2: Clean + chunk
        text = clean_text(data.value)
        chunks = text_to_chunks(text)
        data.chunks = chunks

        # Step 3: NER tagging
        ner_tags = get_ner_tags(text)
        data.tags = [Tag(name=tag['name'], label=tag['label']) for tag in ner_tags]

        # Step 4: Store chunks into vector DB (Chroma will embed automatically)
        add_chunks(data_id=data.id, chunks=chunks)

        # Step 5: (Optional) Save metadata to Postgres/MySQL
        # e.g., store tags, data metadata, etc.

        return {"data_id": data.id, "chunks_added": len(chunks), "tags": [t.name for t in data.tags]}
    except Exception as e:
        print(e)
        return None