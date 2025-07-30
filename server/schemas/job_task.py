from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobTaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    default_price: float = 0.0
    sequence: int = 0

class JobTaskCreate(JobTaskBase):
    pass

class JobTaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    default_price: Optional[float] = None
    sequence: Optional[int] = None

class JobTaskRead(JobTaskBase):
    id: int
    sequence: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 