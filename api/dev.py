import os
import secrets

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database.db import get_db
from models.models import Base

load_dotenv()

DEV_SECRET = os.getenv("SECRET")
api_key_header = APIKeyHeader(name="X-Dev-Secret", auto_error=False)


def verify_dev_secret(provided: str | None = Depends(api_key_header)) -> None:
    if not DEV_SECRET or not provided or not secrets.compare_digest(provided, DEV_SECRET):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing dev secret")


router = APIRouter(dependencies=[Depends(verify_dev_secret)])


@router.get("/healthz")
def get_status():
    return {"Hello": "World"}

@router.delete("/reset")
def reset_db(db: Session = Depends(get_db)):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    return {"detail": "Database reset: all data deleted"}

