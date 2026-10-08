import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, History, Sun, Moon } from 'lucide-react';

const LINKS = [
  { to: '/', kn: 'ಮುಖಪುಟ', en: 'Home' },
  { to: '/summarize', kn: 'ಸಾರಾಂಶ', en: 'Summarize' },
  { to: '/how-it-works', kn: 'ಕಾರ್ಯವೈಖರಿ', en: 'How It Works' },
  { to: '/about', kn: 'ಯೋಜನೆ ಬಗ್ಗೆ', en: 'About' },
];

export default function Navbar({ theme, toggleTheme, onOpenHistory }) {
  const location = useLocation();

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="brand">
          <div className="neu-card-sm" style={{ padding: '8px', borderRadius: '12px', display: 'flex' }}>
            <Sparkles size={22} color="var(--accent-primary)" />
          </div>
          <div>
            <h1>KannadaSaar</h1>
            <span className="brand-sub">ಕನ್ನಡ ಪಠ್ಯ ಸಂಕ್ಷಿಪ್ತಗೊಳಿಸುವಿಕೆ</span>
          </div>
        </Link>

        <nav className="nav-links" aria-label="Main">
          {LINKS.map(({ to, kn, en }) => (
            <Link
              key={to}
              to={to}
              className={`nav-link ${location.pathname === to ? 'active' : ''}`}
              aria-current={location.pathname === to ? 'page' : undefined}
            >
              <span>{kn}</span>
              <small>{en}</small>
            </Link>
          ))}
        </nav>

        <div className="nav-actions">
          <button onClick={onOpenHistory} className="neu-button" aria-label="History" title="ಇತಿಹಾಸ (History)" style={{ padding: '9px 12px' }}>
            <History size={18} />
          </button>
          <button onClick={toggleTheme} className="neu-button" aria-label="Toggle theme" title="ಥೀಮ್ ಬದಲಾಯಿಸಿ (Toggle Theme)" style={{ padding: '9px 12px' }}>
            {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
