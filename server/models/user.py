from edgy import fields

from models.base import BaseModel
from datetime import datetime

class User(BaseModel):
    class Meta:
        label = "Utilisateur"
        label_plural = "Utilisateurs"

    email: str | None = fields.EmailField(unique=True, label="Email") # type: ignore
    name: str | None = fields.CharField(max_length=255, null=True, label="Nom") # type: ignore
    avatar: str | None = fields.CharField(max_length=255, null=True, label="Avatar") # type: ignore
    password: str | None = fields.PasswordField(exclude=True, label="Mot de passe") # type: ignore
    is_active: bool | None = fields.BooleanField(default=True, label="Actif") # type: ignore
    is_verified: bool | None = fields.BooleanField(default=False, label="Vérifié") # type: ignore
    verification_code: str | None = fields.CharField(max_length=6, null=True, exclude=True, label="Code de vérification") # type: ignore
    verification_code_expires_at: datetime | None = fields.DateTimeField(null=True, exclude=True, label="Expiration du code") # type: ignore
    password_reset_token: str | None = fields.CharField(max_length=255, null=True, exclude=True, label="Token de réinitialisation") # type: ignore
    password_reset_expires_at: datetime | None = fields.DateTimeField(null=True, exclude=True, label="Expiration du token de réinitialisation") # type: ignore
    is_superuser: bool | None = fields.BooleanField(default=False, exclude=True, label="Super utilisateur") # type: ignore
    preferences: dict | None = fields.JSONField(default=dict, null=True, label="Préférances") # type: ignore
    
    google_access_token: str | None = fields.TextField(null=True, exclude=True, label="Token d'accès Google") # type: ignore
    google_refresh_token: str | None = fields.TextField(null=True, exclude=True, label="Token de rafraîchissement Google") # type: ignore
    google_token_expires_at: datetime | None = fields.DateTimeField(null=True, exclude=True, label="Expiration du token Google") # type: ignore
    google_email: str | None = fields.EmailField(null=True, label="Email Google connecté") # type: ignore
    google_connected_at: datetime | None = fields.DateTimeField(null=True, label="Date de connexion Google") # type: ignore
    
    initials: str | None = fields.ComputedField(getter='get_initials', label="Initials") # type: ignore

    @classmethod
    def get_initials(cls, field, instance, owner=None) -> str:
        if instance.name:
            words = instance.name.split()
            initials = ''.join([word[:2].upper() for word in words if word])

            return initials[:6]

        return instance.email[0].upper() if instance.email else ''
