from datetime import datetime, timedelta, timezone
from typing import Tuple
from jose import jwt
import bcrypt
import secrets
from core.config import get_settings
from models.user_refresh_token import UserRefreshToken
from models.user import User


settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        return False


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


async def store_refresh_token(user: User, token: str, expires_delta: timedelta) -> UserRefreshToken:
    expires_at = datetime.now() + expires_delta
    refresh_token = await UserRefreshToken.query.create(
        token=token,
        user=user,
        expires_at=expires_at,
        revoked=False
    )
    return refresh_token


async def authenticate_user(email: str, password: str) -> User | None:
    user = await User.query.filter(email=email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def verify_refresh_token(token: str) -> User | None:
    refresh_token = await UserRefreshToken.query.filter(
        token=token,
        revoked=False,
        expires_at__gt=datetime.now()
    ).first()
    
    if not refresh_token:
        return None
    
    user = await User.query.get(id=refresh_token.user.id)
    return user


async def create_tokens(user: User) -> Tuple[str, str, int]:
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token()
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    await store_refresh_token(user, refresh_token, refresh_token_expires)
    
    return access_token, refresh_token, settings.access_token_expire_minutes * 60


async def revoke_refresh_token(token: str) -> bool:
    await UserRefreshToken.query.filter(token=token).update(revoked=True)
    return True
