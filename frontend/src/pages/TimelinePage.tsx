import { useSystemStore } from '@/store/systemStore';
import { format } from 'date-fns';

export function TimelinePage() {
  const timeline = useSystemStore((state) => state.timeline);

  if (timeline.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-text-secondary">
          <p className="text-lg mb-2">No timeline events yet</p>
          <p className="text-sm">Events will appear as you interact with the system.</p>
        </div>
      </div>
    );
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'interaction_start':
      case 'interaction_complete':
        return '💬';
      case 'trigger':
        return '🎯';
      case 'memory':
        return '💾';
      case 'system_reset':
        return '🔄';
      default:
        return '●';
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-text-primary mb-6">
        System Timeline
        <span className="ml-3 text-sm font-normal text-text-secondary">
          ({timeline.length} events)
        </span>
      </h2>

      <div className="space-y-3">
        {timeline.slice().reverse().map((event, idx) => (
          <div key={idx} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="text-2xl">{getEventIcon(event.event_type)}</div>
              {idx < timeline.length - 1 && (
                <div className="flex-1 w-px bg-border my-2" />
              )}
            </div>

            <div className="flex-1 bg-surface border border-border rounded-lg p-4 mb-2">
              <div className="flex items-start justify-between mb-2">
                <span className="text-sm font-medium text-text-primary">
                  {event.description}
                </span>
                <span className="text-xs text-text-tertiary">
                  {format(new Date(event.timestamp), 'HH:mm:ss')}
                </span>
              </div>

              <div className="text-xs text-text-secondary">
                Type: {event.event_type}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
