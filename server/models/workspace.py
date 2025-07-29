from datetime import datetime, UTC
from typing import TYPE_CHECKING, Union

from edgy import fields
from edgy.core.signals import pre_save

from models.base import BaseModel
from models.country import Country
import string
import random
from enum import Enum


if TYPE_CHECKING:
    from models.user import User


class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"

class DefaultJobDuration(str, Enum):
    minutes_60 = "60"
    minutes_90 = "90"
    minutes_120 = "120"
    minutes_180 = "180"
    minutes_240 = "240"
    minutes_300 = "300"
    minutes_360 = "360"
    minutes_420 = "420"
    minutes_480 = "480"

class DefaultJobPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"

def generate_unique_id(length=8) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Workspace(BaseModel):
    class Meta:
        tablename = "workspaces"
        label = "Espace de travail"
        label_plural = "Espaces de travail"

    name: str | None = fields.CharField(max_length=255, label="Nom")
    unique_id: str | None = fields.CharField(max_length=8, unique=True, label="ID unique")
    image_url: str | None = fields.CharField(max_length=255, null=True, label="Image")
    currency: str | None = fields.CharField(max_length=20, default="EUR", label="Devise")
    street: str | None = fields.CharField(max_length=255, null=True, label="Adresse")
    street2: str | None = fields.CharField(max_length=255, null=True, label="Complément d'adresse")
    default_job_duration: str | None = fields.ChoiceField(DefaultJobDuration, default=DefaultJobDuration.minutes_60, label="Durée par défaut") # type: ignore
    default_job_priority: str | None = fields.ChoiceField(DefaultJobPriority, default=DefaultJobPriority.normal, label="Priorité par défaut") # type: ignore
    metadata = fields.JSONField(null=True, label="Métadonnées")
    zip: str | None = fields.CharField(max_length=20, null=True, label="Code postal")
    city: str | None = fields.CharField(max_length=255, null=True, label="Ville")
    country: Country | None = fields.ForeignKey(Country, null=True, on_delete="SET NULL", label="Pays")
    siren: str | None = fields.CharField(max_length=20, null=True, label="SIREN")
    vat: str | None = fields.CharField(max_length=30, null=True, label="Numéro TVA")
    dashboard_config: dict | None = fields.JSONField(null=True, exclude=True)
    stripe_customer_id: str | None = fields.CharField(max_length=255, null=True, unique=True, label="ID Client Stripe")
    trial_end: datetime | None = fields.DateTimeField(null=True, label="Fin essai")
    comply_with_local_privacy_laws: bool = fields.BooleanField(default=True, label="Je respecte les lois locales sur la confidentialité lors de la gestion des données de mes prospects")
    use_subsites: bool = fields.BooleanField(default=False, label="Utiliser la gestion des lots")
    use_diagnostics: bool = fields.BooleanField(default=False, label="Utiliser la gestion des diagnostics")

    @property
    def is_trial(self) -> bool:
        return bool(self.trial_end and self.trial_end > datetime.now(UTC))

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

