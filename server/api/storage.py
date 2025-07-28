from edgy import ObjectNotFound
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from starlette.responses import Response
import mimetypes

from api.auth import get_current_user
from models.base import BaseModel
from models.user import User
from models.workspace import Workspace
from services.storage import StorageService
from services.workspace import get_user_workspace

router = APIRouter()

@router.post("/storage/upload/{model:str}/{model_id}/{field:str}")
async def upload_file(
        model: str,
        field: str,
        model_id: int,
        file: UploadFile = File(...),
        storage: StorageService = Depends(),
        current_user: User = Depends(get_current_user),
        workspace: Workspace = Depends(get_user_workspace),
) -> str:
    try:
        record = await _get_record(model, field, model_id, current_user, workspace)

        if getattr(record, field):
            await storage.delete(getattr(record, field))

        path = await storage.upload(file, model)
        setattr(record, field, path)
        await record.save()

        return path
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error uploading file")


@router.delete("/storage/file/{model:str}/{model_id}/{field:str}")
async def delete_file(
        model: str,
        field: str,
        model_id: int,
        storage: StorageService = Depends(),
        current_user: User = Depends(get_current_user),
        workspace=Depends(get_user_workspace),
) -> None:
    try:
        record = await _get_record(model, field, model_id, current_user, workspace)

        if getattr(record, field):
            await storage.delete(getattr(record, field))

        setattr(record, field, None)
        await record.save()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error deleteing file")


@router.get("/storage/download/{path:path}")
async def download_file(
        path: str,
        force_download: bool = Query(False),
        storage: StorageService = Depends(),
) -> Response:
    try:
        file_path = storage.get_file_path(path, ensure_exists=False)

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Fichier non trouvé")

        filename = file_path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        async def file_stream():
            chunk_size = 1024 * 1024  # 1MB

            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    yield chunk

        headers = {
            "Content-Disposition": (
                f"attachment; filename=\"{filename}\"" if force_download
                else f"inline; filename=\"{filename}\""
            ),
        }

        return StreamingResponse(
            file_stream(),
            media_type=content_type,
            headers=headers,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement: {str(e)}")


async def _get_record(
        model: str,
        field: str,
        model_id: int,
        current_user: User,
        workspace: Workspace
) -> BaseModel:
    if model == "users":
        record = await User.query.get(id=model_id)

        if field not in User.meta.fields:
            raise ValueError(f"Field {field} not found in model {model}")
    elif model == "workspaces":
        record = await Workspace.query.get(id=workspace.id)

        if field not in Workspace.meta.fields:
            raise ValueError(f"Field {field} not found in model {model}")
    else:
        meta_model = await metadata_model_registry.get_metadata(model)

        if field not in meta_model.fields:
            raise ValueError(f"Field {field} not found in model {model}")

        model_cls = await metadata_model_registry.get_model_from_metadata(meta_model)
        record = await model_cls.query.get(id=model_id)

    return record
