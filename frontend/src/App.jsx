import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useTheme } from './hooks/useTheme';
import { useHistory } from './hooks/useHistory';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HistoryDrawer from './components/HistoryDrawer';
import LandingPage from './pages/LandingPage';
import SummarizerPage from './pages/SummarizerPage';
import HowItWorksPage from './pages/HowItWorksPage';
import AboutPage from './pages/AboutPage';
import { AlertTriangle, Home } from 'lucide-react';
import './styles/neumorphism.css';

function NotFoundPage() {
  return (
    <div style={{ textAlign: 'center', padding: '100px 24px', maxWidth: '500px', margin: '0 auto' }}>
      <div className="neu-card">
        <AlertTriangle size={48} color="var(--warning)" style={{ marginBottom: '16px' }} />
        <h1 style={{ fontSize: '1.8rem', fontWeight: '700', marginBottom: '8px' }}>೪೦೪ – ಪುಟ ಕಂಡುಬಂದಿಲ್ಲ</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
          ನೀವು ಹುಡುಕುತ್ತಿರುವ ಪುಟವು ಅಸ್ತಿತ್ವದಲ್ಲಿಲ್ಲ ಅಥವಾ ಸ್ಥಳಾಂತರಿಸಲಾಗಿದೆ.
        </p>
        <Link to="/" className="neu-button neu-button-primary">
          <Home size={18} /> ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ (Go Home)
        </Link>
      </div>
    </div>
  );
}

export default function App() {
  const { theme, toggleTheme } = useTheme();
  const { history, addHistoryItem, removeHistoryItem, clearHistory } = useHistory();
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  return (
    <Router>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Navbar
          theme={theme}
          toggleTheme={toggleTheme}
          onOpenHistory={() => setIsHistoryOpen(true)}
        />

        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/summarize" element={<SummarizerPage onAddHistory={addHistoryItem} />} />
            <Route path="/how-it-works" element={<HowItWorksPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>

        <Footer />

        <HistoryDrawer
          isOpen={isHistoryOpen}
          onClose={() => setIsHistoryOpen(false)}
          history={history}
          onLoadHistoryItem={(item) => {
            window.location.href = '/summarize';
          }}
          onDeleteHistoryItem={removeHistoryItem}
          onClearHistory={clearHistory}
        />
      </div>
    </Router>
  );
}
