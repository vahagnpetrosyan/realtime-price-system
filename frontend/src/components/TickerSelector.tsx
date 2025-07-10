import React, { useEffect, useState } from 'react';
import { Ticker } from '../types';
import { tickerApi } from '../services/api';

interface TickerSelectorProps {
  selectedTicker: string | null;
  onSelectTicker: (tickerId: string) => void;
}

export const TickerSelector: React.FC<TickerSelectorProps> = ({
  selectedTicker,
  onSelectTicker
}) => {
  const [tickers, setTickers] = useState<Ticker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTickers = async () => {
      try {
        const data = await tickerApi.getAllTickers();
        setTickers(data);

        // Auto-select first ticker if none selected
        if (!selectedTicker && data.length > 0) {
          onSelectTicker(data[0].id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load tickers');
      } finally {
        setLoading(false);
      }
    };

    loadTickers();
  }, [selectedTicker, onSelectTicker]);

  if (loading) return <div className="ticker-selector-loading">Loading tickers...</div>;
  if (error) return <div className="ticker-selector-error">Error: {error}</div>;
  if (tickers.length === 0) return <div className="ticker-selector-empty">No tickers available</div>;

  return (
    <div className="ticker-selector">
      <h3>Select a Ticker</h3>
      <div className="ticker-grid">
        {tickers.map(ticker => (
          <button
            key={ticker.id}
            className={`ticker-button ${selectedTicker === ticker.id ? 'active' : ''}`}
            onClick={() => onSelectTicker(ticker.id)}
          >
            <div className="ticker-name">{ticker.name}</div>
          </button>
        ))}
      </div>
    </div>
  );
};