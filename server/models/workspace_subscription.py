from datetime import datetime
from typing import TYPE_CHECKING, Union

from edgy import fields
from enum import Enum
from edgy.core.signals import pre_save

from models.base import BaseModel


if TYPE_CHECKING:
    from models.workspace import Workspace


class SubscriptionStatus(str, Enum):
    incomplete = "incomplete"
    incomplete_expired = "incomplete_expired"
    trialing = "trialing"
    active = "active"
    past_due = "past_due"
    canceled = "canceled"
    unpaid = "unpaid"
    paused = "paused"

