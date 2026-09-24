from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import JobPostingsSkills
from fastapi import HTTPException
from schemas.job_postings_skills import JobPostingSkillCreate, JobPostingSkillUpdate, JobPostingSkillResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=JobPostingSkillResp, status_code=status.HTTP_201_CREATED)
def create_job_posting_skill(payload: JobPostingSkillCreate, db: Session = Depends(get_db)):
    job_posting_skill = JobPostingsSkills(**payload.model_dump())
    db.add(job_posting_skill)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Skill {payload.skills_id} is already linked to job posting {payload.job_postings_id}")
    db.refresh(job_posting_skill)
    return job_posting_skill


@router.get("/{id}", response_model=JobPostingSkillResp)
def get_job_posting_skill_by_id(id: UUID, db: Session = Depends(get_db)):
    job_posting_skill = db.get(JobPostingsSkills, id)
    if not job_posting_skill:
        raise HTTPException(status_code=404, detail=f"Job posting skill {id} not found")
    return job_posting_skill

@router.get("/", response_model=list[JobPostingSkillResp])
def get_all_job_posting_skills(db: Session = Depends(get_db)):
    stmt = select(JobPostingsSkills)
    all_job_posting_skills = db.scalars(stmt).all()
    return all_job_posting_skills

@router.put("/{id}", response_model=JobPostingSkillResp)
def update_job_posting_skill(id: UUID, payload: JobPostingSkillUpdate, db: Session = Depends(get_db)):
    job_posting_skill = db.get(JobPostingsSkills, id)
    if not job_posting_skill:
        raise HTTPException(status_code=404, detail=f"Job posting skill {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(job_posting_skill, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Skill {job_posting_skill.skills_id} is already linked to job posting {job_posting_skill.job_postings_id}")
    db.refresh(job_posting_skill)
    return job_posting_skill

@router.delete("/{id}")
def delete_job_posting_skill(id: UUID, db: Session = Depends(get_db)):
    job_posting_skill = db.get(JobPostingsSkills, id)
    if not job_posting_skill:
        raise HTTPException(status_code=404, detail=f"Job posting skill {id} not found")
    db.delete(job_posting_skill)
    db.commit()