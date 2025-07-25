from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models.company import StaffRange


class UserInvitationCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    staff_range: Optional[StaffRange] = None


class UserInvitationUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    staff_range: Optional[StaffRange] = None
    invitation_code: Optional[str] = None


class UserInvitationResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    company: Optional[str] = None
    staff_range: Optional[StaffRange] = None
    invitation_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInvitationSendCode(BaseModel):
    message: str = "Code d'invitation envoyé avec succès"


class UserRegistrationWithCode(BaseModel):
    email: EmailStr
    name: str | None = None
    avatar: str | None = None
    password: str
    invitation_code: str
    recaptcha_token: str | None = None
