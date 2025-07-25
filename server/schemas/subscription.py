from datetime import datetime
from pydantic import BaseModel

from models.service_plan import ServicePlan
from models.workspace_subscription import SubscriptionStatus


class SubscriptionRequest(BaseModel):
    service_plan: int
    quantity: int = 1


class SubscriptionCancelRequest(BaseModel):
    at_period_end: bool = True


class SubscriptionBillingPortalRequest(BaseModel):
    return_url: str


class SubscriptionResponse(BaseModel):
    service_plan: ServicePlan | None = None
    status: SubscriptionStatus | None = None
    available_users_count: int
    start_date: datetime | None = None
    end_date: datetime | None = None
    trial_start: datetime | None = None
    trial_end: datetime | None = None
    cancel_at_period_end: bool
    canceled_at: datetime | None = None
    is_active: bool


class BillingPortalResponse(BaseModel):
    url: str 
