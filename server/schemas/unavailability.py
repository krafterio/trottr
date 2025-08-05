from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UnavailabilityType(str, Enum):
    DISEASE = "disease"
    TRAINING = "training"
    PAID_LEAVE = "paid_leave"
    OTHER = "other"

class UserRead(BaseModel):
    id: int
    email: str
    name: Optional[str] = None

    class Config:
        from_attributes = True

class UnavailabilityBase(BaseModel):
    start: datetime
    end: datetime
    type: UnavailabilityType
    description: Optional[str] = None

class UnavailabilityCreate(UnavailabilityBase):
    user: int

class UnavailabilityUpdate(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    type: Optional[UnavailabilityType] = None
    user: Optional[int] = None
    description: Optional[str] = None

class UnavailabilityRead(UnavailabilityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserRead

    class Config:
        from_attributes = True 