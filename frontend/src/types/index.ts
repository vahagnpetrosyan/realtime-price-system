export interface Ticker {
  id: string;
  name: string;
  current_price: number;
  initial_price: number;
  created_at: string;
  updated_at: string;
}

export interface PricePoint {
  value: number;
  timestamp: string;
}

export interface PriceHistory {
  ticker: Ticker;
  history: PricePoint[];
}

export interface WebSocketMessage {
  type: 'price_update' | 'error';
  data?: {
    ticker_id: string;
    price: number;
    timestamp: string;
  };
  message?: string;
}

export enum ConnectionStatus {
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  DISCONNECTED = 'disconnected',
  ERROR = 'error'
}