from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.company import Company
from models.country import Country
from schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User

from pydantic import BaseModel

router = APIRouter()


class PaginatedCompanyResponse(BaseModel):
    items: List[CompanyRead]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("", response_model=PaginatedCompanyResponse)
async def list_companies(
    page: int = 1,
    per_page: int = 50,
    current_user: User = Depends(get_current_user)
):
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    
    total = await Company.query.count()
    companies = await Company.query.order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedCompanyResponse(
        items=companies,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/quick_search", response_model=PaginatedCompanyResponse)
async def quick_search_companies(
    q: str,
    page: int = 1,
    per_page: int = 50,
    current_user: User = Depends(get_current_user)
):
    if not q or len(q.strip()) < 2:
        return PaginatedCompanyResponse(
            items=[],
            total=0,
            page=1,
            per_page=per_page,
            total_pages=0
        )
    
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    search_term = f"%{q.strip()}%"
    
    query = Company.query.filter(
        Company.columns.name.ilike(search_term) | 
        Company.columns.invoice_city.ilike(search_term) |
        Company.columns.reference.ilike(search_term)
    )
    
    total = await query.count()
    companies = await query.order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedCompanyResponse(
        items=companies,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user)
):
    company = await Company.query.get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_company(company: CompanyCreate):
    if company.invoice_country_id:
        country = await Country.query.get(id=company.invoice_country_id)
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")
    
    data = company.model_dump()
    obj = Company(**data)
    await obj.save()
    
    return obj


@router.put("/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    current_user: User = Depends(get_current_user)
):
    company = await Company.query.get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company_update.model_dump(exclude_unset=True)
    
    if "invoice_country_id" in update_data and update_data["invoice_country_id"]:
        country = await Country.query.get(id=update_data["invoice_country_id"])
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")
    
    await company.update(**update_data)
    return await Company.query.select_related("invoice_country").get(id=company_id)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user)
):
    company = await Company.query.get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    await company.delete()
    return None


@router.get("/{company_id}/sites", response_model=List)
async def get_company_sites(
    company_id: int,
    current_user: User = Depends(get_current_user)
):
    from models.site import Site
    
    company = await Company.query.get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    sites = await Site.query.filter(company=company).select_related("country", "company").all()
    return sites


class CompanyKPIsResponse(BaseModel):
    sites_count: int
    contacts_count: int
    interventions_count: int
    lots_count: int


@router.get("/{company_id}/kpis", response_model=CompanyKPIsResponse)
async def get_company_kpis(
    company_id: int,
    current_user: User = Depends(get_current_user)
):
    from models.site import Site
    from models.contact import Contact
    
    company = await Company.query.get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    sites_count = await Site.query.filter(company=company).count()
    contacts_count = await Contact.query.filter(company=company).count()
    
    return CompanyKPIsResponse(
        sites_count=sites_count,
        contacts_count=contacts_count,
        interventions_count=0,
        lots_count=0
    ) 