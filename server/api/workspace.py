from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, File, Query, status
from models.workspace import Workspace
from models.user import User
from models.workspace_invitation import WorkspaceInvitation
from schemas.base import List
from schemas.user import UserRegister, VerificationResponse
from schemas.workspace import WorkspaceUpdate, WorkspaceRead, WorkspaceUserRead
from schemas.workspace_invitation import WorkspaceInvitationCreate, WorkspaceInvitationResponse, WorkspaceInvitationDetails
from api.auth import get_current_user
from services.auth import get_password_hash
from services.mail import MailService
from services.storage import StorageService
from models.workspace_user import WorkspaceUser
from services.verification import create_verification_code, send_verification_email
from core.config import get_settings

from services.workspace import get_user_workspace

router = APIRouter()


@router.get("", response_model=WorkspaceRead)
async def get_workspace(
    workspace: Workspace = Depends(get_user_workspace),
):
    return await _get_workspace_read(workspace)


@router.patch("", response_model=WorkspaceRead)
async def update_workspace(
    workspace_data: WorkspaceUpdate = Body(...),
    workspace: Workspace = Depends(get_user_workspace)
):
    try:
        data = workspace_data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(workspace, key, value)

        await workspace.save()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return await _get_workspace_read(workspace)


@router.get("/members", response_model=List[WorkspaceUserRead])
async def get_workspace_members(
    search: str = Query(None),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser

    # Find workspace where the current user is a member
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(user=current_user).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=404, detail="Aucun workspace trouvé")

    workspace = workspace_user.workspace

    # Get all members of the workspace with their roles
    members_with_roles = await workspace.get_members_with_roles()

    # Filter by search if provided
    if search:
        filtered_members = []
        for member_data in members_with_roles:
            user = member_data["user"]
            if (user.name and search.lower() in user.name.lower()) or \
                    (user.email and search.lower() in user.email.lower()):
                filtered_members.append(member_data)
        members_with_roles = filtered_members

    # Apply pagination
    total = len(members_with_roles)
    paginated_members = members_with_roles[offset:offset + limit]

    # Format for s-many2one component
    items = []
    for member_data in paginated_members:
        user = member_data["user"]
        items.append({
            "id": user.id,
            "name": user.name or user.email,
            "email": user.email,
            "initials": user.initials,
            "avatar": user.avatar,
            "role": member_data["role"],
        })

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/members/{user_id:int}", response_model=WorkspaceUserRead)
async def get_workspace_member(user_id: int):
    from models.workspace_user import WorkspaceUser

    workspace_user = await (WorkspaceUser.query
        .select_related('workspace')
        .select_related('user')
        .filter(
            user=user_id,
        )
        .first())

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=404, detail="Aucun workspace trouvé")

    user = workspace_user.user

    return {
        "id": user.id,
        "name": user.name or user.email,
        "email": user.email,
        "initials": user.initials,
        "avatar": user.avatar,
        "role": workspace_user.role,
    }


