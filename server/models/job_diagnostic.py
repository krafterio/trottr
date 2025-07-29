from edgy import fields

from .base import BaseModel
from .mixins import WorkspaceableMixin


class JobDiagnostic(BaseModel, WorkspaceableMixin):
    sequence: int = fields.IntegerField(label="Séquence")
    name: str = fields.CharField(max_length=255, label="Nom")
    description: str = fields.TextField(label="Description")

    class Meta:
        tablename = "job_diagnostics" 