from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime
from schemas.company import CompanyRead
from schemas.contact import ContactRead
from schemas.site import SiteRead
from schemas.user import User
from schemas.job_category import JobCategoryRead
from schemas.job_status import JobStatusRead

class JobBase(BaseModel):
    customer_reference: Optional[str] = None
    name: str
    description: Optional[str] = None
    customer_company: Optional[Union[int, dict]] = None
    customer_contact: Optional[Union[int, dict]] = None
    priority: str = "normal"
    site: Optional[Union[int, dict]] = None
    operator: Optional[Union[int, dict]] = None
    scheduled_start: Optional[Union[datetime, str]] = None
    scheduled_end: Optional[Union[datetime, str]] = None
    category: Optional[Union[int, dict]] = None
    status: Optional[Union[int, dict]] = None

    @field_validator('customer_company', 'customer_contact', 'site', 'operator', 'category', 'status', mode='before')
    @classmethod
    def extract_id(cls, v):
        if isinstance(v, dict) and 'id' in v:
            return v['id']
        return v

    @field_validator('scheduled_start', 'scheduled_end', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v

class JobCreate(JobBase):
    class Config:
        exclude = {"reference"}

class JobUpdate(BaseModel):
    customer_reference: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    customer_company: Optional[int] = None
    customer_contact: Optional[int] = None
    priority: Optional[str] = None
    site: Optional[int] = None
    operator: Optional[int] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    category: Optional[int] = None
    status: Optional[int] = None

class JobRead(JobBase):
    id: int
    reference: str
    created_at: datetime
    updated_at: datetime
    customer_company: Optional[CompanyRead] = None
    customer_contact: Optional[ContactRead] = None
    site: Optional[SiteRead] = None
    operator: Optional[User] = None
    category: Optional[JobCategoryRead] = None
    status: Optional[JobStatusRead] = None
    
    class Config:
        from_attributes = True 