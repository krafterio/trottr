from pydantic import BaseModel


class RecaptchaConfig(BaseModel):
    enabled: bool
    site_key: str | None = None
