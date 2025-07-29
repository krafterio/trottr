from pydantic import BaseModel, Field
from typing import Optional


class JobDiagnosticCreate(BaseModel):
    sequence: Optional[int] = Field(None, description="Séquence")
    name: str = Field(..., max_length=255, description="Nom")
    description: str = Field(..., description="Description")


class JobDiagnosticUpdate(BaseModel):
    sequence: Optional[int] = Field(None, description="Séquence")
    name: Optional[str] = Field(None, max_length=255, description="Nom")
    description: Optional[str] = Field(None, description="Description")


class JobDiagnosticRead(BaseModel):
    id: int
    sequence: int
    name: str
    description: str