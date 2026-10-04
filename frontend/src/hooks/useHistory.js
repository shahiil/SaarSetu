import { useState, useEffect } from 'react';

const STORAGE_KEY = 'kannadasaar_history';
const MAX_HISTORY = 10;

export function useHistory() {
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch (e) {
      console.error('Failed to save history to localStorage', e);
    }
  }, [history]);

  const addHistoryItem = (originalText, resultData) => {
    const preview = originalText.slice(0, 70) + (originalText.length > 70 ? '...' : '');
    const newItem = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleString('kn-IN'),
      preview,
      originalText,
      result: resultData
    };

    setHistory(prev => [newItem, ...prev.slice(0, MAX_HISTORY - 1)]);
  };

  const removeHistoryItem = (id) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return { history, addHistoryItem, removeHistoryItem, clearHistory };
}
