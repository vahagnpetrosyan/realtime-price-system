import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketService } from '../services/websocket';
import { ConnectionStatus } from '../types';

export const useWebSocket = () => {
  const wsRef = useRef<WebSocketService | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>(ConnectionStatus.DISCONNECTED);

  useEffect(() => {
    wsRef.current = new WebSocketService(process.env.REACT_APP_WS_URL);

    return () => {
      wsRef.current?.disconnect();
    };
  }, []);

  const connect = useCallback((tickerId: string) => {
    if (wsRef.current) {
      wsRef.current.connect(tickerId, setConnectionStatus);
    }
  }, []);

  const disconnect = useCallback(() => {
    wsRef.current?.disconnect();
    setConnectionStatus(ConnectionStatus.DISCONNECTED);
  }, []);

  const on = useCallback((event: string, callback: (data: any) => void) => {
    wsRef.current?.on(event, callback);
  }, []);

  const off = useCallback((event: string, callback: (data: any) => void) => {
    wsRef.current?.off(event, callback);
  }, []);

  return {
    connect,
    disconnect,
    on,
    off,
    connectionStatus,
    isConnected: connectionStatus === ConnectionStatus.CONNECTED,
  };
};