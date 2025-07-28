from edgy import fields

from .base import BaseModel
from .mixins import WorkspaceableMixin


class JobCategory(BaseModel, WorkspaceableMixin):
    sequence: int = fields.IntegerField(label="Séquence")
    color: str = fields.CharField(max_length=7, label="Couleur")
    name: str = fields.CharField(max_length=255, label="Nom")

    class Meta:
        tablename = "job_categories" 