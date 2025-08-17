import fitz
import urllib
import re
import html
import unicodedata
import numpy as np
import os
import dotenv
import requests
from nlp.main import nlp

dotenv.load_dotenv()

def get_embeddings(chunks:list):
    if not chunks:
        raise ValueError("Chunks cannot be empty")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv("JINAAI_API_KEY")}"
    }
    data =   {
    "model": os.getenv("JINA_EMBEDDING_MODEL"), #jina-embeddings-v3
    "input": chunks
    }
    response = requests.post(url=os.getenv("JINA_EMBEDDING_URL"), json=data, headers=headers)
    resdata = response.json()['data']
    return [emb['embedding'] for emb in resdata]



def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def text_to_chunks(text, max_tokens=100, overlap=10)->list[str]:
    """
    Splits text into chunks with semantic overlap.
        :param text: The text to split
        :param max_tokens: Max tokens per chunk
        :param overlap: Tokens to overlap between chunks
        :return: List of text chunks
    """
    doc = nlp(text)
    chunks = []
    current_chunk = []
    total_tokens = 0

    for sent in doc.sents:
        sent_tokens = len(sent)
        # If adding this sentence would exceed the max chunk size
        if total_tokens + sent_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            # Keep the overlap from the last chunk
            current_chunk = current_chunk[-overlap:]
            total_tokens = len(current_chunk)

        current_chunk.append(sent.text)
        total_tokens += sent_tokens

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def is_url(data):
    try:
        result = urllib.parse.urlparse(data)
        return all([result.scheme, result.netloc])
    except:
        return False

def pdf_to_text(file_path:str)->str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


