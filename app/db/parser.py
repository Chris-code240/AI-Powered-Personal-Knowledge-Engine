from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Optional
import uuid
import datetime
import mimetypes
import re
from urllib.parse import urlparse
import pathlib

def is_url(url: str) -> bool:
    """
    Checks if a given string is a valid URL.

    This function first attempts to parse the URL to ensure it has a scheme
    (like http or https) and a network location (like a domain name).
    It then uses a regular expression for a more comprehensive validation
    of the URL's format.

    Args:
        url (str): The string to be validated as a URL.

    Returns:
        bool: True if the string is a valid URL, False otherwise.
    """
    # A common and robust regular expression for URL validation.
    # It checks for a protocol (http/https), an optional subdomain,
    # a domain name, a top-level domain, and optional path/query/fragment.
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    try:
        # urlparse is used to check for a valid scheme and netloc.
        # This helps catch simple cases before regex.
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        # Use the regex to validate the full string format.
        return re.match(url_regex, url) is not None
    except ValueError:
        # Handles potential errors during parsing.
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

DATA_TYPES = ("audio","video", "image", "pdf", "bookmark", "code-repo", "text")


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



    
    @field_validator("type")
    def validate_type(cls, value):
        if value not in DATA_TYPES:
            raise ValueError(f"Data Type '{value}' not supported")
        return value
    
    @model_validator(mode="after")
    def validate_model(self):
        if self.type == "bookmark":
            if not is_url(self.data_path):
                raise ValueError(f"Data path:url '{self.data_path}'")
        elif self.type == "text":
            if len(self.value) < 1:
                raise ValueError("Text must have a value")
            self.data_path = "unknown"
        else:
            if not pathlib.Path(self.data_path).is_file():
                 raise ValueError(f"Data path '{self.data_path}' is invalid URL")
        return self
            
    






