import React from 'react';
import { Link } from 'react-router-dom';
import { Code2, Heart, Sparkles } from 'lucide-react';

export default function Footer() {
  return (
    <footer style={{
      marginTop: 'auto',
      borderTop: '1px solid var(--border-color)',
      padding: '40px 24px 24px',
      backgroundColor: 'var(--bg-color)',
      color: 'var(--text-secondary)'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '30px',
        marginBottom: '30px'
      }}>
        <div>
          <h3 style={{ color: 'var(--text-primary)', fontSize: '1.1rem', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles size={18} color="var(--accent-primary)" /> KannadaSaar
          </h3>
          <p style={{ fontSize: '0.88rem', lineHeight: '1.5' }}>
            Kannada Text Summarization and Keyword Extraction Using Natural Language Processing & Indic Transformer Models.
          </p>
        </div>

        <div>
          <h4 style={{ color: 'var(--text-primary)', fontSize: '0.95rem', marginBottom: '12px' }}>ತ್ವರಿತ ಲಿಂಕ್‌ಗಳು (Quick Links)</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.88rem' }}>
            <li><Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>ಮುಖಪುಟ (Home)</Link></li>
            <li><Link to="/summarize" style={{ color: 'inherit', textDecoration: 'none' }}>ಸಾರಾಂಶ ಸೃಷ್ಟಿಸಿ (Summarize)</Link></li>
            <li><Link to="/how-it-works" style={{ color: 'inherit', textDecoration: 'none' }}>ಕಾರ್ಯವೈಖರಿ (How It Works)</Link></li>
            <li><Link to="/about" style={{ color: 'inherit', textDecoration: 'none' }}>ಯೋಜನೆ ವಿವರಣೆ (About)</Link></li>
          </ul>
        </div>

        <div>
          <h4 style={{ color: 'var(--text-primary)', fontSize: '0.95rem', marginBottom: '12px' }}>NLP ಮಾದರಿ & ತಂತ್ರಜ್ಞಾನ</h4>
          <p style={{ fontSize: '0.88rem', lineHeight: '1.5' }}>
            AI4Bharat MultiIndicSentenceSummarizationSS / IndicBART & TF-IDF Keyword Extraction Pipeline.
          </p>
        </div>
      </div>

      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        paddingTop: '20px',
        borderTop: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        fontSize: '0.82rem'
      }}>
        <p>Built as an academic NLP mini-project for Kannada language intelligence.</p>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span>© {new Date().getFullYear()} KannadaSaar</span>
        </div>
      </div>
    </footer>
  );
}
