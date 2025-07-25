from datetime import datetime
from typing import Union, TYPE_CHECKING

from edgy import fields
from models.base import BaseModel


if TYPE_CHECKING:
    from models.user import User


class UserRefreshToken(BaseModel):
    """Refresh token model for OAuth2 authentication"""

    class Meta:
        tablename = "user_refresh_tokens"
        label = "Token de rafraîchissement"
        label_plural = "Tokens de rafraîchissement"

    token: str | None = fields.CharField(max_length=256, unique=True, label="Token") # type: ignore
    user: Union["User", None] = fields.ForeignKey("User", on_delete="CASCADE", related_name="refresh_tokens", label="Utilisateur") # type: ignore
    expires_at: datetime | None = fields.DateTimeField(label="Expire le") # type: ignore
    revoked: bool | None = fields.BooleanField(default=False, label="Revoqué") # type: ignore
