from minio import Minio
from src.common.env import settings

minio_client:Minio = Minio(
    settings.minio_url,
    access_key=settings.minio_root_user,
    secret_key=settings.minio_root_password,
    secure=settings.minio_secure
)