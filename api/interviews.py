from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Interviews
from fastapi import HTTPException
from schemas.interviews import InterviewCreate, InterviewUpdate, InterviewResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=InterviewResp, status_code=status.HTTP_201_CREATED)
def create_interview(payload: InterviewCreate, db: Session = Depends(get_db)):
    interview = Interviews(**payload.model_dump())
    db.add(interview)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Application {payload.applications_id} does not exist")
    db.refresh(interview)
    return interview


@router.get("/{id}", response_model=InterviewResp)
def get_interview_by_id(id: UUID, db: Session = Depends(get_db)):
    interview = db.get(Interviews, id)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview {id} not found")
    return interview

@router.get("/", response_model=list[InterviewResp])
def get_all_interviews(db: Session = Depends(get_db)):
    stmt = select(Interviews)
    all_interviews = db.scalars(stmt).all()
    return all_interviews

@router.put("/{id}", response_model=InterviewResp)
def update_interview(id: UUID, payload: InterviewUpdate, db: Session = Depends(get_db)):
    interview = db.get(Interviews, id)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(interview, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Application {interview.applications_id} does not exist")
    db.refresh(interview)
    return interview

@router.delete("/{id}")
def delete_interview(id: UUID, db: Session = Depends(get_db)):
    interview = db.get(Interviews, id)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview {id} not found")
    db.delete(interview)
    db.commit()
