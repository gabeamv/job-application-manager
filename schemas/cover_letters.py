from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CoverLetterBase(BaseModel):
    job_postings_id: UUID
    name: str
    url: str

class CoverLetterCreate(CoverLetterBase):
    pass

class CoverLetterUpdate(CoverLetterBase):
    job_postings_id: UUID | None = None
    name: str | None = None
    url: str | None = None

class CoverLetterResp(BaseModel):
    id: UUID
    job_postings_id: UUID
    name: str
    url: str

    model_config = ConfigDict(from_attributes=True)
