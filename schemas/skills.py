from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SkillBase(BaseModel):
    name: str
    description: str | None = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: str | None = None
    description: str | None = None

class SkillResp(BaseModel):
    id: UUID
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
