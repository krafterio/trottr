from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_job_task import JobJobTask
from models.job import Job
from models.job_task import JobTask
from models.user import User
from schemas.job_job_task import JobJobTaskCreate, JobJobTaskUpdate, JobJobTaskRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User as CurrentUser
from pydantic import BaseModel

class JobJobTaskReorderItem(BaseModel):
    id: int
    sequence: int

class JobJobTaskReorder(BaseModel):
    job_tasks: List[JobJobTaskReorderItem]

router = APIRouter()

@router.get("", response_model=List[JobJobTaskRead])
async def list_job_job_tasks(
    skip: int = 0,
    limit: int = 100,
    job: int = None,
    current_user: CurrentUser = Depends(get_current_user)
):
    query = JobJobTask.query.select_related("done_by", "job", "job_task")
    
    if job is not None:
        query = query.filter(job=job)
    
    job_job_tasks = await query.order_by("sequence").offset(skip).limit(limit).all()
    return job_job_tasks

@router.get("/{job_job_task_id}", response_model=JobJobTaskRead)
async def get_job_job_task(
    job_job_task_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_task = await JobJobTask.query.select_related("done_by", "job", "job_task").get(id=job_job_task_id)
    if not job_job_task:
        raise HTTPException(status_code=404, detail="Job job task not found")
    return job_job_task

@router.post("", response_model=JobJobTaskRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_job_task(job_job_task: JobJobTaskCreate, workspace=Depends(get_user_workspace)):
    job_job_task_data = job_job_task.model_dump()
    job_job_task_data["workspace"] = workspace
    
    last_job_task = await JobJobTask.query.order_by("-sequence").first()
    job_job_task_data["sequence"] = (last_job_task.sequence + 1) if last_job_task else 1
    
    if job_job_task_data.get("job"):
        job = await Job.query.get(id=job_job_task_data["job"])
        if not job:
            raise HTTPException(status_code=400, detail="Job not found")
    
    if job_job_task_data.get("job_task"):
        job_task = await JobTask.query.get(id=job_job_task_data["job_task"])
        if not job_task:
            raise HTTPException(status_code=400, detail="Job task not found")
    
    if job_job_task_data.get("done_by"):
        done_by = await User.query.get(id=job_job_task_data["done_by"])
        if not done_by:
            raise HTTPException(status_code=400, detail="User not found")
    
    new_job_job_task = await JobJobTask.query.create(**job_job_task_data)
    return await JobJobTask.query.select_related("done_by", "job", "job_task").get(id=new_job_job_task.id)

@router.patch("/{job_job_task_id}", response_model=JobJobTaskRead)
async def update_job_job_task(
    job_job_task_id: int,
    job_job_task_update: JobJobTaskUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_task = await JobJobTask.query.get(id=job_job_task_id)
    if not job_job_task:
        raise HTTPException(status_code=404, detail="Job job task not found")
    
    update_data = job_job_task_update.model_dump(exclude_unset=True)
    
    if update_data.get("job"):
        job = await Job.query.get(id=update_data["job"])
        if not job:
            raise HTTPException(status_code=400, detail="Job not found")
    
    if update_data.get("job_task"):
        job_task = await JobTask.query.get(id=update_data["job_task"])
        if not job_task:
            raise HTTPException(status_code=400, detail="Job task not found")
    
    if update_data.get("done_by"):
        done_by = await User.query.get(id=update_data["done_by"])
        if not done_by:
            raise HTTPException(status_code=400, detail="User not found")
    
    await job_job_task.update(**update_data)
    return await JobJobTask.query.select_related("done_by", "job", "job_task").get(id=job_job_task_id)

@router.delete("/{job_job_task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_job_task(
    job_job_task_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_task = await JobJobTask.query.get(id=job_job_task_id)
    if not job_job_task:
        raise HTTPException(status_code=404, detail="Job job task not found")
    
    await job_job_task.delete()
    return None

@router.get("/by-job/{job_id}", response_model=List[JobJobTaskRead])
async def get_job_job_tasks_by_job(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job_job_tasks = await JobJobTask.query.select_related("done_by", "job", "job_task").filter(job=job_id).order_by("sequence").all()
    return job_job_tasks

@router.put("/reorder", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def reorder_job_job_tasks(data: JobJobTaskReorder):
    try:
        for job_task_item in data.job_tasks:
            job_job_task = await JobJobTask.query.filter(id=job_task_item.id).first()
            if job_job_task:
                job_job_task.sequence = job_task_item.sequence
                await job_job_task.save()
        
        return {"message": "Tâches de job réorganisées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 