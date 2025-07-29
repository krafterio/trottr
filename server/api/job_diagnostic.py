from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_diagnostic import JobDiagnostic
from schemas.job_diagnostic import JobDiagnosticCreate, JobDiagnosticUpdate, JobDiagnosticRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User as CurrentUser
from pydantic import BaseModel

router = APIRouter()

class JobDiagnosticReorderItem(BaseModel):
    id: int
    sequence: int

class JobDiagnosticReorder(BaseModel):
    diagnostics: List[JobDiagnosticReorderItem]

@router.get("", response_model=List[JobDiagnosticRead], dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def list_job_diagnostics():
    job_diagnostics = await JobDiagnostic.query.order_by("sequence").all()
    return job_diagnostics

@router.post("", response_model=JobDiagnosticRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_diagnostic(job_diagnostic_data: JobDiagnosticCreate):
    data = job_diagnostic_data.model_dump()
    
    last_diagnostic = await JobDiagnostic.query.order_by("-sequence").first()
    data["sequence"] = (last_diagnostic.sequence + 1) if last_diagnostic else 1
    
    obj = JobDiagnostic(**data)
    await obj.save()
    return obj

@router.get("/{job_diagnostic_id}", response_model=JobDiagnosticRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_job_diagnostic(job_diagnostic_id: int):
    job_diagnostic = await JobDiagnostic.query.get(id=job_diagnostic_id)
    if not job_diagnostic:
        raise HTTPException(status_code=404, detail="Job diagnostic not found")
    return job_diagnostic

@router.patch("/{job_diagnostic_id}", response_model=JobDiagnosticRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def update_job_diagnostic(job_diagnostic_id: int, job_diagnostic_data: JobDiagnosticUpdate):
    job_diagnostic = await JobDiagnostic.query.get(id=job_diagnostic_id)
    if not job_diagnostic:
        raise HTTPException(status_code=404, detail="Job diagnostic not found")
    
    update_data = job_diagnostic_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_diagnostic, field, value)
    
    await job_diagnostic.save()
    return job_diagnostic

@router.delete("/{job_diagnostic_id}", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def delete_job_diagnostic(job_diagnostic_id: int):
    job_diagnostic = await JobDiagnostic.query.get(id=job_diagnostic_id)
    if not job_diagnostic:
        raise HTTPException(status_code=404, detail="Job diagnostic not found")
    
    await job_diagnostic.delete()
    return {"message": "Job diagnostic supprimé"} 

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_diagnostics(data: JobDiagnosticReorder):
    try:
        for diagnostic_item in data.diagnostics:
            job_diagnostic = await JobDiagnostic.query.filter(id=diagnostic_item.id).first()
            if job_diagnostic:
                job_diagnostic.sequence = diagnostic_item.sequence
                await job_diagnostic.save()
        
        return {"message": "Diagnostics réorganisés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 