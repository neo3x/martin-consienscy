/**
 * React hook for WebSocket connection and real-time updates.
 */

import { useEffect } from 'react';
import { wsClient } from '@/services/websocket';
import { useSystemStore } from '@/store/systemStore';
import type { WSMessage } from '@/types';

export function useWebSocket() {
  const setEmotionalState = useSystemStore((state) => state.setEmotionalState);
  const setProcessing = useSystemStore((state) => state.setProcessing);
  const setConnected = useSystemStore((state) => state.setConnected);
  const addTimelineEvent = useSystemStore((state) => state.addTimelineEvent);

  useEffect(() => {
    // Connect to WebSocket
    wsClient.connect();

    // Set up message handler
    const unsubscribe = wsClient.addHandler((message: WSMessage) => {
      console.log('WS message received:', message.type);

      switch (message.type) {
        case 'connected':
          setConnected(true);
          break;

        case 'state_update':
          setEmotionalState(message.data as any);
          break;

        case 'trigger_detected':
          addTimelineEvent({
            timestamp: message.timestamp || new Date().toISOString(),
            event_type: 'trigger',
            description: `Trigger: ${message.data.trigger}`,
            data: message.data,
          });
          break;

        case 'memory_consolidated':
          addTimelineEvent({
            timestamp: message.timestamp || new Date().toISOString(),
            event_type: 'memory',
            description: `Memory consolidated: ${message.data.summary}`,
            data: message.data,
          });
          break;

        case 'response':
          setProcessing(false);
          break;

        case 'processing':
          setProcessing(true);
          break;

        case 'error':
          console.error('WebSocket error:', message.data);
          break;

        default:
          console.log('Unknown message type:', message.type);
      }
    });

    // Ping periodically to keep connection alive
    const pingInterval = setInterval(() => {
      if (wsClient.isConnected()) {
        wsClient.ping();
      }
    }, 30000); // Every 30 seconds

    // Cleanup on unmount
    return () => {
      unsubscribe();
      clearInterval(pingInterval);
      wsClient.disconnect();
      setConnected(false);
    };
  }, [setEmotionalState, setProcessing, setConnected, addTimelineEvent]);

  return {
    isConnected: wsClient.isConnected(),
  };
}
