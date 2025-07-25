from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core import context
from core.config import get_settings
from models.user import User
from models.workspace import Workspace
from models.workspace_user import WorkspaceUser
from schemas.user import (
    UserLoginPassword,
    UserRegister,
    UserPasswordUpdate,
    AuthToken,
    RefreshToken,
    PasswordUpdateResponse,
    VerificationCode,
    ResendVerificationCode,
    VerificationResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordResetResponse
)
from services.auth import (
    authenticate_user,
    get_password_hash,
    verify_password,
    create_tokens,
    verify_refresh_token,
    revoke_refresh_token
)
from services.verification import (
    create_verification_code,
    verify_code,
    send_verification_email,
    resend_verification_code
)
from services.password_reset import (
    create_password_reset_token,
    verify_reset_token,
    reset_password_with_token,
    send_password_reset_email
)
from services.mail import MailService
from services.recaptcha import RecaptchaService


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(settings=Depends(get_settings), token: str = Depends(oauth2_scheme)) -> User:
    user = context.get_user()

    if user:
        return user

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.query.filter(email=email).first()
    if user is None:
        raise credentials_exception

    context.set_user(user)

    return user


@router.post("/token", response_model=VerificationResponse)
async def login_for_access_token(
    login: UserLoginPassword, 
    mail_service: MailService = Depends(),
    recaptcha_service: RecaptchaService = Depends(),
    settings = Depends(get_settings)
):
    if settings.recaptcha_enabled:
        await recaptcha_service.verify_token(login.recaptcha_token, "login")

    user = await authenticate_user(str(login.email), login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    code = await create_verification_code(user)
    template_name = "emails/verification_login.html" if user.is_verified else "emails/verification_first_login.html"
    await send_verification_email(user, code, mail_service, template_name)
    
    return VerificationResponse(
        message="Verification code sent to your email",
        verified=False
    )


@router.post("/refresh", response_model=AuthToken)
async def refresh_tokens(refresh_token: RefreshToken):
    user = await verify_refresh_token(refresh_token.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, new_refresh_token, expires_in = await create_tokens(user)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user,
    }


@router.post("/logout")
async def logout(refresh_token: RefreshToken):
    success = await revoke_refresh_token(refresh_token.refresh_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )

    return {"message": "Logged out successfully"}


@router.post("/register", response_model=VerificationResponse)
async def register_user(
    user: UserRegister, 
    mail_service: MailService = Depends(),
    recaptcha_service: RecaptchaService = Depends(),
    settings = Depends(get_settings)
):
    invitation = None
    workspace_invitation = None
    
    if settings.mode_preview and not user.invitation_code and not user.workspace_invitation_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code d'invitation requis en mode preview"
        )
    
    if user.workspace_invitation_token:
        from models.workspace_invitation import WorkspaceInvitation
        workspace_invitation = await WorkspaceInvitation.query.select_related('workspace').filter(
            invitation_token=user.workspace_invitation_token,
            email=user.email,
            used_at__is=None
        ).first()
        
        if not workspace_invitation or workspace_invitation.is_expired():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation workspace invalide ou expirée"
            )
    
    if settings.recaptcha_enabled and user.recaptcha_token:
        await recaptcha_service.verify_token(user.recaptcha_token, "register")

    db_user = await User.query.filter(email=user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    password = get_password_hash(user.password)
    user_name = invitation.name if invitation else user.name
    
    db_user = await User.query.create(
        email=user.email,
        name=user_name,
        avatar=user.avatar,
        password=password,
        is_active=True,
        is_verified=False,
        is_superuser=False
    )

    if workspace_invitation:
        # Ajouter l'utilisateur au workspace existant
        await WorkspaceUser.create_member(workspace_invitation.workspace, db_user)
        await workspace_invitation.mark_as_used()
        
        workspace = workspace_invitation.workspace
        workspace_user = await WorkspaceUser.query.filter(workspace=workspace, user=db_user).first()
        context.set_user(db_user)
        context.set_workspace(workspace)
        context.set_workspace_user(workspace_user)
    else:
        # Créer un nouveau workspace (comportement par défaut)
        workspace = await Workspace.create_default(owner=db_user)
        
        if invitation and invitation.company:
            workspace.name = invitation.company
            await workspace.save()
        
        workspace_user = await WorkspaceUser.query.filter(workspace=workspace, user=db_user).first()
        context.set_user(db_user)
        context.set_workspace(workspace)
        context.set_workspace_user(workspace_user)

        if invitation:
            await invitation.delete()

    code = await create_verification_code(db_user)
    await send_verification_email(db_user, code, mail_service)

    return VerificationResponse(
        message="Account created successfully. Please check your email for verification code.",
        verified=False
    )



@router.post("/verify-email", response_model=VerificationResponse)
async def verify_email(verification: VerificationCode):
    user = await User.query.filter(email=verification.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return VerificationResponse(
            message="Email already verified",
            verified=True
        )
    
    is_valid = await verify_code(user, verification.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    return VerificationResponse(
        message="Email verified successfully. You can now log in.",
        verified=True
    )


@router.post("/resend-verification", response_model=VerificationResponse)
async def resend_verification(resend_request: ResendVerificationCode, mail_service: MailService = Depends()):
    user = await User.query.filter(email=resend_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return VerificationResponse(
            message="Email already verified",
            verified=True
        )
    
    await resend_verification_code(user, mail_service)
    
    return VerificationResponse(
        message="Verification code resent successfully. Please check your email.",
        verified=False
    )


@router.post("/resend-login-code", response_model=VerificationResponse)
async def resend_login_code(resend_request: ResendVerificationCode, mail_service: MailService = Depends()):
    user = await User.query.filter(email=resend_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    code = await create_verification_code(user)
    template_name = "emails/verification_login.html" if user.is_verified else "emails/verification_first_login.html"
    await send_verification_email(user, code, mail_service, template_name)
    
    return VerificationResponse(
        message="Verification code resent successfully. Please check your email.",
        verified=False
    )


@router.put("/password", response_model=PasswordUpdateResponse)
async def update_password(
    password_update: UserPasswordUpdate,
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_update.current_password, current_user.password or ""):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    current_user.password = get_password_hash(password_update.new_password)
    await current_user.save()
    return PasswordUpdateResponse()


@router.post("/verify-login-code", response_model=AuthToken)
async def verify_login_code(verification: VerificationCode):
    user = await User.query.filter(email=verification.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    is_valid = await verify_code(user, verification.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    access_token, refresh_token, expires_in = await create_tokens(user)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user,
    }


@router.post("/password-reset-request", response_model=PasswordResetResponse)
async def request_password_reset(
    password_reset_request: PasswordResetRequest,
    mail_service: MailService = Depends(),
    recaptcha_service: RecaptchaService = Depends(),
    settings = Depends(get_settings)
):
    if settings.recaptcha_enabled and password_reset_request.recaptcha_token:
        await recaptcha_service.verify_token(password_reset_request.recaptcha_token, "password_reset")

    user = await User.query.filter(email=password_reset_request.email).first()
    if not user:
        return PasswordResetResponse(
            message="Si cette adresse email existe dans notre système, un lien de réinitialisation a été envoyé."
        )
    
    token = await create_password_reset_token(user)
    await send_password_reset_email(user, token, mail_service)
    
    return PasswordResetResponse(
        message="Si cette adresse email existe dans notre système, un lien de réinitialisation a été envoyé."
    )


@router.post("/password-reset-confirm", response_model=PasswordResetResponse)
async def confirm_password_reset(
    password_reset_confirm: PasswordResetConfirm
):
    success = await reset_password_with_token(password_reset_confirm.token, password_reset_confirm.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de réinitialisation invalide ou expiré"
        )
    
    return PasswordResetResponse(
        message="Votre mot de passe a été réinitialisé avec succès"
    )


@router.get("/workspace-invitation/{token}")
async def get_workspace_invitation(token: str):
    from models.workspace_invitation import WorkspaceInvitation
    
    invitation = await WorkspaceInvitation.query.select_related('workspace').filter(
        invitation_token=token,
        used_at__is=None
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée"
        )
    
    if invitation.is_expired():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation expirée"
        )
    
    return {
        "email": invitation.email,
        "workspace_name": invitation.workspace.name,
        "expires_at": invitation.expires_at
    }
