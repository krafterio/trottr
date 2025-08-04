from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from typing import List
from datetime import datetime
import os
import base64
from models.job_report import JobReport
from models.user import User
from models.job import Job
from models.job_job_diagnostic import JobJobDiagnostic
from models.job_job_task import JobJobTask
from models.workspace import Workspace
from schemas.job_report import JobReportCreate, JobReportUpdate, JobReportRead
from api.auth import get_current_user
from services.workspace import get_user_workspace
from services.pdf_render import PDFRenderService
from core.config import get_settings

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

@router.get("/{report_id}/pdf", dependencies=[Depends(get_current_user), Depends(get_user_workspace)])
async def generate_job_report_pdf(
    report_id: int,
    workspace: Workspace = Depends(get_user_workspace)
):
    # Recharger les settings pour s'assurer d'avoir la dernière config
    from core.config import Settings
    settings = Settings()
    
    print(f"DEBUG ENDPOINT: pdf_display = {settings.pdf_display}")
    
    report = await JobReport.query.select_related(
        "created_by", 
        "job", 
        "job__customer_company", 
        "job__customer_contact", 
        "job__site", 
        "job__operator",
        "job__category",
        "job__status"
    ).get(id=report_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    
    diagnostics = []
    tasks = []
    
    if report.include_diagnostics:
        diagnostics = await JobJobDiagnostic.query.select_related(
            "job_diagnostic"
        ).filter(job=report.job).order_by("sequence").all()
    
    if report.include_tasks:
        tasks = await JobJobTask.query.select_related(
            "job_task", "done_by"
        ).filter(job=report.job).order_by("sequence").all()
    
    logo_data_url = None
    logo_path = os.path.join(settings.project_dir, 'uploads', 'logos', 'trottr-favicon-simple.png')
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                logo_data_url = f"data:image/png;base64,{encoded_string}"
        except Exception:
            pass
    
    context = {
        'report': report,
        'job': report.job,
        'diagnostics': diagnostics,
        'tasks': tasks,
        'workspace': workspace,
        'logo_data_url': logo_data_url,
        'current_date': datetime.now().strftime('%d/%m/%Y à %H:%M')
    }
    
    pdf_service = PDFRenderService()
    
    if settings.pdf_display:
        html_content = await pdf_service.generate_pdf('job_report.html', context)
        return HTMLResponse(content=html_content, media_type="text/html")
    else:
        pdf_path = await pdf_service.generate_pdf('job_report.html', context)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="Erreur lors de la génération du PDF")
        
        filename = f"rapport_intervention_{report.job.reference}_{report_id}.pdf"
        
        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type='application/pdf',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        ) 