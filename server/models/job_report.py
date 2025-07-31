import edgy
from .base import BaseModel
from .user import User
from .job import Job
from .mixins import WorkspaceableMixin
from edgy import fields

class JobReport(BaseModel,WorkspaceableMixin):
    name: str = edgy.CharField(max_length=255)
    content: str = edgy.CharField(max_length=1000)
    include_diagnostics: bool = edgy.BooleanField(default=True)
    include_tasks: bool = edgy.BooleanField(default=True)
    job = edgy.ForeignKey(Job, on_delete="CASCADE")
    created_by = edgy.ForeignKey(User, on_delete="CASCADE")
    customer_signature: str | None = edgy.TextField(null=True, blank=True)
    operator_signature: str | None = edgy.TextField(null=True, blank=True)
    
    class Meta:
        tablename = "job_reports" 