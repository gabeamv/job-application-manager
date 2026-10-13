from fastapi import APIRouter, Depends, Query
from database.db import get_db
from sqlalchemy import select, outerjoin, func, desc, cast, Float, and_, or_
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Applications, Skills, Interviews, JobPostings, JobPostingsSkills, Resumes
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from datetime import date
from schemas.stats import (
    SkillsRate, SkillsDemand, ResumesRate, 
    ApplicationsStatusRate, ApplicationsStatusCount, Rate)
from models.application_status import ApplicationStatus


router = APIRouter()

def _dateConds(start: date | None, end: date | None):
    conds = []
    if start:
        conds.append(Applications.date_applied >= start)
    if end:
        conds.append(Applications.date_applied <= end)
    return conds

@router.get("/skills/top-by-interview-rate", response_model=list[SkillsRate])
def get_skills_top_by_interview_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):

    dateConds = _dateConds(applied_start_date, applied_end_date)
    
    stmt = (
        select(
            Skills.id.label("skill_id"),
            Skills.name,
            (
                cast(func.count(func.distinct(Interviews.applications_id)), Float) / func.count(func.distinct(Applications.id))
            ).label("rate"),
        )
        .select_from(Skills)
        .join(JobPostingsSkills, JobPostingsSkills.skills_id == Skills.id)
        .join(JobPostings, JobPostings.id == JobPostingsSkills.job_postings_id)
        .join(Applications, Applications.job_postings_id == JobPostings.id)
        .outerjoin(Interviews, Interviews.applications_id == Applications.id)
        .where(*dateConds)
        .group_by(Skills.id, Skills.name)
        .order_by(desc("rate"))
        .limit(limit)
    )

    stats = db.execute(stmt).all()
    return stats
    


@router.get("/skills/top-by-screening-rate", response_model=list[SkillsRate])
def get_skills_top_by_screening_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):

    dateConds = _dateConds(applied_start_date, applied_end_date)

    # Applications that have at least reached the screening process.
    screened = Applications.status.in_([
        ApplicationStatus.REJECTED_AT_SCREENING,
        ApplicationStatus.REJECTED_AT_INTERVIEW,
        ApplicationStatus.IN_HIRING_PROCESS,
        ApplicationStatus.RETURN_OFFER,
    ])

    stmt = (
        select(
            Skills.id.label("skill_id"),
            Skills.name,
            (
                cast(
                    func.count(func.distinct(Applications.id)).filter(screened), 
                    Float
                )
                / func.count(func.distinct(Applications.id))
            ).label("rate"),
        )
        .select_from(Skills)
        .join(JobPostingsSkills, JobPostingsSkills.skills_id == Skills.id)
        .join(JobPostings, JobPostings.id == JobPostingsSkills.job_postings_id)
        .join(Applications, Applications.job_postings_id == JobPostings.id)
        .where(*dateConds)
        .group_by(Skills.id, Skills.name)
        .order_by(desc("rate"))
        .limit(limit)
    )
    stats = db.execute(stmt).all()
    return stats

