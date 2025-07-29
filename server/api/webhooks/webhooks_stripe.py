import logging
import stripe
from fastapi import APIRouter, Request, HTTPException, status, Header

from core.config import get_settings
from models.workspace_subscription import WorkspaceSubscription, SubscriptionStatus
from services.subscription_service import subscription_service

logger = logging.getLogger("webhooks_stripe_api")
router = APIRouter()


@router.post("/stripe")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(None, alias="stripe-signature")
):
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signature Stripe manquante"
        )

    settings = get_settings()
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload invalide"
        )
    except stripe.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signature invalide"
        )

    if event["type"] == "customer.subscription.created":
        await handle_subscription_created(event["data"]["object"])
    elif event["type"] == "customer.subscription.updated":
        await handle_subscription_updated(event["data"]["object"])
    elif event["type"] == "customer.subscription.deleted":
        await handle_subscription_deleted(event["data"]["object"])
    elif event["type"] == "invoice.payment_succeeded":
        await handle_payment_succeeded(event["data"]["object"])
    elif event["type"] == "invoice.payment_failed":
        await handle_payment_failed(event["data"]["object"])

    return {"received": True}


async def handle_subscription_created(subscription_data: dict):
    try:
        await subscription_service.sync_subscription_from_stripe(subscription_data["id"])
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'abonnement: {e}")


async def handle_subscription_updated(subscription_data: dict):
    try:
        await subscription_service.sync_subscription_from_stripe(subscription_data["id"])
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'abonnement: {e}")


async def handle_subscription_deleted(subscription_data: dict):
    try:
        subscription = await WorkspaceSubscription.query.filter(
            stripe_subscription_id=subscription_data["id"]
        ).first()

        if subscription:
            subscription.status = SubscriptionStatus.canceled
            subscription.is_active = False
            if subscription_data.get("canceled_at"):
                subscription.canceled_at = subscription_data["canceled_at"]
            await subscription.save()

    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'abonnement: {e}")


async def handle_payment_succeeded(invoice_data: dict):
    try:
        subscription_id = invoice_data.get("subscription")

        if subscription_id:
            await subscription_service.sync_subscription_from_stripe(subscription_id)

    except Exception as e:
        logger.error(f"Erreur lors du traitement du paiement réussi: {e}")


async def handle_payment_failed(invoice_data: dict):
    try:
        subscription_id = invoice_data.get("subscription")

        if subscription_id:
            await subscription_service.sync_subscription_from_stripe(subscription_id)

    except Exception as e:
        logger.error(f"Erreur lors du traitement du paiement échoué: {e}")
