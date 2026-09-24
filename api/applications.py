from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Applications
from fastapi import HTTPException
from schemas.applications import ApplicationCreate, ApplicationUpdate, ApplicationResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=ApplicationResp, status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    application = Applications(**payload.model_dump())
    db.add(application)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Job posting {payload.job_postings_id} or resume {payload.resumes_id} does not exist")
    db.refresh(application)
    return application


@router.get("/{id}", response_model=ApplicationResp)
def get_application_by_id(id: UUID, db: Session = Depends(get_db)):
    application = db.get(Applications, id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {id} not found")
    return application

@router.get("/", response_model=list[ApplicationResp])
def get_all_applications(db: Session = Depends(get_db)):
    stmt = select(Applications)
    all_applications = db.scalars(stmt).all()
    return all_applications

@router.put("/{id}", response_model=ApplicationResp)
def update_application(id: UUID, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    application = db.get(Applications, id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(application, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Job posting {application.job_postings_id} or resume {application.resumes_id} does not exist")
    db.refresh(application)
    return application

@router.delete("/{id}")
def delete_application(id: UUID, db: Session = Depends(get_db)):
    application = db.get(Applications, id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {id} not found")
    db.delete(application)
    db.commit()
