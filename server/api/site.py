from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.site import Site
from models.country import Country
from models.company import Company
from models.contact import Contact
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
    company: int = None,
    contact: int = None,
    current_user: User = Depends(get_current_user)
):
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    
    query = Site.query
    if company:
        query = query.filter(Site.columns.company == company)
    if contact:
        query = query.filter(Site.columns.contact == contact)
    
    total = await query.count()
    sites = await query.select_related("country", "company", "contact").order_by("-created_at").offset(skip).limit(per_page).all()
    
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
    site = await Site.query.select_related("country", "company", "contact").get(id=site_id)
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
    
    contact = None
    if site.contact:
        contact = await Contact.query.get(id=site.contact)
        if not contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    
    data = site.model_dump()
    obj = Site(**data)
    obj.country = country
    if company:
        obj.company = company
    if contact:
        obj.contact = contact
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
    
    if "contact" in update_data and update_data["contact"]:
        contact = await Contact.query.get(id=update_data["contact"])
        if not contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        update_data["contact"] = contact
    elif "contact" in update_data and update_data["contact"] is None:
        update_data["contact"] = None
    
    await site.update(**update_data)
    return await Site.query.select_related("country", "company", "contact").get(id=site_id)

@router.patch("/{site_id}", response_model=SiteRead)
async def patch_site(
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
    
    if "company" in update_data:
        if update_data["company"]:
            company = await Company.query.get(id=update_data["company"])
            if not company:
                raise HTTPException(status_code=400, detail="Company not found")
            update_data["company"] = company
        else:
            update_data["company"] = None
    
    if "contact" in update_data:
        if update_data["contact"]:
            contact = await Contact.query.get(id=update_data["contact"])
            if not contact:
                raise HTTPException(status_code=400, detail="Contact not found")
            update_data["contact"] = contact
        else:
            update_data["contact"] = None
    
    await site.update(**update_data)
    return await Site.query.select_related("country", "company", "contact").get(id=site_id)

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