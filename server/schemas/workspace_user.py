from pydantic import BaseModel
from datetime import datetime
from .user import User
from enum import Enum


class WorkspaceUserRole(str, Enum):
    OWNER = "Owner"
    MEMBER = "Member"


class WorkspaceUserBase(BaseModel):
    role: WorkspaceUserRole


class WorkspaceUserCreate(WorkspaceUserBase):
    user_id: int
    workspace_id: int


class WorkspaceUserUpdate(BaseModel):
    role: WorkspaceUserRole | None = None


class WorkspaceUserRead(WorkspaceUserBase):
    id: int
    user: User
    workspace_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
