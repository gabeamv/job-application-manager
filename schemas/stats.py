from pydantic import BaseModel, ConfigDict
from models.application_status import ApplicationStatus
from uuid import UUID

class RespConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class SkillsRate(RespConfig):
    skill_id: UUID
    name: str
    rate: float

class SkillsDemand(RespConfig):
    skill_id: UUID
    name: str
    demand_job_postings: int

class ResumesRate(RespConfig):
    resume_id: UUID
    name: str
    version: float
    rate: float
    
class ApplicationsStatusRate(RespConfig):
    status: str
    rate: float

class ApplicationsStatusCount(RespConfig):
    status: str
    count: int
