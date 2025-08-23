from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.minio.schema import initialize_buckets

# Routes
from src.routes.home import router as home
from src.routes.signed_upload import router as signed_upload
from src.routes.create_upload_key import router as create_upload_key
from src.routes.upload import router as upload
from src.routes.get_file import router as get_file

## Start
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_buckets()
    yield

# Create app
app = FastAPI(lifespan=lifespan)

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Routes
app.include_router(home)
app.include_router(upload,prefix="/upload")
app.include_router(create_upload_key,prefix="/sign")
app.include_router(signed_upload,prefix="/signed_upload")
app.include_router(get_file,prefix="/get")
