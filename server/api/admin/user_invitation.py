from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import secrets
import string

from core.config import get_settings
from services.mail import MailService

router = APIRouter(prefix="/admin/user_invitations")


class SendInvitationCodeResponse(BaseModel):
    message: str = "Code d'invitation envoyé avec succès"


@router.post("/{invitation_id}/send-code", response_model=SendInvitationCodeResponse)
async def send_invitation_code(
        invitation_id: int,
        mail_service: MailService = Depends(),
        settings=Depends(get_settings)
):
    if not settings.mode_preview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This endpoint is not available"
        )

    invitation = await UserInvitation.query.filter(id=invitation_id).first()
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée"
        )

    if not invitation.invitation_code:
        chars = string.ascii_uppercase + string.digits
        code = ''.join(secrets.choice(chars) for _ in range(8))
        invitation.invitation_code = code
        await invitation.save()

    try:
        register_url = f"{settings.base_url_email}/register/{invitation.invitation_code}"
        await mail_service.send_template(
            template_name="emails/invitation_code.html",
            tpl_vals={
                "app_name": "Trottr",
                "customer_name": invitation.name,
                "register_url": register_url,
                "invitation_code": invitation.invitation_code,
                "settings": settings,
            },
            email_parts={
                "To": invitation.email,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi de l'email"
        )

    return SendInvitationCodeResponse()
