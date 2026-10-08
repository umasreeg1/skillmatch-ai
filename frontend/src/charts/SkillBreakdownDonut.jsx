import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export const SkillBreakdownDonut = ({ matching = 0, missing = 0, partial = 0, additional = 0 }) => {
  const data = [
    { name: 'Matching Skills', value: matching, color: '#10b981' },
    { name: 'Partial Matches', value: partial, color: '#f59e0b' },
    { name: 'Missing Skills', value: missing, color: '#ef4444' },
    { name: 'Additional Skills', value: additional, color: '#3b82f6' }
  ].filter(item => item.value > 0);

  const total = matching + missing + partial;

  return (
    <div className="chart-wrapper" style={{ width: '100%', height: 260, position: 'relative' }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#0f1626',
              borderColor: 'rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: '#fff'
            }}
          />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
      <div className="donut-center-text" style={{
        position: 'absolute',
        top: '44%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        textAlign: 'center',
        pointerEvents: 'none'
      }}>
        <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fff' }}>{total}</div>
        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Total Skills</div>
      </div>
    </div>
  );
};
