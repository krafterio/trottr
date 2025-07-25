import json
from typing import Dict, Any, Callable, List, Optional
from fastapi import WebSocketDisconnect
from starlette.websockets import WebSocket
import logging
import uuid
from .presence import presence_service


logger = logging.getLogger("websocket_service")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.user_workspaces: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, user_id: str, workspace_id: str) -> str:
        connection_id = str(uuid.uuid4())

        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}

        self.active_connections[user_id][connection_id] = websocket
        self.user_workspaces[user_id] = workspace_id

        await presence_service.user_connected(user_id, workspace_id, connection_id)

        logger.info(f"Client connected: {user_id} to workspace {workspace_id} (connection_id: {connection_id})")

        return connection_id

    def disconnect(self, user_id: str, connection_id: str):
        if user_id in self.active_connections and connection_id in self.active_connections[user_id]:
            del self.active_connections[user_id][connection_id]
            logger.info(f"Client disconnected: {user_id} (connection_id: {connection_id})")

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

                if user_id in self.user_workspaces:
                    del self.user_workspaces[user_id]

        import asyncio
        asyncio.create_task(presence_service.user_disconnected(user_id, connection_id))

    async def send_message(self, user_id: str, event_type: str, data: Any, workspace_id: str | None = None):
        from core.context import get_workspace

        if workspace_id is None:
            workspace = get_workspace()
            workspace_id = workspace.id if workspace else None

        if workspace_id is not None:
            await self._send_to_workspace_users(workspace_id, event_type, data)

            return

        if user_id in self.active_connections:
            message = {
                "type": event_type,
                "data": data
            }

            payload = json.dumps(message)
            disconnected_connections = []

            for connection_id, websocket in self.active_connections[user_id].items():
                try:
                    await websocket.send_text(payload)
                except Exception as e:
                    logger.debug(f"Error sending message: {e}")
                    disconnected_connections.append((user_id, connection_id))

            for user_id, connection_id in disconnected_connections:
                self.disconnect(user_id, connection_id)

    async def broadcast(self, event_type: str, data: Any, exclude_user_id: Optional[str] = None, workspace_id: str | None = None):
        from core.context import get_workspace

        if workspace_id is None:
            workspace = get_workspace()
            workspace_id = workspace.id if workspace else None

        if workspace_id is not None:
            await self._send_to_workspace_users(workspace_id, event_type, data, exclude_user_id)

            return

        message = {
            "type": event_type,
            "data": data
        }

        payload = json.dumps(message)
        disconnected_connections = []

        for user_id, connections in self.active_connections.items():
            if exclude_user_id and user_id == exclude_user_id:
                continue

            for connection_id, websocket in connections.items():
                try:
                    await websocket.send_text(payload)
                except Exception as e:
                    logger.debug(f"Error during broadcast: {e}")
                    disconnected_connections.append((user_id, connection_id))

        for user_id, connection_id in disconnected_connections:
            self.disconnect(user_id, connection_id)

    def register_handler(self, event_type: str, handler: Callable):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        self.event_handlers[event_type].append(handler)

    async def handle_event(self, event_type: str, data: Any, user_id: str):
        if event_type == "heartbeat":
            await presence_service.user_heartbeat(user_id)

        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                await handler(data, user_id)

    async def _send_to_workspace_users(self, workspace_id: str, event_type: str, data: Any, exclude_user_id: Optional[str] = None):
        workspace_users = await presence_service.get_workspace_users(workspace_id)

        if exclude_user_id:
            workspace_users = [uid for uid in workspace_users if uid != exclude_user_id]

        message = {
            "type": event_type,
            "data": data
        }
        payload = json.dumps(message)
        disconnected_connections = []

        for user_id in workspace_users:
            if user_id in self.active_connections:
                for connection_id, websocket in self.active_connections[user_id].items():
                    try:
                        await websocket.send_text(payload)
                    except Exception as e:
                        logger.debug(f"Error sending message to workspace users: {e}")
                        disconnected_connections.append((user_id, connection_id))

        for user_id, connection_id in disconnected_connections:
            self.disconnect(user_id, connection_id)

        logger.info(f"Sent {event_type} to {len(workspace_users)} users in workspace {workspace_id}")


connection_manager = ConnectionManager()


async def handle_websocket_connection(websocket: WebSocket, user_id: str, workspace_id: str):
    connection_id = await connection_manager.connect(websocket, user_id, workspace_id)

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                event_type = message.get("type")
                event_data = message.get("data", {})

                if not event_type:
                    logger.warning(f"Message received without event type: {data}")
                    continue

                await connection_manager.handle_event(event_type, event_data, user_id)

            except json.JSONDecodeError:
                logger.debug(f"Invalid JSON received: {data}")
            except Exception as e:
                logger.debug(f"Error processing message: {e}")
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, connection_id)
    except Exception as e:
        logger.debug(f"WebSocket connection error: {e}")
        connection_manager.disconnect(user_id, connection_id)
