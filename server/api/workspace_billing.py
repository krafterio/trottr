import calendar
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends

from models.workspace import Workspace
from models.job import Job
from services.workspace import get_user_workspace
from services.subscription_service import subscription_service
from schemas.workspace_billing import WorkspaceBillingResponse

router = APIRouter()


@router.get("/workspace/billing")
async def get_workspace_billing_info(workspace: Workspace = Depends(get_user_workspace)) -> WorkspaceBillingResponse:
    current_date = datetime.now(ZoneInfo("UTC"))
    month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    last_day = calendar.monthrange(month_start.year, month_start.month)[1]
    month_end = datetime(month_start.year, month_start.month, last_day, 23, 59, 59, tzinfo=timezone.utc)
    
    active_users_count = await workspace.workspace_users.filter().count()
    
    current_month_jobs_count = await Job.query.filter(
        Job.columns.created_at.between(month_start, month_end)
    ).count()
    
    subscription = await subscription_service.get_active_subscription(workspace)

    return WorkspaceBillingResponse(
        invoice_name=workspace.name or None,
        invoice_street=workspace.street or None,
        invoice_street2=workspace.street2 or None,
        invoice_zip=workspace.zip or None,
        invoice_city=workspace.city or None,
        invoice_country=workspace.country or None,
        invoice_siren=workspace.siren or None,
        invoice_vat=workspace.vat or None,
        invoice_currency=workspace.currency or None,
        plan_name=workspace.service_plan.name if workspace.service_plan else None,
        plan_type=workspace.service_plan.type if workspace.service_plan else None,
        plan_period=workspace.service_plan.period if workspace.service_plan else None,
        plan_price=workspace.service_plan.price if workspace.service_plan else None,
        plan_currency=workspace.service_plan.currency if workspace.service_plan else None,
        active_users_count=active_users_count,
        current_month_jobs_count=current_month_jobs_count,
        subscription_status=subscription.status if subscription else None,
        subscription_available_users_count=subscription.available_users_count if subscription else None,
        subscription_start_date=subscription.start_date if subscription else None,
        subscription_end_date=subscription.end_date if subscription else None,
        subscription_trial_start=subscription.trial_start if subscription else None,
        subscription_trial_end=subscription.trial_end if subscription else None,
        subscription_cancel_at_period_end=subscription.cancel_at_period_end if subscription else None,
        subscription_canceled_at=subscription.canceled_at if subscription else None,
        subscription_is_active=subscription.is_active if subscription else None,
        subscription_next_billing_date=subscription.next_billing_date if subscription else None,
    ) 