@router.get("/resumes/top-by-screening-rate", response_model=list[ResumesRate])
def get_resumes_top_by_screening_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    
    dateConds = _dateConds(applied_start_date, applied_end_date)

    screened = Applications.status.in_([
        ApplicationStatus.REJECTED_AT_SCREENING,
        ApplicationStatus.REJECTED_AT_INTERVIEW,
        ApplicationStatus.IN_HIRING_PROCESS,
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select (
            Resumes.id.label("resume_id"),
            Resumes.name,
            Resumes.version,
            (
                cast(
                    func.count(func.distinct(Applications.id)).filter(screened), 
                    Float
                )
                / func.count(func.distinct(Applications.id))
            ).label("rate"),
        )
        .select_from(Resumes)
        .join(Applications, Applications.resumes_id == Resumes.id)
        .where(*dateConds)
        .group_by(Resumes.id, Resumes.name, Resumes.version)
        .order_by(desc("rate"))
        .limit(limit)
    )

    stats = db.execute(stmt).all()
    return stats

@router.get("/resumes/top-by-interview-rate", response_model=list[ResumesRate])
def get_resumes_top_by_interview_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    # get applications relevant to the date params.
    
    dateConds = _dateConds(applied_start_date, applied_end_date)
    
    stmt = (
        select(
            Resumes.id.label("resume_id"),
            Resumes.name,
            Resumes.version,
            (
                cast(func.count(func.distinct(Interviews.applications_id)), Float) / func.count(func.distinct(Applications.id))
            ).label("rate"),
        )
        .select_from(Resumes)
        .join(Applications, Applications.resumes_id == Resumes.id)
        .outerjoin(Interviews, Interviews.applications_id == Applications.id)
        .where(*dateConds)
        .group_by(Resumes.id, Resumes.name, Resumes.version)
        .order_by(desc("rate"))
        .limit(limit)
    )

    stats = db.execute(stmt).all()
    return stats
    
@router.get("/screenings-to-applications", response_model=Rate)
def get_screenings_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    screened = Applications.status.in_([
        ApplicationStatus.REJECTED_AT_SCREENING,
        ApplicationStatus.REJECTED_AT_INTERVIEW,
        ApplicationStatus.IN_HIRING_PROCESS,
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select(
            (
                cast(func.count(Applications.id).filter(screened), Float) /
                func.nullif(func.count(Applications.id), 0)
            ).label("rate")
        )
        .where(*dateConds)
    )
    stats = db.execute(stmt).one()
    return stats

@router.get("/interviews-to-applications", response_model=Rate)
def get_interviews_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    interviewed = Applications.status.in_([
        ApplicationStatus.REJECTED_AT_INTERVIEW,
        ApplicationStatus.IN_HIRING_PROCESS,
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select(
            (
                cast(func.count(Applications.id).filter(interviewed), Float) /
                func.nullif(func.count(Applications.id), 0)
            ).label("rate")
        )
        .where(*dateConds)
    )
    stats = db.execute(stmt).one()
    return stats

@router.get("/offers-to-applications")
def get_offers_to_applications_rate(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    offered = Applications.status.in_([
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select(
            (
                cast(func.count(Applications.id).filter(offered), Float) /
                func.nullif(func.count(Applications.id), 0)
            ).label("rate")
        )
        .where(*dateConds)
    )
    stats = db.execute(stmt).one()
    return stats

@router.get("/resumes/{id}/screening-rate", response_model=Rate)
def get_resume_screening_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    screened = Applications.status.in_([
            ApplicationStatus.REJECTED_AT_SCREENING,
            ApplicationStatus.REJECTED_AT_INTERVIEW,
            ApplicationStatus.IN_HIRING_PROCESS,
            ApplicationStatus.RETURN_OFFER,
        ])
    stmt = (
        select(
            (
                cast(func.count(Applications.id).filter(screened), Float) /
                func.nullif(func.count(Applications.id), 0)
            ).label("rate")
        )
        .where(Applications.resumes_id == id, *dateConds)
    )
    stats = db.execute(stmt).one()
    return stats


@router.get("/resumes/{id}/interview-rate", response_model=Rate)
def get_resume_interview_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)  
    stmt = (
        select(
            (

                cast(func.count(func.distinct(Interviews.applications_id)), Float) / 
                func.nullif(func.count(func.distinct(Applications.id)), 0)
            ).label("rate"),
        )
        .select_from(Resumes)
        .join(Applications, Applications.resumes_id == Resumes.id)
        .outerjoin(Interviews, Interviews.applications_id == Applications.id)
        .where(Resumes.id == id, *dateConds)
    )

    stats = db.execute(stmt).one()
    return stats

@router.get("/resumes/top-by-offer-rate", response_model=list[ResumesRate])
def get_resumes_top_by_offer_rate(
    limit: int | None = Query(None, ge=1), 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    offered = Applications.status.in_([
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select(
                Resumes.id.label("resume_id"),
                Resumes.name,
                Resumes.version,
                (
                    cast(func.count(Applications.id).filter(offered), Float) /
                        func.nullif(func.count(Applications.id), 0)
                ).label("rate")  
        )
        .select_from(Resumes)
        .join(Applications, Applications.resumes_id == Resumes.id)
        .where(*dateConds)
        .group_by(Resumes.id, Resumes.name, Resumes.version)
        .order_by(desc("rate"))
        .limit(limit)

    )
    stats = db.execute(stmt).all()
    return stats
    

@router.get("/resumes/{id}/offer-rate", response_model=Rate)
def get_resume_offer_rate(
    id: UUID, 
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    offered = Applications.status.in_([
        ApplicationStatus.RETURN_OFFER,
    ])
    stmt = (
        select(
            (
                cast(func.count(Applications.id).filter(offered), Float) /
                func.nullif(func.count(Applications.id), 0)
            ).label("rate")
        )
        .where(Applications.resumes_id == id, *dateConds)
    )
    stats = db.execute(stmt).one()
    return stats

@router.get("/skills/demand", response_model=list[SkillsDemand])
def get_skills_demand(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    stmt = (
        select(
            Skills.id.label("skill_id"),
            Skills.name,
            (
                func.count(func.distinct(JobPostingsSkills.id))  
            ).label("demand_job_postings")
            
        )
        .select_from(Skills)
        .join(JobPostingsSkills, JobPostingsSkills.skills_id == Skills.id)
        .join(JobPostings, JobPostings.id == JobPostingsSkills.job_postings_id)
        .join(Applications, Applications.job_postings_id == JobPostings.id)
        .where(*dateConds)
        .group_by(Skills.id, Skills.name)
        .order_by(desc("demand_job_postings"), Skills.name)
    )
    stats = db.execute(stmt).all()
    return stats

@router.get("/applications/status", response_model=list[ApplicationsStatusCount])
def get_applications_status(
    applied_start_date: date | None = None, 
    applied_end_date: date | None = None,
    db: Session = Depends(get_db)):
    dateConds = _dateConds(applied_start_date, applied_end_date)
    stmt = (
        select(
            Applications.status,
            (
                func.count(Applications.status)
            ).label("count")
        )
        .where(*dateConds)
        .group_by(Applications.status)
        .order_by(Applications.status)
    )
    stats = db.execute(stmt).all()
    return stats