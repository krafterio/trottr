from fastapi import Depends, HTTPException, status

from api.auth import get_current_user
from models.user import User


def is_superuser() -> Depends:
    def dependency(user: User = Depends(get_current_user)):
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access is not allowed",
            )

    return Depends(dependency)
