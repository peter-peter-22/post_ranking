from dataclasses import dataclass

@dataclass
class UploadResponse:
    object_name:str
    bucket_name:str
    mime_type:str
    label:str|None=None