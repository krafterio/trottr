from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from starlette.responses import Response
import mimetypes

from services.storage import StorageService

router = APIRouter()


@router.get("/storage/download/{workspace_id:int}/{path:path}")
async def download_file(
        workspace_id: int,
        path: str,
        force_download: bool = Query(False),
        storage: StorageService = Depends(),
) -> Response:
    try:
        file_path = storage.get_file_path(str(workspace_id) + '/' + path, ensure_exists=False, global_storage=True)

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
