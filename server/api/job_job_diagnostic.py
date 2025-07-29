from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_job_diagnostic import JobJobDiagnostic
from models.job import Job
from models.job_diagnostic import JobDiagnostic
from schemas.job_job_diagnostic import JobJobDiagnosticCreate, JobJobDiagnosticUpdate, JobJobDiagnosticRead
from api.auth import get_current_user
from models.user import User as CurrentUser

router = APIRouter()

@router.get("", response_model=List[JobJobDiagnosticRead])
async def list_job_job_diagnostics(
    skip: int = 0,
    limit: int = 100,
    job_id: int = None,
    current_user: CurrentUser = Depends(get_current_user)
):
    query = JobJobDiagnostic.query.select_related("job", "job_diagnostic")
    
    if job_id is not None:
        query = query.filter(job=job_id)
    
    job_job_diagnostics = await query.order_by("sequence").offset(skip).limit(limit).all()
    return job_job_diagnostics

@router.get("/{job_job_diagnostic_id}", response_model=JobJobDiagnosticRead)
async def get_job_job_diagnostic(
    job_job_diagnostic_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_diagnostic = await JobJobDiagnostic.query.select_related("job", "job_diagnostic").get(id=job_job_diagnostic_id)
    if not job_job_diagnostic:
        raise HTTPException(status_code=404, detail="Job job diagnostic not found")
    return job_job_diagnostic

@router.post("", response_model=JobJobDiagnosticRead, status_code=status.HTTP_201_CREATED)
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
    
    new_job_job_diagnostic = await JobJobDiagnostic.query.create(**job_job_diagnostic.model_dump())
    return await JobJobDiagnostic.query.select_related("job", "job_diagnostic").get(id=new_job_job_diagnostic.id)

@router.put("/{job_job_diagnostic_id}", response_model=JobJobDiagnosticRead)
async def update_job_job_diagnostic(
    job_job_diagnostic_id: int,
    job_job_diagnostic_update: JobJobDiagnosticUpdate,
    current_user: CurrentUser = Depends(get_current_user)
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
    return await JobJobDiagnostic.query.select_related("job", "job_diagnostic").get(id=job_job_diagnostic_id)

@router.delete("/{job_job_diagnostic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_job_diagnostic(
    job_job_diagnostic_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_diagnostic = await JobJobDiagnostic.query.get(id=job_job_diagnostic_id)
    if not job_job_diagnostic:
        raise HTTPException(status_code=404, detail="Job job diagnostic not found")
    
    await job_job_diagnostic.delete()
    return None 