from edgy import fields

from core.api_route_model.decorators import admin_api_route_model
from core.metadata_model import metadata_model
from models.base import BaseModel


@metadata_model()
@admin_api_route_model()
class ServiceTax(BaseModel):
    class Meta:
        tablename = "service_taxes"
        label = "Taxe"
        label_plural = "Taxes"

    is_active: bool = fields.BooleanField(default=True, label="Actif")  # type: ignore
    name: str | None = fields.CharField(max_length=255, label="Nom")  # type: ignore
    rate: float | None = fields.FloatField(label="Pourcentage")  # type: ignore
    country_code: str | None = fields.CharField(max_length=2, null=True, label="Code pays")  # type: ignore
    description: str | None = fields.TextField(null=True, label="Description")  # type: ignore
    stripe_id: str | None = fields.CharField(max_length=255, null=True, unique=True, label="ID Stripe")  # type: ignore

    def __str__(self) -> str:
        return f"{self.name} ({self.rate}%)"
