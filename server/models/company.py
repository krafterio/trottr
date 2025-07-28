import edgy
from .base import BaseModel
from .country import Country
from enum import Enum
from edgy import fields


class CompanyType(str, Enum):
    CLIENT_FINAL = "client_final"
    REGIE_GESTIONNAIRE = "regie_gestionnaire"
    DONNEUR_ORDRE = "donneur_ordre"
    SOUS_TRAITANT = "sous_traitant"
    FOURNISSEUR = "fournisseur"
    AUTRE = "autre"


class Company(BaseModel):
    name = edgy.CharField(max_length=255)
    reference = edgy.CharField(max_length=100, null=True, blank=True)
    company_type: str | None = fields.ChoiceField(CompanyType, default=CompanyType.CLIENT_FINAL, label="Type de société") # type: ignore
    phone = edgy.CharField(max_length=20, null=True, blank=True)
    email = edgy.EmailField(null=True, blank=True)
    invoice_street = edgy.CharField(max_length=255, null=True, blank=True)
    invoice_zip = edgy.CharField(max_length=10, null=True, blank=True)
    invoice_city = edgy.CharField(max_length=100, null=True, blank=True)
    invoice_country = edgy.ForeignKey(Country, on_delete="CASCADE", null=True, blank=True)
    siret = edgy.CharField(max_length=14, null=True, blank=True)
    vat = edgy.CharField(max_length=20, null=True, blank=True)

    class Meta:
        tablename = "companies" 