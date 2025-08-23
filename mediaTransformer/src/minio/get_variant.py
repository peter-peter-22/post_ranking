from src.minio.variants import variantsSchema,VariantRoute
from fastapi import HTTPException
import re
from src.minio.client import minio_client
from src.minio.common import FileMeta
from minio.error import S3Error
from src.process_media.image.create_variant import create_image_variant

def ensure_variant(bucket:str,path:str,variant_name:str):
    # Check if the variant is appliable for this file
    variant_config=get_variant_config(variant_name)
    check_variant_permission(bucket,path,variant_config)
    # Get the path of the variant
    v_path=f"{bucket}/{variant_name}/{path}"
    v_bucket="variants"
    try:
        # Get the file size if the variant exists
        stat = minio_client.stat_object(v_bucket, v_path)
        file_size = stat.size or 0
        # Return the existing variant metadata
        return FileMeta(v_bucket,v_path,file_size)
    except S3Error as e:
        if e.code not in ["NoSuchKey"]:
            raise e
        # If the variant does not have a file, create it
        return create_image_variant(bucket,path,v_bucket,v_path,variant_config.config)


def check_variant_permission(bucket:str,path:str,variant_config:VariantRoute):
    """Check if the selected variant is appliable to this file"""
    path_config=variant_config.path
    if path_config.bucket and not path_config.bucket==bucket: raise HTTPException(400, "Invalid bucket for this variant")
    if path_config.pathRegex and not re.search(path_config.pathRegex,path): raise HTTPException(400, "Invalid path for this variant")

def get_variant_config(variant_name:str):
    """Get a media variant config based on a name"""
    variant=variantsSchema[variant_name]
    if not variant: raise HTTPException(400, "Invalid variant name")
    return variant
