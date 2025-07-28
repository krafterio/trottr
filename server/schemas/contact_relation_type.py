from pydantic import BaseModel, Field
from typing import Optional


class ContactRelationTypeCreate(BaseModel):
    sequence: int = Field(..., description="Séquence")
    name: str = Field(..., max_length=255, description="Nom")


class ContactRelationTypeUpdate(BaseModel):
    sequence: Optional[int] = Field(None, description="Séquence")
    name: Optional[str] = Field(None, max_length=255, description="Nom")


class ContactRelationTypeRead(BaseModel):
    id: int
    sequence: int
    name: str 