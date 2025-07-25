from edgy import fields, Model
from typing import Any

from pydantic import ConfigDict, model_validator

from core import context


class WorkspaceableMixin(Model):
    """
    Mixin to automatically add a workspace relationship field.
    
    This mixin adds a foreign key relationship to the Workspace model, making it easy
    to associate any model with a specific workspace.
    
    Usage:
        class MyModel(BaseModel, WorkspaceableMixin):
            # Your model fields here
            pass
    """
    class Meta:
        abstract = True

    model_config = ConfigDict(
        extra='ignore',
    )

    workspace = fields.ForeignKey(
        "Workspace", 
        on_delete="CASCADE", 
        related_name="+",  # "+" means no reverse relation is created
        exclude = True,
        null = True,
        label = "Espace de travail",
    )

    # This is a class method that will be called when the model is being created
    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        This method is called when a class inherits from WorkspaceMixin.
        It ensures the workspace field is properly set up.
        """
        super().__init_subclass__(**kwargs)
        
        # If the model has a Meta class, we can customize the related_name
        if hasattr(cls, "Meta") and hasattr(cls.Meta, "tablename"):
            # Get the table name from the Meta class
            tablename = cls.Meta.tablename
            
            # Override the workspace field with a custom related_name based on the table name
            cls.workspace = fields.ForeignKey(
                "Workspace",
                on_delete="CASCADE",
                related_name=tablename,  # This creates a reverse relation named after the table
                exclude = True,
            )

    async def save(self: Model, force_insert: bool = False, values: dict[str, Any] | set[str] | None = None,
                   force_save: bool | None = None) -> Model:
        workspace = context.get_workspace()

        if workspace and (not hasattr(self, "workspace") or self.workspace != workspace):
            self.workspace = workspace

        return await super().save(force_insert, values, force_save)

