import { WebSocketMessage, ConnectionStatus } from '../types';

export class WebSocketService {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectInterval: number = 5000;
  private maxReconnectAttempts: number = 5;
  private reconnectAttempts: number = 0;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  constructor(baseUrl?: string) {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    this.url = baseUrl || `${wsProtocol}//${window.location.hostname}:8000`;
  }

  connect(tickerId: string, onStatusChange: (status: ConnectionStatus) => void): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.disconnect();
    }

    onStatusChange(ConnectionStatus.CONNECTING);

    try {
      this.ws = new WebSocket(`${this.url}/ws/${tickerId}`);

      this.ws.onopen = () => {
        console.log(`WebSocket connected to ticker ${tickerId}`);
        this.reconnectAttempts = 0;
        onStatusChange(ConnectionStatus.CONNECTED);
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        onStatusChange(ConnectionStatus.ERROR);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        onStatusChange(ConnectionStatus.DISCONNECTED);

        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          setTimeout(() => {
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            this.connect(tickerId, onStatusChange);
          }, this.reconnectInterval);
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      onStatusChange(ConnectionStatus.ERROR);
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.listeners.clear();
  }

  on(event: string, callback: (data: any) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: (data: any) => void): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback);
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    const callbacks = this.listeners.get(message.type);
    if (callbacks) {
      callbacks.forEach(callback => {
        if (message.type === 'price_update' && message.data) {
          callback(message.data);
        } else if (message.type === 'error' && message.message) {
          callback(message.message);
        }
      });
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}