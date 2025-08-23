from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # redis
    redis_host: str
    redis_port:int
    redis_password:str
    # authentication
    secret_key:str
    # minio
    minio_url:str
    minio_root_user:str
    minio_root_password:str
    minio_secure:bool
    # ffmpeg
    ffmpeg_name:str

settings = Settings() # type: ignore