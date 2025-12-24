from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id = Column(Integer, primary_key=True, index=True)
    hh_id = Column(String, unique=True, index=True)
    name = Column(String)
    salary_from = Column(Float, nullable=True)
    salary_to = Column(Float, nullable=True)
    salary_currency = Column(String, nullable=True)
    employer = Column(String)
    experience = Column(String)
    employment = Column(String)
    schedule = Column(String)
    description = Column(Text)
    skills = Column(Text)
    area = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

