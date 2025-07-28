from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union
from datetime import datetime

class CompanyRead(BaseModel):
    id: int
    name: str
    reference: Optional[str] = None
    company_type: str
    
    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    function: Optional[str] = None
    company: Optional[int] = None
    email: Union[EmailStr, str, None] = None
    mobile: Optional[str] = None
    phone: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        if '@' not in v:
            raise ValueError('Email invalide')
        return v

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    function: Optional[str] = None
    company: Optional[int] = None
    email: Union[EmailStr, str, None] = None
    mobile: Optional[str] = None
    phone: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        if '@' not in v:
            raise ValueError('Email invalide')
        return v

class ContactRead(ContactBase):
    id: int
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    company: Optional[CompanyRead] = None
    
    class Config:
        from_attributes = True 