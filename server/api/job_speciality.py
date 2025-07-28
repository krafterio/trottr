from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from models.job_speciality import JobSpeciality
from models.user import User
from schemas.job_speciality import JobSpecialityCreate, JobSpecialityUpdate, JobSpecialityRead
from api.auth import get_current_user
from services.workspace import get_user_workspace

router = APIRouter()

class JobSpecialityReorderItem(BaseModel):
    id: int
    sequence: int

class JobSpecialityReorder(BaseModel):
    specialities: List[JobSpecialityReorderItem]

@router.get("", response_model=List[JobSpecialityRead], dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def list_job_specialities():
    job_specialities = await JobSpeciality.query.order_by("sequence").all()
    return job_specialities

@router.post("", response_model=JobSpecialityRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_speciality(job_speciality_data: JobSpecialityCreate):
    data = job_speciality_data.model_dump()
    obj = JobSpeciality(**data)
    await obj.save()
    return obj

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_specialities(data: JobSpecialityReorder):
    try:
        for speciality_item in data.specialities:
            job_speciality = await JobSpeciality.query.filter(id=speciality_item.id).first()
            if job_speciality:
                job_speciality.sequence = speciality_item.sequence
                await job_speciality.save()
        
        return {"message": "Spécialités réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_speciality_id}", response_model=JobSpecialityRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_job_speciality(job_speciality_id: int):
    job_speciality = await JobSpeciality.query.get(id=job_speciality_id)
    if not job_speciality:
        raise HTTPException(status_code=404, detail="Spécialité de job non trouvée")
    return job_speciality

@router.patch("/{job_speciality_id}", response_model=JobSpecialityRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def update_job_speciality(job_speciality_id: int, job_speciality_data: JobSpecialityUpdate):
    job_speciality = await JobSpeciality.query.get(id=job_speciality_id)
    if not job_speciality:
        raise HTTPException(status_code=404, detail="Spécialité de job non trouvée")
    
    update_data = job_speciality_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_speciality, field, value)
    
    await job_speciality.save()
    return job_speciality

@router.delete("/{job_speciality_id}", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def delete_job_speciality(job_speciality_id: int):
    job_speciality = await JobSpeciality.query.get(id=job_speciality_id)
    if not job_speciality:
        raise HTTPException(status_code=404, detail="Spécialité de job non trouvée")
    
    await job_speciality.delete()
    return {"message": "Spécialité de job supprimée"} 