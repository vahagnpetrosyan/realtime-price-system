import axios from 'axios';
import { Ticker, PriceHistory } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const tickerApi = {
  getAllTickers: async (): Promise<Ticker[]> => {
    const response = await api.get<Ticker[]>('/tickers');
    return response.data;
  },

  getTickerHistory: async (tickerId: string, limit?: number): Promise<PriceHistory> => {
    const params = limit ? { limit } : {};
    const response = await api.get<PriceHistory>(`/tickers/${tickerId}/history`, { params });
    return response.data;
  },
};