from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Companies
from fastapi import HTTPException
from schemas.companies import CompanyCreate, CompanyUpdate, CompanyResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=CompanyResp, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate,  db: Session = Depends(get_db)):
    company = Companies(**payload.model_dump())
    db.add(company)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Company {company.name} already exists")
    db.refresh(company)
    return company
                   

@router.get("/{id}", response_model=CompanyResp)
def get_company_by_id(id: UUID, db: Session = Depends(get_db)):
    company = db.get(Companies, id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {id} not found")
    return company

@router.get("/", response_model=list[CompanyResp])
def get_all_companies(db: Session = Depends(get_db)):
    stmt = select(Companies)
    all_companies = db.scalars(stmt).all()
    return all_companies

@router.put("/{id}", response_model=CompanyResp)
def update_company(id: UUID, payload: CompanyUpdate, db: Session = Depends(get_db)):
    company = db.get(Companies, id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(company, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Company {company.name} already exists")
    db.refresh(company)
    return company

@router.delete("/{id}")
def delete_company(id: UUID, db: Session = Depends(get_db)):
    company = db.get(Companies, id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {id} not found")
    db.delete(company)
    db.commit()