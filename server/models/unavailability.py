from edgy import fields
from enum import Enum
from datetime import datetime
from models.base import BaseModel
from models.user import User
from .mixins import WorkspaceableMixin

class UnavailabilityType(str, Enum):
    DISEASE = "disease"
    TRAINING = "training"
    PAID_LEAVE = "paid_leave"
    OTHER = "other"

class Unavailability(BaseModel, WorkspaceableMixin):
    class Meta:
        tablename = "unavailability"
        label = "Indisponibilité"
        label_plural = "Indisponibilités"

    start: datetime = fields.DateTimeField(label="Début")
    end: datetime = fields.DateTimeField(label="Fin")
    type: str = fields.ChoiceField(UnavailabilityType, label="Type")
    user: User = fields.ForeignKey(User, on_delete="CASCADE", label="Utilisateur")
    description: str | None = fields.TextField(null=True, blank=True, label="Description") 