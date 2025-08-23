from fastapi import APIRouter, File, UploadFile, Form, Depends
from src.process_media.video.upload import upload_video
from src.process_media.image.upload import upload_image
from src.common.admin import verify_secret_key

router = APIRouter()

@router.post("/video", dependencies=[Depends(verify_secret_key)])
async def upload_video_route(file: UploadFile = File(...), options:str=Form(...)):
    return await upload_video(file,options) # type: ignore

@router.post("/image", dependencies=[Depends(verify_secret_key)])
async def upload_image_route(file: UploadFile = File(...), options:str=Form(...)):
    return await upload_image(file,options)