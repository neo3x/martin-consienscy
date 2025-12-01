/**
 * React hook for loading and managing system state.
 */

import { useEffect, useState } from 'react';
import { apiClient } from '@/services/api';
import { useSystemStore } from '@/store/systemStore';

export function useSystemState() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const setEmotionalState = useSystemStore((state) => state.setEmotionalState);
  const setSystemStatus = useSystemStore((state) => state.setSystemStatus);
  const setMemories = useSystemStore((state) => state.setMemories);

  useEffect(() => {
    async function loadInitialState() {
      try {
        setIsLoading(true);

        // Load system status (includes emotional state)
        const status = await apiClient.getSystemStatus();
        setSystemStatus(status);
        setEmotionalState(status.emotional_state);

        // Load memories
        const memoriesData = await apiClient.getMemories(100, 0);
        setMemories(memoriesData.memories);

        setError(null);
      } catch (err) {
        console.error('Failed to load system state:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    }

    loadInitialState();
  }, [setEmotionalState, setSystemStatus, setMemories]);

  return {
    isLoading,
    error,
  };
}
