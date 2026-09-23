from pydantic import BaseModel, ConfigDict
from uuid import UUID

class JobPostingsBase(BaseModel):
    company_id: UUID
    job_title: str | None = None
    url: str | None = None
    