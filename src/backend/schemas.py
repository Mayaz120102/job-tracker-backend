from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from backend.models import ApplicationStatus


class ApplicationCreate(BaseModel):
    company_name: str = Field(max_length=100)
    job_title: str = Field(max_length=100)
    status: ApplicationStatus | None = None
    applied_date: date
    job_url: str = Field(max_length=500)
    notes: str = Field(max_length=2000)


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = Field(default=None, max_length=100)
    job_title: Optional[str] = Field(default=None, max_length=100)
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    job_url: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=2000)


class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    job_title: str
    status: ApplicationStatus
    applied_date: date
    job_url: str
    notes: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str
    phone_number: str = Field(max_length=20)
    address: str = Field(max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
