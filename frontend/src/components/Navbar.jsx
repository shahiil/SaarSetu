import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, History, Sun, Moon } from 'lucide-react';

export default function Navbar({ theme, toggleTheme, onOpenHistory }) {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backdropFilter: 'blur(12px)',
      backgroundColor: 'var(--bg-color)',
      borderBottom: '1px solid var(--border-color)',
      padding: '12px 24px'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Brand Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
          <div className="neu-card-sm" style={{ padding: '8px', borderRadius: '12px', display: 'flex' }}>
            <Sparkles size={22} color="var(--accent-primary)" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.3rem', fontWeight: '700', color: 'var(--text-primary)', lineHeight: 1.1 }}>
              KannadaSaar
            </h1>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: '500' }}>
              ಕನ್ನಡ ಪಠ್ಯ ಸಂಕ್ಷಿಪ್ತಗೊಳಿಸುವಿಕೆ (Kannada Summarizer)
            </span>
          </div>
        </Link>

        {/* Nav Links */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Link to="/" className={`neu-button ${isActive('/') ? 'active' : ''}`} style={{ fontSize: '0.88rem', padding: '8px 14px' }}>
            ಮುಖಪುಟ (Home)
          </Link>
          <Link to="/summarize" className={`neu-button ${isActive('/summarize') ? 'active' : ''}`} style={{ fontSize: '0.88rem', padding: '8px 14px' }}>
            ಸಾರಾಂಶ (Summarize)
          </Link>
          <Link to="/how-it-works" className={`neu-button ${isActive('/how-it-works') ? 'active' : ''}`} style={{ fontSize: '0.88rem', padding: '8px 14px' }}>
            ಕಾರ್ಯವೈಖರಿ (How It Works)
          </Link>
          <Link to="/about" className={`neu-button ${isActive('/about') ? 'active' : ''}`} style={{ fontSize: '0.88rem', padding: '8px 14px' }}>
            ಯೋಜನೆ ಬಗ್ಗೆ (About)
          </Link>
        </nav>

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button onClick={onOpenHistory} className="neu-button" title="ಇತಿಹಾಸ (History)" style={{ padding: '8px 12px' }}>
            <History size={18} />
          </button>
          <button onClick={toggleTheme} className="neu-button" title="ಥೀಮ್ ಬದಲಾಯಿಸಿ (Toggle Theme)" style={{ padding: '8px 12px' }}>
            {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
