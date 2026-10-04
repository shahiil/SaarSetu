const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error('Health check failed');
  }
  return response.json();
}

export async function analyzeText(text) {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Analysis request failed');
  }
  return response.json();
}

export async function summarizeText(text, summaryLength = 'medium', keywordCount = 10) {
  const response = await fetch(`${API_BASE_URL}/api/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      summary_length: summaryLength,
      keyword_count: Number(keywordCount)
    })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'ಸಾರಾಂಶ ಸೃಷ್ಟಿಯಲ್ಲಿ ದೋಷ ಉಂಟಾಗಿದೆ (Summarization failed).');
  }

  return response.json();
}
