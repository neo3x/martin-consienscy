/**
 * Zustand store for global application state.
 */

import { create } from 'zustand';
import type {
  ChatMessage,
  EmotionalState,
  Memory,
  MemoryNetwork,
  SystemStatus,
  TimelineEvent,
  TriggerEvent,
} from '@/types';

interface SystemStore {
  // State
  emotionalState: EmotionalState | null;
  chatMessages: ChatMessage[];
  memories: Memory[];
  memoryNetwork: MemoryNetwork | null;
  systemStatus: SystemStatus | null;
  timeline: TimelineEvent[];
  isProcessing: boolean;
  isConnected: boolean;

  // Actions
  setEmotionalState: (state: EmotionalState) => void;
  addChatMessage: (message: ChatMessage) => void;
  clearChat: () => void;
  setMemories: (memories: Memory[]) => void;
  setMemoryNetwork: (network: MemoryNetwork) => void;
  setSystemStatus: (status: SystemStatus) => void;
  setTimeline: (events: TimelineEvent[]) => void;
  addTimelineEvent: (event: TimelineEvent) => void;
  setProcessing: (isProcessing: boolean) => void;
  setConnected: (isConnected: boolean) => void;
}

export const useSystemStore = create<SystemStore>((set) => ({
  // Initial state
  emotionalState: null,
  chatMessages: [],
  memories: [],
  memoryNetwork: null,
  systemStatus: null,
  timeline: [],
  isProcessing: false,
  isConnected: false,

  // Actions
  setEmotionalState: (state) => set({ emotionalState: state }),

  addChatMessage: (message) =>
    set((state) => ({
      chatMessages: [...state.chatMessages, message],
    })),

  clearChat: () => set({ chatMessages: [] }),

  setMemories: (memories) => set({ memories }),

  setMemoryNetwork: (network) => set({ memoryNetwork: network }),

  setSystemStatus: (status) => set({ systemStatus: status }),

  setTimeline: (events) => set({ timeline: events }),

  addTimelineEvent: (event) =>
    set((state) => ({
      timeline: [...state.timeline, event],
    })),

  setProcessing: (isProcessing) => set({ isProcessing }),

  setConnected: (isConnected) => set({ isConnected }),
}));
