from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    name: str | None = None
    avatar: str | None = None
    password: str
    invitation_code: str | None = None
    workspace_invitation_token: str | None = None
    recaptcha_token: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr
    name: str | None = None
    avatar: str | None = None


class UserLoginPassword(BaseModel):
    email: EmailStr
    password: str
    recaptcha_token: str | None = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class VerificationCode(BaseModel):
    email: EmailStr
    code: str


class ResendVerificationCode(BaseModel):
    email: EmailStr


class VerificationResponse(BaseModel):
    message: str
    verified: bool = False


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: 'User'


class RefreshToken(BaseModel):
    refresh_token: str


class PasswordUpdateResponse(BaseModel):
    message: str = "Password updated successfully"


class PasswordResetRequest(BaseModel):
    email: EmailStr
    recaptcha_token: str | None = None


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class PasswordResetResponse(BaseModel):
    message: str


class User(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    avatar: str | None = None
    initials: str | None = None
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
