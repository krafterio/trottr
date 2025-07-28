import edgy
from .base import BaseModel
from .country import Country
from .company import Company
from .contact import Contact
from .mixins import WorkspaceableMixin
from enum import Enum
from edgy import fields

class BuildingType(str, Enum):
    RESIDENCE_COLLECTIVE = "residence_collective"
    MAISON_INDIVIDUELLE = "maison_individuelle"
    BATIMENT_TERTIAIRE = "batiment_tertiaire"
    LOCAL_COMMERCIAL = "local_commercial"
    AUTRE = "autre"

class Site(BaseModel, WorkspaceableMixin):
    name: str = edgy.CharField(max_length=255)
    street: str = edgy.CharField(max_length=255)
    street_2: str = edgy.CharField(max_length=255, null=True, blank=True)
    zip: str = edgy.CharField(max_length=20)
    city: str = edgy.CharField(max_length=255)
    country = edgy.ForeignKey(Country, on_delete="SET NULL", null=True, blank=True)
    building_type: str = fields.ChoiceField(BuildingType, default=BuildingType.AUTRE, label="Type de bâtiment") # type: ignore
    company = edgy.ForeignKey(Company, on_delete="SET NULL", null=True, blank=True)
    contact = edgy.ForeignKey(Contact, on_delete="SET NULL", null=True, blank=True)
    access_info: str = edgy.TextField(null=True, blank=True)
    
    class Meta:
        tablename = "site" 