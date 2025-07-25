from fastapi import APIRouter, Depends

from models.user import User
from models.user_presence import UserPresence
from services.presence import presence_service
from api.auth import get_current_user
from services.workspace import get_user_workspace
from services.websocket import connection_manager


router = APIRouter()


@router.get("/presence/stats")
async def get_presence_stats():
    return await presence_service.get_presence_stats()


@router.get("/presence/detailed")
async def get_detailed_presence_stats(
    current_user: User = Depends(get_current_user),
    workspace = Depends(get_user_workspace)
):
    db_stats = await UserPresence.get_presence_stats()
    online_users = await UserPresence.get_online_users_for_workspace(workspace)

    multi_device_stats = {
        "total_websocket_connections": sum(
            len(connections) for connections in connection_manager.active_connections.values()
        ),
        "users_with_multiple_devices": sum(
            1 for connections in connection_manager.active_connections.values() 
            if len(connections) > 1
        ),
        "connection_details": {
            user_id: len(connections) 
            for user_id, connections in connection_manager.active_connections.items()
            if len(connections) > 1
        }
    }

    return {
        "workspace_id": workspace.id,
        "workspace_name": workspace.name,
        "total_stats": db_stats,
        "workspace_online_users": [{"id": u.id, "email": u.email, "name": u.name} for u in online_users],
        "multi_device_stats": multi_device_stats
    }
