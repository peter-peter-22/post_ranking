from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from src.process_media.image.image_options import ImageOptions
from src.process_media.video.video_options import VideoOptions
from src.common.admin import verify_secret_key
from src.common.redis import r
from src.common.upload_keys import get_upload_key_redis

router = APIRouter()

class ImageUploadKey(BaseModel):
    key:str
    expiration:int
    options:ImageOptions

@router.post("/image", dependencies=[Depends(verify_secret_key)])
async def create_image_upload_key(body:ImageUploadKey):
    print("Creating image upload key for:",body)
    # Create upload key in redis with expiration time
    await r.setex(
        get_upload_key_redis(body.key),
        body.expiration,
        body.options.model_dump_json()
    )
    return Response("Upload key created",status.HTTP_201_CREATED)

class VideoUploadKey(BaseModel):
    key:str
    expiration:int
    options:VideoOptions

@router.post("/video", dependencies=[Depends(verify_secret_key)])
async def create_video_upload_key(body:VideoUploadKey):
    print("Creating video upload key for:",body)
    # Create upload key in redis with expiration time
    await r.setex(
        get_upload_key_redis(body.key),
        body.expiration,
        body.options.model_dump_json()
    )
    return Response("Upload key created",status.HTTP_201_CREATED)
    