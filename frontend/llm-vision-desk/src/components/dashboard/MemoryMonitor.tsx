import { Panel } from "./Panel";
import { useMemory } from "@/lib/queries";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function MemoryMonitor({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useMemory(sessionId);

  const latest = data && data.length > 0 ? data[data.length - 1] : { gpu: 0, cpu: 0 };

  return (
    <Panel
      title="Memory Monitor"
      subtitle={`GPU ${latest.gpu.toFixed(2)} GB · CPU ${latest.cpu.toFixed(2)} GB`}
      className="h-full"
    >
      <div className="h-48">
        {isLoading && <div className="flex h-full items-center justify-center text-sm text-muted-foreground">Loading memory profile...</div>}
        {isError && <div className="flex h-full items-center justify-center text-sm text-destructive">Error loading memory.</div>}
        {!isLoading && !isError && (!data || data.length === 0) && (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No memory data available.</div>
        )}
        {!isLoading && !isError && data && data.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ left: -16, right: 8, top: 8, bottom: 0 }}>
              <defs>
                <linearGradient id="gpuGrad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.6} />
                  <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="cpuGrad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-info)" stopOpacity={0.5} />
                  <stop offset="100%" stopColor="var(--color-info)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="t" tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8, fontSize: 12 }} />
              <Area type="monotone" dataKey="gpu" stroke="var(--color-primary)" fill="url(#gpuGrad)" strokeWidth={2} />
              <Area type="monotone" dataKey="cpu" stroke="var(--color-info)" fill="url(#cpuGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </Panel>
  );
}
