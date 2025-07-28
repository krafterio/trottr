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

@router.get("", response_model=List[JobCategoryRead], dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def list_job_categories():
    job_categories = await JobCategory.query.order_by("sequence").all()
    return job_categories

@router.post("", response_model=JobCategoryRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_category(job_category_data: JobCategoryCreate):
    data = job_category_data.model_dump()
    obj = JobCategory(**data)
    await obj.save()
    return obj

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_categories(data: JobCategoryReorder):
    try:
        for category_item in data.categories:
            job_category = await JobCategory.query.filter(id=category_item.id).first()
            if job_category:
                job_category.sequence = category_item.sequence
                await job_category.save()
        
        return {"message": "Catégories réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_category_id}", response_model=JobCategoryRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_job_category(job_category_id: int):
    job_category = await JobCategory.query.get(id=job_category_id)
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    return job_category

@router.patch("/{job_category_id}", response_model=JobCategoryRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def update_job_category(job_category_id: int, job_category_data: JobCategoryUpdate):
    job_category = await JobCategory.query.get(id=job_category_id)
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    update_data = job_category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_category, field, value)
    
    await job_category.save()
    return job_category

@router.delete("/{job_category_id}", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def delete_job_category(job_category_id: int):
    job_category = await JobCategory.query.get(id=job_category_id)
    if not job_category:
        raise HTTPException(status_code=404, detail="Catégorie d'intervention non trouvée")
    
    await job_category.delete()
    return {"message": "Catégorie d'intervention supprimée"} 