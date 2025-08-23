from fastapi import UploadFile, HTTPException
from src.minio.client import minio_client
from PIL import Image
import io
from src.process_media.image.image_options import ImageOptions
from src.tagging.tag_image import describe_image
from src.common.response import UploadResponse
import asyncio

async def upload_image(file: UploadFile, options:str):
    # Get and validate the options
    parsed_options=ImageOptions.model_validate_json(options)
    print("Options: ",parsed_options)

    # Get the file type
    mime_type=file.content_type
    print("Mime Type: ",mime_type)
    if mime_type is None:
        raise HTTPException(status_code=422, detail="Mime type is required")

    # Get the file size
    size=file.size
    print("Size: ",size)
    if size is None:
        raise HTTPException(status_code=422, detail="File size is required")

    # Validate the mimetype when necessary
    if parsed_options.mime_type:
        if parsed_options.mime_type != mime_type:
            raise HTTPException(status_code=422, detail=f"Mime type mismatch. Expected {parsed_options.mime_type}, got {mime_type}")
        
    # Validate the file size when necessary
    if parsed_options.max_size:
        if size > parsed_options.max_size:
            raise HTTPException(status_code=422, detail=f"File size exceeds maximum allowed. Maximum size: {parsed_options.max_size} bytes, got: {size} bytes")
    
    # Read uploaded file
    contents = await file.read()
    bytes=io.BytesIO(contents)
    image = Image.open(bytes)

    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Tag image if necessary
    label=None
    if parsed_options.describe:
        label=describe_image(image,parsed_options.prompt,parsed_options.prompt_max_tokens)

    # Limit max resolution if necessary
    if parsed_options.limit_resolution:
        image.thumbnail((parsed_options.limit_resolution.x,parsed_options.limit_resolution.y))

    # Skip the upload if necessary
    if not parsed_options.skip_upload:

        # Convert, compress and save
        buffer = io.BytesIO()
        image.save(
            buffer, 
            format=parsed_options.convert_to or image.format, 
            quality=parsed_options.quality or 100
        )
        buffer.seek(0)
    
        # Upload
        await asyncio.to_thread(
            lambda: minio_client.put_object(
                bucket_name=parsed_options.bucket_name,
                object_name= parsed_options.object_name,
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type=parsed_options.upload_mime_type
            )
        )

    # Return results
    return UploadResponse(
        bucket_name=parsed_options.bucket_name,
        object_name=parsed_options.object_name,
        mime_type=parsed_options.upload_mime_type,
        label=label
    )