from pydantic import BaseModel
from typing import Optional, Union


class JobDiagnosticRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class UserRead(BaseModel):
    id: int
    email: str


class JobRead(BaseModel):
    id: int


class JobJobDiagnosticBase(BaseModel):
    sequence: int
    job: Union[int, JobRead]
    job_diagnostic: Union[int, JobDiagnosticRead]
    description: Optional[str] = None
    created_by: Optional[Union[int, UserRead]] = None


class JobJobDiagnosticCreate(BaseModel):
    sequence: int
    job: int
    job_diagnostic: int
    description: Optional[str] = None
    created_by: Optional[int] = None


class JobJobDiagnosticUpdate(BaseModel):
    sequence: Optional[int] = None
    job: Optional[int] = None
    job_diagnostic: Optional[int] = None
    description: Optional[str] = None
    created_by: Optional[int] = None


class JobJobDiagnosticRead(BaseModel):
    id: int
    sequence: int
    job: Union[int, JobRead]
    job_diagnostic: JobDiagnosticRead
    description: Optional[str] = None
    created_by: Optional[UserRead] = None 