/**
 * API client for communication with the backend.
 */

import type {
  EmotionalState,
  InteractionResponse,
  Memory,
  MemoryNetwork,
  SystemStatus,
  TimelineEvent,
} from '@/types';

const API_BASE = '/api/v1';

class APIClient {
  /**
   * Send a message and get response.
   */
  async sendMessage(message: string): Promise<InteractionResponse> {
    const response = await fetch(`${API_BASE}/interactions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get current emotional state.
   */
  async getState(): Promise<EmotionalState> {
    const response = await fetch(`${API_BASE}/state`);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Reset emotional state.
   */
  async resetState(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE}/state/reset`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get memories with pagination.
   */
  async getMemories(limit: number = 50, offset: number = 0): Promise<{
    memories: Memory[];
    total: number;
    formative_count: number;
  }> {
    const response = await fetch(
      `${API_BASE}/memories?limit=${limit}&offset=${offset}`
    );

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get specific memory by ID.
   */
  async getMemory(memoryId: string): Promise<Memory> {
    const response = await fetch(`${API_BASE}/memories/${memoryId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get memory network for visualization.
   */
  async getMemoryNetwork(similarityThreshold: number = 0.7): Promise<MemoryNetwork> {
    const response = await fetch(
      `${API_BASE}/memories/network?similarity_threshold=${similarityThreshold}`
    );

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get system status.
   */
  async getSystemStatus(): Promise<SystemStatus> {
    const response = await fetch(`${API_BASE}/system/status`);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get timeline of events.
   */
  async getTimeline(minutes: number = 60): Promise<{
    events: TimelineEvent[];
    start_time: string;
    end_time: string;
    total_events: number;
  }> {
    const response = await fetch(`${API_BASE}/system/timeline?minutes=${minutes}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new APIClient();
