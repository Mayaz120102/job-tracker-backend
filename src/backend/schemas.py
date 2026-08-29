from pydantic import BaseModel, Field
from backend.models import ApplicationStatus
from datetime import date
from typing import Optional


class ApplicationCreate(BaseModel):
    company_name : str
    job_title : str
    status : ApplicationStatus | None = None
    applied_date : date
    job_url : str
    notes : str

class ApplicationUpdate(BaseModel):

    company_name : Optional[str] = Field(default=None)
    job_title : Optional[str] = Field(default=None)
    status : Optional[ApplicationStatus] = None
    applied_date : Optional[date] = None
    job_url : Optional[str] =None
    notes : Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    job_title: str
    status: ApplicationStatus
    applied_date: date
    job_url: str
    notes: str
    owner_id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):

    email : str
    username : str
    password : str
    phone_number : str
    address : str


class Token(BaseModel):
    access_token: str
    token_type: str