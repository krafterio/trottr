from edgy import fields

from .base import BaseModel
from .mixins import WorkspaceableMixin


class ContactRelationType(BaseModel, WorkspaceableMixin):
    sequence: int = fields.IntegerField(label="Séquence")
    name: str = fields.CharField(max_length=255, label="Nom")

    class Meta:
        tablename = "contact_relation_types" 