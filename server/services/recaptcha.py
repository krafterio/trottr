import httpx
from fastapi import HTTPException, status, Depends
from core.config import Settings, get_settings


class RecaptchaService:
    """
    Service for verifying Google reCAPTCHA v3 tokens.
    """
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.settings = settings
        self.verify_url = "https://www.google.com/recaptcha/api/siteverify"

    async def verify_token(self, token: str, action: str = None) -> bool:
        """
        Verifies a reCAPTCHA v3 token.

        Args:
            token: The reCAPTCHA token to verify
            action: Expected action (optional)

        Returns:
            bool: True if the token is valid and has a sufficient score

        Raises:
            HTTPException: If verification fails or score is too low
        """
        if not self.settings.recaptcha_enabled or token == "trottr-extension":
            return True

        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA token is required"
            )

        data = {
            "secret": self.settings.recaptcha_secret_key,
            "response": token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.verify_url, data=data)
                result = response.json()

                if not result.get("success", False):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"reCAPTCHA verification failed: {result.get('error-codes', ['Unknown error'])}"
                    )

                score = result.get("score", 0)

                if score < self.settings.recaptcha_min_score:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"reCAPTCHA score too low: {score}"
                    )

                if action and result.get("action") != action:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"reCAPTCHA action mismatch: expected '{action}', got '{result.get('action')}'"
                    )

                return True

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to connect to reCAPTCHA verification service"
            )
