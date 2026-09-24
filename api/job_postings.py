from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import JobPostings
from fastapi import HTTPException
from schemas.job_postings import JobPostingCreate, JobPostingUpdate, JobPostingResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=JobPostingResp, status_code=status.HTTP_201_CREATED)
def create_job_posting(payload: JobPostingCreate, db: Session = Depends(get_db)):
    job_posting = JobPostings(**payload.model_dump())
    db.add(job_posting)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Company {payload.company_id} does not exist")
    db.refresh(job_posting)
    return job_posting


@router.get("/{id}", response_model=JobPostingResp)
def get_job_posting_by_id(id: UUID, db: Session = Depends(get_db)):
    job_posting = db.get(JobPostings, id)
    if not job_posting:
        raise HTTPException(status_code=404, detail=f"Job posting {id} not found")
    return job_posting

@router.get("/", response_model=list[JobPostingResp])
def get_all_job_postings(db: Session = Depends(get_db)):
    stmt = select(JobPostings)
    all_job_postings = db.scalars(stmt).all()
    return all_job_postings

@router.put("/{id}", response_model=JobPostingResp)
def update_job_posting(id: UUID, payload: JobPostingUpdate, db: Session = Depends(get_db)):
    job_posting = db.get(JobPostings, id)
    if not job_posting:
        raise HTTPException(status_code=404, detail=f"Job posting {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(job_posting, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Company {job_posting.company_id} does not exist")
    db.refresh(job_posting)
    return job_posting

@router.delete("/{id}")
def delete_job_posting(id: UUID, db: Session = Depends(get_db)):
    job_posting = db.get(JobPostings, id)
    if not job_posting:
        raise HTTPException(status_code=404, detail=f"Job posting {id} not found")
    db.delete(job_posting)
    db.commit()
