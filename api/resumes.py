from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Resumes
from fastapi import HTTPException
from schemas.resumes import ResumeCreate, ResumeUpdate, ResumeResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=ResumeResp, status_code=status.HTTP_201_CREATED)
def create_resume(payload: ResumeCreate, db: Session = Depends(get_db)):
    resume = Resumes(**payload.model_dump())
    db.add(resume)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Resume {resume.name} v{resume.version} already exists")
    db.refresh(resume)
    return resume


@router.get("/{id}", response_model=ResumeResp)
def get_resume_by_id(id: UUID, db: Session = Depends(get_db)):
    resume = db.get(Resumes, id)
    if not resume:
        raise HTTPException(status_code=404, detail=f"Resume {id} not found")
    return resume

@router.get("/", response_model=list[ResumeResp])
def get_all_resumes(db: Session = Depends(get_db)):
    stmt = select(Resumes)
    all_resumes = db.scalars(stmt).all()
    return all_resumes

@router.put("/{id}", response_model=ResumeResp)
def update_resume(id: UUID, payload: ResumeUpdate, db: Session = Depends(get_db)):
    resume = db.get(Resumes, id)
    if not resume:
        raise HTTPException(status_code=404, detail=f"Resume {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(resume, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Resume {resume.name} v{resume.version} already exists")
    db.refresh(resume)
    return resume

@router.delete("/{id}")
def delete_resume(id: UUID, db: Session = Depends(get_db)):
    resume = db.get(Resumes, id)
    if not resume:
        raise HTTPException(status_code=404, detail=f"Resume {id} not found")
    db.delete(resume)
    db.commit()
