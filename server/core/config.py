import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from urllib.parse import urlparse

from core.logger import LogFormat, LogLevel, LogOutput


class Settings(BaseSettings):
    title: str = 'Trottr'
    database_url: str = ''
    database_pool_size: int = 20
    database_max_overflow: int = 10
    secret_key: str = ''
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    dataforseo_api_token: str = ''
    dataforseo_api_production: bool = False
    debug_admin: bool = False
    debug_simulate_contact_enrichment: bool = False
    debug_simulate_company_enrichment: bool = False
    base_url: str = ''
    base_url_email: str = ''
    smtp_host: str = ''
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_username: str = ''
    smtp_password: str = ''
    smtp_default_from: str = ''
    http_workers: int | None = None
    log_level: LogLevel = LogLevel.INFO
    log_output: LogOutput = LogOutput.CONSOLE
    log_format: LogFormat | str = LogFormat.TEXT_LIGHT
    log_file: str = ''
    stripe_enabled: bool = False
    stripe_publishable_key: str = ''
    stripe_secret_key: str = ''
    stripe_webhook_secret: str = ''
    recaptcha_enabled: bool = False
    recaptcha_site_key: str | None = None
    recaptcha_secret_key: str | None = None
    recaptcha_min_score: float = 0.5
    mode_preview: bool = False
    mode_preview_notif_email: str | None = None
    data_path: str | None = None

    google_client_id: str = ''
    google_client_secret: str = ''
    google_redirect_uri: str = ''

    sxng_url: str = ''
    assembly_ai_token: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        env_prefix='',
        extra='ignore',
    )

    @field_validator('log_format')
    def validate_log_format(cls, v):
        if isinstance(v, str) and v in [item.value for item in LogFormat]:
            return LogFormat(v)
        return v

    @property
    def db_name(self) -> str:
        return urlparse(self.database_url).path.lstrip('/')

    @property
    def project_dir(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @property
    def log_file_path(self) -> str:
        return self.log_file or os.path.join(self.project_dir, "logs", "trottr.log")

    @property
    def storage_data_path(self) -> str:
        return self.data_path or os.path.join(self.project_dir, "data")

    @property
    def subscription_stripe_enabled(self):
        return (self.stripe_enabled
            and self.stripe_publishable_key
            and self.stripe_secret_key
            and self.stripe_webhook_secret
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
