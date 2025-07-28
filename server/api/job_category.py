from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from models.job_category import JobCategory
from models.user import User
from schemas.job_category import JobCategoryCreate, JobCategoryUpdate, JobCategoryRead
from api.auth import get_current_user
from services.workspace import get_user_workspace

router = APIRouter()

class JobCategoryReorderItem(BaseModel):
    id: int
    sequence: int

class JobCategoryReorder(BaseModel):
    categories: List[JobCategoryReorderItem]

@router.get("", response_model=List[JobCategoryRead])
async def list_job_categories(
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_categories = await JobCategory.query.filter(workspace=workspace).order_by("sequence").all()
    return job_categories

@router.post("", response_model=JobCategoryRead)
async def create_job_category(
    job_category_data: JobCategoryCreate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_category = await JobCategory.query.create(**job_category_data.model_dump(), workspace=workspace)
    return job_category

@router.put("/reorder")
async def reorder_job_categories(
    data: JobCategoryReorder,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    try:
        for category_item in data.categories:
            job_category = await JobCategory.query.filter(id=category_item.id, workspace=workspace).first()
            if job_category:
                job_category.sequence = category_item.sequence
                await job_category.save()
        
        return {"message": "Catégories réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_category_id}", response_model=JobCategoryRead)
async def get_job_category(
    job_category_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_category = await JobCategory.query.filter(id=job_category_id, workspace=workspace).first()
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    return job_category

@router.patch("/{job_category_id}", response_model=JobCategoryRead)
async def update_job_category(
    job_category_id: int,
    job_category_data: JobCategoryUpdate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_category = await JobCategory.query.filter(id=job_category_id, workspace=workspace).first()
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    update_data = job_category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_category, field, value)
    
    await job_category.save()
    return job_category

@router.delete("/{job_category_id}")
async def delete_job_category(
    job_category_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_category = await JobCategory.query.filter(id=job_category_id, workspace=workspace).first()
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    await job_category.delete()
    return {"message": "Catégorie d'intervention supprimée"} 