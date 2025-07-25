<template>
</template>

<script setup>
import { onBeforeUnmount, ref, watch } from 'vue';
import { useWebSocket } from '@/common/composables/websocket';
import { useAuthStore } from '@/common/stores/auth';
import { usePresenceStore } from '@/common/stores/presence';
import { useRealtimeStore } from '@/common/stores/realtime';

const { isConnected, connectionError, connect, disconnect, on, sendMessage } = useWebSocket();
const authStore = useAuthStore();
const presenceStore = usePresenceStore();
const realtimeStore = useRealtimeStore();
const connectionStatus = ref('disconnected');

const notificationColors = {
  info: 'info',
  success: 'success',
  warning: 'warning',
  error: 'error',
};

const showNotification = (message, color = 'info', timeout = 5000) => {
  console.log('showNotification:', message, color, timeout);
};

const handleNotification = (payload) => {
  const { type, content } = payload;
  const color = notificationColors[type] || 'info';

  if (content && content.message) {
    showNotification(content.message, color);
  }
};

const handleEntityUpdate = (payload) => {
  const { entity_type, action, data } = payload;
  console.log(`[WebSocket] Update ${entity_type}.${action}`, data);
};

const handleModelUpdate = async (payload) => {
  await realtimeStore.handleModelUpdate(payload);
};

const handleSystemMessage = (payload) => {
  console.log('[WebSocket] System message:', payload);

  if (payload.message) {
    connectionStatus.value = 'connected';
  }
};

const pingServer = async () => {
  if (isConnected.value) {
    try {
      await sendMessage('ping', { timestamp: Date.now() });
    } catch (error) {
      console.warn('[WebSocket] Ping error:', error);
    }
  }
};

const tryConnect = async () => {
  if (!authStore.isAuthenticated) {
    return;
  }

  connectionStatus.value = 'connecting';
  console.log('[WebSocket] Connection attempt...');

  try {
    const success = await connect();

    if (success) {
      on('notification', handleNotification);
      on('entity_update', handleEntityUpdate);
      on('system', handleSystemMessage);

      connectionStatus.value = 'connected';
      console.log('[WebSocket] Connection established');
    } else {
      connectionStatus.value = 'error';
      showNotification(
        'Real-time connection problem. Some updates might be delayed.', 
        'warning'
      );
    }
  } catch (error) {
    connectionStatus.value = 'error';
    console.error('[WebSocket] Connection error:', error);
  }
};

let pingInterval = null;

watch(() => authStore.isAuthenticated, async (isAuth) => {
  if (isAuth) {
    await tryConnect();

    if (!pingInterval) {
      pingInterval = setInterval(pingServer, 30000);
    }
  } else {
    if (pingInterval) {
      clearInterval(pingInterval);
      pingInterval = null;
    }

    await presenceStore.cleanup();
    disconnect();
    connectionStatus.value = 'disconnected';
  }
}, { immediate: true });

watch(connectionError, (error) => {
  if (error) {
    console.error('[WebSocket] Error:', error);
  }
});

onBeforeUnmount(async () => {
  if (pingInterval) {
    clearInterval(pingInterval);
  }

  await presenceStore.cleanup();
  disconnect();
});
</script> 
