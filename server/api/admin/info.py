from fastapi import APIRouter


router = APIRouter()


@router.get("/info")
async def get_admin_info() -> dict:
    return {
        "success": True,
    }
