from typing import TYPE_CHECKING, Union

from edgy import fields

from core.config import get_settings
from models.base import BaseModel
from enum import Enum

from services.websocket import connection_manager


if TYPE_CHECKING:
    from models.workspace import Workspace
    from models.user import User


class WorkspaceUserRole(str, Enum):
    OWNER = "Owner"
    MEMBER = "Member"

class WorkspaceUser(BaseModel):
    """Model for managing workspace users and their roles"""
    class Meta:
        tablename = "workspace_users"
        label = "Utilisateur de l'espace de travail"
        label_plural = "Utilisateurs de l'espace de travail"
        unique_together = [("workspace", "user")]

    workspace: Union["Workspace", None] = fields.ForeignKey('Workspace', on_delete='CASCADE', related_name='workspace_users', label="Espace de travail") # type: ignore
    user: Union["User", None] = fields.ForeignKey('User', on_delete='CASCADE', related_name='workspace_memberships', label="Utilisateur") # type: ignore
    role: str | None = fields.ChoiceField(WorkspaceUserRole, default=WorkspaceUserRole.MEMBER, label="Rôle") # type: ignore

    @classmethod
    async def create_owner(cls, workspace: "Workspace", user: "User") -> "WorkspaceUser":
        """Create a workspace user with Owner role"""
        workspace_user = cls(
            workspace=workspace,
            user=user,
            role=WorkspaceUserRole.OWNER
        )
        await workspace_user.save()
        return workspace_user

    @classmethod
    async def create_member(cls, workspace: "Workspace", user: "User") -> "WorkspaceUser":
        """Create a workspace user with Member role"""
        settings = get_settings()
        workspace_user = cls(
            workspace=workspace,
            user=user,
            role=WorkspaceUserRole.MEMBER
        )
        await workspace_user.save()

        active_users_count = await WorkspaceUser.query.select_related('user').filter(
            workspace=workspace,
            user__is_active=True
        ).count()

        return workspace_user
