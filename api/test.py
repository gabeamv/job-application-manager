from database import db
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
async def get_status():
    return {"Hello": "World"}