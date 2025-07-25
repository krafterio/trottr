from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any

from models.country import Country
from schemas.country import CountryCreate, CountryUpdate, CountryResponse
from api.auth import get_current_user
from models.user import User

router = APIRouter()


@router.post("", response_model=CountryResponse, dependencies=[Depends(get_current_user)])
async def create_country(country: CountryCreate):
    try:
        obj = Country(**country.model_dump())
        await obj.save()
        return CountryResponse.model_validate(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating country: {str(e)}")


@router.get("", response_model=Dict[str, Any])
async def list_countries(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: str = Query(None),
    current_user: User = Depends(get_current_user)
):
    query = Country.query
    
    if search:
        query = query.filter(name__icontains=search)
    
    query = query.order_by("name")
    
    total = await query.count()
    items = await query.limit(limit).offset(offset).all()
    
    formatted_items = [
        CountryResponse.model_validate(item)
        for item in items
    ]
    
    return {"items": formatted_items, "total": total}


@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(country_id: int, current_user: User = Depends(get_current_user)):
    country = await Country.query.get_or_none(id=country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountryResponse.model_validate(country)


@router.patch("/{country_id}", response_model=CountryResponse)
async def update_country(country_id: int, country: CountryUpdate, current_user: User = Depends(get_current_user)):
    obj = await Country.query.get_or_none(id=country_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    
    update_data = country.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(obj, field, value)
    
    await obj.save()
    return CountryResponse.model_validate(obj)


@router.delete("/{country_id}")
async def delete_country(country_id: int, current_user: User = Depends(get_current_user)):
    obj = await Country.query.get_or_none(id=country_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    
    await obj.delete()
    return {"message": "Country deleted successfully"} 