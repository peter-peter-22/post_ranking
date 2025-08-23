from fastapi import APIRouter, HTTPException, Request
from src.minio.client import minio_client
from fastapi.responses import StreamingResponse
from minio.error import S3Error
import mimetypes
import re
from typing import Generator, Optional
from urllib3.response import BaseHTTPResponse
from src.minio.get_variant import ensure_variant
from src.minio.common import FileMeta

router = APIRouter()

@router.get("/{bucket}/{path:path}")
def get_file(request:Request, bucket:str, path:str, variant: Optional[str] = None):
    try:
        # Get the metadata
        bucket, path, file_size=get_meta(bucket,path,variant)

        # Get range header
        range_header = request.headers.get("range")

        # Create a partial or full file stream depending on the headers
        if range_header:
            return video_stream(range_header,bucket,path,file_size)
        else:
            return full(bucket,path,file_size)

    except S3Error as e:
        if e.code in ["NoSuchBucket", "NoSuchKey", "NoSuchObject"]:
            raise HTTPException(status_code=404, detail=f"{e.code}: {e.message}")
        else:
            raise HTTPException(status_code=500, detail=f"MinIO error: {e.code} — {e.message}")

def get_meta(bucket:str, path:str, variant: Optional[str]):
    # If no variant is used, get the metadata normally
    if not variant:
        # Get file size
        stat = minio_client.stat_object(bucket, path)
        file_size = stat.size or 0
        return FileMeta(bucket,path,file_size)
    # If a variant is used, get or create it
    else:
        # Get the bucket and path of the variant
        return ensure_variant(bucket,path,variant)

def full(bucket:str, path:str, file_size: int):
    # Get data stream from minio 
    minio_obj = minio_client.get_object(bucket, path)

    # Guess content type based on file extension
    content_type, _ = mimetypes.guess_type(path)
    if content_type is None:
        content_type = "application/octet-stream"

    # Stream the response to the client
    return StreamingResponse(
        set_stream_chunks(minio_obj),
        media_type=content_type,
        headers={
            "Content-Disposition": f"inline; filename={path}",
            "Content-Length": str(file_size),
            "Cache-Control": "public, max-age=31536000, immutable"
        }
    )

def video_stream(range_header:str, bucket:str, path:str, file_size:int):
        # Get the start and end of the range header
        start, end = parse_range_header(range_header, file_size)

        # Get partial data stream from minio 
        minio_obj = minio_client.get_object(bucket, path, offset=start, length=end)
    
        # Guess content type based on file extension
        content_type, _ = mimetypes.guess_type(path)
        if content_type is None:
            content_type = "application/octet-stream"

        # Stream the response to the client
        return StreamingResponse(
            set_stream_chunks(minio_obj),
            media_type=content_type,
            headers={
                "Content-Disposition": f"inline; filename={path}",
                "Accept-Ranges": "bytes",
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(end - start + 1),
                "Cache-Control": "public, max-age=31536000, immutable"
            },
            status_code=206
        )

def parse_range_header(range_header: str, file_size: int):
    match = re.match(r"bytes=(\d*)-(\d*)", range_header)
    if match:
        start_str, end_str = match.groups()
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else file_size - 1
        if end >= file_size:
            end = file_size - 1
        return start, end
    else:
        raise HTTPException(status_code=422, detail="Invalid range header")
    
def set_stream_chunks(obj: BaseHTTPResponse, chunk_size: int = 1024 * 1024) -> Generator[bytes, None, None]:
    try:
        while True:
            data = obj.read(chunk_size)
            if not data:
                break
            yield data
    finally:
        obj.close()
        obj.release_conn()