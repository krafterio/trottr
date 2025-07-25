import asyncio
import logging
from typing import Dict, Set, Optional, List

from models.user import User
from models.workspace import Workspace

logger = logging.getLogger("presence_service")


class PresenceService:
    def __init__(self):
        self.active_connections: Dict[str, Set[str]] = {}
        self.user_workspaces: Dict[str, str] = {}
        self.cleanup_interval = 300
        self.inactive_threshold = 600
        self._cleanup_task = None

    async def start_cleanup_task(self):
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def stop_cleanup_task(self):
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None

    async def user_connected(self, user_id: str, workspace_id: str, connection_id: str):
        from models.user import User
        from models.workspace import Workspace
        from models.user_presence import UserPresence

        logger.debug(f"User {user_id} connected to workspace {workspace_id} (connection: {connection_id})")

        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()

        self.active_connections[user_id].add(connection_id)

        self.user_workspaces[user_id] = workspace_id

        try:
            user = await User.query.get(id=int(user_id))
            workspace = await Workspace.query.get(id=int(workspace_id))

            if user and workspace:
                await UserPresence.set_user_online(user, workspace)
                await self.broadcast_online_users(workspace, user)
        except Exception as e:
            logger.error(f"Error setting user online in DB: {e}")

    async def user_disconnected(self, user_id: str, connection_id: str):
        from models.user import User
        from models.workspace import Workspace
        from models.user_presence import UserPresence

        logger.debug(f"User {user_id} disconnected (connection: {connection_id})")

        if user_id in self.active_connections:
            self.active_connections[user_id].discard(connection_id)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            workspace_id = self.user_workspaces.get(user_id)

            if workspace_id:
                try:
                    user = await User.query.get(id=int(user_id))
                    workspace = await Workspace.query.get(id=int(workspace_id))

                    if user and workspace:
                        await UserPresence.set_user_offline(user, workspace)
                        await self.broadcast_online_users(workspace, user)
                except Exception as e:
                    logger.error(f"Error setting user offline in DB: {e}")

                if user_id in self.user_workspaces:
                    del self.user_workspaces[user_id]

            logger.debug(f"User {user_id} fully disconnected from workspace {workspace_id}")

    async def user_heartbeat(self, user_id: str):
        from models.user import User
        from models.workspace import Workspace
        from models.user_presence import UserPresence

        workspace_id = self.user_workspaces.get(user_id)

        if not workspace_id:
            return

        try:
            user = await User.query.get(id=int(user_id))
            workspace = await Workspace.query.get(id=int(workspace_id))

            if user and workspace:
                await UserPresence.heartbeat(user, workspace)
        except Exception as e:
            logger.error(f"Error updating heartbeat in DB: {e}")


    async def get_workspace_users(self, workspace_id: str) -> List[str]:
        from models.workspace import Workspace
        from models.user_presence import UserPresence

        try:
            workspace = await Workspace.query.get(id=int(workspace_id))

            if not workspace:
                return []

            users = await UserPresence.get_online_users_for_workspace(workspace)

            return [str(user.id) for user in users]
        except Exception as e:
            logger.error(f"Error getting workspace users from DB: {e}")

            return []

    async def is_user_online(self, user_id: str) -> bool:
        return user_id in self.active_connections

    async def get_user_current_topic(self, user_id: str) -> Optional[str]:
        from models.user import User
        from models.workspace import Workspace
        from models.user_presence import UserPresence

        workspace_id = self.user_workspaces.get(user_id)

        if not workspace_id:
            return None

        try:
            user = await User.query.get(id=int(user_id))
            workspace = await Workspace.query.get(id=int(workspace_id))

            if user and workspace:
                presence = await UserPresence.query.filter(user=user, workspace=workspace).first()

                return presence.current_topic if presence else None
        except Exception as e:
            logger.error(f"Error getting user current topic from DB: {e}")

            return None

    async def get_online_users_data(self, workspace: Workspace, user: User) -> List[Dict]:
        from models.user_presence import UserPresence, PresenceStatus

        try:
            user_data = []

            online_users = await UserPresence.get_online_users_for_workspace(workspace)
            for online_user in online_users:
                user_data.append({
                    "id": online_user.id,
                    "name": online_user.name,
                    "email": online_user.email,
                    "initials": user.initials,
                    "avatar": online_user.avatar
                })

            return user_data
        except Exception as e:
            logger.error(f"Error getting online users data: {e}")

            return []

    async def broadcast_online_users(self, workspace: Workspace, user: User):
        from services.websocket import connection_manager

        try:
            online_users = await self.get_online_users_data(workspace, user)

            await connection_manager.broadcast(
                "online_users_update", 
                {"users": online_users},
                workspace_id=workspace.id,
            )

            logger.debug(f"Broadcasted online users update to workspace {workspace.id}: {len(online_users)} users")
        except Exception as e:
            logger.error(f"Error broadcasting online users: {e}")

    async def _periodic_cleanup(self):
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_inactive_users()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")

    async def _cleanup_inactive_users(self):
        from models.user_presence import UserPresence

        try:
            cleaned = await UserPresence.cleanup_inactive_users(inactive_minutes=self.inactive_threshold // 60)

            if cleaned > 0:
                logger.debug(f"Cleaned up {cleaned} inactive users")
        except Exception as e:
            logger.error(f"Error cleaning up inactive users: {e}")

    async def get_presence_stats(self) -> Dict:
        from models.user_presence import UserPresence

        try:
            db_stats = await UserPresence.get_presence_stats()

            active_connections_count = len(self.active_connections)
            total_websocket_connections = sum(len(connections) for connections in self.active_connections.values())

            return {
                "database": db_stats,
                "websocket": {
                    "active_users": active_connections_count,
                    "total_connections": total_websocket_connections
                }
            }
        except Exception as e:
            logger.error(f"Error getting presence stats: {e}")
            return {"database": {}, "websocket": {"active_users": 0, "total_connections": 0}}

    async def reset_all_presence_statuses(self):
        from models.user_presence import UserPresence, PresenceStatus
        
        try:
            logger.debug("Resetting all user presence statuses and connection counts...")

            await UserPresence.query.update(
                status=PresenceStatus.OFFLINE,
                connection_count=0,
                current_topic=""
            )
            
            logger.debug("All user presence statuses and connection counts have been reset")
        except Exception as e:
            logger.error(f"Error resetting user presence statuses: {e}")


presence_service = PresenceService()
