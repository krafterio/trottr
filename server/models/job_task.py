import edgy
from edgy import fields
from .base import BaseModel
from .mixins import WorkspaceableMixin

class JobTask(BaseModel, WorkspaceableMixin):
    name: str = edgy.CharField(max_length=255)
    sequence: int = edgy.IntegerField(default=0)
    description: str = edgy.TextField(null=True, blank=True)
    default_price: float = edgy.FloatField(default=0.0)

    class Meta:
        tablename = "job_task" 