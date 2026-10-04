import React from 'react';
import { History, X, Trash2, ArrowRight } from 'lucide-react';

export default function HistoryDrawer({ isOpen, onClose, history = [], onLoadHistoryItem, onDeleteHistoryItem, onClearHistory }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.4)',
      zIndex: 200,
      display: 'flex',
      justifyContent: 'flex-end',
      backdropFilter: 'blur(4px)'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '420px',
        height: '100%',
        backgroundColor: 'var(--bg-color)',
        borderLeft: '1px solid var(--border-color)',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '-8px 0 24px rgba(0,0,0,0.15)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <History size={20} color="var(--accent-primary)" /> ಸಾರಾಂಶ ಇತಿಹಾಸ (History)
          </h2>
          <button onClick={onClose} className="neu-button" style={{ padding: '6px' }}>
            <X size={18} />
          </button>
        </div>

        {history.length === 0 ? (
          <div style={{ textAlign: 'center', margin: 'auto 0', color: 'var(--text-secondary)' }}>
            <History size={40} opacity={0.4} style={{ marginBottom: '12px' }} />
            <p>ಯಾವುದೇ ಇತಿಹಾಸ ಕಂಡುಬಂದಿಲ್ಲ.</p>
            <span style={{ fontSize: '0.8rem' }}>ನಿಮ್ಮ ಸಾರಾಂಶಗಳು ಇಲ್ಲಿ ಸಂಗ್ರಹಗೊಳ್ಳುತ್ತವೆ.</span>
          </div>
        ) : (
          <>
            <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px', paddingRight: '4px' }}>
              {history.map(item => (
                <div key={item.id} className="neu-card-sm" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    <span>{item.timestamp}</span>
                    <button
                      onClick={() => onDeleteHistoryItem(item.id)}
                      style={{ background: 'none', border: 'none', color: 'var(--error)', cursor: 'pointer' }}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', fontWeight: '500' }}>
                    {item.preview}
                  </p>
                  <button
                    onClick={() => {
                      onLoadHistoryItem(item);
                      onClose();
                    }}
                    className="neu-button"
                    style={{ padding: '4px 10px', fontSize: '0.8rem', alignSelf: 'flex-start', marginTop: '4px' }}
                  >
                    <span>ಲೋಡ್ ಮಾಡಿ</span> <ArrowRight size={14} />
                  </button>
                </div>
              ))}
            </div>

            <div style={{ paddingTop: '16px', borderTop: '1px solid var(--border-color)', marginTop: '16px' }}>
              <button onClick={onClearHistory} className="neu-button" style={{ width: '100%', color: 'var(--error)' }}>
                <Trash2 size={16} /> ಇತಿಹಾಸ ತೆರವುಗೊಳಿಸಿ (Clear History)
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
