/**
 * Main App component with routing.
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/Layout/MainLayout';
import { ChatPage } from './pages/ChatPage';
import { DashboardPage } from './pages/DashboardPage';
import { MemoryPage } from './pages/MemoryPage';
import { TimelinePage } from './pages/TimelinePage';
import { useWebSocket } from './hooks/useWebSocket';
import { useSystemState } from './hooks/useSystemState';

function App() {
  // Initialize WebSocket connection
  useWebSocket();

  // Load initial system state
  const { isLoading, error } = useSystemState();

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="text-4xl mb-4">🧠</div>
          <div className="text-text-primary">Loading system...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <div className="text-text-primary mb-2">Failed to load system</div>
          <div className="text-text-secondary text-sm">{error}</div>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-accent text-white rounded-lg"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<ChatPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="memory" element={<MemoryPage />} />
          <Route path="timeline" element={<TimelinePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
