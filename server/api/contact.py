from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.contact import Contact
from models.company import Company
from schemas.contact import ContactCreate, ContactUpdate, ContactRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User

from pydantic import BaseModel

router = APIRouter()


class PaginatedContactResponse(BaseModel):
    items: List[ContactRead]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("", response_model=PaginatedContactResponse)
async def list_contacts(
    page: int = 1,
    per_page: int = 50,
    company_id: int = None,
    current_user: User = Depends(get_current_user)
):
    if per_page not in [20, 50, 80]:
        per_page = 50
    
    if page < 1:
        page = 1
    
    skip = (page - 1) * per_page
    
    query = Contact.query
    if company_id:
        query = query.filter(Contact.columns.company == company_id)
    
    total = await query.count()
    contacts = await query.select_related("company").order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedContactResponse(
        items=contacts,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/quick_search", response_model=PaginatedContactResponse)
async def quick_search_contacts(
    q: str,
    page: int = 1,
    per_page: int = 50,
    company_id: int = None,
    current_user: User = Depends(get_current_user)
):
    if not q or len(q.strip()) < 2:
        return PaginatedContactResponse(
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
    
    query = Contact.query.filter(
        Contact.columns.first_name.ilike(search_term) | 
        Contact.columns.last_name.ilike(search_term) |
        Contact.columns.full_name.ilike(search_term) |
        Contact.columns.email.ilike(search_term) |
        Contact.columns.function.ilike(search_term)
    )
    
    if company_id:
        query = query.filter(Contact.columns.company == company_id)
    
    total = await query.count()
    contacts = await query.select_related("company").order_by("-created_at").offset(skip).limit(per_page).all()
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedContactResponse(
        items=contacts,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{contact_id}", response_model=ContactRead)
async def get_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user)
):
    contact = await Contact.query.select_related("company").get(id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_contact(contact: ContactCreate):
    if contact.company:
        company = await Company.query.get(id=contact.company)
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
    
    data = contact.model_dump()
    obj = Contact(**data)
    await obj.save()
    
    return await Contact.query.select_related("company").get(id=obj.id)


@router.put("/{contact_id}", response_model=ContactRead)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    current_user: User = Depends(get_current_user)
):
    contact = await Contact.query.get(id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = contact_update.model_dump(exclude_unset=True)
    
    if "company" in update_data and update_data["company"]:
        company = await Company.query.get(id=update_data["company"])
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
    
    await contact.update(**update_data)
    return await Contact.query.select_related("company").get(id=contact_id)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user)
):
    contact = await Contact.query.get(id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    await contact.delete()
    return None 