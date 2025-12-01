/**
 * Main chat interface component.
 */

import { useState, useRef, useEffect } from 'react';
import { apiClient } from '@/services/api';
import { useSystemStore } from '@/store/systemStore';
import type { ChatMessage } from '@/types';

export function ChatInterface() {
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const chatMessages = useSystemStore((state) => state.chatMessages);
  const addChatMessage = useSystemStore((state) => state.addChatMessage);
  const emotionalState = useSystemStore((state) => state.emotionalState);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isProcessing) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };

    addChatMessage(userMessage);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await apiClient.sendMessage(userMessage.content);

      const systemMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: response.response,
        timestamp: new Date().toISOString(),
        triggers: response.triggers_detected,
        memory_consolidated: response.memory_consolidated,
      };

      addChatMessage(systemMessage);
    } catch (error) {
      console.error('Failed to send message:', error);

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: 'Error: Failed to process message. Please try again.',
        timestamp: new Date().toISOString(),
      };

      addChatMessage(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {chatMessages.length === 0 && (
          <div className="text-center text-text-secondary mt-12">
            <p className="text-lg mb-2">Start a conversation</p>
            <p className="text-sm">
              Ask about emotional states, consciousness, or just chat naturally.
            </p>
          </div>
        )}

        {chatMessages.map((message) => (
          <div key={message.id} className="space-y-2">
            <div
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-3xl rounded-lg px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-accent text-white'
                    : 'bg-surface text-text-primary'
                }`}
              >
                <div className="flex items-start gap-2 mb-1">
                  <span className="font-semibold text-sm">
                    {message.role === 'user' ? 'You' : 'System'}
                  </span>
                  <span className="text-xs opacity-70">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="whitespace-pre-wrap">{message.content}</div>

                {message.triggers && message.triggers.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {message.triggers.map((trigger, idx) => (
                      <span
                        key={idx}
                        className="text-xs bg-warning bg-opacity-20 text-warning px-2 py-1 rounded"
                      >
                        🎯 {trigger.name}
                      </span>
                    ))}
                  </div>
                )}

                {message.memory_consolidated && (
                  <div className="mt-2">
                    <span className="text-xs bg-success bg-opacity-20 text-success px-2 py-1 rounded">
                      💾 Memory consolidated
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {isProcessing && (
          <div className="flex justify-start">
            <div className="bg-surface rounded-lg px-4 py-3">
              <div className="flex items-center gap-2 text-text-secondary">
                <div className="animate-pulse">●</div>
                <div className="animate-pulse animation-delay-200">●</div>
                <div className="animate-pulse animation-delay-400">●</div>
                <span className="ml-2 text-sm">Processing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Current state indicator */}
      {emotionalState && (
        <div className="border-t border-border bg-surface px-6 py-3">
          <div className="flex items-center gap-4 text-xs">
            <span className="text-text-secondary">Current State:</span>
            <div className="flex gap-3">
              <span>
                Valence:{' '}
                <span
                  className={
                    emotionalState.dimensions.valence >= 0
                      ? 'text-success'
                      : 'text-error'
                  }
                >
                  {emotionalState.dimensions.valence.toFixed(2)}
                </span>
              </span>
              <span>
                Certainty:{' '}
                <span className="text-certainty-high">
                  {emotionalState.dimensions.certainty.toFixed(2)}
                </span>
              </span>
              <span>
                Activation:{' '}
                <span className="text-activation-high">
                  {emotionalState.dimensions.activation.toFixed(2)}
                </span>
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Input form */}
      <div className="border-t border-border bg-surface p-6">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isProcessing}
            className="flex-1 bg-background border border-border rounded-lg px-4 py-3 text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="px-6 py-3 bg-accent text-white rounded-lg font-medium hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
