from edgy import fields
from enum import Enum

from core.api_route_model.decorators import admin_api_route_model
from core.metadata_model import metadata_model
from models.base import BaseModel


class ServicePlanType(str, Enum):
    essential = "Essential"
    advanced = "Advanced"
    business = "Business"


class ServicePlanPeriod(str, Enum):
    monthly = "Mensuel"
    yearly = "Annuel"


@metadata_model()
@admin_api_route_model()
class ServicePlan(BaseModel):
    class Meta:
        tablename = "service_plans"
        label = "Plan"
        label_plural = "Plans"
        unique_together = [
            ("type", "period"),
            ("stripe_product_id", "stripe_price_id"),
        ]

    is_active: bool = fields.BooleanField(default=True, label="Actif")  # type: ignore
    name: str | None = fields.CharField(max_length=255, label="Nom")  # type: ignore
    type: ServicePlanType | None = fields.ChoiceField(ServicePlanType, label="Type")  # type: ignore
    period: ServicePlanPeriod | None = fields.ChoiceField(ServicePlanPeriod, label="Periode")  # type: ignore
    price: float | None = fields.FloatField(label="Prix")  # type: ignore
    currency: str | None = fields.CharField(max_length=3, default="EUR", label="Devise")  # type: ignore
    description: str | None = fields.TextField(null=True, label="Description")  # type: ignore
    stripe_product_id: str | None = fields.CharField(max_length=255, null=True, label="ID Produit Stripe")  # type: ignore
    stripe_price_id: str | None = fields.CharField(max_length=255, null=True, label="ID Prix Stripe")  # type: ignore

    def __str__(self) -> str:
        return f"{self.name} ({self.type})" 
