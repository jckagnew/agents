'use client';

import React from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface DataPoint {
  [key: string]: string | number;
}

interface TrendChartProps {
  data: DataPoint[];
  xKey: string;
  yKey: string;
  type?: 'line' | 'area';
  showGrid?: boolean;
  showLegend?: boolean;
  className?: string;
}

export function TrendChart({
  data,
  xKey,
  yKey,
  type = 'line',
  showGrid = true,
  showLegend = false,
  className = '',
}: TrendChartProps) {
  // Loading state
  if (!data || data.length === 0) {
    return (
      <div className={`flex items-center justify-center p-12 bg-gray-50 rounded-lg ${className}`}>
        <div className="text-center">
          <div className="text-gray-400 mb-2">No data available</div>
          <div className="text-sm text-gray-500">Start logging entries to see your progress</div>
        </div>
      </div>
    );
  }

  const Chart = type === 'line' ? LineChart : AreaChart;
  const DataSeries = type === 'line' ? Line : Area;

  return (
    <div className={`w-full ${className}`}>
      {/* Chart visualization */}
      <ResponsiveContainer width="100%" height={300}>
        <Chart data={data}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />}
          <XAxis 
            dataKey={xKey} 
            stroke="#6B7280"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              // Format dates or keep as-is
              if (typeof value === 'string' && value.includes('-')) {
                return new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
              }
              return value;
            }}
          />
          <YAxis 
            stroke="#6B7280"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `${value} lbs`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
          />
          {showLegend && <Legend />}
          <DataSeries
            type="monotone"
            dataKey={yKey}
            stroke="#2563EB"
            fill={type === 'area' ? 'url(#colorGradient)' : undefined}
            strokeWidth={2}
            dot={{ fill: '#2563EB', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </Chart>
      </ResponsiveContainer>

      {/* Gradient definition for area charts */}
      {type === 'area' && (
        <defs>
          <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#2563EB" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#2563EB" stopOpacity={0} />
          </linearGradient>
        </defs>
      )}

      {/* Tabular fallback for screen readers */}
      <details className="mt-4">
        <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-900">
          View data as table
        </summary>
        <div className="mt-2 overflow-x-auto">
          <table className="min-w-full text-sm border border-gray-200 rounded-lg">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-200">
                  {xKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-200">
                  {yKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </th>
              </tr>
            </thead>
            <tbody>
              {data.map((point, index) => (
                <tr key={index} className="border-b border-gray-100">
                  <td className="px-4 py-2 text-gray-700">{point[xKey]}</td>
                  <td className="px-4 py-2 text-gray-900 font-medium">{point[yKey]} lbs</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  );
}
