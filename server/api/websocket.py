import logging
import json
import asyncio

from fastapi import APIRouter, WebSocket, status
from jose import JWTError, jwt
from typing import Optional

from core.config import get_settings
from models.user import User
from models.workspace_user import WorkspaceUser
from services.websocket import handle_websocket_connection


router = APIRouter()
logger = logging.getLogger("websocket_api")


AUTH_TIMEOUT = 30  # seconds


async def authenticate_user_by_token(token: str) -> Optional[User]:
    settings = get_settings()

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: Optional[str] = payload.get("sub")

        if email is None:
            logger.debug(f"Token without 'sub' claim")

            return None
    except JWTError:
        logger.debug(f"Invalid JWT token")

        return None

    user = await User.query.filter(email=email).first()

    if user is None:
        logger.debug(f"User not found for email: {email}")

        return None

    return user


async def get_user_workspace_id(user: User) -> Optional[str]:
    workspace_user = await WorkspaceUser.query.select_related('workspace').filter(user=user).first()

    if workspace_user and workspace_user.workspace:
        return str(workspace_user.workspace.id)

    return None


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.debug(f"New WebSocket connection accepted, waiting for authentication")

    try:
        try:
            auth_message_raw = await asyncio.wait_for(
                websocket.receive_text(), 
                timeout=AUTH_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.debug(f"Authentication timeout after {AUTH_TIMEOUT} seconds")
            await websocket.send_text(json.dumps({
                "type": "auth_error", 
                "data": {"message": "Authentication timeout"}
            }))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

            return

        try:
            auth_message = json.loads(auth_message_raw)
        except json.JSONDecodeError:
            logger.debug(f"Invalid authentication message: incorrect JSON format")
            await websocket.send_text(json.dumps({"type": "auth_error", "data": {"message": "Invalid authentication format"}}))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

            return

        if auth_message.get("type") != "authenticate" or not auth_message.get("data", {}).get("token"):
            logger.debug(f"Invalid authentication message: incorrect structure")
            await websocket.send_text(json.dumps({"type": "auth_error", "data": {"message": "Invalid authentication message"}}))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

            return

        token = auth_message["data"]["token"]
        user = await authenticate_user_by_token(token)

        if not user:
            logger.debug(f"Authentication failed: invalid token or user not found")
            await websocket.send_text(json.dumps({"type": "auth_error", "data": {"message": "Invalid authentication token"}}))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

            return

        workspace_id = await get_user_workspace_id(user)

        if not workspace_id:
            logger.debug(f"No workspace found for user: {user.email}")
            await websocket.send_text(json.dumps({"type": "auth_error", "data": {"message": "No workspace found for user"}}))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

            return

        logger.debug(f"WebSocket connection authenticated for user: {user.email} in workspace: {workspace_id}")

        await websocket.send_text(json.dumps({
            "type": "auth_success", 
            "data": {
                "user_id": str(user.id),
                "email": user.email,
                "workspace_id": workspace_id
            }
        }))

        await handle_websocket_connection(websocket, str(user.id), workspace_id)

    except Exception as e:
        logger.debug(f"Error handling WebSocket connection: {e}")

        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass
