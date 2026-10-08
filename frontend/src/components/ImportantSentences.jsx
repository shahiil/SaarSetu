import React from 'react';
import { Bookmark } from 'lucide-react';

export default function ImportantSentences({ sentences = [], showEnglish = false }) {
  if (!sentences || sentences.length === 0) return null;

  return (
    <div className="neu-card">
      <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Bookmark size={18} color="var(--accent-primary)" /> ಪ್ರಮುಖ ವಾಕ್ಯಗಳು (Important Sentences)
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {sentences.map((item, idx) => (
          <div key={idx} className="neu-card-sm" style={{
            borderLeft: '4px solid var(--accent-primary)',
            backgroundColor: 'var(--card-bg)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span className="badge" style={{ fontSize: '0.75rem' }}>
                ವಾಕ್ಯ #{item.index + 1} (Sentence #{item.index + 1})
              </span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                ಸ್ಕೋರ್ (Score): {(item.score * 100).toFixed(1)}%
              </span>
            </div>
            <p style={{ fontSize: '0.92rem', color: 'var(--text-primary)', lineHeight: 1.5, marginBottom: item.sentence_english && showEnglish ? '6px' : '0' }}>
              "{item.sentence}"
            </p>
            {showEnglish && item.sentence_english && (
              <p style={{ fontSize: '0.86rem', color: 'var(--accent-primary)', fontStyle: 'italic', lineHeight: 1.4 }}>
                🇬🇧 English: "{item.sentence_english}"
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
