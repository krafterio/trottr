from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.job_report import JobReport
from models.user import User
from models.job import Job
from schemas.job_report import JobReportCreate, JobReportUpdate, JobReportRead
from api.auth import get_current_user
from services.workspace import get_user_workspace

router = APIRouter()

@router.get("", response_model=List[JobReportRead], dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def list_job_reports(
    job: int = None,
    skip: int = 0,
    limit: int = 100
):
    query = JobReport.query.select_related("created_by")
    
    if job:
        query = query.filter(job=job)
    
    reports = await query.order_by("created_at").offset(skip).limit(limit).all()
    return reports

@router.get("/{report_id}", response_model=JobReportRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def get_job_report(
    report_id: int
):
    report = await JobReport.query.select_related("created_by").get(id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return report

@router.post("", response_model=JobReportRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def create_job_report(
    report: JobReportCreate,
    current_user: User = Depends(get_current_user)
):
    if report.job:
        job = await Job.query.get(id=report.job)
        if not job:
            raise HTTPException(status_code=400, detail="Intervention non trouvée")
    
    data = report.model_dump()
    data["created_by"] = current_user.id
    obj = JobReport(**data)
    await obj.save()
    
    return await JobReport.query.select_related("created_by", "job").get(id=obj.id)

@router.put("/{report_id}", response_model=JobReportRead, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def update_job_report(
    report_id: int,
    report_update: JobReportUpdate
):
    report = await JobReport.query.get(id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    
    update_data = report_update.model_dump(exclude_unset=True)
    
    if "job" in update_data and update_data["job"]:
        job = await Job.query.get(id=update_data["job"])
        if not job:
            raise HTTPException(status_code=400, detail="Intervention non trouvée")
    
    await report.update(**update_data)
    return await JobReport.query.select_related("created_by", "job").get(id=report_id)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def delete_job_report(
    report_id: int
):
    report = await JobReport.query.get(id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    
    await report.delete()
    return None 