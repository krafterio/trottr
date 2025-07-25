from fastapi import APIRouter

from api.admin.info import router as info
from api.admin.storage import router as storage

router = APIRouter()
router.include_router(info)
router.include_router(storage)
