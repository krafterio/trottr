import random
import string
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from models.user import User
from services.mail import MailService
from core.config import get_settings


def generate_verification_code() -> str:
    return ''.join(random.choices(string.digits, k=6))


async def create_verification_code(user: User) -> str:
    code = generate_verification_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    user.verification_code = code
    user.verification_code_expires_at = expires_at
    await user.save()
    
    return code


async def verify_code(user: User, code: str) -> bool:
    if not user.verification_code or not user.verification_code_expires_at:
        return False
    
    if user.verification_code != code:
        return False
    
    if datetime.now(timezone.utc) > user.verification_code_expires_at:
        return False
    
    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires_at = None
    await user.save()
    
    return True


async def send_verification_email(user: User, code: str, mail_service: MailService, template_name: str = "emails/verification_email.html"):
    email = EmailMessage()
    email['To'] = user.email
    
    template_vars = {
        'customer_name': user.name or (user.email.split('@')[0] if user.email else 'Utilisateur'),
        'verification_code': code,
        'app_name': 'Trottr',
        'settings': get_settings(),
    }
    
    await mail_service.send_template(template_name, template_vars, email)


async def resend_verification_code(user: User, mail_service: MailService, template_name: str = "emails/verification_email.html") -> str:
    code = await create_verification_code(user)
    await send_verification_email(user, code, mail_service, template_name)
    return code 