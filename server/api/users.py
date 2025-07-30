from fastapi import APIRouter, Depends, Query
from models.user import User
from api.auth import get_current_user
from typing import Dict, Any
from services.workspace import get_user_workspace
from models.workspace_user import WorkspaceUser
from fastapi import HTTPException

router = APIRouter()

@router.get("/check-email", response_model=Dict[str, Any])
async def check_user_email(
    email: str = Query(..., description="Email to check"),
    current_user: User = Depends(get_current_user)
):
    """
    Check if a user with the given email exists.
    Returns a dictionary with:
    - exists: boolean indicating if the user exists
    - user: user data if exists is True, otherwise None
    """
    user = await User.query.filter(email=email).first()
    
    if user:
        return {
            "exists": True,
            "user": user
        }
    else:
        return {
            "exists": False,
            "user": None
        }

@router.get("", response_model=Dict[str, Any])
async def list_workspace_users(
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace),
    role: str = Query(None, description="Filter users by role")
):
    workspace_users = await WorkspaceUser.query.select_related('user').filter(workspace=workspace).all()
    users = []
    for wu in workspace_users:
        if wu.user:
            # Filtrer par rôle si spécifié
            if role and wu.role != role:
                continue
                
            users.append({
                "id": wu.user.id,
                "name": wu.user.name,
                "email": wu.user.email,
                "avatar": wu.user.avatar,
                "initials": wu.user.initials,
                "role": wu.role,
                "google_connected": bool(wu.user.google_access_token),
                "google_email": wu.user.google_email,
                "google_connected_at": wu.user.google_connected_at
            })
    return {"items": users, "total": len(users)}

@router.get("/me/preferences")
async def get_user_preferences(current_user: User = Depends(get_current_user)):
    return {"preferences": current_user.preferences or {}}

@router.put("/me/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user)
):
    await current_user.update(preferences=preferences)
    return {"preferences": preferences}

@router.patch("/me/preferences")
async def patch_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user)
):
    current_preferences = current_user.preferences or {}
    current_preferences.update(preferences)
    await current_user.update(preferences=current_preferences)
    return {"preferences": current_preferences}

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    user = await User.query.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
