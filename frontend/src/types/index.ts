/**
 * TypeScript types for the frontend application.
 * Mirrors backend API models.
 */

export interface EmotionalDimensions {
  valence: number; // -1 to 1
  activation: number; // 0 to 1
  certainty: number; // 0 to 1
  aperture: number; // 0 to 1
  connection: number; // 0 to 1
}

export interface EmotionalState {
  dimensions: EmotionalDimensions;
  intensity: number;
  duration: number;
  timestamp: string;
}

export interface TriggerEvent {
  name: string;
  intensity: number;
  timestamp: string;
  dimensions_affected: string[];
}

export interface InteractionResponse {
  response: string;
  state_after: EmotionalState;
  triggers_detected: TriggerEvent[];
  memory_consolidated: boolean;
  memory_id: string | null;
  processing_time_ms: number;
}

export interface Memory {
  id: string;
  type: string;
  summary: string;
  emotional_valence: number;
  subjective_importance: number;
  surprise: number;
  created_at: string;
  last_recalled: string | null;
  times_recalled: number;
  retention_strength: number;
  interpretation_evolution: any[];
}

export interface MemoryNode {
  id: string;
  summary: string;
  importance: number;
  valence: number;
  times_recalled: number;
  created_at: string;
}

export interface MemoryEdge {
  source: string;
  target: string;
  similarity: number;
}

export interface MemoryNetwork {
  nodes: MemoryNode[];
  edges: MemoryEdge[];
}

export interface MemoryStats {
  total_memories: number;
  formative_memories: number;
  average_consolidation_score: number;
  last_consolidation: string | null;
}

export interface SystemStatus {
  phase: string;
  uptime_seconds: number;
  total_interactions: number;
  emotional_state: EmotionalState;
  memory_stats: MemoryStats;
}

export interface TimelineEvent {
  timestamp: string;
  event_type: string;
  description: string;
  data: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'system';
  content: string;
  timestamp: string;
  triggers?: TriggerEvent[];
  state_changes?: Partial<EmotionalDimensions>;
  memory_consolidated?: boolean;
}

// WebSocket message types
export interface WSMessage {
  type: string;
  data: Record<string, any>;
  timestamp?: string;
}

export interface WSStateUpdate extends WSMessage {
  type: 'state_update';
  data: EmotionalState;
}

export interface WSTriggerDetected extends WSMessage {
  type: 'trigger_detected';
  data: {
    trigger: string;
    intensity: number;
  };
}

export interface WSMemoryConsolidated extends WSMessage {
  type: 'memory_consolidated';
  data: {
    memory_id: string;
    summary: string;
    score: number;
  };
}

export interface WSResponse extends WSMessage {
  type: 'response';
  data: {
    content: string;
    processing_time_ms: number;
  };
}

export interface WSProcessing extends WSMessage {
  type: 'processing';
  data: Record<string, never>;
}
