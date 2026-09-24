from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date

class JobPostingBase(BaseModel):
    company_id: UUID
    job_title: str
    url: str
    description: str | None = None
    employment_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    deadline: date | None = None
    date_posted: date | None = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingUpdate(JobPostingBase):
    company_id: UUID | None = None
    job_title: str | None = None
    url: str | None = None
    description: str | None = None
    employment_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    deadline: date | None = None
    date_posted: date | None = None

class JobPostingResp(BaseModel):
    id: UUID
    company_id: UUID
    job_title: str
    url: str
    description: str | None = None
    employment_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    deadline: date | None = None
    date_posted: date | None = None

    model_config = ConfigDict(from_attributes=True)
