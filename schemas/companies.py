from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CompanyBase(BaseModel):
    name: str   
    url : str | None = None
    industry: str | None = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: str | None = None
    url: str | None = None
    industry: str | None = None

class CompanyResp(BaseModel):
    id: UUID
    name: str
    url : str | None = None
    industry: str | None = None

    model_config = ConfigDict(from_attributes=True)

