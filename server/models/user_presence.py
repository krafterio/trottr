from typing import Union, TYPE_CHECKING

from edgy import fields
from models.base import BaseModel
from models.mixins import WorkspaceableMixin
from enum import Enum
from datetime import datetime, timedelta


if TYPE_CHECKING:
    from models.user import User


class PresenceStatus(str, Enum):
    ONLINE = "online"
    AWAY = "away"
    OFFLINE = "offline"


class UserPresence(BaseModel, WorkspaceableMixin):
    class Meta:
        label = "Présence"
        label_plural = "Présences"

    user: Union["User", None] = fields.ForeignKey("User", on_delete="CASCADE", related_name="user_presences", label="Utilisateur")

    last_poll = fields.DateTimeField(auto_now=True, label="Dernière poll")
    last_presence = fields.DateTimeField(auto_now_add=True, label="Dernière presence")
    status: str | None = fields.ChoiceField(PresenceStatus, default=PresenceStatus.OFFLINE, label="Statut") # type: ignore

    current_topic = fields.CharField(max_length=255, null=True, blank=True, label="Topic")
    connection_count = fields.IntegerField(default=0, label="Nombre de connexions")

    class Meta:
        tablename = "user_presences"
        unique_together = [("user", "workspace")]

    @classmethod
    async def set_user_online(cls, user, workspace, topic: str = ""):
        presence, created = await cls.query.get_or_create(
            user=user, 
            workspace=workspace,
            defaults={
                "status": PresenceStatus.ONLINE,
                "connection_count": 1,
                "current_topic": topic,
                "last_presence": datetime.utcnow(),
                "last_poll": datetime.utcnow()
            }
        )

        if not created:
            presence.status = PresenceStatus.ONLINE
            presence.connection_count += 1
            presence.last_presence = datetime.utcnow()
            presence.last_poll = datetime.utcnow()

            if topic:
                presence.current_topic = topic

            await presence.save()
        
        return presence, created

    @classmethod
    async def set_user_offline(cls, user, workspace):
        try:
            presence = await cls.query.filter(user=user, workspace=workspace).first()

            if presence:
                presence.connection_count = max(0, presence.connection_count - 1)

                if presence.connection_count == 0:
                    presence.status = PresenceStatus.OFFLINE
                    presence.current_topic = ""

                await presence.save()

                return True
        except Exception:
            pass

        return False

    @classmethod
    async def update_user_topic(cls, user, workspace, topic: str) -> bool:
        try:
            presence = await cls.query.filter(user=user, workspace=workspace).first()

            if presence:
                presence.current_topic = topic
                presence.last_poll = datetime.utcnow()
                await presence.save()

                return True
        except Exception:
            pass

        return False

    @classmethod
    async def heartbeat(cls, user, workspace):
        try:
            presence = await cls.query.filter(user=user, workspace=workspace).first()
            if presence:
                presence.last_poll = datetime.utcnow()

                await presence.save()
        except Exception:
            pass

    @classmethod
    async def get_online_users_for_topic(cls, topic: str, workspace):
        presences = await cls.query.select_related("user").filter(
            workspace=workspace,
            status=PresenceStatus.ONLINE,
            current_topic=topic,
        ).all()

        return [presence.user for presence in presences]

    @classmethod
    async def get_online_users_for_workspace(cls, workspace):
        presences = await cls.query.select_related("user").filter(
            workspace=workspace,
            status=PresenceStatus.ONLINE
        ).all()

        return [presence.user for presence in presences]

    @classmethod
    async def get_presence_stats(cls):
        total_online = await cls.query.filter(status=PresenceStatus.ONLINE).count()
        total_offline = await cls.query.filter(status=PresenceStatus.OFFLINE).count()
        total_away = await cls.query.filter(status=PresenceStatus.AWAY).count()

        return {
            "online": total_online,
            "offline": total_offline, 
            "away": total_away,
            "total": total_online + total_offline + total_away
        }

    @classmethod
    async def cleanup_inactive_users(cls, inactive_minutes: int = 10) -> int:
        cutoff_time = datetime.utcnow() - timedelta(minutes=inactive_minutes)

        inactive_presences = await cls.query.filter(
            last_poll__lt=cutoff_time,
            status=PresenceStatus.ONLINE
        ).all()

        count = 0

        for presence in inactive_presences:
            presence.status = PresenceStatus.OFFLINE
            presence.connection_count = 0
            presence.current_topic = ""
            await presence.save()
            count += 1

        return count 
