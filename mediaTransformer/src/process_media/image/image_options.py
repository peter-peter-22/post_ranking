from pydantic import BaseModel,ConfigDict
from typing import Literal
from src.process_media.common import Vector2IntSchema,Vector2Int
from dataclasses import dataclass

type ImageFormat=Literal["WEBP","JPEG"]

@dataclass
class ImageVariant:
    convert_to: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2Int|None=None
    upload_mime_type:str|None=None

class ImageOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucket_name: str
    object_name: str
    mime_type: str|None=None
    upload_mime_type:str
    convert_to: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2IntSchema|None=None
    max_size: int|None=None
    describe: bool=False
    prompt:str="briefly describe the image, be short and to the point"
    prompt_max_tokens: int=32
    skip_upload: bool=False    