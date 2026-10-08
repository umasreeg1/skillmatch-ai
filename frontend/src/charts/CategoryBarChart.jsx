import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export const CategoryBarChart = ({ categorySummary = [] }) => {
  const data = categorySummary.map(c => ({
    name: c.category,
    matchPercentage: c.match_percentage,
    matched: c.matched_count,
    total: c.total_required
  }));

  const getColor = (perc) => {
    if (perc >= 80) return '#10b981';
    if (perc >= 50) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div style={{ width: '100%', height: 260 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
          <XAxis
            dataKey="name"
            tick={{ fill: '#94a3b8', fontSize: 11 }}
            axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            tickLine={false}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: '#94a3b8', fontSize: 11 }}
            axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            unit="%"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0f1626',
              borderColor: 'rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: '#fff'
            }}
            formatter={(val, name, item) => [`${val}% (${item.payload.matched}/${item.payload.total} matched)`, 'Category Match']}
          />
          <Bar dataKey="matchPercentage" radius={[6, 6, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.matchPercentage)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
