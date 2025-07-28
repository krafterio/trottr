from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from models.contact_relation_type import ContactRelationType
from models.user import User
from schemas.contact_relation_type import ContactRelationTypeCreate, ContactRelationTypeUpdate, ContactRelationTypeRead
from api.auth import get_current_user
from services.workspace import get_user_workspace

router = APIRouter()

class ContactRelationTypeReorderItem(BaseModel):
    id: int
    sequence: int

class ContactRelationTypeReorder(BaseModel):
    types: List[ContactRelationTypeReorderItem]

@router.get("", response_model=List[ContactRelationTypeRead])
async def list_contact_relation_types(
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    contact_relation_types = await ContactRelationType.query.filter(workspace=workspace).order_by("sequence").all()
    return contact_relation_types

@router.post("", response_model=ContactRelationTypeRead)
async def create_contact_relation_type(
    contact_relation_type_data: ContactRelationTypeCreate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    contact_relation_type = await ContactRelationType.query.create(**contact_relation_type_data.model_dump(), workspace=workspace)
    return contact_relation_type

@router.put("/reorder")
async def reorder_contact_relation_types(
    data: ContactRelationTypeReorder,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    try:
        for type_item in data.types:
            contact_relation_type = await ContactRelationType.query.filter(id=type_item.id, workspace=workspace).first()
            if contact_relation_type:
                contact_relation_type.sequence = type_item.sequence
                await contact_relation_type.save()
        
        return {"message": "Relations réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{contact_relation_type_id}", response_model=ContactRelationTypeRead)
async def get_contact_relation_type(
    contact_relation_type_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    contact_relation_type = await ContactRelationType.query.filter(id=contact_relation_type_id, workspace=workspace).first()
    if not contact_relation_type:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    return contact_relation_type

@router.patch("/{contact_relation_type_id}", response_model=ContactRelationTypeRead)
async def update_contact_relation_type(
    contact_relation_type_id: int,
    contact_relation_type_data: ContactRelationTypeUpdate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    contact_relation_type = await ContactRelationType.query.filter(id=contact_relation_type_id, workspace=workspace).first()
    if not contact_relation_type:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    update_data = contact_relation_type_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact_relation_type, field, value)
    
    await contact_relation_type.save()
    return contact_relation_type

@router.delete("/{contact_relation_type_id}")
async def delete_contact_relation_type(
    contact_relation_type_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    contact_relation_type = await ContactRelationType.query.filter(id=contact_relation_type_id, workspace=workspace).first()
    if not contact_relation_type:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    await contact_relation_type.delete()
    return {"message": "Catégorie d'intervention supprimée"} 