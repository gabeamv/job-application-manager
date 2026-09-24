from fastapi import APIRouter, Depends
from database.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from models.models import Skills
from fastapi import HTTPException
from schemas.skills import SkillCreate, SkillUpdate, SkillResp
from sqlalchemy.exc import IntegrityError
from fastapi import status


router = APIRouter()

@router.post("/", response_model=SkillResp, status_code=status.HTTP_201_CREATED)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db)):
    skill = Skills(**payload.model_dump())
    db.add(skill)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Skill {skill.name} already exists")
    db.refresh(skill)
    return skill


@router.get("/{id}", response_model=SkillResp)
def get_skill_by_id(id: UUID, db: Session = Depends(get_db)):
    skill = db.get(Skills, id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill {id} not found")
    return skill

@router.get("/", response_model=list[SkillResp])
def get_all_skills(db: Session = Depends(get_db)):
    stmt = select(Skills)
    all_skills = db.scalars(stmt).all()
    return all_skills

@router.put("/{id}", response_model=SkillResp)
def update_skill(id: UUID, payload: SkillUpdate, db: Session = Depends(get_db)):
    skill = db.get(Skills, id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill {id} not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(skill, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Skill {skill.name} already exists")
    db.refresh(skill)
    return skill

@router.delete("/{id}")
def delete_skill(id: UUID, db: Session = Depends(get_db)):
    skill = db.get(Skills, id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill {id} not found")
    db.delete(skill)
    db.commit()
