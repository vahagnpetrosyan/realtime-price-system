import { useState, useEffect, useCallback } from 'react';
import { PricePoint, Ticker } from '../types';
import { tickerApi } from '../services/api';
import { useWebSocket } from './useWebSocket';

interface UsePriceDataReturn {
  ticker: Ticker | null;
  priceHistory: PricePoint[];
  loading: boolean;
  error: string | null;
}

export const usePriceData = (tickerId: string | null): UsePriceDataReturn => {
  const [ticker, setTicker] = useState<Ticker | null>(null);
  const [priceHistory, setPriceHistory] = useState<PricePoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { connect, disconnect, on, off } = useWebSocket();

  const handlePriceUpdate = useCallback((data: any) => {
    setPriceHistory(prev => {
      const newPoint: PricePoint = {
        value: data.price,
        timestamp: data.timestamp,
      };

      // Keep last 100 points for performance
      const updated = [...prev, newPoint];
      return updated.slice(-100);
    });

    // Update ticker current price
    setTicker(prev =>
      prev ? { ...prev, current_price: data.price, updated_at: data.timestamp } : null
    );
  }, []);

  useEffect(() => {
    if (!tickerId) {
      setTicker(null);
      setPriceHistory([]);
      return;
    }

    let mounted = true;

    const loadInitialData = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await tickerApi.getTickerHistory(tickerId, 100);
        if (mounted) {
          setTicker(data.ticker);
          setPriceHistory(data.history);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to load ticker data');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadInitialData();

    // Connect WebSocket
    connect(tickerId);
    on('price_update', handlePriceUpdate);

    return () => {
      mounted = false;
      off('price_update', handlePriceUpdate);
      disconnect();
    };
  }, [tickerId, connect, disconnect, on, off, handlePriceUpdate]);

  return { ticker, priceHistory, loading, error };
};