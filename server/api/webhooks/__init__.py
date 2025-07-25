from fastapi import APIRouter
from .webhooks_gmail import router as webhooks_gmail


router = APIRouter(prefix="/webhooks")
router.include_router(webhooks_gmail)
