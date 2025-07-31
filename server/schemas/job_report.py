from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserRead(BaseModel):
    id: int
    email: str
    name: str
    
    class Config:
        from_attributes = True

class JobRead(BaseModel):
    id: int
    
    class Config:
        from_attributes = True

class JobReportBase(BaseModel):
    name: str
    content: str
    include_diagnostics: bool = True
    include_tasks: bool = True
    job: int
    customer_signature: Optional[str] = None
    operator_signature: Optional[str] = None

class JobReportCreate(JobReportBase):
    pass

class JobReportUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    include_diagnostics: Optional[bool] = None
    include_tasks: Optional[bool] = None
    job: Optional[int] = None
    customer_signature: Optional[str] = None
    operator_signature: Optional[str] = None

class JobReportRead(JobReportBase):
    id: int
    job: JobRead
    created_by: UserRead
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 