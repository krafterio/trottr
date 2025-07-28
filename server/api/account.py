from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, File
from models.user import User
from models.workspace import Workspace
from models.workspace_user import WorkspaceUser, WorkspaceUserRole
from schemas.user import UserUpdate
from api.auth import get_current_user
from typing import Dict, Optional
from pydantic import BaseModel

from services.storage import StorageService

router = APIRouter()


@router.get("", response_model=User)
async def get_account(current_user: User = Depends(get_current_user)):
    return current_user


class UpdateUserProfile(BaseModel):
    name: Optional[str] = None
    zone: Optional[str] = None
    phone: Optional[str] = None
    job_speciality_ids: Optional[list[int]] = None



@router.patch("/profile", response_model=dict)
async def update_user_profile(
    data: UpdateUserProfile,
    current_user: User = Depends(get_current_user)
):
    try:
        if data.name is not None:
            current_user.name = data.name
        if data.zone is not None:
            current_user.zone = data.zone
        if data.phone is not None:
            current_user.phone = data.phone
        
        if data.job_speciality_ids is not None:
            from models.job_speciality import JobSpeciality
            await current_user.job_specialities.clear()
            for speciality_id in data.job_speciality_ids:
                speciality = await JobSpeciality.query.get(id=speciality_id)
                if speciality:
                    await current_user.job_specialities.add(speciality)
        
        await current_user.save()
        
        job_specialities = []
        async for speciality in current_user.job_specialities.all():
            job_specialities.append({
                "id": speciality.id,
                "name": speciality.name,
                "color": speciality.color,
                "sequence": speciality.sequence
            })
        
        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "avatar": current_user.avatar,
            "zone": current_user.zone,
            "phone": current_user.phone,
            "job_specialities": job_specialities,
            "is_verified": current_user.is_verified
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour du profil")



@router.get("/workspace-role", response_model=dict)
async def get_user_workspace_role(current_user: User = Depends(get_current_user)):
    try:
        workspace_user = await WorkspaceUser.query.filter(
            user=current_user
        ).select_related('workspace').first()
        
        if not workspace_user:
            raise HTTPException(status_code=404, detail="Aucun workspace trouvé")
        
        return {
            "role": workspace_user.role,
            "is_owner": workspace_user.role == WorkspaceUserRole.OWNER
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du rôle: {str(e)}")


@router.get("/setup-status", response_model=dict)
async def get_setup_status(current_user: User = Depends(get_current_user)):
    try:
        workspace_user = await WorkspaceUser.query.filter(
            user=current_user
        ).select_related('workspace').first()
        
        workspace = None
        if workspace_user:
            workspace = workspace_user.workspace
        
        user_complete = bool(current_user.name and current_user.name.strip())
        workspace_complete = bool(workspace and workspace.name and workspace.name.strip())
        
        return {
            "user_complete": user_complete,
            "workspace_complete": workspace_complete,
            "setup_complete": user_complete and workspace_complete,
            "user": {
                "name": current_user.name,
                "avatar": current_user.avatar
            },
            "workspace": {
                "name": workspace.name if workspace else None,
                "image_url": workspace.image_url if workspace else None
            } if workspace else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification du statut: {str(e)}")

@router.patch("", response_model=User)
async def update_account(
    user: UserUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    if user.name is not None:
        current_user.name = user.name
    if user.email is not None:
        current_user.email = str(user.email)
    if user.avatar is not None:
        current_user.avatar = user.avatar
    if user.zone is not None:
        current_user.zone = user.zone
    if user.phone is not None:
        current_user.phone = user.phone
    
    if user.job_speciality_ids is not None:
        from models.job_speciality import JobSpeciality
        await current_user.job_specialities.clear()
        for speciality_id in user.job_speciality_ids:
            speciality = await JobSpeciality.query.get(id=speciality_id)
            if speciality:
                await current_user.job_specialities.add(speciality)

    await current_user.save()
    return await User.query.get(id=current_user.id)


@router.get("/workspace-status", response_model=Dict[str, bool])
async def check_workspace_status(current_user: User = Depends(get_current_user)):
    workspace_user = await WorkspaceUser.query.filter(
        user=current_user.id, 
        role=WorkspaceUserRole.OWNER
    ).select_related('workspace').first()
    
    if not workspace_user:
        raise HTTPException(status_code=404, detail="Aucun workspace trouvé")
    
    workspace = workspace_user.workspace
    members_count = await WorkspaceUser.query.filter(workspace=workspace.id).count()
    
    return {
        "is_sole_member": members_count == 1
    }


@router.delete("", status_code=204)
async def delete_account(current_user: User = Depends(get_current_user)):
    workspace_user = await WorkspaceUser.query.filter(
        user=current_user.id, 
        role=WorkspaceUserRole.OWNER
    ).first()
    
    if workspace_user:
        workspace_id = workspace_user.workspace.id
        members_count = await WorkspaceUser.query.filter(workspace=workspace_id).count()
        
        if members_count == 1:
            workspace = await Workspace.query.get(id=workspace_id)
            await workspace.delete()
        else:
            await WorkspaceUser.query.filter(workspace=workspace_id, user=current_user.id).delete()
            
            other_member = await WorkspaceUser.query.filter(workspace=workspace_id).first()
            if other_member:
                other_member.role = WorkspaceUserRole.OWNER
                await other_member.save()
    
    await current_user.delete()
    return None


@router.post("/upload-image", response_model=User)
async def upload_account_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    storage: StorageService = Depends(),
):
    try:
        user = await User.query.get(id=current_user.id)
        await storage.delete(user.avatar)
        path = await storage.upload(file, 'users')
        user.avatar = path
        await user.save()

        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload de l'image")


@router.delete("/image", response_model=User)
async def delete_account_image(
    current_user: User = Depends(get_current_user),
    storage: StorageService = Depends(),
):
    user = await User.query.get(id=current_user.id)

    try:
        if user.avatar:
            await storage.delete(user.avatar)
            user.avatar = None
            await user.save()

        return user
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression de l'image")
