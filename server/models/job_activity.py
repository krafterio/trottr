import edgy
from edgy import fields
from enum import Enum

from core.api_route_model import api_route_model
from .base import BaseModel
from .mixins import WorkspaceableMixin, BlameableMixin
from .job import Job
from .user import User


class JobActivityType(str, Enum):
    MESSAGE = "message"
    NOTE = "note"
    TRACKING_CREATE = "tracking_create"
    TRACKING_UPDATE = "tracking_update"


class JobActivityValueType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    OBJECT = "object"


@api_route_model(
    list=True,
    get=True,
    export=False,
    create=False,
    patch=False,
    delete=False,
)
class JobActivity(BaseModel, WorkspaceableMixin, BlameableMixin):
    """Model for logging job activities and tracking changes"""
    
    class Meta:
        tablename = "job_activities"
        
    job = fields.ForeignKey(
        Job, 
        on_delete="CASCADE", 
        related_name="activities",
        label="Job"
    )
    
    type = fields.ChoiceField(
        JobActivityType,
        label="Type d'activité"
    )
    
    content = fields.TextField(
        null=True,
        blank=True,
        label="Contenu"
    )
    
    field_name = fields.CharField(
        max_length=255,
        null=True,
        blank=True,
        label="Nom du champ"
    )
    
    value_type = fields.ChoiceField(
        JobActivityValueType,
        null=True,
        blank=True,
        label="Type de valeur"
    )
    
    old_value = fields.TextField(
        null=True,
        blank=True,
        label="Ancienne valeur"
    )
    
    new_value = fields.TextField(
        null=True,
        blank=True,
        label="Nouvelle valeur"
    ) 
