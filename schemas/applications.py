from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime

class ApplicationBase(BaseModel):
    job_postings_id: UUID
    resumes_id: UUID
    date_applied: date
    status: str | None = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    job_postings_id: UUID | None = None
    resumes_id: UUID | None = None
    date_applied: date | None = None
    status: str | None = None

class ApplicationResp(BaseModel):
    id: UUID
    job_postings_id: UUID
    resumes_id: UUID
    date_applied: date
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
