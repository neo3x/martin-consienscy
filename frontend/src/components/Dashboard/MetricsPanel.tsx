/**
 * Metrics panel showing current dimensional values.
 */

import { useSystemStore } from '@/store/systemStore';

export function MetricsPanel() {
  const emotionalState = useSystemStore((state) => state.emotionalState);
  const systemStatus = useSystemStore((state) => state.systemStatus);

  if (!emotionalState) return null;

  const dimensions = [
    { name: 'Valence', value: emotionalState.dimensions.valence, range: '[-1, 1]', color: emotionalState.dimensions.valence >= 0 ? 'text-success' : 'text-error' },
    { name: 'Activation', value: emotionalState.dimensions.activation, range: '[0, 1]', color: 'text-activation-high' },
    { name: 'Certainty', value: emotionalState.dimensions.certainty, range: '[0, 1]', color: 'text-certainty-high' },
    { name: 'Aperture', value: emotionalState.dimensions.aperture, range: '[0, 1]', color: 'text-aperture-open' },
    { name: 'Connection', value: emotionalState.dimensions.connection, range: '[0, 1]', color: 'text-connection' },
  ];

  return (
    <div className="p-6 bg-surface rounded-lg">
      <h3 className="text-lg font-semibold text-text-primary mb-4">
        Current Metrics
      </h3>

      <div className="space-y-3">
        {dimensions.map((dim) => (
          <div key={dim.name} className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-text-secondary">{dim.name}</span>
                <span className="text-xs text-text-tertiary">{dim.range}</span>
              </div>
              <div className="h-2 bg-background rounded-full overflow-hidden">
                <div
                  className="h-full bg-accent transition-all duration-300"
                  style={{
                    width: `${
                      dim.name === 'Valence'
                        ? ((dim.value + 1) / 2) * 100
                        : dim.value * 100
                    }%`,
                  }}
                />
              </div>
            </div>
            <span className={`ml-4 text-lg font-bold ${dim.color}`}>
              {dim.value.toFixed(2)}
            </span>
          </div>
        ))}
      </div>

      {systemStatus && (
        <div className="mt-6 pt-4 border-t border-border space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-text-secondary">Total Memories:</span>
            <span className="text-text-primary font-semibold">
              {systemStatus.memory_stats.total_memories}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-text-secondary">Formative:</span>
            <span className="text-text-primary font-semibold">
              {systemStatus.memory_stats.formative_memories}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-text-secondary">Interactions:</span>
            <span className="text-text-primary font-semibold">
              {systemStatus.total_interactions}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
