from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from models.job_status import JobStatus
from models.user import User
from schemas.job_status import JobStatusCreate, JobStatusUpdate, JobStatusRead
from api.auth import get_current_user
from services.workspace import get_user_workspace

router = APIRouter()

class JobStatusReorderItem(BaseModel):
    id: int
    sequence: int

class JobStatusReorder(BaseModel):
    statuses: List[JobStatusReorderItem]

@router.get("", response_model=List[JobStatusRead])
async def list_job_statuses(
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_statuses = await JobStatus.query.filter(workspace=workspace).order_by("sequence").all()
    return job_statuses

@router.post("", response_model=JobStatusRead)
async def create_job_status(
    job_status_data: JobStatusCreate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_status = await JobStatus.query.create(**job_status_data.model_dump(), workspace=workspace)
    return job_status

@router.put("/reorder")
async def reorder_job_statuses(
    data: JobStatusReorder,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    try:
        for status_item in data.statuses:
            job_status = await JobStatus.query.filter(id=status_item.id, workspace=workspace).first()
            if job_status:
                job_status.sequence = status_item.sequence
                await job_status.save()
        
        return {"message": "Statuts réorganisés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_status_id}", response_model=JobStatusRead)
async def get_job_status(
    job_status_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_status = await JobStatus.query.filter(id=job_status_id, workspace=workspace).first()
    if not job_status:
        raise HTTPException(status_code=404, detail="Statut de job non trouvé")
    return job_status

@router.patch("/{job_status_id}", response_model=JobStatusRead)
async def update_job_status(
    job_status_id: int,
    job_status_data: JobStatusUpdate,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_status = await JobStatus.query.filter(id=job_status_id, workspace=workspace).first()
    if not job_status:
        raise HTTPException(status_code=404, detail="Statut de job non trouvé")
    
    update_data = job_status_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_status, field, value)
    
    await job_status.save()
    return job_status

@router.delete("/{job_status_id}")
async def delete_job_status(
    job_status_id: int,
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    job_status = await JobStatus.query.filter(id=job_status_id, workspace=workspace).first()
    if not job_status:
        raise HTTPException(status_code=404, detail="Statut de job non trouvé")
    
    await job_status.delete()
    return {"message": "Statut de job supprimé"} 