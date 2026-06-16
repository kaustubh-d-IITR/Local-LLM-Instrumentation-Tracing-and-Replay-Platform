import { Panel } from "./Panel";
import { useActivations } from "@/lib/queries";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function ActivationStatistics({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useActivations(sessionId);

  return (
    <Panel title="Activation Statistics" subtitle="Per-layer aggregate" className="h-full">
      <div className="h-56">
        {isLoading && <div className="flex h-full items-center justify-center text-sm text-muted-foreground">Loading activations...</div>}
        {isError && <div className="flex h-full items-center justify-center text-sm text-destructive">Error loading activations.</div>}
        {!isLoading && !isError && (!data || data.length === 0) && (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No activation data available.</div>
        )}
        {!isLoading && !isError && data && data.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ left: -16, right: 8, top: 8, bottom: 0 }}>
              <XAxis dataKey="layer" tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="variance" fill="var(--color-primary)" radius={[2, 2, 0, 0]} />
              <Bar dataKey="sparsity" fill="var(--color-info)" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
      <div className="mt-2 flex items-center justify-center gap-4 text-[11px] text-muted-foreground">
        <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-primary" />variance</span>
        <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-[color:var(--color-info)]" />sparsity</span>
      </div>
    </Panel>
  );
}
