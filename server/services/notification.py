import logging

from typing import Dict, Any, Optional
from services.websocket import connection_manager


logger = logging.getLogger("notification_service")


class NotificationService:
    async def send_notification(self, user_id: str, notification_type: str, content: Dict[str, Any]) -> bool:
        """
        Sends a notification to a specific user.

        Args:
            user_id: User ID
            notification_type: Notification type (info, success, warning, error)
            content: Notification content

        Returns:
            bool: True if the notification was sent
        """
        try:
            logger.info(f"Sending notification to user {user_id}: {notification_type}")

            payload = {
                "type": notification_type,
                "content": content
            }

            await connection_manager.send_message(user_id, "notification", payload)

            return True
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

            return False

    async def broadcast_notification(self, notification_type: str, content: Dict[str, Any], exclude_user_id: Optional[str] = None) -> bool:
        """
        Broadcasts a notification to all connected users

        Args:
            notification_type: Notification type (info, success, warning, error)
            content: Notification content
            exclude_user_id: User ID to exclude (optional)

        Returns:
            bool: True if the notification was broadcast
        """
        try:
            logger.info(f"Broadcasting a notification: {notification_type}")
            payload = {
                "type": notification_type,
                "content": content
            }

            await connection_manager.broadcast("notification", payload, exclude_user_id)

            return True
        except Exception as e:
            logger.error(f"Error broadcasting notification: {e}")

            return False

    async def send_update(self, user_id: str, entity_type: str, action: str, data: Dict[str, Any]) -> bool:
        """
        Sends an entity update to a specific user

        Args:
            user_id: User ID
            entity_type: Entity type (lead, contact, company, etc.)
            action: Action performed (create, update, delete)
            data: Entity data

        Returns:
            bool: True if the update was sent
        """
        try:
            logger.info(f"Sending update to user {user_id}: {entity_type}.{action}")

            payload = {
                "entity_type": entity_type,
                "action": action,
                "data": data
            }

            await connection_manager.send_message(user_id, "entity_update", payload)

            return True
        except Exception as e:
            logger.error(f"Error sending update: {e}")

            return False

    async def broadcast_update(self, entity_type: str, action: str, data: Dict[str, Any], exclude_user_id: Optional[str] = None) -> bool:
        """
        Broadcasts an entity update to all connected users

        Args:
            entity_type: Entity type (lead, contact, company, etc.)
            action: Action performed (create, update, delete)
            data: Entity data
            exclude_user_id: User ID to exclude (optional)

        Returns:
            bool: True if the update was broadcast
        """
        try:
            logger.info(f"Broadcasting an update: {entity_type}.{action}")

            payload = {
                "entity_type": entity_type,
                "action": action,
                "data": data
            }

            await connection_manager.broadcast("entity_update", payload, exclude_user_id)

            return True
        except Exception as e:
            logger.error(f"Error broadcasting update: {e}")

            return False

notification_service = NotificationService() 
