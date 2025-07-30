import edgy
from edgy import fields
from datetime import datetime
from .base import BaseModel
from .mixins import WorkspaceableMixin
from .user import User
from .job import Job
from .job_task import JobTask

class JobJobTask(BaseModel, WorkspaceableMixin):
    name: str = edgy.CharField(max_length=255)
    sequence: int = edgy.IntegerField(default=0)
    description: str = edgy.TextField(null=True, blank=True)
    is_done: bool = edgy.BooleanField(default=False)
    done_at: datetime = edgy.DateTimeField(null=True, blank=True)
    done_by: User = edgy.ForeignKey(User, on_delete="SET NULL", null=True, blank=True)
    job: Job = edgy.ForeignKey(Job, on_delete="CASCADE")
    job_task: JobTask = edgy.ForeignKey(JobTask, on_delete="CASCADE")

    class Meta:
        tablename = "job_job_task" 