from core import context
from models.workspace import Workspace
from api.auth import get_current_user
from models.workspace_user import WorkspaceUser
from fastapi import Depends, HTTPException, status


async def get_user_workspace(current_user = Depends(get_current_user)) -> Workspace:
    workspace = context.get_workspace()
    workspace_user = context.get_workspace_user()

    if workspace and workspace_user:
        return workspace

    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(user=current_user).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun workspace trouvé",
        )

    workspace = await Workspace.query.get(id=workspace_user.workspace.id)
    context.set_user(current_user)
    context.set_workspace(workspace)
    context.set_workspace_user(workspace_user)

    return workspace

