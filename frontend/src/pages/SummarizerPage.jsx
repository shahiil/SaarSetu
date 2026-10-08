import React, { useState } from 'react';
import { summarizeText } from '../services/api';
import SampleSelector from '../components/SampleSelector';
import StatCard from '../components/StatCard';
import KeywordVisualizer from '../components/KeywordVisualizer';
import ImportantSentences from '../components/ImportantSentences';
import {
  Sparkles, Copy, Download, RefreshCw, Trash2, Clipboard,
  FileText, Clock, Percent, Hash, AlertCircle, CheckCircle2, Globe
} from 'lucide-react';

export default function SummarizerPage({ onAddHistory }) {
  const [inputText, setInputText] = useState('');
  const [summaryLength, setSummaryLength] = useState('medium');
  const [keywordCount, setKeywordCount] = useState(10);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [result, setResult] = useState(null);
  const [activeKeyword, setActiveKeyword] = useState(null);
  const [showEnglishTranslation, setShowEnglishTranslation] = useState(false);

  const handleSummarize = async () => {
    if (!inputText || !inputText.trim()) {
      setError('ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ (Please enter Kannada text).');
      return;
    }

    setError('');
    setLoading(true);
    setLoadingStage('ಕನ್ನಡ ಪಠ್ಯವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ (Analyzing text)...');

    try {
      setTimeout(() => setLoadingStage('ಸಾರಾಂಶವನ್ನು ರೂಪಿಸಲಾಗುತ್ತಿದೆ (Generating summary)...'), 1000);
      setTimeout(() => setLoadingStage('ಮುಖ್ಯ ಪದಗಳು ಮತ್ತು ಅನುವಾದ ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ (Extracting keywords)...'), 2000);

      const data = await summarizeText(inputText, summaryLength, keywordCount);
      setResult(data);
      if (onAddHistory) {
        onAddHistory(inputText, data);
      }
    } catch (err) {
      setError(err.message || 'ಸಾರಾಂಶ ಸೃಷ್ಟಿಯಲ್ಲಿ ದೋಷ ಸಂಭವಿಸಿದೆ (Summarization error).');
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  };

  const handlePaste = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      setInputText(clipboardText);
      setError('');
    } catch (e) {
      setError('ಕ್ಲಿಪ್‌ಬೋರ್ಡ್ ಪ್ರವೇಶಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ (Could not access clipboard).');
    }
  };

  const handleClear = () => {
    setInputText('');
    setResult(null);
    setError('');
    setActiveKeyword(null);
  };

  const handleCopySummary = () => {
    const textToCopy = showEnglishTranslation && result?.summary_english
      ? result.summary_english
      : result?.summary;
    if (!textToCopy) return;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadTXT = () => {
    if (!result) return;
    const content = `==================================================
KANNADASAAR SUMMARY REPORT
==================================================

ಕನ್ನಡ ಸಾರಾಂಶ (KANNADA SUMMARY):
--------------------------------------------------
${result.summary}

ENGLISH TRANSLATED SUMMARY:
--------------------------------------------------
${result.summary_english || 'N/A'}

ಮುಖ್ಯ ಪದಗಳು (KEYWORDS):
--------------------------------------------------
${result.keywords.map((k, i) => `${i + 1}. ${k.word} (${k.word_english || ''}) - ${(k.score * 100).toFixed(1)}%`).join('\n')}

ಪ್ರಮುಖ ವಾಕ್ಯಗಳು (IMPORTANT SENTENCES):
--------------------------------------------------
${result.important_sentences.map((s, i) => `${i + 1}. "${s.sentence}"\n   EN: "${s.sentence_english || ''}"`).join('\n')}

ಅಂಕಿಅಂಶಗಳು (STATISTICS):
--------------------------------------------------
- ಮೂಲ ಪದಗಳು (Original Words): ${result.statistics.original_words}
- ಸಾರಾಂಶ ಪದಗಳು (Summary Words): ${result.statistics.summary_words}
- ಕುಗ್ಗಿಸುವಿಕೆ (Compression Ratio): ${result.statistics.compression_ratio}%
- ವಾಚನ ಸಮಯ (Reading Time): ${result.statistics.reading_time_before} min → ${result.statistics.reading_time_after} min
- ಪ್ರಕ್ರಿಯೆ ಸಮಯ (Processing Time): ${result.processing_time}s
`;

    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `kannadasaar_summary_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const charCount = inputText.length;
  const wordCount = inputText.trim() ? inputText.trim().split(/\s+/).length : 0;

  return (
    <div className="page-wrap">
      <div style={{ marginBottom: '24px' }}>
        <h1 className="page-title">
          ಕನ್ನಡ ಲೇಖನ ಸಾರಾಂಶ ಮತ್ತು ಮುಖ್ಯ ಪದಗಳ ಸೃಷ್ಟಿ
          <span style={{ display: 'block', fontSize: '0.6em', color: 'var(--text-secondary)', fontWeight: 500, marginTop: '4px' }}>
            Kannada Text Summarizer
          </span>
        </h1>
        <p className="page-sub">
          ನಿಮ್ಮ ಕನ್ನಡ ಲೇಖನವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ ಹಾಗೂ ಕೆಲವೇ ಕ್ಷಣಗಳಲ್ಲಿ ಪ್ರಮುಖ ಅಂಶಗಳನ್ನು ಪಡೆಯಿರಿ (Paste Kannada text to get summaries & keywords).
        </p>
      </div>

      <SampleSelector onSelectSample={(text) => {
        setInputText(text);
        setError('');
      }} />

      <div className="summ-grid">
        {/* LEFT COLUMN: Input Card */}
        <div className="neu-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: '600' }}>ನಿಮ್ಮ ಕನ್ನಡ ಪಠ್ಯ (Original Text)</h2>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button onClick={handlePaste} className="neu-button" style={{ padding: '6px 12px', fontSize: '0.8rem' }} title="ಪೇಸ್ಟ್ ಮಾಡಿ">
                <Clipboard size={14} /> ಪೇಸ್ಟ್ (Paste)
              </button>
              <button onClick={handleClear} className="neu-button" style={{ padding: '6px 12px', fontSize: '0.8rem' }} title="ತೆರವುಗೊಳಿಸಿ">
                <Trash2 size={14} color="var(--error)" /> ತೆರವು (Clear)
              </button>
            </div>
          </div>

          <textarea
            className="neu-textarea"
            rows={14}
            aria-label="Kannada text input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="ಇಲ್ಲಿ ನಿಮ್ಮ ಕನ್ನಡ ಲೇಖನ ಅಥವಾ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ... (Paste your Kannada passage here)"
            style={{ marginBottom: '12px', resize: 'vertical' }}
          />

          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '20px' }}>
            <span>ಅಕ್ಷರಗಳು (Characters): {charCount}</span>
            <span>ಪದಗಳು (Words): {wordCount}</span>
          </div>

          {/* Settings Section */}
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '16px', marginBottom: '20px' }}>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
              <div style={{ flex: 1, minWidth: '130px' }}>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '600', marginBottom: '8px' }}>
                  ಸಾರಾಂಶದ ಉದ್ದ (Summary Length):
                </label>
                <div className="seg" role="group" aria-label="Summary length">
                  {[['short', 'ಸಣ್ಣ', 'Short'], ['medium', 'ಮಧ್ಯಮ', 'Medium'], ['detailed', 'ಉದ್ದ', 'Detailed']].map(([len, kn, en]) => (
                    <button
                      key={len}
                      onClick={() => setSummaryLength(len)}
                      aria-pressed={summaryLength === len}
                      className={`neu-button ${summaryLength === len ? 'active' : ''}`}
                    >
                      <span>{kn}</span>
                      <small>{en}</small>
                    </button>
                  ))}
                </div>
              </div>

              <div style={{ width: '170px', flexShrink: 0 }}>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '600', marginBottom: '8px' }}>
                  ಮುಖ್ಯ ಪದಗಳು (Keywords):
                </label>
                <select
                  value={keywordCount}
                  onChange={(e) => setKeywordCount(Number(e.target.value))}
                  className="neu-input"
                  style={{ padding: '6px 10px', fontSize: '0.82rem' }}
                >
                  <option value={5}>5 ಪದಗಳು (5 Words)</option>
                  <option value={10}>10 ಪದಗಳು (10 Words)</option>
                  <option value={15}>15 ಪದಗಳು (15 Words)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Action Submit Button */}
          <button
            onClick={handleSummarize}
            disabled={loading}
            className="neu-button neu-button-primary"
            style={{ width: '100%', padding: '14px', fontSize: '1rem' }}
            aria-busy={loading}
          >
            {loading ? (
              <>
                <RefreshCw size={18} className="spin" />
                <span>{loadingStage}</span>
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <span>ಸಾರಾಂಶಿಸಿ (Summarize Text)</span>
              </>
            )}
          </button>

          {error && (
            <div role="alert" style={{
              marginTop: '16px',
              padding: '12px',
              borderRadius: '10px',
              backgroundColor: 'rgba(217, 92, 92, 0.1)',
              border: '1px solid var(--error)',
              color: 'var(--error)',
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Results Card */}
        <div className={result && !loading ? "" : "sticky-col"}>
          {loading ? (
            <div className="neu-card" aria-live="polite">
              <h2 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '18px' }}>
                <RefreshCw size={18} className="spin" color="var(--accent-primary)" /> {loadingStage}
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {[100, 94, 98, 70, 85].map((w, i) => (
                  <div key={i} className="skeleton" style={{ width: `${w}%` }} />
                ))}
              </div>
            </div>
          ) : result ? (
            <div className="result-stack fade-up">
              {/* Summary Card */}
              <div className="neu-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
                  <h2 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Sparkles size={18} color="var(--accent-primary)" /> ಸಾರಾಂಶ (Generated Summary)
                  </h2>

                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                    {/* ENGLISH TRANSLATION TOGGLE BUTTON */}
                    <button
                      onClick={() => setShowEnglishTranslation(!showEnglishTranslation)}
                      className={`neu-button ${showEnglishTranslation ? 'active' : ''}`}
                      style={{
                        padding: '6px 12px',
                        fontSize: '0.8rem',
                        borderColor: showEnglishTranslation ? 'var(--accent-primary)' : 'transparent',
                        color: showEnglishTranslation ? 'var(--accent-primary)' : 'var(--text-primary)'
                      }}
                      title="ಇಂಗ್ಲಿಷ್ ಅನುವಾದಕ್ಕೆ ಬದಲಾಯಿಸಿ (Toggle English Translation)"
                    >
                      <Globe size={14} color="var(--accent-primary)" />
                      <span>{showEnglishTranslation ? '🇬🇧 English View (Active)' : '🌐 English Translation'}</span>
                    </button>

                    <button onClick={handleCopySummary} className="neu-button" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                      {copied ? <CheckCircle2 size={14} color="var(--success)" /> : <Copy size={14} />}
                      <span>{copied ? 'ಕಾಪಿ ಮಾಡಲಾಗಿದೆ (Copied)' : 'ಕಾಪಿ (Copy)'}</span>
                    </button>

                    <button onClick={handleDownloadTXT} className="neu-button" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                      <Download size={14} /> ಡೌನ್‌ಲೋಡ್ (Download)
                    </button>
                  </div>
                </div>

                {/* Summary Text (Kannada / English depending on toggle) */}
                <div style={{
                  fontSize: '1.02rem',
                  lineHeight: '1.7',
                  color: 'var(--text-primary)',
                  backgroundColor: showEnglishTranslation ? 'var(--accent-light)' : 'var(--accent-light)',
                  padding: '18px',
                  borderRadius: '12px',
                  border: showEnglishTranslation ? '1px solid var(--accent-primary)' : '1px solid var(--border-color)',
                  marginBottom: '20px',
                  fontFamily: showEnglishTranslation ? 'Inter, sans-serif' : "'Noto Sans Kannada', Inter, sans-serif"
                }}>
                  {showEnglishTranslation && result.summary_english ? (
                    <div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--accent-primary)', fontWeight: '700', marginBottom: '6px', textTransform: 'uppercase' }}>
                        🇬🇧 English Translation:
                      </div>
                      <p>{result.summary_english}</p>
                    </div>
                  ) : (
                    <div>
                      <p>{result.summary}</p>
                    </div>
                  )}
                </div>

                {/* Statistics Row */}
                <div className="stat-row">
                  <StatCard
                    title="ಮೂಲ ಪದಗಳು (Original Words)"
                    value={result.statistics.original_words}
                    icon={FileText}
                  />
                  <StatCard
                    title="ಸಾರಾಂಶ ಪದಗಳು (Summary Words)"
                    value={result.statistics.summary_words}
                    icon={Hash}
                  />
                  <StatCard
                    title="ಕುಗ್ಗಿಸುವಿಕೆ (Compression)"
                    value={`${result.statistics.compression_ratio}%`}
                    icon={Percent}
                    accentColor="var(--success)"
                  />
                  <StatCard
                    title="ವಾಚನ ಸಮಯ (Reading Time)"
                    value={`${result.statistics.reading_time_before}m → ${result.statistics.reading_time_after}m`}
                    icon={Clock}
                  />
                </div>
              </div>

              {/* Keywords Visualizer Component */}
              <KeywordVisualizer
                keywords={result.keywords}
                onSelectKeyword={(kw) => setActiveKeyword(kw)}
                activeKeyword={activeKeyword}
                showEnglish={showEnglishTranslation}
              />

              {/* Important Sentences Component */}
              <ImportantSentences
                sentences={result.important_sentences}
                showEnglish={showEnglishTranslation}
              />
            </div>
          ) : (
            <div className="neu-card" style={{ textAlign: 'center', padding: '64px 24px', color: 'var(--text-secondary)' }}>
              <div style={{ display: 'inline-flex', padding: '18px', borderRadius: '50%', background: 'var(--accent-light)', marginBottom: '18px' }}>
                <FileText size={40} color="var(--accent-primary)" />
              </div>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '8px', color: 'var(--text-primary)' }}>
                ಯಾವುದೇ ಸಾರಾಂಶ ಲಭ್ಯವಿಲ್ಲ (No Summary Generated Yet)
              </h3>
              <p style={{ fontSize: '0.9rem', maxWidth: '380px', margin: '0 auto' }}>
                ಎಡಭಾಗದಲ್ಲಿ ನಿಮ್ಮ ಕನ್ನಡ ಲೇಖನವನ್ನು ನಮೂದಿಸಿ ಮತ್ತು "ಸಾರಾಂಶಿಸಿ" ಬಟನ್ ಒತ್ತಿ. (Paste Kannada text on the left and click Summarize).
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
