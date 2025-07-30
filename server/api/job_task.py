from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_task import JobTask
from schemas.job_task import JobTaskCreate, JobTaskUpdate, JobTaskRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User as CurrentUser
from pydantic import BaseModel

class JobTaskReorderItem(BaseModel):
    id: int
    sequence: int

class JobTaskReorder(BaseModel):
    tasks: List[JobTaskReorderItem]

router = APIRouter()

@router.get("", response_model=List[JobTaskRead])
async def list_job_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_tasks = await JobTask.query.order_by("sequence").offset(skip).limit(limit).all()
    return job_tasks

@router.get("/{job_task_id}", response_model=JobTaskRead)
async def get_job_task(
    job_task_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_task = await JobTask.query.get(id=job_task_id)
    if not job_task:
        raise HTTPException(status_code=404, detail="Job task not found")
    return job_task

@router.post("", response_model=JobTaskRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_task(job_task: JobTaskCreate, workspace=Depends(get_user_workspace)):
    job_task_data = job_task.model_dump()
    job_task_data["workspace"] = workspace
    
    last_task = await JobTask.query.order_by("-sequence").first()
    job_task_data["sequence"] = (last_task.sequence + 1) if last_task else 1
    
    new_job_task = await JobTask.query.create(**job_task_data)
    return await JobTask.query.get(id=new_job_task.id)

@router.patch("/{job_task_id}", response_model=JobTaskRead)
async def update_job_task(
    job_task_id: int,
    job_task_update: JobTaskUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_task = await JobTask.query.get(id=job_task_id)
    if not job_task:
        raise HTTPException(status_code=404, detail="Job task not found")
    
    update_data = job_task_update.model_dump(exclude_unset=True)
    await job_task.update(**update_data)
    return await JobTask.query.get(id=job_task_id)

@router.delete("/{job_task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_task(
    job_task_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_task = await JobTask.query.get(id=job_task_id)
    if not job_task:
        raise HTTPException(status_code=404, detail="Job task not found")
    
    await job_task.delete()
    return None

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_tasks(data: JobTaskReorder):
    try:
        for task_item in data.tasks:
            job_task = await JobTask.query.filter(id=task_item.id).first()
            if job_task:
                job_task.sequence = task_item.sequence
                await job_task.save()
        
        return {"message": "Tâches réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 