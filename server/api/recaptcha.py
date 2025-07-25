from fastapi import APIRouter, Depends
from core.config import get_settings, Settings

from schemas.recaptcha import RecaptchaConfig

router = APIRouter()


@router.get("/recaptcha/config")
async def get_recaptcha_config(settings: Settings = Depends(get_settings)) -> RecaptchaConfig:
    return RecaptchaConfig(
        enabled=settings.recaptcha_enabled,
        site_key=settings.recaptcha_site_key if settings.recaptcha_enabled else None
    )
