from pydantic import BaseModel,ConfigDict
from typing import Literal
from src.process_media.common import Vector2IntSchema

type VideoFormat=Literal["mp4","webm"]

class FfmpegSettings(BaseModel):
    model_config = ConfigDict(strict=True)

    vf:str|None=None
    vcodec:str|None=None
    acodec:str|None=None

class VideoOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucket_name: str
    object_name: str
    mime_type: str|None=None
    upload_mime_type:str
    convert_to: VideoFormat|None=None
    bitrate: str|None=None
    limit_resolution: Vector2IntSchema|None=None
    max_size: int|None=None
    ffmpeg_settings:FfmpegSettings|None=None
    describe:bool=False
    prompt:str="briefly describe the video, be short and to the point"
    prompt_max_tokens: int=64
    skip_upload: bool=False

    