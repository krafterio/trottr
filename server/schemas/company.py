from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union
from datetime import datetime

class CountryRead(BaseModel):
    id: int
    name: str
    iso_code: str

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    reference: Optional[str] = None
    company_type: str
    phone: Optional[str] = None
    email: Union[EmailStr, str, None] = None
    invoice_street: Optional[str] = None
    invoice_zip: Optional[str] = None
    invoice_city: Optional[str] = None
    invoice_country_id: Optional[int] = None
    siret: Optional[str] = None
    vat: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        # Si l'email n'est pas vide, on valide qu'il est correct
        if '@' not in v:
            raise ValueError('Email invalide')
        return v


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    reference: Optional[str] = None
    company_type: Optional[str] = None
    phone: Optional[str] = None
    email: Union[EmailStr, str, None] = None
    invoice_street: Optional[str] = None
    invoice_zip: Optional[str] = None
    invoice_city: Optional[str] = None
    invoice_country_id: Optional[int] = None
    siret: Optional[str] = None
    vat: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        # Si l'email n'est pas vide, on valide qu'il est correct
        if '@' not in v:
            raise ValueError('Email invalide')
        return v


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    invoice_country: Optional[CountryRead] = None
    
    class Config:
        from_attributes = True 