from fastapi import APIRouter, Depends, Query, HTTPException
from models.user import User
from models.workspace_user import WorkspaceUser, WorkspaceUserRole
from api.auth import get_current_user
from services.workspace import get_user_workspace
from schemas.base import List as ListSchema
from typing import List

router = APIRouter(tags=["operators"])

@router.get("", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_operators(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=1000),
    q: str = Query(None),
    speciality_ids: List[int] = Query(None),
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    # Get all operators in the workspace
    query = WorkspaceUser.query.select_related('user').filter(
        workspace=workspace,
        role=WorkspaceUserRole.OPERATOR
    )
    
    # Apply search filter if provided
    if q:
        query = query.filter(
            User.name.icontains(q) | 
            User.email.icontains(q)
        )
    
    # Calculate pagination
    total = await query.count()
    offset = (page - 1) * per_page
    workspace_users = await query.offset(offset).limit(per_page).all()
    
    # Prepare items with job specialities
    items = []
    for workspace_user in workspace_users:
        user = workspace_user.user
        
        # Get job specialities for this user
        job_specialities = []
        try:
            if hasattr(user, 'job_specialities'):
                async for speciality in user.job_specialities.all():
                    job_specialities.append({
                        "id": speciality.id,
                        "name": speciality.name,
                        "color": speciality.color,
                        "sequence": speciality.sequence
                    })
        except Exception as e:
            print(f"Error loading specialities for user {user.id}: {e}")
            job_specialities = []
        
        # Filter by specialities if provided
        if speciality_ids:
            user_speciality_ids = [s["id"] for s in job_specialities]
            if not any(sid in user_speciality_ids for sid in speciality_ids):
                continue
        
        items.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "initials": user.initials,
            "avatar": user.avatar,
            "zone": user.zone,
            "phone": user.phone,
            "job_specialities": job_specialities,
            "role": workspace_user.role.value
        })
    
    # Recalculate total if filtering by specialities
    if speciality_ids:
        total = len(items)
    
    total_pages = (total + per_page - 1) // per_page
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    } 