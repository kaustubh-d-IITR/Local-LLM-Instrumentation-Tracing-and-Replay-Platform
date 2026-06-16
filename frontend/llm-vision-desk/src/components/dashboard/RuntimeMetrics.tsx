import { Panel } from "./Panel";
import { useMetrics } from "@/lib/queries";

export function RuntimeMetrics({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useMetrics(sessionId);

  // In Phase 1, we derive runtime metrics from the latest metric event if available
  const latestMetric = data && data.length > 0 ? data[0] : null;

  const items = [
    { label: "Latency", value: latestMetric ? `${latestMetric.dur_ms} ms` : "-", accent: "text-primary" },
    { label: "Throughput", value: latestMetric ? `- tok/s` : "-", accent: "text-[color:var(--color-info)]" },
    { label: "Shape", value: latestMetric?.shape || "-", mono: true },
    { label: "dtype", value: latestMetric?.dtype || "-", mono: true },
    { label: "Device", value: latestMetric?.device || "-", mono: true },
  ];

  return (
    <Panel title="Runtime Metrics" subtitle={isLoading ? "Loading..." : "Forward pass · current"} className="h-full">
      {isError ? (
        <div className="p-4 text-center text-sm text-destructive">Error loading runtime metrics.</div>
      ) : (
        <dl className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {items.map((it) => (
            <div key={it.label} className="rounded-md border border-border bg-secondary/40 px-3 py-2.5">
              <dt className="text-[10px] uppercase tracking-wider text-muted-foreground">{it.label}</dt>
              <dd className={`mt-1 truncate text-sm font-semibold ${it.mono ? "font-mono" : ""} ${it.accent ?? ""}`}>
                {isLoading ? "..." : it.value}
              </dd>
            </div>
          ))}
        </dl>
      )}
    </Panel>
  );
}
