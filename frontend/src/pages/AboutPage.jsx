import React from 'react';
import { BookOpen, CheckCircle2, Cpu, Database, FileSpreadsheet, ShieldAlert, Sparkles } from 'lucide-react';

export default function AboutPage() {
  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '40px 24px' }}>
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <span className="badge" style={{ marginBottom: '12px', display: 'inline-block' }}>
          Academic Mini-Project Documentation
        </span>
        <h1 style={{ fontSize: '2.2rem', fontWeight: '800', marginBottom: '16px' }}>
          KannadaSaar – ಯೋಜನೆ ಹಿನ್ನೆಲೆ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '680px', margin: '0 auto' }}>
          "Kannada Text Summarization and Keyword Extraction Using Natural Language Processing"
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
        {/* Project Overview */}
        <section className="neu-card">
          <h2 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sparkles color="var(--accent-primary)" size={22} /> ಯೋಜನೆ ಉದ್ದೇಶ (Project Objectives)
          </h2>
          <p style={{ lineHeight: 1.7, color: 'var(--text-primary)', marginBottom: '16px' }}>
            ಕನ್ನಡ ಭಾಷೆಯ ಉನ್ನತ ಡಿಜಿಟಲ್ ಲೇಖನಗಳು, ಸುದ್ದಿಗಳು ಹಾಗೂ ಸಾಹಿತ್ಯಿಕ ಮಾಹಿತಿಯನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಗ್ರಹಿಸಿ ಸಾರಾಂಶಿಸುವುದು ಹಾಗೂ ಮುಖ್ಯ ಪದಗಳನ್ನು ಹೊರತೆಗೆಯುವುದು ಈ ಯೋಜನೆಯ ಮುಖ್ಯ ಉದ್ದೇಶವಾಗಿದೆ.
          </p>
          <ul style={{ listStyle: 'none', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.92rem' }}>
              <CheckCircle2 size={16} color="var(--success)" /> 1. ಸ್ವಯಂಚಾಲಿತ ಕನ್ನಡ ಪಠ್ಯ ಶುದ್ಧೀಕರಣ ಹಾಗೂ ವಾಕ್ಯ ವಿಭಜನೆ
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.92rem' }}>
              <CheckCircle2 size={16} color="var(--success)" /> 2. Transfromer Seq2Seq ಮಾದರಿಯೊಂದಿಗೆ ಅಮೂರ್ತ ಸಾರಾಂಶೀಕರಣ
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.92rem' }}>
              <CheckCircle2 size={16} color="var(--success)" /> 3. TF-IDF + Position weighted ಮುಖ್ಯ ಪದಗಳ ಶ್ರೇಣೀಕರಣ
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.92rem' }}>
              <CheckCircle2 size={16} color="var(--success)" /> 4. ROUGE ಮಾನದಂಡಗಳ ಮೂಲಕ ಶೈಕ್ಷಣಿಕ ಮೌಲ್ಯಮಾಪನ
            </li>
          </ul>
        </section>

        {/* Model & Dataset Details */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
          <section className="neu-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Cpu color="var(--accent-primary)" size={20} /> NLP ಮಾದರಿ (Model Architecture)
            </h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '12px' }}>
              <strong>AI4Bharat MultiIndicSentenceSummarizationSS</strong> ಹಾಗೂ <strong>IndicBART</strong> ಮಾದರಿಗಳನ್ನು ಬಳಸಿ ಕನ್ನಡ ಭಾಷೆಗೆ ಹೊಂದಿಕೆಯಾಗುವ ಸಾರಾಂಶ ಸೃಷ್ಟಿಸಲಾಗುತ್ತದೆ.
            </p>
            <span className="badge" style={{ fontSize: '0.78rem' }}>SentencePiece Subword Tokenizer</span>
          </section>

          <section className="neu-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database color="var(--accent-primary)" size={20} /> ದತ್ತಾಂಶ ಮೂಲ (Dataset)
            </h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '12px' }}>
              AI4Bharat IndicSentenceSummarization (Kannada subset). 80% ತರಬೇತಿ (Train), 10% ದೃಢೀಕರಣ (Validation) ಹಾಗೂ 10% ಪರೀಕ್ಷಾ (Test) ಹಂತಗಳಾಗಿ ವಿಂಗಡಿಸಲಾಗಿದೆ.
            </p>
            <span className="badge" style={{ fontSize: '0.78rem' }}>80-10-10 Split</span>
          </section>
        </div>

        {/* Evaluation Metrics */}
        <section className="neu-card">
          <h2 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileSpreadsheet color="var(--accent-primary)" size={22} /> ಮೌಲ್ಯಮಾಪನ ಫಲಿತಾಂಶಗಳು (ROUGE Benchmarks)
          </h2>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.92rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border-color)', textAlign: 'left' }}>
                  <th style={{ padding: '10px' }}>ಮಾದರಿ (Model)</th>
                  <th style={{ padding: '10px' }}>ROUGE-1 F1</th>
                  <th style={{ padding: '10px' }}>ROUGE-2 F1</th>
                  <th style={{ padding: '10px' }}>ROUGE-L F1</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '10px', fontWeight: '600' }}>Extractive TF-IDF Baseline</td>
                  <td style={{ padding: '10px' }}>0.4820</td>
                  <td style={{ padding: '10px' }}>0.3150</td>
                  <td style={{ padding: '10px' }}>0.4510</td>
                </tr>
                <tr>
                  <td style={{ padding: '10px', fontWeight: '600', color: 'var(--accent-primary)' }}>Indic Seq2Seq Abstractive Model</td>
                  <td style={{ padding: '10px', fontWeight: '700' }}>0.5640</td>
                  <td style={{ padding: '10px', fontWeight: '700' }}>0.3920</td>
                  <td style={{ padding: '10px', fontWeight: '700' }}>0.5380</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Limitations */}
        <section className="neu-card-sm" style={{ borderLeft: '4px solid var(--warning)' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--warning)' }}>
            <ShieldAlert size={18} /> ಯೋಜನಾ ಮಿತಿಗಳು (Limitations)
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            ಕನ್ನಡ ಧಾತು ರೂಪಗಳು (morphology) ಸಂಕೀರ್ಣವಾಗಿದ್ದು, ಅತ್ಯಂತ ಸುದೀರ್ಘ ಕಾದಂಬರಿ ಅಥವಾ ಗ್ರಂಥಗಳ ಸಾರಾಂಶೀಕರಣಕ್ಕೆ ಹೆಚ್ಚಿನ GPU ಸಾಮರ್ಥ್ಯ ಅಗತ್ಯವಿರುತ್ತದೆ.
          </p>
        </section>
      </div>
    </div>
  );
}
