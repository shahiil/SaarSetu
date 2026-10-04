import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, CheckCircle2, Zap, Shield, BookOpen, BarChart3, Layers } from 'lucide-react';

export default function LandingPage() {
  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 24px' }}>
      {/* Hero Section */}
      <section style={{
        textAlign: 'center',
        padding: '60px 20px',
        marginBottom: '60px'
      }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }} className="badge">
          <Sparkles size={16} /> Indic Natural Language Processing Pipeline
        </div>
        
        <h1 style={{
          fontSize: 'clamp(2.2rem, 5vw, 3.5rem)',
          fontWeight: '800',
          lineHeight: '1.2',
          marginBottom: '20px',
          color: 'var(--text-primary)'
        }}>
          ಕನ್ನಡ ಪಠ್ಯವನ್ನು ಸರಳವಾಗಿ <span style={{ color: 'var(--accent-primary)' }}>ಸಂಕ್ಷಿಪ್ತಗೊಳಿಸಿ.</span>
        </h1>
        
        <p style={{
          fontSize: '1.15rem',
          color: 'var(--text-secondary)',
          maxWidth: '700px',
          margin: '0 auto 36px',
          lineHeight: '1.6'
        }}>
          "Turn long Kannada articles and passages into meaningful summaries, extract key domain terms, and analyze statistical insights."
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap' }}>
          <Link to="/summarize" className="neu-button neu-button-primary" style={{ padding: '14px 28px', fontSize: '1.05rem' }}>
            <span>ಸಾರಾಂಶ ಪ್ರಾರಂಭಿಸಿ (Start Summarizing)</span>
            <ArrowRight size={20} />
          </Link>
          <Link to="/how-it-works" className="neu-button" style={{ padding: '14px 28px', fontSize: '1.05rem' }}>
            <span>ಕಾರ್ಯವೈಖರಿ ನೋಡಿ (How It Works)</span>
          </Link>
        </div>
      </section>

      {/* Interactive Neumorphic Preview Card */}
      <section className="neu-card" style={{ marginBottom: '80px', padding: '36px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', alignItems: 'center' }}>
          <div>
            <span className="badge" style={{ marginBottom: '12px', display: 'inline-block' }}>ಮಾದರಿ ಫಲಿತಾಂಶ</span>
            <h2 style={{ fontSize: '1.6rem', fontWeight: '700', marginBottom: '14px' }}>
              ನೈಜ ಸಮಯದ ಕನ್ನಡ NLP ಸಾರಾಂಶ
            </h2>
            <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '20px' }}>
              ಅತಿ ಉದ್ದದ ಕನ್ನಡ ಸುದ್ದಿಗಳು, ಲೇಖನಗಳು ಮತ್ತು ಅಧ್ಯಯನ ಸಾಮಗ್ರಿಗಳನ್ನು ಪ್ರಮುಖ ಸಾಲುಗಳಿಗೆ ಕುಗ್ಗಿಸುತ್ತದೆ.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle2 size={18} color="var(--success)" /> IndicBART / MultiIndicSentenceSummarizationSS transformer model
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle2 size={18} color="var(--success)" /> TF-IDF + Position weighted keyword extraction
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle2 size={18} color="var(--success)" /> Compression ratio & reading time comparison
              </li>
            </ul>
          </div>

          <div className="neu-card-sm" style={{ backgroundColor: 'var(--card-bg)' }}>
            <div style={{ paddingBottom: '12px', borderBottom: '1px solid var(--border-color)', marginBottom: '12px', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: '600', fontSize: '0.9rem' }}>ಸಾರಾಂಶ ಫಲಿತಾಂಶ</span>
              <span style={{ fontSize: '0.78rem', color: 'var(--success)', fontWeight: '600' }}>೭೪% ಕುಗ್ಗಿಸುವಿಕೆ</span>
            </div>
            <p style={{ fontSize: '0.92rem', lineHeight: 1.6, color: 'var(--text-primary)', marginBottom: '14px' }}>
              "ಬೆಂಗಳೂರು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಪ್ರಸಿದ್ಧವಾಗಿದ್ದು, ನೂರಾರು ಐಟಿ ಸಂಸ್ಥೆಗಳು ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಪಾರ್ಕ್‌ಗಳನ್ನು ಹೊಂದಿರುವ ಪ್ರಮುಖ ನವೋದ್ಯಮ ಕೇಂದ್ರವಾಗಿದೆ."
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              <span className="badge" style={{ fontSize: '0.75rem' }}>ಬೆಂಗಳೂರು</span>
              <span className="badge" style={{ fontSize: '0.75rem' }}>ತಂತ್ರಜ್ಞಾನ</span>
              <span className="badge" style={{ fontSize: '0.75rem' }}>ನವೋದ್ಯಮ</span>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section style={{ marginBottom: '60px' }}>
        <h2 style={{ textAlign: 'center', fontSize: '1.8rem', fontWeight: '700', marginBottom: '40px' }}>
          ಪ್ರಮುಖ ವೈಶಿಷ್ಟ್ಯಗಳು (Key Features)
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '24px'
        }}>
          <div className="neu-card">
            <Zap size={28} color="var(--accent-primary)" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px' }}>ಕನ್ನಡ ವಾಕ್ಯ ವಿಭಜನೆ</h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              ಕನ್ನಡ ಪೂರ್ಣವಿರಾಮ (.), ದಂಡ (।) ಮತ್ತು ಚಿಹ್ನೆಗಳನ್ನು ಬಳಸಿಕೊಂಡು ನಿಖರ ವಾಕ್ಯ ವಿಭಜನೆ ನಡೆಸುತ್ತದೆ.
            </p>
          </div>

          <div className="neu-card">
            <BookOpen size={28} color="var(--accent-primary)" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px' }}>ಮಾದರಿ ರಹಿತ ಸಾರಾಂಶ</h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              Indic-language pretrained transformer Seq2Seq ಮಾದರಿಯ ಮೂಲಕ ಅಮೂಲ್ಯ ಅರ್ಥವನ್ನು ಕಾಯ್ದುಕೊಳ್ಳುತ್ತದೆ.
            </p>
          </div>

          <div className="neu-card">
            <Layers size={28} color="var(--accent-primary)" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px' }}>ಮುಖ್ಯ ಪದಗಳ ಗಣನೆ</h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              TF-IDF, ಶಬ್ದ ಪುನರಾವರ್ತನೆ ಮತ್ತು ಸ್ಥಾನಿಕ ತೂಕ ಆಧರಿಸಿ ಪ್ರಮುಖ ಪದಗಳನ್ನು ಹೊರತೆಗೆಯುತ್ತದೆ.
            </p>
          </div>

          <div className="neu-card">
            <BarChart3 size={28} color="var(--accent-primary)" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px' }}>ROUGE ಮೌಲ್ಯಮಾಪನ</h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              ROUGE-1, ROUGE-2, ROUGE-L ಮಾನದಂಡಗಳ ಮೂಲಕ ಶೈಕ್ಷಣಿಕ ಮೌಲ್ಯಮಾಪನ ಒದಗಿಸುತ್ತದೆ.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
