from fastapi import APIRouter, Depends, HTTPException, status, Response

from core.context import get_workspace_user
from models.workspace import Workspace
from models.service_plan import ServicePlan
from models.workspace_user import WorkspaceUser, WorkspaceUserRole
from services.subscription_service import subscription_service
from schemas.subscription import (
    SubscriptionRequest,
    SubscriptionResponse,
    BillingPortalResponse,
    SubscriptionCancelRequest,
    SubscriptionBillingPortalRequest,
    InvoicesListResponse
)
from services.workspace import get_user_workspace


def get_workspace_owner(workspace_user: WorkspaceUser | None = Depends(get_workspace_user)):
    if not workspace_user or workspace_user.role != WorkspaceUserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le propriétaire peut gérer un abonnement"
        )

    return workspace_user


router = APIRouter(dependencies=[Depends(get_workspace_owner)])


@router.get("/workspace/subscription")
async def get_current_subscription(
    response: Response,
    workspace: Workspace = Depends(get_user_workspace)
) -> SubscriptionResponse | None:
    subscription = await subscription_service.get_active_subscription(workspace)

    if not subscription:
        response.status_code = status.HTTP_204_NO_CONTENT

    return subscription


@router.patch("/workspace/subscription")
async def create_or_update_subscription(
    request: SubscriptionRequest,
    workspace: Workspace = Depends(get_user_workspace)
) -> SubscriptionResponse:
    subscription = await subscription_service.get_active_subscription(workspace)
    plan = await ServicePlan.query.filter(id=request.service_plan).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan non trouvé"
        )

    try:
        if not subscription:
            subscription = await subscription_service.create_subscription(
                workspace=workspace,
                service_plan=plan,
                quantity=request.quantity,
            )
        else:
            subscription = await subscription_service.update_subscription_plan(
                subscription=subscription,
                new_plan=plan,
                quantity=request.quantity,
            )

        return subscription
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la mise à jour de l'abonnement: {str(e)}"
        )


@router.post("/workspace/subscription/cancel")
async def cancel_subscription(
    request: SubscriptionCancelRequest,
    workspace: Workspace = Depends(get_user_workspace)
) -> SubscriptionResponse:
    subscription = await subscription_service.get_active_subscription(workspace)

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonnement non trouvé"
        )

    try:
        subscription = await subscription_service.cancel_subscription(
            subscription=subscription,
            at_period_end=request.at_period_end,
        )

        return subscription

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de l'annulation: {str(e)}"
        )


@router.post("/workspace/subscription/billing-portal")
async def create_billing_portal_session(
    request: SubscriptionBillingPortalRequest,
    workspace: Workspace = Depends(get_user_workspace)
) -> BillingPortalResponse:
    try:
        session = await subscription_service.create_billing_portal_session(
            workspace=workspace,
            return_url=request.return_url,
        )

        return BillingPortalResponse(url=session.url)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création de la session: {str(e)}"
        )


@router.get("/workspace/subscription/invoices")
async def get_workspace_invoices(
    workspace: Workspace = Depends(get_user_workspace),
    limit: int = 20
) -> InvoicesListResponse:
    try:
        invoices = await subscription_service.get_workspace_invoices(
            workspace=workspace,
            limit=limit
        )

        return InvoicesListResponse(invoices=invoices)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la récupération des factures: {str(e)}"
        )
