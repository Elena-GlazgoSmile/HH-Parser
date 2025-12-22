from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VacancyBase(BaseModel):
    hh_id: str
    name: str
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    salary_currency: Optional[str] = None
    employer: str
    experience: str
    employment: str
    schedule: str
    description: str
    skills: str
    area: str
    url: str
    published_at: datetime

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    is_active: Optional[bool] = None

class VacancyResponse(VacancyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class TaskRunResponse(BaseModel):
    message: str
    task_id: str
    started_at: datetime

class WSMessage(BaseModel):
    type: str
    data: dict
    timestamp: datetime = datetime.utcnow()
