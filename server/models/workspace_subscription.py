from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Union

from edgy import fields
from enum import Enum
from edgy.core.signals import pre_save

from core.api_route_model.decorators import admin_api_route_model
from core.metadata_model import metadata_model
from models.base import BaseModel


if TYPE_CHECKING:
    from models.workspace import Workspace
    from models.service_plan import ServicePlan


class SubscriptionStatus(str, Enum):
    incomplete = "incomplete"
    incomplete_expired = "incomplete_expired"
    trialing = "trialing"
    active = "active"
    past_due = "past_due"
    canceled = "canceled"
    unpaid = "unpaid"
    paused = "paused"


@metadata_model()
@admin_api_route_model()
class WorkspaceSubscription(BaseModel):
    class Meta:
        tablename = "workspace_subscriptions"
        label = "Abonnement d'espace de travail"
        label_plural = "Abonnements d'espaces de travail"

    workspace: Union["Workspace", None] = fields.ForeignKey("Workspace", related_name="subscriptions", null=True, on_delete="SET NULL", label="Espace de travail")  # type: ignore
    service_plan: Union["ServicePlan", None] = fields.ForeignKey("ServicePlan", related_name="subscriptions", label="Plan")  # type: ignore
    stripe_subscription_id: str | None = fields.CharField(max_length=255, unique=True, label="ID Abonnement Stripe")  # type: ignore
    stripe_customer_id: str | None = fields.CharField(max_length=255, label="ID Client Stripe")  # type: ignore
    status: SubscriptionStatus | None = fields.ChoiceField(SubscriptionStatus, label="Statut")  # type: ignore
    available_users_count: int = fields.IntegerField(default=1, label="Nombre d'utilisateurs disponibles")  # type: ignore
    start_date: datetime | None = fields.DateTimeField(null=True, label="Début")  # type: ignore
    end_date: datetime | None = fields.DateTimeField(null=True, label="Fin")  # type: ignore
    trial_start: datetime | None = fields.DateTimeField(null=True, label="Début essai")  # type: ignore
    trial_end: datetime | None = fields.DateTimeField(null=True, label="Fin essai")  # type: ignore
    cancel_at_period_end: bool = fields.BooleanField(default=False, label="Annuler en fin de période")  # type: ignore
    canceled_at: datetime | None = fields.DateTimeField(null=True, label="Annulé le")  # type: ignore
    is_active: bool = fields.BooleanField(default=True, label="Actif")  # type: ignore

    def __str__(self) -> str:
        return f"Abonnement {self.workspace.name if self.workspace else 'N/A'} - {self.service_plan.name if self.service_plan else 'N/A'}"

    @property
    def is_trial(self) -> bool:
        if not self.trial_start or not self.trial_end:
            return False

        now = datetime.now()

        return self.trial_start <= now <= self.trial_end

    @property
    def is_subscription_active(self) -> bool:
        return self.status in [SubscriptionStatus.active, SubscriptionStatus.trialing]

    @property
    def next_billing_date(self) -> datetime | None:
        current_date = datetime.now(timezone.utc)
        next_billing_date = None

        if self.trial_end and self.trial_end > current_date:
            next_billing_date = self.trial_end
        elif self.end_date:
            next_billing_date = self.end_date
        elif self.start_date and self.service_plan:
            if self.service_plan.period.value == "Mensuel":
                next_billing_date = self.start_date + timedelta(days=30)
            else:
                next_billing_date = self.start_date + timedelta(days=365)

        return next_billing_date


@pre_save.connect_via(WorkspaceSubscription)
async def update_workspace_plan(_, instance: WorkspaceSubscription, **kwargs) -> None:
    if hasattr(instance, "workspace") and instance.workspace:
        await instance.workspace.load()
        workspace = instance.workspace

        if hasattr(instance, "service_plan") and instance.service_plan:
            workspace.service_plan = instance.service_plan

        workspace.trial_end = instance.trial_end
        await workspace.save()
