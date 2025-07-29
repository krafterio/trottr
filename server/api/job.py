from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from models.job import Job
from models.company import Company
from models.contact import Contact
from models.site import Site
from models.user import User
from models.job_category import JobCategory
from models.job_status import JobStatus
from schemas.job import JobCreate, JobUpdate, JobRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User as CurrentUser

router = APIRouter()

@router.get("", response_model=List[JobRead])
async def list_jobs(
    skip: int = 0,
    limit: int = 50,
    customer_company: int = None,
    customer_contact: int = None,
    current_user: CurrentUser = Depends(get_current_user)
):
    query = Job.query.select_related("customer_company", "customer_contact", "site", "operator", "category", "status")
    
    if customer_company is not None:
        query = query.filter(customer_company=customer_company)
    
    if customer_contact is not None:
        query = query.filter(customer_contact=customer_contact)
    
    jobs = await query.order_by("-created_at").offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobRead)
async def get_job(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job = await Job.query.select_related("customer_company", "customer_contact", "site", "operator", "category", "status").get(id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job(job: JobCreate, workspace=Depends(get_user_workspace)):
    job_data = job.model_dump()
    job_data.pop("reference", None)
    job_data["workspace"] = workspace
    
    if job_data.get("customer_company"):
        company = await Company.query.get(id=job_data["customer_company"])
        if not company:
            raise HTTPException(status_code=400, detail="Customer company not found")
    
    if job_data.get("customer_contact"):
        contact = await Contact.query.get(id=job_data["customer_contact"])
        if not contact:
            raise HTTPException(status_code=400, detail="Customer contact not found")
    
    if job_data.get("site"):
        site = await Site.query.get(id=job_data["site"])
        if not site:
            raise HTTPException(status_code=400, detail="Site not found")
    
    if job_data.get("operator"):
        operator = await User.query.get(id=job_data["operator"])
        if not operator:
            raise HTTPException(status_code=400, detail="Operator not found")
    
    if job_data.get("category"):
        category = await JobCategory.query.get(id=job_data["category"])
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    if job_data.get("status"):
        status = await JobStatus.query.get(id=job_data["status"])
        if not status:
            raise HTTPException(status_code=400, detail="Status not found")
    
    obj = Job(**job_data)
    await obj.save()
    
    return await Job.query.select_related("customer_company", "customer_contact", "site", "operator", "category", "status").get(id=obj.id)

@router.patch("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    job = await Job.query.get(id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job_update.model_dump(exclude_unset=True)
    
    if update_data.get("customer_company"):
        company = await Company.query.get(id=update_data["customer_company"])
        if not company:
            raise HTTPException(status_code=400, detail="Customer company not found")
    
    if update_data.get("customer_contact"):
        contact = await Contact.query.get(id=update_data["customer_contact"])
        if not contact:
            raise HTTPException(status_code=400, detail="Customer contact not found")
    
    if update_data.get("site"):
        site = await Site.query.get(id=update_data["site"])
        if not site:
            raise HTTPException(status_code=400, detail="Site not found")
    
    if update_data.get("operator"):
        operator = await User.query.get(id=update_data["operator"])
        if not operator:
            raise HTTPException(status_code=400, detail="Operator not found")
    
    if update_data.get("category"):
        category = await JobCategory.query.get(id=update_data["category"])
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    if update_data.get("status"):
        status = await JobStatus.query.get(id=update_data["status"])
        if not status:
            raise HTTPException(status_code=400, detail="Status not found")
    
    for field, value in update_data.items():
        setattr(job, field, value)
    
    await job.save()
    
    return await Job.query.select_related("customer_company", "customer_contact", "site", "operator", "category", "status").get(id=job.id)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    job = await Job.query.get(id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    await job.delete()
    return None 

@router.get("/by-operator/{operator_id}", response_model=List[JobRead])
async def get_jobs_by_operator(
    operator_id: int,
    start_date: str = None,
    end_date: str = None,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Récupère les jobs d'un opérateur avec filtres de date optionnels
    start_date et end_date au format ISO (ex: 2025-07-30T00:00:00)
    """
    from datetime import datetime
    
    query = Job.query.select_related("customer_company", "customer_contact", "site", "operator", "category", "status").filter(operator=operator_id)
    
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(scheduled_start__gte=start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format")
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(scheduled_end__lte=end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format")
    
    jobs = await query.order_by("scheduled_start").all()
    return jobs 