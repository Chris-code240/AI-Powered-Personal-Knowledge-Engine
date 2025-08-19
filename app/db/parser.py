from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Optional
import uuid
import datetime
import mimetypes
import re
import urllib.parse
import pathlib
import fitz
def is_url(data):
    try:
        result = urllib.parse.urlparse(data)
        return all([result.scheme, result.netloc])
    except:
        return False
def get_media_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type:
        if mime_type.startswith('audio'):
            return "audio"
        elif mime_type.startswith('video'):
            return "video"
        elif mime_type.startswith('image'):
            return "image"
        else:
            return "document"
    return "unknown"

DATA_TYPES = ("audio","video", "image", "pdf", "bookmark", "code-repo")


class Tag(BaseModel):
    id:uuid.UUID = uuid.uuid1
    name:str
    label:str
class Chunk(BaseModel):
    id:uuid.UUID  = uuid.uuid3
    raw_text:str
    vector:str

class Data(BaseModel):
    metadata_:dict = {"title":""}
    type: str
    data_path: str
    value: Optional[Any] = None # Added a default value
    tags: list[Tag] = []
    chunks: list[str] = []
    has_been_indexed: bool = False

# Now, this instance will be valid


    
    @field_validator("type")
    def validate_type(cls, value):
        if value not in DATA_TYPES:
            raise ValueError(f"Data Type '{value}' not supported")
        return value
    @field_validator("data_path")
    def validate_data_path(cls, value):
        if pathlib.Path(value).is_file():
            return value
        raise ValueError(f"Data path '{value}' invalid")
    






