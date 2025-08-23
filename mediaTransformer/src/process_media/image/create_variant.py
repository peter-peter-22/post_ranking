from src.process_media.image.image_options import ImageVariant
from src.minio.client import minio_client
from PIL import Image
from io import BytesIO
from src.minio.common import FileMeta

def create_image_variant(original_bucket:str,original_path:str,variant_bucket:str,variant_path:str,config:ImageVariant):
    # Get the metadata of the modified file
    meta=minio_client.stat_object(original_bucket,original_path)

    # Get the file to modify
    image=load_image(original_bucket,original_path)

    # Apply transformations

    # Max size
    if config.limit_resolution:
        image.thumbnail((config.limit_resolution.x, config.limit_resolution.y))

    # Convert, compress and save
    buffer = BytesIO()
    image.save(
        buffer, 
        quality=config.quality or 100,
        format=config.convert_to or image.format
    )
    buffer.seek(0)

    # Save to minio
    size=buffer.getbuffer().nbytes
    minio_client.put_object(
        bucket_name=variant_bucket,
        object_name=variant_path,
        data=buffer,
        length=size,
        content_type=config.upload_mime_type or meta.content_type or "application/octet-stream"
    )

    # Return the metadata of the created file
    return FileMeta(variant_bucket,variant_path,size)

def load_image(bucket,path):
    # Read from minio
    res=minio_client.get_object(bucket,path)
    # Read the image data into a BytesIO buffer
    image_data = BytesIO(res.data)
    # Load the image using Pillow
    return Image.open(image_data)
