import json
from typing import Any, Optional
from models.job_activity import JobActivity, JobActivityType, JobActivityValueType
from models.job import Job


class JobActivityService:
    """Service for creating and managing job activities"""
    
    @staticmethod
    async def create_message(
        job: Job,
        message: str
    ) -> JobActivity:
        """Create a message activity"""
        activity = JobActivity(
            job=job,
            type=JobActivityType.message,
            content=message
        )

        await activity.save()

        return activity
    
    @staticmethod
    async def create_note(
        job: Job,
        note: str
    ) -> JobActivity:
        """Create a note activity"""
        activity = JobActivity(
            job=job,
            type=JobActivityType.note,
            content=note
        )

        await activity.save()

        return activity
    
    @staticmethod
    async def create_tracking_create(
        job: Job,
        content: Optional[str] = None
    ) -> JobActivity:
        """Create a tracking create activity"""
        activity = JobActivity(
            job=job,
            type=JobActivityType.tracking_create,
            content=content or f"Job créé"
        )

        await activity.save()

        return activity
    
    @staticmethod
    async def create_tracking_update(
        job: Job,
        field_name: str,
        old_value: Any,
        new_value: Any,
        content: Optional[str] = None
    ) -> JobActivity:
        """Create a tracking update activity"""
        
        value_type = JobActivityService._detect_value_type(new_value)
        
        activity = JobActivity(
            job=job,
            type=JobActivityType.tracking_update,
            content=content or f"Champ '{field_name}' modifié",
            field_name=field_name,
            value_type=value_type,
            old_value=JobActivityService._serialize_value(old_value),
            new_value=JobActivityService._serialize_value(new_value)
        )

        await activity.save()

        return activity
    
    @staticmethod
    def _detect_value_type(value: Any) -> JobActivityValueType:
        """Detect the type of a value"""
        if isinstance(value, str):
            return JobActivityValueType.string
        elif isinstance(value, int):
            return JobActivityValueType.integer
        elif isinstance(value, float):
            return JobActivityValueType.float
        elif isinstance(value, bool):
            return JobActivityValueType.bool
        else:
            return JobActivityValueType.object
    
    @staticmethod
    def _serialize_value(value: Any) -> str:
        """Serialize a value to JSON string"""
        if value is None:
            return ""
        
        if isinstance(value, (str, int, float, bool)):
            return str(value)

        try:
            return json.dumps(value, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(value)
