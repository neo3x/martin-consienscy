/**
 * Header component with system status.
 */

import { useSystemStore } from '@/store/systemStore';

export function Header() {
  const systemStatus = useSystemStore((state) => state.systemStatus);
  const isConnected = useSystemStore((state) => state.isConnected);

  return (
    <header className="bg-surface border-b border-border px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">
            🧠 Artificial Consciousness Architecture
          </h1>
          <p className="text-sm text-text-secondary">
            Phase {systemStatus?.phase || '0'} - Experimental Exploration of Emergent Cognition
          </p>
        </div>

        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-success' : 'bg-error'
              }`}
            />
            <span className="text-text-secondary">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {systemStatus && (
            <>
              <div className="text-text-secondary">
                Interactions:{' '}
                <span className="text-text-primary font-semibold">
                  {systemStatus.total_interactions}
                </span>
              </div>
              <div className="text-text-secondary">
                Memories:{' '}
                <span className="text-text-primary font-semibold">
                  {systemStatus.memory_stats.total_memories}
                </span>
              </div>
              <div className="text-text-secondary">
                Uptime:{' '}
                <span className="text-text-primary font-semibold">
                  {Math.floor(systemStatus.uptime_seconds / 60)}m
                </span>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
