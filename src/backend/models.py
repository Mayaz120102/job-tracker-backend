from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum, Date
from backend.database import Base

import enum

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected  = "rejected"

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    phone_number = Column(String)
    address = Column(String)


class Applications(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    job_title = Column(String)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    applied_date = Column(Date)
    job_url = Column(String)
    notes = Column(Text)
    owner_id  = Column(Integer, ForeignKey("users.id"))