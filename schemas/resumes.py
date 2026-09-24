from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ResumeBase(BaseModel):
    name: str
    version: float
    url: str

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(ResumeBase):
    name: str | None = None
    version: float | None = None
    url: str | None = None

class ResumeResp(BaseModel):
    id: UUID
    name: str
    version: float
    url: str

    model_config = ConfigDict(from_attributes=True)
