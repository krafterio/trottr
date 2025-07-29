import edgy
from .base import BaseModel
from .job import Job
from .job_diagnostic import JobDiagnostic
from .user import User


class JobJobDiagnostic(BaseModel):
    sequence: int = edgy.IntegerField()
    job: Job = edgy.ForeignKey(Job, on_delete="CASCADE")
    job_diagnostic: JobDiagnostic = edgy.ForeignKey(JobDiagnostic, on_delete="CASCADE")
    description: str = edgy.TextField(null=True, blank=True)
    created_by: User = edgy.ForeignKey(User, on_delete="SET NULL", null=True, blank=True)

    class Meta:
        tablename = "job_job_diagnostic" 