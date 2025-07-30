from datetime import datetime
from typing import Union

from pydantic import BaseModel

from models.service_plan import ServicePlanPeriod, ServicePlanType
from models.workspace_subscription import SubscriptionStatus
from schemas.workspace import CountryRead


class WorkspaceBillingResponse(BaseModel):
    invoice_name: str | None = None
    invoice_street: str | None = None
    invoice_street2: str | None = None
    invoice_zip: str | None = None
    invoice_city: str | None = None
    invoice_country: CountryRead | None = None
    invoice_siren: str | None = None
    invoice_vat: str | None = None
    invoice_currency: str | None = None
    plan_name: str | None = None
    plan_type: Union[ServicePlanType, None] = None
    plan_period: Union[ServicePlanPeriod, None] = None
    plan_price: float | None = None
    plan_currency: str | None = None
    active_users_count: int
    current_month_jobs_count: int
    subscription_status: Union[SubscriptionStatus, None] = None
    subscription_available_users_count: int
    subscription_price: float
    subscription_start_date: datetime | None = None
    subscription_end_date: datetime | None = None
    subscription_trial_start: datetime | None = None
    subscription_trial_end: datetime | None = None
    subscription_cancel_at_period_end: bool
    subscription_canceled_at: datetime | None = None
    subscription_is_active: bool
    subscription_next_billing_date: datetime | None = None
