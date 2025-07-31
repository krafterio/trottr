from pydantic import BaseModel as PydanticBaseModel
from typing import List


class JobAttachmentResponse(PydanticBaseModel):
    id: int
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    file_extension: str
    is_image: bool
    created_at: str
    job_activity_id: int


class JobAttachmentUploadResponse(PydanticBaseModel):
    success_count: int
    error_count: int
    uploaded_files: List[JobAttachmentResponse]
    errors: List[str]
