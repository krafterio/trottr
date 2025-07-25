from pydantic import BaseModel, EmailStr
from datetime import datetime


class WorkspaceInvitationCreate(BaseModel):
    email: EmailStr


class WorkspaceInvitationResponse(BaseModel):
    message: str = "Invitation envoyée avec succès"


class WorkspaceInvitationDetails(BaseModel):
    id: int
    workspace_id: int
    email: EmailStr
    invitation_token: str
    expires_at: datetime
    used_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True 