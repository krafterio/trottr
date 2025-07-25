import { useAuthStore } from '@/common/stores/auth';
import {getApiUrl} from "@/common/plugins/fetcher.js";

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectInterval = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 2000;
    this.eventListeners = {};
    this.connectionPromise = null;
    this.manualDisconnect = false;
    this.connectingUrl = null;
    this.authenticated = false;
  }

  async connect() {
    if (this.isConnected && this.socket && this.socket.readyState === WebSocket.OPEN && this.authenticated) {
      console.debug('[WebSocketService] Already connected and authenticated, connection ignored');

      return Promise.resolve();
    }

    if (this.connectionPromise) {
      console.debug('[WebSocketService] Connection already in progress, returning existing promise');

      return this.connectionPromise;
    }

    const authStore = useAuthStore();
    if (!authStore.token) {
      console.error('[WebSocketService] No authentication token');

      return Promise.reject(new Error('No authentication token available'));
    }

    this.manualDisconnect = false;
    this.authenticated = false;

    if (this.socket) {
      try {
        console.debug('[WebSocketService] Closing old socket before reconnection');
        this.socket.close();
      } catch (e) {
        console.warn('[WebSocketService] Error when closing old socket:', e);
      }

      this.socket = null;
    }

    this.connectionPromise = new Promise((resolve, reject) => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = getApiUrl().replace(/^https?:\/\//, '');
      const wsUrl = `${protocol}//${host}/ws`;

      this.connectingUrl = wsUrl;
      console.debug(`[WebSocketService] Connecting to ${wsUrl}`);

      try {
        this.socket = new WebSocket(wsUrl);
      } catch (error) {
        console.error('[WebSocketService] Error creating WebSocket:', error);
        this.connectionPromise = null;
        this.connectingUrl = null;
        reject(error);

        return;
      }

      this.socket.onopen = async () => {
        console.debug('[WebSocketService] WebSocket connection opened, sending authentication token');

        try {
          const authMessage = {
            type: 'authenticate',
            data: {
              token: authStore.token
            }
          };

          this.socket.send(JSON.stringify(authMessage));

        } catch (error) {
          console.error('[WebSocketService] Error sending token:', error);

          if (this.socket) {
            this.socket.close();
            this.socket = null;
          }

          this.connectionPromise = null;
          this.connectingUrl = null;
          reject(error);
        }
      };

      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          const { type, data } = message;

          if (type === 'auth_success') {
            console.debug('[WebSocketService] WebSocket authentication successful');
            this.isConnected = true;
            this.authenticated = true;
            this.reconnectAttempts = 0;
            this.connectingUrl = null;

            if (this.reconnectInterval) {
              clearInterval(this.reconnectInterval);
              this.reconnectInterval = null;
            }

            resolve();
            this.connectionPromise = null;
            console.info('[WebSocketService] WebSocket connected and authenticated');

            return;
          }

          if (type === 'auth_error') {
            if (this.socket) {
              this.socket.close();
              this.socket = null;
            }

            this.connectionPromise = null;
            this.connectingUrl = null;
            this.authenticated = false;
            reject(new Error(data.message || 'Authentication failed'));

            return;
          }

          if (type && this.eventListeners[type]) {
            this.eventListeners[type].forEach(callback => callback(data));
          }
        } catch (error) {
          console.error('[WebSocketService] Error parsing WebSocket message:', error);
        }
      };

      this.socket.onclose = (event) => {
        console.debug(`[WebSocketService] Connection closed, code: ${event.code}, reason: ${event.reason}`);
        this.isConnected = false;
        this.authenticated = false;
        this.socket = null;
        this.connectionPromise = null;
        this.connectingUrl = null;

        if (!this.manualDisconnect) {
          console.warn('[WebSocketService] WebSocket disconnected, attempting to reconnect...');
          this.scheduleReconnect();
        }

        reject(new Error(`WebSocket connection closed: ${event.code}`));
      };

      this.socket.onerror = (error) => {
        console.error('[WebSocketService] WebSocket error:', error);
        this.connectionPromise = null;
        this.connectingUrl = null;
        reject(error);
      };

      setTimeout(() => {
        if (this.connectionPromise && this.connectingUrl === wsUrl) {
          console.warn('[WebSocketService] Connection timeout reached');

          if (this.socket && this.socket.readyState !== WebSocket.OPEN) {
            this.socket.close();
            this.socket = null;
            this.connectionPromise = null;
            this.connectingUrl = null;
            reject(new Error('Connection timeout'));
          }
        }
      }, 10000);
    });

    return this.connectionPromise;
  }

  disconnect() {
    this.manualDisconnect = true;
    console.debug('[WebSocketService] Manual disconnection');

    if (this.reconnectInterval) {
      clearInterval(this.reconnectInterval);
      this.reconnectInterval = null;
    }

    if (this.socket) {
      try {
        this.socket.close();
      } catch (e) {
        console.warn('[WebSocketService] Error when closing:', e);
      }

      this.socket = null;
    }

    this.isConnected = false;
    this.authenticated = false;
    this.connectionPromise = null;
    this.connectingUrl = null;
  }

  scheduleReconnect() {
    if (this.reconnectInterval) {
      return;
    }

    this.reconnectInterval = setInterval(() => {
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.error('[WebSocketService] Maximum reconnect attempts reached');
        clearInterval(this.reconnectInterval);
        this.reconnectInterval = null;

        return;
      }

      this.reconnectAttempts++;
      console.info(`[WebSocketService] Reconnection attempt (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      this.connect().catch(() => {});
    }, this.reconnectDelay);
  }

  async sendMessage(type, data = {}) {
    if (!this.isConnected || !this.authenticated || !this.socket || this.socket.readyState !== WebSocket.OPEN) {
      try {
        await this.connect();
      } catch (error) {
        throw new Error('Failed to establish WebSocket connection');
      }
    }

    const message = { type, data };

    try {
      this.socket.send(JSON.stringify(message));
    } catch (error) {
      console.error('[WebSocketService] Error sending:', error);

      throw error;
    }
  }

  on(eventType, callback) {
    if (!this.eventListeners[eventType]) {
      this.eventListeners[eventType] = [];
    }

    if (!this.eventListeners[eventType].includes(callback)) {
      this.eventListeners[eventType].push(callback);
    }

    return () => this.off(eventType, callback);
  }

  off(eventType, callback) {
    if (!this.eventListeners[eventType]) {
      return;
    }

    this.eventListeners[eventType] = this.eventListeners[eventType].filter(
      cb => cb !== callback
    );
  }
}

export const websocketService = new WebSocketService(); 
