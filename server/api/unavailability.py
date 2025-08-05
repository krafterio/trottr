from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.unavailability import Unavailability
from models.user import User
from schemas.unavailability import UnavailabilityCreate, UnavailabilityUpdate, UnavailabilityRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from pydantic import BaseModel
from datetime import datetime
from dateutil import parser

router = APIRouter()

class PaginatedUnavailabilityResponse(BaseModel):
    items: List[UnavailabilityRead]
    total: int
    page: int
    per_page: int
    total_pages: int

@router.get("", response_model=PaginatedUnavailabilityResponse)
async def list_unavailabilities(
    page: int = 1,
    per_page: int = 50,
    type: str = None,
    user: int = None,
    start_date: str = None,
    end_date: str = None,
    current_user: User = Depends(get_current_user)
):
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    
    query = Unavailability.query.select_related("user")
    
    if type:
        query = query.filter(Unavailability.columns.type == type)
    
    if user:
        query = query.filter(Unavailability.columns.user == user)
    
    if start_date:
        query = query.filter(Unavailability.columns.end >= parser.parse(start_date))
    
    if end_date:
        query = query.filter(Unavailability.columns.start <= parser.parse(end_date))
    
    total = await query.count()
    unavailabilities = await query.order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedUnavailabilityResponse(
        items=unavailabilities,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/{unavailability_id}", response_model=UnavailabilityRead)
async def get_unavailability(
    unavailability_id: int,
    current_user: User = Depends(get_current_user)
):
    unavailability = await Unavailability.query.select_related("user").get(id=unavailability_id)
    if not unavailability:
        raise HTTPException(status_code=404, detail="Indisponibilité non trouvée")
    return unavailability

@router.post("", response_model=UnavailabilityRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_unavailability(
    unavailability: UnavailabilityCreate,
    current_user: User = Depends(get_current_user)
):
    user = await User.query.get(id=unavailability.user)
    if not user:
        raise HTTPException(status_code=400, detail="Utilisateur non trouvé")
    
    data = unavailability.model_dump()
    obj = Unavailability(**data)
    await obj.save()
    
    return obj

@router.put("/{unavailability_id}", response_model=UnavailabilityRead)
async def update_unavailability(
    unavailability_id: int,
    unavailability_update: UnavailabilityUpdate,
    current_user: User = Depends(get_current_user)
):
    unavailability = await Unavailability.query.get(id=unavailability_id)
    if not unavailability:
        raise HTTPException(status_code=404, detail="Indisponibilité non trouvée")
    
    update_data = unavailability_update.model_dump(exclude_unset=True)
    
    if "user" in update_data and update_data["user"]:
        user = await User.query.get(id=update_data["user"])
        if not user:
            raise HTTPException(status_code=400, detail="Utilisateur non trouvé")
    
    await unavailability.update(**update_data)
    return await Unavailability.query.select_related("user").get(id=unavailability_id)

@router.delete("/{unavailability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unavailability(
    unavailability_id: int,
    current_user: User = Depends(get_current_user)
):
    unavailability = await Unavailability.query.get(id=unavailability_id)
    if not unavailability:
        raise HTTPException(status_code=404, detail="Indisponibilité non trouvée")
    
    await unavailability.delete()
    return None 