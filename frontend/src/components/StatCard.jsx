import React from 'react';

export default function StatCard({ title, value, subtext, icon: Icon, accentColor = 'var(--accent-primary)' }) {
  return (
    <div className="neu-card-sm" style={{
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      flex: 1,
      minWidth: '160px'
    }}>
      {Icon && (
        <div style={{
          padding: '12px',
          borderRadius: '12px',
          backgroundColor: 'var(--accent-light)',
          color: accentColor,
          display: 'flex'
        }}>
          <Icon size={22} />
        </div>
      )}
      <div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: '500', display: 'block' }}>
          {title}
        </span>
        <span style={{ fontSize: '1.4rem', fontWeight: '700', color: 'var(--text-primary)', lineHeight: 1.2 }}>
          {value}
        </span>
        {subtext && (
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginTop: '2px' }}>
            {subtext}
          </span>
        )}
      </div>
    </div>
  );
}
