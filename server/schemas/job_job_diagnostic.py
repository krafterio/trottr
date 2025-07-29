from pydantic import BaseModel
from typing import Optional


class JobDiagnosticRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class JobJobDiagnosticBase(BaseModel):
    sequence: int
    job: int
    job_diagnostic: int
    description: Optional[str] = None


class JobJobDiagnosticCreate(JobJobDiagnosticBase):
    pass


class JobJobDiagnosticUpdate(BaseModel):
    sequence: Optional[int] = None
    job: Optional[int] = None
    job_diagnostic: Optional[int] = None
    description: Optional[str] = None


class JobJobDiagnosticRead(JobJobDiagnosticBase):
    id: int
    created_at: str
    updated_at: str
    job_diagnostic: JobDiagnosticRead
    
    class Config:
        from_attributes = True 