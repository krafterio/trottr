from pydantic import BaseModel, Field
from typing import Optional


class JobSpecialityCreate(BaseModel):
    sequence: int = Field(..., description="Séquence")
    color: str = Field(..., max_length=7, description="Couleur (hex)")
    name: str = Field(..., max_length=255, description="Nom")


class JobSpecialityUpdate(BaseModel):
    sequence: Optional[int] = Field(None, description="Séquence")
    color: Optional[str] = Field(None, max_length=7, description="Couleur (hex)")
    name: Optional[str] = Field(None, max_length=255, description="Nom")


class JobSpecialityRead(BaseModel):
    id: int
    sequence: int
    color: str
    name: str 