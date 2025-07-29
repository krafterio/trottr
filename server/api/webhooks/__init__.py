from fastapi import APIRouter
from .webhooks_stripe import router as webhooks_stripe
from .webhooks_gmail import router as webhooks_gmail


router = APIRouter(prefix="/webhooks")
router.include_router(webhooks_stripe)
router.include_router(webhooks_gmail)
