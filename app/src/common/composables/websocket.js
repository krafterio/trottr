import { onBeforeUnmount, ref, computed } from 'vue';
import { useAuthStore } from '@/common/stores/auth';
import { websocketService } from '@/common/services/websocket';

export function useWebSocket(autoConnect = false) {
  const isConnected = ref(false);
  const connectionError = ref(null);
  const authStore = useAuthStore();
  let connectionAttempted = false;

  const isWebSocketSupported = computed(() => {
    return typeof WebSocket !== 'undefined';
  });

  const connect = async () => {
    if (connectionAttempted || isConnected.value) {
      console.debug("[WebSocket] Connection already attempted or active");

      return isConnected.value;
    }

    connectionAttempted = true;

    if (!isWebSocketSupported.value) {
      connectionError.value = "WebSockets are not supported by your browser";
      connectionAttempted = false;

      return false;
    }

    if (!authStore.token) {
      connectionError.value = "Authentication required";
      connectionAttempted = false;

      return false;
    }

    try {
      connectionError.value = null;
      await websocketService.connect();
      isConnected.value = true;

      return true;
    } catch (error) {
      connectionError.value = error.message || "WebSocket connection failed";
      isConnected.value = false;
      console.error("[WebSocket] Connection error:", error);

      return false;
    } finally {
      connectionAttempted = false;
    }
  };

  const disconnect = () => {
    if (!isConnected.value && !websocketService.socket) {
      return;
    }

    websocketService.disconnect();
    isConnected.value = false;
    connectionAttempted = false;
  };

  const sendMessage = async (type, data = {}) => {
    if (!isConnected.value) {
      try {
        const connected = await connect();
        if (!connected) {
          throw new Error("Unable to establish WebSocket connection");
        }
      } catch (error) {
        connectionError.value = error.message;

        throw error;
      }
    }

    try {
      await websocketService.sendMessage(type, data);

      return true;
    } catch (error) {
      connectionError.value = error.message || "Failed to send message";
      console.error("[WebSocket] Send error:", error);

      return false;
    }
  };

  const on = (eventType, callback) => {
    return websocketService.on(eventType, callback);
  };

  onBeforeUnmount(() => {
    disconnect();
  });

  return {
    isConnected,
    connectionError,
    isWebSocketSupported,
    connect,
    disconnect,
    sendMessage,
    on,
  };
}
