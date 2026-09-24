from pydantic import BaseModel, ConfigDict
from uuid import UUID

class JobPostingSkillBase(BaseModel):
    job_postings_id: UUID
    skills_id: UUID

class JobPostingSkillCreate(JobPostingSkillBase):
    pass

class JobPostingSkillUpdate(JobPostingSkillBase):
    job_postings_id: UUID | None = None
    skills_id: UUID | None = None

class JobPostingSkillResp(BaseModel):
    id: UUID
    job_postings_id: UUID
    skills_id: UUID

    model_config = ConfigDict(from_attributes=True)
