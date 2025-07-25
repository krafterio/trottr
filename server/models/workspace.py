from datetime import datetime, UTC
from typing import TYPE_CHECKING, Union

from edgy import fields
from edgy.core.signals import pre_save

from models.base import BaseModel
import string
import random
from enum import Enum


if TYPE_CHECKING:
    from models.user import User


class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"


def generate_unique_id(length=8) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Workspace(BaseModel):
    class Meta:
        tablename = "workspaces"
        label = "Espace de travail"
        label_plural = "Espaces de travail"

    name: str | None = fields.CharField(max_length=255, label="Nom") # type: ignore
    unique_id: str | None = fields.CharField(max_length=8, unique=True, label="ID unique") # type: ignore
    image_url: str | None = fields.CharField(max_length=255, null=True, label="Image") # type: ignore
    currency: str | None = fields.CharField(max_length=20, default="EUR", label="Devise") # type: ignore
    available_usage_credits: float = fields.FloatField(default=0.0, label="Credits disponibles")  # type: ignore
    plan_available_usage_credits: float = fields.FloatField(default=0.0, label="Crédits disponibles du plan")  # type: ignore
    pack_available_usage_credits: float = fields.FloatField(default=0.0, label="Crédits disponibles des packs")  # type: ignore
    current_usage_credits: float = fields.FloatField(default=0.0, label="Crédits utilisés")  # type: ignore
    plan_current_usage_credits: float = fields.FloatField(default=0.0, label="Crédits utilisés du plan")  # type: ignore
    pack_current_usage_credits: float = fields.FloatField(default=0.0, label="Crédits utilisés des packs")  # type: ignore
    reset_usage_date: datetime | None = fields.DateTimeField(null=True, label="Date de réinitialisation des crédits")  # type: ignore
    dashboard_config: dict | None = fields.JSONField(null=True, exclude=True)  # type: ignore
    stripe_customer_id: str | None = fields.CharField(max_length=255, null=True, unique=True, label="ID Client Stripe")  # type: ignore
    trial_end: datetime | None = fields.DateTimeField(null=True, label="Fin essai")  # type: ignore
    comply_with_local_privacy_laws: bool = fields.BooleanField(default=True, label="Je respecte les lois locales sur la confidentialité lors de la gestion des données de mes prospects") # type: ignore
    icp: str | None = fields.TextField(null=True, label="ICP (Ideal Customer Profile)") # type: ignore

    @property
    def is_trial(self) -> bool:
        return bool(self.trial_end and self.trial_end > datetime.now(UTC))

    @property
    def remaining_usage_credits(self) -> float:
        return self.plan_remaining_usage_credits + self.pack_remaining_usage_credits

    @property
    def plan_remaining_usage_credits(self) -> float:
        return self.plan_available_usage_credits - self.plan_current_usage_credits

    @property
    def pack_remaining_usage_credits(self) -> float:
        return self.pack_available_usage_credits - self.pack_current_usage_credits



    @classmethod
    async def create_default(cls, owner: "User") -> "Workspace":
        unique_id = generate_unique_id()
        workspace = cls(
            name="",
            unique_id=unique_id,
        )
        await workspace.save()

        from models.workspace_user import WorkspaceUser
        await WorkspaceUser.create_owner(workspace, owner)

        return workspace

    async def get_owner(self):
        from models.workspace_user import WorkspaceUserRole

        workspace_user = await self.workspace_users.filter(role=WorkspaceUserRole.OWNER).first()
        if workspace_user:
            return workspace_user.user
        return None

    async def get_members(self) -> list["User"]:
        members = []
        workspace_users = await self.workspace_users.all()
        for workspace_user in workspace_users:
            members.append(workspace_user.user)
        return members

    async def get_members_with_roles(self) -> list[dict[str, Union["User", str]]]:
        members_with_roles = []
        workspace_users = await self.workspace_users.all()
        for workspace_user in workspace_users:
            members_with_roles.append({
                "user": workspace_user.user,
                "role": workspace_user.role
            })
        return members_with_roles


@pre_save.connect_via(Workspace)
async def update_available_usage_credits(_, instance, values, column_values, **kwargs) -> None:
    """Update available_usage_credits as the sum of plan and pack credits before saving."""
    if "plan_available_usage_credits" in values or "pack_available_usage_credits" in values:
        plan_credits = values.get("plan_available_usage_credits", instance.plan_available_usage_credits)
        pack_credits = values.get("pack_available_usage_credits", instance.pack_available_usage_credits)
        total_credits = plan_credits + pack_credits

        values["available_usage_credits"] = total_credits
        column_values["available_usage_credits"] = total_credits
        instance.available_usage_credits = total_credits


@pre_save.connect_via(Workspace)
async def update_current_usage_credits(_, instance, values, column_values, **kwargs) -> None:
    """Update current_usage_credits as the sum of plan and pack credits before saving."""
    if "plan_current_usage_credits" in values or "pack_current_usage_credits" in values:
        plan_credits = values.get("plan_current_usage_credits", instance.plan_current_usage_credits)
        pack_credits = values.get("pack_current_usage_credits", instance.pack_current_usage_credits)
        total_credits = plan_credits + pack_credits

        values["current_usage_credits"] = total_credits
        column_values["current_usage_credits"] = total_credits
        instance.current_usage_credits = total_credits
