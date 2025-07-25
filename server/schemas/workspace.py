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


class WorkspaceBase(BaseModel):
    name: str
    unique_id: str


class WorkspaceCreate(BaseModel):
    name: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    currency: Currency | None = None
    comply_with_local_privacy_laws: bool = False
    icp: str | None = None


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
    selected_plan: str
    available_plans: list[str]
    owner: UserRead | None = None
    member_count: int = Field(default=0, description="Nombre de membres dans le workspace")
    available_usage_credits: float
    plan_available_usage_credits: float
    pack_available_usage_credits: float
    current_usage_credits: float
    plan_current_usage_credits: float
    pack_current_usage_credits: float
    remaining_usage_credits: float
    plan_remaining_usage_credits: float
    pack_remaining_usage_credits: float
    comply_with_local_privacy_laws: bool
    trial_end: datetime | None = None
    is_trial: bool
    icp: str | None = None

    class Config:
        from_attributes = True
