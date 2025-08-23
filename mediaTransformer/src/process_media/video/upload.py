from fastapi import UploadFile, HTTPException
from src.common.response import UploadResponse
import shutil
import tempfile
import ffmpeg
from src.process_media.video.video_options import VideoOptions
from src.tagging.tag_video import describe_video
import os
from pathlib import Path
import asyncio
from src.minio.client import minio_client
from src.ffmpeg.get_ffmpeg_path import ffmpeg_path

async def upload_video(file: UploadFile, options:str):
    # Define the file paths to access them later
    upload_path=None
    output_path=None

    try:
        # Get and validate the options
        c=VideoOptions.model_validate_json(options)
        print("Options: ",c)

        # Get file extension
        if file.filename is None:
            raise HTTPException(status_code=422, detail="File name is required")
        ext = Path(file.filename).suffix
        print("Extension: ",ext)
        
        # Create a temporary path for the uploaded video
        with tempfile.NamedTemporaryFile(delete=False,suffix=ext) as upload:
            upload_path = upload.name 
            print("Upload Path: ",upload_path)

            # Place the video to a temp path
            shutil.copyfileobj(file.file, upload)

            # Get the file type
            mime_type=file.content_type
            print("Mime Type: ",mime_type)
            if mime_type is None:
                raise HTTPException(status_code=422, detail="Mime type is required")
            
            # Validate the mimetype when necessary
            if c.mime_type:
                if c.mime_type != mime_type:
                    raise HTTPException(status_code=422, detail=f"Mime type mismatch. Expected {c.mime_type}, got {mime_type}")


            # Get the file size
            size=file.size
            print("Size: ",size)
            if size is None:
                raise HTTPException(status_code=422, detail="File size is required")
            
            # Create a temporary path for the transformed video
            output_ext=c.convert_to or ext
            with tempfile.NamedTemporaryFile(delete=False,suffix=output_ext) as output:
                output_path=output.name
                print("Output Path: ",output_path)
            
                # Define mpeg settings
                fm_config={
                    "vf":c.ffmpeg_settings and c.ffmpeg_settings.vf or \
                        f"scale='min({c.limit_resolution.x},iw)':'min({c.limit_resolution.y},ih)':force_original_aspect_ratio=decrease:force_divisible_by=2:flags=bicubic" \
                        if c.limit_resolution else None,
                    "vcodec":c.ffmpeg_settings and c.ffmpeg_settings.vcodec or \
                        'libx264',
                    "acodec":c.ffmpeg_settings and c.ffmpeg_settings.acodec or \
                        'aac',
                    "format":c.convert_to,
                    "bitrate":c.bitrate,
                    "loglevel":"quiet"
                }

                # Transform the file in mpeg
                print("Transforming video",flush=True)
                (
                    ffmpeg
                    .input(upload_path)
                    .output(
                        output_path,
                        **{k: v for k, v in fm_config.items() if v is not None} # Remove None args to avoid errors
                    )
                    .overwrite_output()
                    .run(cmd=ffmpeg_path)
                )

                # Tag if necessary
                label= describe_video(output_path,c.prompt,c.prompt_max_tokens) if c.describe else None
                
                # Skip upload when necessary
                if not c.skip_upload:

                    # Upload
                    file_size = os.path.getsize(output_path)
                    with open(output_path, 'rb') as data_to_upload:
                        await asyncio.to_thread(
                            lambda: minio_client.put_object(
                                c.bucket_name,
                                c.object_name,
                                data=data_to_upload,
                                length=file_size,
                                content_type=c.upload_mime_type
                            )
                        )

                # Return the response
                return UploadResponse(
                    object_name=c.object_name,
                    bucket_name=c.bucket_name, 
                    mime_type=c.upload_mime_type,
                    label=label
                )

    # Handle errors
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e}")
        raise HTTPException(status_code=400, detail="Error processing video")
    
    # Remove the temporary files
    finally:
        try:
            if output_path: os.remove(output_path)
            if upload_path: os.remove(upload_path)
        except PermissionError as e:
            print("Warning: Failed to remove temporary file.", e)
