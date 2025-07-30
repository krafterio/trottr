from datetime import datetime
from pydantic import BaseModel, Field
from models.workspace_user import WorkspaceUserRole
from models.workspace import Currency, DefaultJobDuration, DefaultJobPriority


class CountryRead(BaseModel):
    id: int
    name: str
    iso_code: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    email: str
    initials: str | None = None
    name: str | None = None
    avatar: str | None = None

    class Config:
        from_attributes = True


class WorkspaceCreate(BaseModel):
    name: str
    currency: Currency = Currency.EUR
    unique_id: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    currency: Currency | None = None
    street: str | None = None
    street2: str | None = None
    zip: str | None = None
    city: str | None = None
    country_id: int | None = None
    siren: str | None = None
    vat: str | None = None
    comply_with_local_privacy_laws: bool | None = None
    default_job_duration: DefaultJobDuration | None = None
    default_job_priority: DefaultJobPriority | None = None
    use_subsites: bool | None = None
    use_diagnostics: bool | None = None

class WorkspaceUserRead(UserRead):
    role: WorkspaceUserRole


class WorkspaceUserWithRole(BaseModel):
    user: UserRead
    role: WorkspaceUserRole

    class Config:
        from_attributes = True


class WorkspaceRead(BaseModel):
    id: int
    name: str
    unique_id: str
    image_url: str | None
    currency: str
    street: str | None = None
    street2: str | None = None
    zip: str | None = None
    city: str | None = None
    country: CountryRead | None = None
    siren: str | None = None
    vat: str | None = None
    owner: UserRead | None = None
    available_member_count: int
    member_count: int = Field(default=0, description="Nombre de membres dans le workspace")
    comply_with_local_privacy_laws: bool
    trial_end: datetime | None = None
    is_trial: bool
    is_valid: bool
    default_job_duration: DefaultJobDuration | None = None
    default_job_priority: DefaultJobPriority | None = None
    use_subsites: bool
    use_diagnostics: bool
    
    class Config:
        from_attributes = True
