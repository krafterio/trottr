from pydantic import BaseModel, Field
from typing import Optional


class JobStatusCreate(BaseModel):
    sequence: int = Field(..., description="Séquence")
    color: str = Field(..., max_length=7, description="Couleur (hex)")
    name: str = Field(..., max_length=255, description="Nom")


class JobStatusUpdate(BaseModel):
    sequence: Optional[int] = Field(None, description="Séquence")
    color: Optional[str] = Field(None, max_length=7, description="Couleur (hex)")
    name: Optional[str] = Field(None, max_length=255, description="Nom")


class JobStatusRead(BaseModel):
    id: int
    sequence: int
    color: str
    name: str 