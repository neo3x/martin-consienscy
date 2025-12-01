/**
 * Emotional state visualization with Recharts.
 */

import { useSystemStore } from '@/store/systemStore';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';

export function EmotionalStateChart() {
  const emotionalState = useSystemStore((state) => state.emotionalState);

  if (!emotionalState) {
    return (
      <div className="flex items-center justify-center h-full text-text-secondary">
        Loading emotional state...
      </div>
    );
  }

  const data = [
    {
      dimension: 'Valence',
      value: (emotionalState.dimensions.valence + 1) / 2, // Normalize to 0-1
    },
    {
      dimension: 'Activation',
      value: emotionalState.dimensions.activation,
    },
    {
      dimension: 'Certainty',
      value: emotionalState.dimensions.certainty,
    },
    {
      dimension: 'Aperture',
      value: emotionalState.dimensions.aperture,
    },
    {
      dimension: 'Connection',
      value: emotionalState.dimensions.connection,
    },
  ];

  return (
    <div className="h-full p-6 bg-surface rounded-lg">
      <h3 className="text-lg font-semibold text-text-primary mb-4">
        Emotional State (Radar)
      </h3>

      <ResponsiveContainer width="100%" height="90%">
        <RadarChart data={data}>
          <PolarGrid stroke="#2a2a2a" />
          <PolarAngleAxis dataKey="dimension" stroke="#a0a0a0" />
          <PolarRadiusAxis domain={[0, 1]} stroke="#606060" />
          <Radar
            name="Current State"
            dataKey="value"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.5}
          />
        </RadarChart>
      </ResponsiveContainer>

      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div>
          <span className="text-text-secondary">Intensity:</span>{' '}
          <span className="text-text-primary font-semibold">
            {emotionalState.intensity.toFixed(2)}
          </span>
        </div>
        <div>
          <span className="text-text-secondary">Duration:</span>{' '}
          <span className="text-text-primary font-semibold">
            {emotionalState.duration} interactions
          </span>
        </div>
      </div>
    </div>
  );
}
