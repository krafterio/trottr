import edgy
from edgy import fields
from enum import Enum
from .base import BaseModel
from .mixins import WorkspaceableMixin
from .company import Company
from .contact import Contact
from .site import Site
from .user import User
from .job_category import JobCategory
from .job_status import JobStatus
import string
import random

class JobPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class Job(BaseModel, WorkspaceableMixin):
    reference: str = edgy.CharField(max_length=6, unique=True, null=True, blank=True)
    customer_reference: str = edgy.CharField(max_length=255, null=True, blank=True)
    name: str = edgy.CharField(max_length=255)
    description: str = edgy.TextField(null=True, blank=True)
    customer_company: Company = edgy.ForeignKey(Company, on_delete="CASCADE", null=True, blank=True)
    customer_contact: Contact = edgy.ForeignKey(Contact, on_delete="SET NULL", null=True, blank=True)
    priority: str = fields.ChoiceField(JobPriority, default=JobPriority.NORMAL, label="Priorité")
    site: Site = edgy.ForeignKey(Site, on_delete="SET NULL", null=True, blank=True)
    operator: User = edgy.ForeignKey(User, on_delete="SET NULL", null=True, blank=True)
    scheduled_start: str = edgy.DateTimeField(null=True, blank=True)
    scheduled_end: str = edgy.DateTimeField(null=True, blank=True)
    category: JobCategory = edgy.ForeignKey(JobCategory, on_delete="SET NULL", null=True, blank=True)
    status: JobStatus = edgy.ForeignKey(JobStatus, on_delete="SET NULL", null=True, blank=True)

    class Meta:
        tablename = "job"

    def generate_reference(self, workspace_id: int) -> str:
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=6))

    async def save(self, *args, **kwargs):
        if not hasattr(self, 'reference') or not self.reference:
            if hasattr(self, 'workspace') and self.workspace:
                while True:
                    reference = self.generate_reference(self.workspace.id)
                    existing = await Job.query.filter(reference=reference, workspace=self.workspace).first()
                    if not existing:
                        self.reference = reference
                        break
            else:
                raise ValueError("workspace is required to generate reference")
        return await super().save(*args, **kwargs) 