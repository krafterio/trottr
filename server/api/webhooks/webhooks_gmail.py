from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from core.config import get_settings
import httpx

router = APIRouter(prefix="/gmail")

@router.get("/callback")
async def gmail_oauth_callback(code: str = Query(...), state: str = Query(None)):
    settings = get_settings()
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code"
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            if resp.status_code != 200:
                return {"error": f"Erreur Google: {resp.text}"}
            token_data = resp.json()
            
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)
            
            # Récupérer l'email Google via l'API
            user_info_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info = user_info_resp.json() if user_info_resp.status_code == 200 else {}
            google_email = user_info.get("email")
            
            # Récupérer l'utilisateur via le state (user_id)
            if state:
                from models.user import User
                from datetime import datetime, timedelta
                
                user = await User.query.get(id=int(state))
                if user:
                    # Sauvegarder les tokens en base
                    user.google_access_token = access_token
                    user.google_refresh_token = refresh_token
                    user.google_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                    user.google_email = google_email
                    user.google_connected_at = datetime.utcnow()
                    await user.save()
            
            # Rediriger vers le frontend avec un message de succès
            return RedirectResponse(url="http://localhost:5175/?gmail_connected=success")
    except Exception as e:
        return {"error": f"Exception: {str(e)}"} 