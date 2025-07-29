from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_job_diagnostic import JobJobDiagnostic
from models.job import Job
from models.job_diagnostic import JobDiagnostic
from schemas.job_job_diagnostic import JobJobDiagnosticCreate, JobJobDiagnosticUpdate, JobJobDiagnosticRead
from api.auth import get_current_user
from models.user import User as CurrentUser
from pydantic import BaseModel
from services.workspace import get_user_workspace

router = APIRouter()

class JobJobDiagnosticReorderItem(BaseModel):
    id: int
    sequence: int

class JobJobDiagnosticReorder(BaseModel):
    diagnostics: List[JobJobDiagnosticReorderItem]

@router.get("", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def list_job_job_diagnostics(
    skip: int = 0,
    limit: int = 100,
    job_id: int = None
):
    query = JobJobDiagnostic.query.select_related("job", "job_diagnostic", "created_by")
    
    if job_id is not None:
        query = query.filter(job=job_id)
    
    job_job_diagnostics = await query.order_by("sequence").offset(skip).limit(limit).all()
    return job_job_diagnostics

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_job_diagnostics(data: JobJobDiagnosticReorder):
    try:
        for diagnostic_item in data.diagnostics:
            job_job_diagnostic = await JobJobDiagnostic.query.filter(id=diagnostic_item.id).first()
            if job_job_diagnostic:
                job_job_diagnostic.sequence = diagnostic_item.sequence
                await job_job_diagnostic.save()

        return {"message": "Diagnostics réorganisés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_job_diagnostic_id}", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_job_job_diagnostic(
    job_job_diagnostic_id: int
):
    job_job_diagnostic = await JobJobDiagnostic.query.select_related("job", "job_diagnostic", "created_by").get(id=job_job_diagnostic_id)
    if not job_job_diagnostic:
        raise HTTPException(status_code=404, detail="Job job diagnostic not found")
    return job_job_diagnostic

@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_job_diagnostic(
    job_job_diagnostic: JobJobDiagnosticCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    # Validation des FK
    if job_job_diagnostic.job:
        job = await Job.query.get(id=job_job_diagnostic.job)
        if not job:
            raise HTTPException(status_code=400, detail="Job not found")
    
    if job_job_diagnostic.job_diagnostic:
        job_diagnostic = await JobDiagnostic.query.get(id=job_job_diagnostic.job_diagnostic)
        if not job_diagnostic:
            raise HTTPException(status_code=400, detail="Job diagnostic not found")
    
    diagnostic_data = job_job_diagnostic.model_dump()
    diagnostic_data["created_by"] = current_user
    
    new_job_job_diagnostic = JobJobDiagnostic(**diagnostic_data)
    await new_job_job_diagnostic.save()
    
    # Retourner l'objet avec les relations chargées
    created_diagnostic = await JobJobDiagnostic.query.select_related("job", "job_diagnostic", "created_by").get(id=new_job_job_diagnostic.id)
    return created_diagnostic

@router.put("/{job_job_diagnostic_id}", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def update_job_job_diagnostic(
    job_job_diagnostic_id: int,
    job_job_diagnostic_update: JobJobDiagnosticUpdate
):
    job_job_diagnostic = await JobJobDiagnostic.query.get(id=job_job_diagnostic_id)
    if not job_job_diagnostic:
        raise HTTPException(status_code=404, detail="Job job diagnostic not found")
    
    update_data = job_job_diagnostic_update.model_dump(exclude_unset=True)
    
    # Validation des FK si dans update_data
    if "job" in update_data and update_data["job"]:
        job = await Job.query.get(id=update_data["job"])
        if not job:
            raise HTTPException(status_code=400, detail="Job not found")
    
    if "job_diagnostic" in update_data and update_data["job_diagnostic"]:
        job_diagnostic = await JobDiagnostic.query.get(id=update_data["job_diagnostic"])
        if not job_diagnostic:
            raise HTTPException(status_code=400, detail="Job diagnostic not found")
    
    await job_job_diagnostic.update(**update_data)
    updated_diagnostic = await JobJobDiagnostic.query.select_related("job", "job_diagnostic", "created_by").get(id=job_job_diagnostic_id)
    return updated_diagnostic

@router.delete("/{job_job_diagnostic_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def delete_job_job_diagnostic(
    job_job_diagnostic_id: int
):
    job_job_diagnostic = await JobJobDiagnostic.query.get(id=job_job_diagnostic_id)
    if not job_job_diagnostic:
        raise HTTPException(status_code=404, detail="Job job diagnostic not found")
    
    await job_job_diagnostic.delete()
    return None 