from edgy import fields

from core.api_route_model import api_route_model
from models.base import BaseModel
from models.mixins import WorkspaceableMixin, BlameableMixin
from models.job import Job

@api_route_model(
    list=True,
    get=True,
    export=False,
    create=False,
    patch=True,
    delete=True,
)
class JobAttachment(BaseModel, WorkspaceableMixin, BlameableMixin):
    class Meta:
        tablename = "job_attachments"

    job = fields.ForeignKey(
        "Job",
        on_delete="CASCADE",
        related_name="attachments",
        label="Job",
    )

    job_activity = fields.ForeignKey(
        "JobActivity",
        on_delete="CASCADE",
        related_name="attachments",
        label="Activité"
    )

    filename: str = fields.CharField(max_length=255, label="Nom du fichier")
    file_path: str = fields.CharField(max_length=500, label="Chemin du fichier")
    file_size: int = fields.IntegerField(label="Taille du fichier")
    mime_type: str = fields.CharField(max_length=100, label="Type MIME")
    file_extension: str = fields.CharField(max_length=10, label="Extension")
    is_image: bool = fields.BooleanField(default=False, label="Est une image")
