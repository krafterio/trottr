from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.company import Company
from models.country import Country
from schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from api.auth import get_current_user
from models.user import User

router = APIRouter()


@router.get("/", response_model=List[CompanyRead])
async def list_companies(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    companies = await Company.query.select_related("invoice_country").offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user)
):
    company = await Company.query.select_related("invoice_country").get(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    current_user: User = Depends(get_current_user)
):
    if company.invoice_country_id:
        country = await Country.query.get(id=company.invoice_country_id)
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")
    
    new_company = await Company.query.create(**company.model_dump())
    return await Company.query.select_related("invoice_country").get(id=new_company.id)


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