@router.patch("/owner/{user_id}", response_model=WorkspaceRead)
async def change_workspace_owner(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser, WorkspaceUserRole

    # Find workspace where the current user is an owner
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(
        user=current_user,
        role=WorkspaceUserRole.OWNER
    ).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour modifier ce workspace")

    workspace = workspace_user.workspace

    # Check if the new owner exists
    new_owner = await User.query.get(id=user_id)
    if not new_owner:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Check if the new owner is a member of the workspace
    is_member = await WorkspaceUser.query.filter(workspace=workspace, user=new_owner).exists()
    if not is_member:
        raise HTTPException(status_code=400, detail="L'utilisateur doit être membre du workspace")

    # Update the new owner's role to Owner or create if not exists
    new_owner_workspace_user = await WorkspaceUser.query.filter(workspace=workspace, user=new_owner).first()
    new_owner_workspace_user.role = WorkspaceUserRole.OWNER
    await new_owner_workspace_user.save()

    return await _get_workspace_read(workspace)


@router.post("/upload-image", response_model=WorkspaceRead)
async def upload_workspace_image(
    file: UploadFile = File(...),
    workspace=Depends(get_user_workspace),
    storage: StorageService = Depends(),
):
    try:
        workspace = await Workspace.query.get(id=workspace.id)
        await storage.delete(workspace.image_url)
        path = await storage.upload(file, 'workspaces')
        workspace.image_url = path
        await workspace.save()

        return await _get_workspace_read(workspace)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload de l'image")


@router.delete("/image", response_model=WorkspaceRead)
async def delete_workspace_image(
    current_user: User = Depends(get_current_user),
    storage: StorageService = Depends(),
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser, WorkspaceUserRole

    # Find workspace where the current user is an owner
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(
        user=current_user,
        role=WorkspaceUserRole.OWNER
    ).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas les droits pour modifier ce workspace"
        )

    workspace = await Workspace.query.get(id=workspace_user.workspace.id)

    try:
        if workspace.image_url:
            await storage.delete(workspace.image_url)
            workspace.image_url = None
            await workspace.save()

        return await _get_workspace_read(workspace)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression de l'image")


@router.post("/member/register")
async def register_workspace_member(
    user: UserRegister,
    mail_service: MailService = Depends(MailService),
    current_user: User = Depends(get_current_user),
) -> VerificationResponse:
    db_user = await User.query.filter(email=user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    password = get_password_hash(user.password)
    db_user = await User.query.create(
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        password=password,
        is_active=True,
        is_verified=False,
        is_superuser=False
    )

    await add_workspace_member(db_user.id, current_user)

    code = await create_verification_code(db_user)
    await send_verification_email(db_user, code, mail_service)

    return VerificationResponse(
        message="Account created successfully. Please check your email for verification code.",
        verified=False
    )


@router.post("/member/{user_id}", response_model=WorkspaceRead)
async def add_workspace_member(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser, WorkspaceUserRole

    # Find workspace where the current user is an owner
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(
        user=current_user,
        role=WorkspaceUserRole.OWNER
    ).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour modifier ce workspace")

    workspace = workspace_user.workspace

    # Check if the user to add exists
    user_to_add = await User.query.get(id=user_id)
    if not user_to_add:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Check if the user is already a member
    is_member = await WorkspaceUser.query.filter(workspace=workspace, user=user_to_add).exists()
    if is_member:
        raise HTTPException(status_code=400, detail="L'utilisateur est déjà membre du workspace")

    # Add the user as a member
    await WorkspaceUser.create_member(workspace, user_to_add)

    return await _get_workspace_read(workspace)


@router.delete("/member/{user_id}", status_code=204)
async def remove_workspace_member(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser, WorkspaceUserRole

    # Find workspace where the current user is an owner
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(
        user=current_user,
        role=WorkspaceUserRole.OWNER
    ).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour modifier ce workspace")

    workspace = workspace_user.workspace

    # Cannot remove yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous retirer vous-même du workspace")

    # Check if the user to remove exists
    user_to_remove = await User.query.get(id=user_id)
    if not user_to_remove:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Check if the user is a member
    user_to_remove_workspace = await WorkspaceUser.query.filter(workspace=workspace, user=user_to_remove).first()
    if not user_to_remove_workspace:
        raise HTTPException(status_code=400, detail="L'utilisateur n'est pas membre du workspace")

    # Cannot remove the owner
    if user_to_remove_workspace.role == WorkspaceUserRole.OWNER:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas retirer le propriétaire du workspace")

    # Remove the user from the workspace
    await user_to_remove_workspace.delete()
    
    # TODO: Cette logique devra être retirée si un jour on veut permettre 
    # à un user d'avoir plusieurs workspaces. Pour l'instant, un user 
    # appartient à un seul workspace, donc on le supprime complètement.
    await user_to_remove.delete()

    return None


@router.patch("/member/{user_id}", response_model=WorkspaceRead)
async def demote_workspace_owner(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Import here to avoid circular imports
    from models.workspace_user import WorkspaceUser, WorkspaceUserRole

    # Find workspace where the current user is an owner
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(
        user=current_user,
        role=WorkspaceUserRole.OWNER
    ).first()

    if not workspace_user or not workspace_user.workspace:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour modifier ce workspace")

    workspace = workspace_user.workspace

    # Check if the user to demote exists
    user_to_demote = await User.query.get(id=user_id)
    if not user_to_demote:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Check if the user is a member of the workspace
    user_to_demote_workspace = await WorkspaceUser.query.filter(workspace=workspace, user=user_to_demote).first()
    if not user_to_demote_workspace:
        raise HTTPException(status_code=400, detail="L'utilisateur n'est pas membre du workspace")

    # Check if the user is an owner
    if user_to_demote_workspace.role != WorkspaceUserRole.OWNER:
        raise HTTPException(status_code=400, detail="L'utilisateur n'est pas propriétaire du workspace")

    # Check if there are other owners
    owners_count = await WorkspaceUser.query.filter(workspace=workspace, role=WorkspaceUserRole.OWNER).count()
    if owners_count <= 1:
        raise HTTPException(status_code=400, detail="Il doit y avoir au moins un propriétaire dans le workspace")

    # Update the user's role to Member
    user_to_demote_workspace.role = WorkspaceUserRole.MEMBER
    await user_to_demote_workspace.save()

    return await _get_workspace_read(workspace    )


@router.post("/invite", response_model=WorkspaceInvitationResponse)
async def invite_user_to_workspace(
    invitation_data: WorkspaceInvitationCreate,
    workspace: Workspace = Depends(get_user_workspace),
    current_user: User = Depends(get_current_user),
    mail_service: MailService = Depends(),
    settings = Depends(get_settings)
):
    existing_user = await User.query.filter(email=invitation_data.email).first()
    if existing_user:
        existing_membership = await WorkspaceUser.query.filter(
            workspace=workspace, 
            user=existing_user
        ).first()
        if existing_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet utilisateur fait déjà partie du workspace"
            )

    existing_invitation = await WorkspaceInvitation.query.filter(
        workspace=workspace,
        email=invitation_data.email
    ).first()
    
    if existing_invitation:
        if existing_invitation.is_used() or existing_invitation.is_expired():
            await existing_invitation.delete()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Une invitation est déjà en cours pour cette adresse email"
            )

    invitation = await WorkspaceInvitation.create_invitation(
        workspace=workspace,
        email=invitation_data.email
    )

    try:
        register_url = f"{settings.base_url_email}/register?token={invitation.invitation_token}"
        await mail_service.send_template(
            template_name="emails/workspace_invitation.html",
            tpl_vals={
                "app_name": "trottr",
                "workspace_name": workspace.name,
                "inviter_name": current_user.name or current_user.email,
                "register_url": register_url,
                "settings": settings,
            },
            email_parts={
                "To": invitation_data.email,
            }
        )
    except Exception as e:
        await invitation.delete()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi de l'email d'invitation"
        )

    return WorkspaceInvitationResponse()


@router.get("/invitations")
async def get_pending_invitations(
    workspace: Workspace = Depends(get_user_workspace),
    current_user: User = Depends(get_current_user)
):
    invitations = await WorkspaceInvitation.query.filter(
        workspace=workspace,
        used_at__is=None
    ).all()
    
    # Filtrer les invitations expirées et formater comme pour les users
    pending_invitations = []
    for invitation in invitations:
        if not invitation.is_expired():
            pending_invitations.append({
                "id": invitation.id,
                "email": invitation.email,
                "created_at": invitation.created_at.isoformat(),
                "expires_at": invitation.expires_at.isoformat(),
                "used_at": invitation.used_at.isoformat() if invitation.used_at else None
            })
    
    return pending_invitations


@router.delete("/invitation/{invitation_id}")
async def cancel_invitation(
    invitation_id: int,
    workspace: Workspace = Depends(get_user_workspace),
    current_user: User = Depends(get_current_user)
):
    invitation = await WorkspaceInvitation.query.filter(
        id=invitation_id,
        workspace=workspace,
        used_at__is=None
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée"
        )
    
    await invitation.delete()
    return {"message": "Invitation annulée"}





async def _get_workspace_read(workspace: Workspace) -> WorkspaceRead:
    owner = await workspace.get_owner()
    member_count = await WorkspaceUser.query.filter(workspace=workspace).count()

    return WorkspaceRead(
        id=workspace.id,
        name=workspace.name,
        unique_id=workspace.unique_id,
        image_url=workspace.image_url,
        currency=workspace.currency,
        selected_plan=workspace.selected_plan,
        available_plans=workspace.available_plans,
        owner=owner,
        member_count=member_count,
        available_usage_credits=workspace.available_usage_credits,
        plan_available_usage_credits=workspace.plan_available_usage_credits,
        pack_available_usage_credits=workspace.pack_available_usage_credits,
        current_usage_credits=workspace.current_usage_credits,
        plan_current_usage_credits=workspace.plan_current_usage_credits,
        pack_current_usage_credits=workspace.pack_current_usage_credits,
        remaining_usage_credits=workspace.remaining_usage_credits,
        plan_remaining_usage_credits=workspace.plan_remaining_usage_credits,
        pack_remaining_usage_credits=workspace.pack_remaining_usage_credits,
        comply_with_local_privacy_laws=workspace.comply_with_local_privacy_laws,
        trial_end=workspace.trial_end,
        is_trial=workspace.is_trial,
        icp=workspace.icp,
    )
