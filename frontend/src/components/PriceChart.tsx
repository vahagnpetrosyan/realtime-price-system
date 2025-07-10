import React, { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  TooltipProps
} from 'recharts';
import { PricePoint, Ticker } from '../types';
import { formatTime, formatPrice } from '../utils/formatters';

interface PriceChartProps {
  ticker: Ticker | null;
  priceHistory: PricePoint[];
}

interface ChartDataPoint {
  time: string;
  price: number;
  timestamp: string;
}

const CustomTooltip: React.FC<TooltipProps<number, string>> = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload as ChartDataPoint;
    return (
      <div className="chart-tooltip">
        <p className="tooltip-time">{formatTime(data.timestamp, true)}</p>
        <p className="tooltip-price">${formatPrice(data.price)}</p>
      </div>
    );
  }
  return null;
};

export const PriceChart: React.FC<PriceChartProps> = ({ ticker, priceHistory }) => {
  const chartData = useMemo(() => {
    return priceHistory.map(point => ({
      time: formatTime(point.timestamp),
      price: point.value,
      timestamp: point.timestamp,
    }));
  }, [priceHistory]);

  const { minPrice, maxPrice } = useMemo(() => {
    if (priceHistory.length === 0) return { minPrice: 0, maxPrice: 100 };

    const prices = priceHistory.map(p => p.value);
    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const padding = (max - min) * 0.1 || 1;

    return {
      minPrice: Math.floor((min - padding) * 100) / 100,
      maxPrice: Math.ceil((max + padding) * 100) / 100,
    };
  }, [priceHistory]);

  if (!ticker) {
    return (
      <div className="price-chart-empty">
        <p>Select a ticker to view price chart</p>
      </div>
    );
  }

  return (
    <div className="price-chart">
      <div className="chart-header">
        <h2>{ticker.name}</h2>
        <div className="current-price">
          ${formatPrice(ticker.current_price)}
        </div>
      </div>

      {priceHistory.length === 0 ? (
        <div className="chart-loading">Waiting for price data...</div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis
              dataKey="time"
              stroke="#666"
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis
              domain={[minPrice, maxPrice]}
              stroke="#666"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#2196f3"
              strokeWidth={2}
              dot={false}
              animationDuration={300}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};