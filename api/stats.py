from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Applications
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

# TODO: Begin implementation of stats handlers.