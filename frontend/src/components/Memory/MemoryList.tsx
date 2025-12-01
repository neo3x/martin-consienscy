/**
 * List of episodic memories.
 */

import { useEffect, useState } from 'react';
import { apiClient } from '@/services/api';
import type { Memory } from '@/types';
import { format } from 'date-fns';

export function MemoryList() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadMemories() {
      try {
        const data = await apiClient.getMemories(100, 0);
        setMemories(data.memories);
      } catch (error) {
        console.error('Failed to load memories:', error);
      } finally {
        setIsLoading(false);
      }
    }

    loadMemories();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-text-secondary">Loading memories...</div>
      </div>
    );
  }

  if (memories.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-text-secondary">
          <p className="text-lg mb-2">No memories yet</p>
          <p className="text-sm">
            Memories will be consolidated from significant interactions.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold text-text-primary mb-6">
        Episodic Memories
        <span className="ml-3 text-sm font-normal text-text-secondary">
          ({memories.length} total)
        </span>
      </h2>

      <div className="space-y-3">
        {memories.map((memory) => (
          <div
            key={memory.id}
            className="bg-surface border border-border rounded-lg p-4 hover:border-accent transition-colors cursor-pointer"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <h3 className="text-text-primary font-medium mb-1">
                  {memory.summary}
                </h3>
                <div className="flex items-center gap-4 text-xs text-text-tertiary">
                  <span>{format(new Date(memory.created_at), 'PPp')}</span>
                  <span>Recalled: {memory.times_recalled}x</span>
                </div>
              </div>
              <div className="flex gap-2 ml-4">
                <span
                  className={`px-2 py-1 rounded text-xs ${
                    memory.emotional_valence >= 0
                      ? 'bg-success bg-opacity-20 text-success'
                      : 'bg-error bg-opacity-20 text-error'
                  }`}
                >
                  {memory.emotional_valence >= 0 ? '😊' : '😔'}{' '}
                  {memory.emotional_valence.toFixed(2)}
                </span>
                <span className="px-2 py-1 rounded text-xs bg-accent bg-opacity-20 text-accent">
                  💪 {memory.retention_strength.toFixed(2)}
                </span>
              </div>
            </div>

            <div className="flex gap-2 text-xs mt-2">
              <span className="text-text-secondary">
                Importance: {(memory.subjective_importance * 100).toFixed(0)}%
              </span>
              <span className="text-text-tertiary">•</span>
              <span className="text-text-secondary">
                Surprise: {(memory.surprise * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
