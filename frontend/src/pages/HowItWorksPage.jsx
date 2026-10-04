import React from 'react';
import { ArrowDown, CheckCircle2, Cpu, FileText, Layers, RefreshCw, Sparkles, Sliders } from 'lucide-react';

export default function HowItWorksPage() {
  const steps = [
    {
      num: "01",
      title: "ಕನ್ನಡ ಪಠ್ಯ ತಪಾಸಣೆ (Language Validation)",
      icon: CheckCircle2,
      desc: "Unicode ಶ್ರೇಣಿ (U+0C80 ರಿಂದ U+0CFF) ಪರಿಶೀಲಿಸಿ ಕನ್ನಡ ಪಠ್ಯದ ಪ್ರಮಾಣ 40% ಗಿಂತ ಹೆಚ್ಚಿದೆಯೇ ಎಂದು ದೃಢೀಕರಿಸುತ್ತದೆ."
    },
    {
      num: "02",
      title: "ಪೂರ್ವಸಂಸ್ಕರಣೆ (NLP Preprocessing)",
      icon: FileText,
      desc: "ಅನಗತ್ಯ ಸಂಕೇತಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, ಪೂರ್ಣವಿರಾಮ ಹಾಗೂ ವಾಕ್ಯ ಗಡಿಗಳನ್ನು ಕಾಯ್ದುಕೊಳ್ಳುತ್ತದೆ."
    },
    {
      num: "03",
      title: "ವಾಕ್ಯ ವಿಭಜನೆ (Sentence Segmentation)",
      icon: Layers,
      desc: "ಕನ್ನಡ ವಾಕ್ಯ ಗಡಿಗಳಾದ (.), (!), (?), (।), (॥) ಮತ್ತು ಹೊಸ ಸಾಲುಗಳ ಆಧಾರದಲ್ಲಿ ಪ್ರತ್ಯೇಕ ವಾಕ್ಯಗಳಾಗಿ ವಿಭಜಿಸುತ್ತದೆ."
    },
    {
      num: "04",
      title: "ಶ್ರೇಣೀಕೃತ ವಿಭಜನೆ (Hierarchical Chunking)",
      icon: Sliders,
      desc: "ದೀರ್ಘ ಲೇಖನಗಳನ್ನು ಟ್ರಾನ್ಸ್‌ಫಾರ್ಮರ್ ಮಾದರಿಯ ಗರಿಷ್ಠ ಟೋಕನ್ ಪರಿಮಿತಿಗೆ ಅನುಗುಣವಾಗಿ ಸಣ್ಣ ತಂಡಗಳಾಗಿ ವಿಂಗಡಿಸುತ್ತದೆ."
    },
    {
      num: "05",
      title: "ಮಾತೃಕೆ ಸಾರಾಂಶೀಕರಣ (Seq2Seq Summarization)",
      icon: Cpu,
      desc: "AI4Bharat MultiIndicSentenceSummarizationSS / IndicBART ಮಾದರಿಯ ಮೂಲಕ ಅರ್ಥಪೂರ್ಣ ಸಾರಾಂಶ ರೂಪಿಸುತ್ತದೆ."
    },
    {
      num: "06",
      title: "ಮುಖ್ಯ ಪದ ಮತ್ತು ವಾಕ್ಯಗಳ ಶ್ರೇಣಿ (Keyword & Sentence Ranking)",
      icon: Sparkles,
      desc: "TF-IDF score, ಶಬ್ದ ಪುನರಾವರ್ತನೆ ಮತ್ತು ಸ್ಥಾನಿಕ ತೂಕಗಳನ್ನು ಸಂಯೋಜಿಸಿ ಪ್ರಮುಖ ಪದಗಳು ಮತ್ತು ಸಾಲುಗಳನ್ನು ಹೊರತೆಗೆಯುತ್ತದೆ."
    }
  ];

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '40px 24px' }}>
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <span className="badge" style={{ marginBottom: '12px', display: 'inline-block' }}>
          NLP Pipeline Architecture
        </span>
        <h1 style={{ fontSize: '2.2rem', fontWeight: '800', marginBottom: '16px' }}>
          KannadaSaar ಕಾರ್ಯವೈಖರಿ (How It Works)
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '640px', margin: '0 auto' }}>
          ಕನ್ನಡ ಪಠ್ಯ ನಮೂದಿನಿಂದ ಸಾರಾಂಶ ರೂಪಿಸುವವರೆಗಿನ ಹಂತ ಹಂತದ ಸ್ವಾಭಾವಿಕ ಭಾಷಾ ಸಂಸ್ಕರಣೆ (NLP) ಪೈಪ್‌ಲೈನ್.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {steps.map((step, idx) => {
          const StepIcon = step.icon;
          return (
            <React.Fragment key={idx}>
              <div className="neu-card" style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
                <div style={{
                  padding: '16px',
                  borderRadius: '16px',
                  backgroundColor: 'var(--accent-light)',
                  color: 'var(--accent-primary)',
                  fontWeight: '800',
                  fontSize: '1.4rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minWidth: '60px',
                  minHeight: '60px'
                }}>
                  {step.num}
                </div>
                <div>
                  <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <StepIcon size={20} color="var(--accent-primary)" />
                    {step.title}
                  </h3>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.94rem', lineHeight: 1.6 }}>
                    {step.desc}
                  </p>
                </div>
              </div>
              {idx < steps.length - 1 && (
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                  <ArrowDown size={24} color="var(--accent-secondary)" opacity={0.6} />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
