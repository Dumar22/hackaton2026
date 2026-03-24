import { useState } from 'react';
import { Home } from './pages/Home';
import { Results } from './pages/Results';
import './App.css';

type Page = 'home' | 'results';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-container">
          <h1>Pipeline de Automatizacion de Procesos</h1>
          <nav className="app-nav">
            <button
              className={`nav-button ${currentPage === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentPage('home')}
              type="button"
            >
              Inicio
            </button>
            <button
              className={`nav-button ${currentPage === 'results' ? 'active' : ''}`}
              onClick={() => setCurrentPage('results')}
              type="button"
            >
              Resultados
            </button>
          </nav>
        </div>
      </header>
      <main className="app-main">
        {currentPage === 'home' && <Home />}
        {currentPage === 'results' && <Results />}
      </main>
    </div>
  );
}

export default App;
