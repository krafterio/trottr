from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.country import CountryResponse
from schemas.company import CompanyRead

class SiteBase(BaseModel):
    name: str
    street: str
    street_2: Optional[str] = None
    zip: str
    city: str
    building_type: str

class SiteCreate(SiteBase):
    country_id: int
    company_id: Optional[int] = None

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    street_2: Optional[str] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    building_type: Optional[str] = None
    company_id: Optional[int] = None

class SiteRead(SiteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    country_id: Optional[int] = None
    company_id: Optional[int] = None
    country: Optional[CountryResponse] = None
    company: Optional[CompanyRead] = None
    
    class Config:
        from_attributes = True 