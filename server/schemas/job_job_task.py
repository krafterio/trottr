from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime
from schemas.user import User
from schemas.job import JobRead
from schemas.job_task import JobTaskRead

class JobJobTaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_done: bool = False
    done_at: Optional[Union[datetime, str]] = None
    done_by: Optional[Union[int, dict]] = None
    job: Union[int, dict]
    job_task: Union[int, dict]
    sequence: int = 0

    @field_validator('done_by', 'job', 'job_task', mode='before')
    @classmethod
    def extract_id(cls, v):
        if isinstance(v, dict):
            if 'id' in v:
                return v['id']
            elif hasattr(v, 'id'):
                return v.id
        return v

    @field_validator('done_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v

class JobJobTaskCreate(JobJobTaskBase):
    pass

class JobJobTaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    done_at: Optional[datetime] = None
    done_by: Optional[int] = None
    job: Optional[int] = None
    job_task: Optional[int] = None
    sequence: Optional[int] = None

class JobJobTaskRead(JobJobTaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    done_by: Optional[User] = None
    job: JobRead
    job_task: JobTaskRead
    sequence: int
    
    class Config:
        from_attributes = True 