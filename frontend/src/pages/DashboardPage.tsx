import { EmotionalStateChart } from '@/components/Dashboard/EmotionalStateChart';
import { MetricsPanel } from '@/components/Dashboard/MetricsPanel';

export function DashboardPage() {
  return (
    <div className="h-full p-6 space-y-6">
      <h2 className="text-2xl font-bold text-text-primary">
        Emotional State Dashboard
      </h2>

      <div className="grid grid-cols-2 gap-6 h-[calc(100%-4rem)]">
        <EmotionalStateChart />
        <MetricsPanel />
      </div>
    </div>
  );
}
