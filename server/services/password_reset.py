import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from models.user import User
from services.mail import MailService
from core.config import get_settings


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


async def create_password_reset_token(user: User) -> str:
    token = generate_reset_token()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    user.password_reset_token = token
    user.password_reset_expires_at = expires_at
    await user.save()

    return token


async def verify_reset_token(token: str) -> Optional[User]:
    user = await User.query.filter(password_reset_token=token).first()

    if not user or not user.password_reset_expires_at:
        return None

    if datetime.now(timezone.utc) > user.password_reset_expires_at:
        user.password_reset_token = None
        user.password_reset_expires_at = None
        await user.save()
        return None

    return user


async def reset_password_with_token(token: str, new_password: str) -> bool:
    from services.auth import get_password_hash

    user = await verify_reset_token(token)
    if not user:
        return False

    user.password = get_password_hash(new_password)
    user.password_reset_token = None
    user.password_reset_expires_at = None
    await user.save()

    return True


async def send_password_reset_email(user: User, token: str, mail_service: MailService):
    settings = get_settings()
    reset_url = f"{settings.base_url_email}/reset-password?token={token}"

    template_vars = {
        'customer_name': user.name or (user.email.split('@')[0] if user.email else 'Utilisateur'),
        'reset_url': reset_url,
        'app_name': 'Trottr',
        'settings': settings,
    }

    await mail_service.send_template(
        template_name="emails/password_reset.html",
        tpl_vals=template_vars,
        email_parts={"To": user.email}
    )
