from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import CoverLetters
from fastapi import HTTPException
from schemas.cover_letters import CoverLetterCreate, CoverLetterUpdate, CoverLetterResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=CoverLetterResp, status_code=status.HTTP_201_CREATED)
def create_cover_letter(payload: CoverLetterCreate, db: Session = Depends(get_db)):
    cover_letter = CoverLetters(**payload.model_dump())
    db.add(cover_letter)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Job posting {payload.job_postings_id} does not exist")
    db.refresh(cover_letter)
    return cover_letter


@router.get("/{id}", response_model=CoverLetterResp)
def get_cover_letter_by_id(id: UUID, db: Session = Depends(get_db)):
    cover_letter = db.get(CoverLetters, id)
    if not cover_letter:
        raise HTTPException(status_code=404, detail=f"Cover letter {id} not found")
    return cover_letter

@router.get("/", response_model=list[CoverLetterResp])
def get_all_cover_letters(db: Session = Depends(get_db)):
    stmt = select(CoverLetters)
    all_cover_letters = db.scalars(stmt).all()
    return all_cover_letters

@router.put("/{id}", response_model=CoverLetterResp)
def update_cover_letter(id: UUID, payload: CoverLetterUpdate, db: Session = Depends(get_db)):
    cover_letter = db.get(CoverLetters, id)
    if not cover_letter:
        raise HTTPException(status_code=404, detail=f"Cover letter {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(cover_letter, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Job posting {cover_letter.job_postings_id} does not exist")
    db.refresh(cover_letter)
    return cover_letter

@router.delete("/{id}")
def delete_cover_letter(id: UUID, db: Session = Depends(get_db)):
    cover_letter = db.get(CoverLetters, id)
    if not cover_letter:
        raise HTTPException(status_code=404, detail=f"Cover letter {id} not found")
    db.delete(cover_letter)
    db.commit()
