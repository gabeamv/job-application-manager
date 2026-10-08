from fastapi import APIRouter, Depends, Query
from database.db import get_db
from sqlalchemy import select, outerjoin, func
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Applications, Skills, Interviews, JobPostings
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from datetime import date
from schemas.stats import (
    SkillsRate, SkillsDemand, ResumesRate, 
    ApplicationsStatusRate, ApplicationsStatusCount)


router = APIRouter()
#
@router.post("/skills/top-by-interview-rate", response_model=SkillsRate())
def get_skills_top_by_interview_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    # get applications relevant to the date params.
    date_conds = []
    if applied_start_date:
        date_conds.append(Applications.date_applied >= applied_start_date)
    if applied_end_date:
        date_conds.append(Applications.date_applied <= applied_end_date)
    relevant_applications = JobPostings.applications
    # filter applications to date.
    if date_conds:
        relevant_applications = relevant_applications.and_(*date_conds)

    # TODO: using the number of relevant applications based off date params, calculate the "the frequency of a skill in all relevant job postings that were applied to which landed an interview" / "the frequency of a skill in all relevant job postings that were applied to"
    
    stmt = (
        select(
            Skills.id.label("skill_id"),
            Skills.name,
            func.count(Interviews.id).label("rate"),
        )
    )


@router.post("/skills/top-by-screening-rate",)
def get_skills_top_by_screening_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("/resumes/top-by-screening-rate")
def get_resumes_top_by_screening_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("/resumes/top-by-interview-rate")
def get_resumes_top_by_interview_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("/screenings-to-applications")
def get_screenings_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("/interviews-to-applications")
def get_interviews_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("/offers-to-applications")
def get_offers_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("resumes/{id}/screening-rate")
def get_resume_screening_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("resumes/{id}/interview-rate")
def get_resume_interview_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("resumes/top-by-offer-rate")
def get_resumes_top_by_offer_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("resumes/{id}/offer-rate")
def get_resume_offer_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("skills/demand")
def get_skills_demand(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass

@router.post("applications/status")
def get_applications_status(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    pass