from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from src.process_media.video.upload import upload_video
from src.process_media.image.upload import upload_image
from src.common.redis import r
from src.common.upload_keys import get_upload_key_redis

router = APIRouter()

@router.post("/video")
async def upload_video_route(file: UploadFile = File(...), key:str=Form(...)):
    print("Using video upload key:",key)
    # Get key
    options=await r.get(get_upload_key_redis(key))
    if not options:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid key")
    
    # Delete key
    await r.delete(key)

    # Process file and options
    return await upload_video(file,str(options)) # type: ignore

@router.post("/image")
async def upload_image_route(file: UploadFile = File(...), key:str=Form(...)):
    print("Using image upload key:",key)
    # Get key
    options=await r.get(get_upload_key_redis(key))
    if not options:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid key")
    
    # Delete key
    await r.delete(key)

    # Process file and options
    return await upload_image(file,str(options))