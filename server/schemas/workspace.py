from datetime import datetime
from pydantic import BaseModel, Field
from models.workspace_user import WorkspaceUserRole
from models.workspace import Currency


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
    comply_with_local_privacy_laws: bool | None = None


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
    owner: UserRead | None = None
    member_count: int = Field(default=0, description="Nombre de membres dans le workspace")
    comply_with_local_privacy_laws: bool
    trial_end: datetime | None = None
    is_trial: bool

    class Config:
        from_attributes = True
