import React, { useState } from 'react';
import { Tag, BarChart2 } from 'lucide-react';

export default function KeywordVisualizer({ keywords = [], onSelectKeyword, activeKeyword, showEnglish = false }) {
  const [showBars, setShowBars] = useState(true);

  if (!keywords || keywords.length === 0) return null;

  return (
    <div className="neu-card" >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Tag size={18} color="var(--accent-primary)" /> ಮುಖ್ಯ ಪದಗಳು (Keywords)
        </h3>
        <button
          onClick={() => setShowBars(!showBars)}
          className="neu-button"
          style={{ padding: '4px 10px', fontSize: '0.8rem' }}
        >
          <BarChart2 size={14} /> {showBars ? 'ಚಿಪ್ ವೀಕ್ಷಣೆ (Chip View)' : 'ಸ್ಕೋರ್ ಬಾರ್ (Score Bar)'}
        </button>
      </div>

      {showBars ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {keywords.map((kw, idx) => {
            const isSelected = activeKeyword === kw.word;
            const displayWord = showEnglish && kw.word_english
              ? `${kw.word} (${kw.word_english})`
              : kw.word;

            return (
              <div
                key={idx}
                onClick={() => onSelectKeyword && onSelectKeyword(kw.word)}
                style={{
                  cursor: 'pointer',
                  padding: '8px 12px',
                  borderRadius: '10px',
                  backgroundColor: isSelected ? 'var(--accent-light)' : 'transparent',
                  border: isSelected ? '1px solid var(--accent-primary)' : '1px solid transparent'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: '600', color: isSelected ? 'var(--accent-primary)' : 'var(--text-primary)' }}>
                    {displayWord}
                  </span>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                    {(kw.score * 100).toFixed(1)}%
                  </span>
                </div>
                <div style={{
                  height: '6px',
                  width: '100%',
                  backgroundColor: 'var(--border-color)',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    height: '100%',
                    width: `${Math.max(12, Math.min(100, kw.score * 100))}%`,
                    backgroundColor: isSelected ? 'var(--accent-primary)' : 'var(--accent-secondary)',
                    borderRadius: '4px',
                    transition: 'width 0.4s ease'
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {keywords.map((kw, idx) => {
            const isSelected = activeKeyword === kw.word;
            const displayWord = showEnglish && kw.word_english
              ? `${kw.word} (${kw.word_english})`
              : kw.word;

            return (
              <button
                key={idx}
                onClick={() => onSelectKeyword && onSelectKeyword(kw.word)}
                className={`neu-button ${isSelected ? 'active' : ''}`}
                style={{
                  padding: '6px 14px',
                  fontSize: '0.88rem',
                  borderRadius: '20px',
                  borderColor: isSelected ? 'var(--accent-primary)' : 'transparent'
                }}
              >
                <span>{displayWord}</span>
                <span style={{ fontSize: '0.72rem', opacity: 0.7, marginLeft: '4px' }}>
                  {(kw.score * 100).toFixed(0)}%
                </span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
