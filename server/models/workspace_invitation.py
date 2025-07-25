from typing import TYPE_CHECKING

from edgy import fields
from datetime import datetime, timedelta, timezone
import secrets

from models.base import BaseModel
from models.mixins import WorkspaceableMixin


if TYPE_CHECKING:
    from models.workspace import Workspace


class WorkspaceInvitation(BaseModel, WorkspaceableMixin):
    class Meta:
        tablename = "workspace_invitations"
        label = "Invitation au workspace"
        label_plural = "Invitations au workspace"
        unique_together = [("workspace", "email")]
    email: str | None = fields.EmailField(max_length=255, label="Email invité") # type: ignore
    invitation_token: str | None = fields.CharField(max_length=64, unique=True, label="Token d'invitation") # type: ignore
    expires_at: datetime | None = fields.DateTimeField(label="Date d'expiration") # type: ignore
    used_at: datetime | None = fields.DateTimeField(null=True, label="Date d'utilisation") # type: ignore

    @classmethod
    async def create_invitation(cls, workspace: "Workspace", email: str) -> "WorkspaceInvitation":
        token = cls.generate_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        invitation = cls(
            workspace=workspace,
            email=email,
            invitation_token=token,
            expires_at=expires_at
        )
        await invitation.save()
        return invitation

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    def is_expired(self) -> bool:
        if not self.expires_at:
            return True
        return datetime.now(timezone.utc) > self.expires_at

    def is_used(self) -> bool:
        return self.used_at is not None

    async def mark_as_used(self):
        self.used_at = datetime.now(timezone.utc)
        await self.save()
