from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class InterviewBase(BaseModel):
    applications_id: UUID
    type: str | None = None
    scheduled_at: datetime | None = None
    notes: str | None = None

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(InterviewBase):
    applications_id: UUID | None = None
    type: str | None = None
    scheduled_at: datetime | None = None
    notes: str | None = None

class InterviewResp(BaseModel):
    id: UUID
    applications_id: UUID
    type: str | None = None
    scheduled_at: datetime | None = None
    notes: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
