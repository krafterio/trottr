from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.site import Site
from models.country import Country
from models.company import Company
from schemas.site import SiteCreate, SiteUpdate, SiteRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User
from pydantic import BaseModel

router = APIRouter()


class PaginatedSiteResponse(BaseModel):
    items: List[SiteRead]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("", response_model=PaginatedSiteResponse)
async def list_sites(
    page: int = 1,
    per_page: int = 50,
    current_user: User = Depends(get_current_user)
):
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    
    total = await Site.query.count()
    sites = await Site.query.select_related("country", "company").order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedSiteResponse(
        items=sites,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/{site_id}", response_model=SiteRead)
async def get_site(
    site_id: int,
    current_user: User = Depends(get_current_user)
):
    site = await Site.query.select_related("country", "company").get(id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/", response_model=SiteRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_site(site: SiteCreate):
    country = await Country.query.get(id=site.country)
    if not country:
        raise HTTPException(status_code=400, detail="Country not found")
    
    company = None
    if site.company:
        company = await Company.query.get(id=site.company)
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
    
    data = site.model_dump()
    obj = Site(**data)
    obj.country = country
    if company:
        obj.company = company
    await obj.save()
    
    return obj

@router.put("/{site_id}", response_model=SiteRead)
async def update_site(
    site_id: int,
    site_update: SiteUpdate,
    current_user: User = Depends(get_current_user)
):
    site = await Site.query.get(id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    update_data = site_update.model_dump(exclude_unset=True)
    
    if "country" in update_data and update_data["country"]:
        country = await Country.query.get(id=update_data["country"])
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")
        update_data["country"] = country
    
    if "company" in update_data and update_data["company"]:
        company = await Company.query.get(id=update_data["company"])
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
        update_data["company"] = company
    elif "company" in update_data and update_data["company"] is None:
        update_data["company"] = None
    
    await site.update(**update_data)
    return await Site.query.select_related("country", "company").get(id=site_id)

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(
    site_id: int,
    current_user: User = Depends(get_current_user)
):
    site = await Site.query.get(id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    await site.delete()
    return None 