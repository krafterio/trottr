import os
from typing import List

from edgy import ObjectNotFound
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from models.job import Job
from models.job_activity import JobActivity, JobActivityType
from models.job_attachment import JobAttachment
from schemas.job_attachment import JobAttachmentUploadResponse, JobAttachmentResponse
from services.storage import StorageService

router = APIRouter(prefix="/job_attachments", tags=["job_attachments"])

@router.post("/{job_id}/upload")
async def upload_job_attachments(
        job_id: int,
        files: List[UploadFile] = File(...),
        storage: StorageService = Depends(),
) -> JobAttachmentUploadResponse:
    try:
        job = await Job.query.get(id=job_id)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Job not found")

    uploaded_files = []
    errors = []
    success_count = 0
    error_count = 0

    attachment_names = []
    valid_files = []

    for file in files:
        if file.size and file.size > 20 * 1024 * 1024:  # 20MB limit
            errors.append(f"Fichier {file.filename} trop volumineux (max 20MB)")
            error_count += 1
        else:
            valid_files.append(file)
            attachment_names.append(file.filename or "fichier sans nom")

    activity = None
    if valid_files:
        activity = JobActivity(
            job=job,
            type=JobActivityType.attachments
        )
        await activity.save()

    for file in valid_files:
        try:
            file_extension = os.path.splitext(file.filename or "")[1].lower()
            is_image = file.content_type and file.content_type.startswith('image/')
            
            path = await storage.upload(file, 'job_attachments')
            
            record = JobAttachment(
                job=job,
                job_activity=activity,
                filename=os.path.basename(path),
                file_path=path,
                file_size=file.size or 0,
                mime_type=file.content_type or "",
                file_extension=file_extension,
                is_image=is_image,
            )
            await record.save()

            uploaded_files.append(JobAttachmentResponse(
                id=record.id,
                filename=record.filename,
                file_path=record.file_path,
                file_size=record.file_size,
                mime_type=record.mime_type,
                file_extension=record.file_extension,
                is_image=record.is_image,
                job_activity_id=record.job_activity.id,
                created_at=record.created_at.isoformat() if record.created_at else ""
            ))
            success_count += 1

        except Exception as e:
            errors.append(f"Erreur lors de l'upload de {file.filename}: {str(e)}")
            error_count += 1

    return JobAttachmentUploadResponse(
        success_count=success_count,
        error_count=error_count,
        uploaded_files=uploaded_files,
        errors=errors
    )
