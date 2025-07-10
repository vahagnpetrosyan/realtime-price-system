import React, { useState } from 'react';
import './App.css';
import { TickerSelector } from './components/TickerSelector';
import { PriceChart } from './components/PriceChart';
import { ConnectionStatus } from './components/ConnectionStatus';
import { usePriceData } from './hooks/usePriceData';
import { useWebSocket } from './hooks/useWebSocket';

function App() {
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null);
  const { ticker, priceHistory, loading, error } = usePriceData(selectedTicker);
  const { connectionStatus } = useWebSocket();

  return (
    <div className="App">
      <header className="app-header">
        <h1>Real-Time Price Data System</h1>
        <ConnectionStatus status={connectionStatus} />
      </header>

      <main className="app-main">
        <div className="content">
          <TickerSelector
            selectedTicker={selectedTicker}
            onSelectTicker={setSelectedTicker}
          />

          {error && (
            <div className="error-message">
              Error: {error}
            </div>
          )}

          {loading ? (
            <div className="loading">Loading price data...</div>
          ) : (
            <PriceChart ticker={ticker} priceHistory={priceHistory} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;