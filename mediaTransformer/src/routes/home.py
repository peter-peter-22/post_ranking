from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return "The server is online!"
