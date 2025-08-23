from fastapi import HTTPException, Header
from src.common.env import settings

def verify_secret_key(secret_key: str = Header(...)):
    if secret_key != settings.secret_key:
        raise HTTPException(401, "Invalid secret key.")