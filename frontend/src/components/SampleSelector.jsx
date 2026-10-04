import React from 'react';
import { FileText, Sparkles } from 'lucide-react';
import sampleArticles from '../../../data/sample_articles.json';

export default function SampleSelector({ onSelectSample }) {
  return (
    <div style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
        <Sparkles size={16} color="var(--accent-primary)" />
        <span style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-secondary)' }}>
          ಮಾದರಿ ಲೇಖನವನ್ನು ಆಯ್ಕೆಮಾಡಿ (Try Sample):
        </span>
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {sampleArticles.map((sample) => (
          <button
            key={sample.id}
            onClick={() => onSelectSample(sample.text)}
            className="neu-button"
            style={{ padding: '6px 12px', fontSize: '0.82rem' }}
          >
            <FileText size={14} color="var(--accent-primary)" />
            <span>{sample.category}: {sample.title.slice(0, 20)}...</span>
          </button>
        ))}
      </div>
    </div>
  );
}
