import edgy
from .base import BaseModel
from .company import Company
from .mixins import WorkspaceableMixin


class Contact(BaseModel, WorkspaceableMixin):
    first_name = edgy.CharField(max_length=255)
    last_name = edgy.CharField(max_length=255)
    full_name = edgy.CharField(max_length=511, null=True, blank=True)
    function = edgy.CharField(max_length=255, null=True, blank=True)
    company = edgy.ForeignKey(Company, on_delete="CASCADE", null=True, blank=True)
    email = edgy.EmailField(null=True, blank=True)
    mobile = edgy.CharField(max_length=20, null=True, blank=True)
    phone = edgy.CharField(max_length=20, null=True, blank=True)

    class Meta:
        tablename = "contacts"

    async def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        elif self.first_name:
            self.full_name = self.first_name
        elif self.last_name:
            self.full_name = self.last_name
        else:
            self.full_name = None
        
        return await super().save(*args, **kwargs) 