import { Panel } from "./Panel";
import { useTokens } from "@/lib/queries";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function TokenTimeline({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useTokens(sessionId);

  return (
    <Panel title="Token Timeline" subtitle={data ? `${data.length} tokens generated` : "Waiting for tokens"} className="h-full">
      <div className="h-40">
        {isLoading && <div className="flex h-full items-center justify-center text-sm text-muted-foreground">Loading tokens...</div>}
        {isError && <div className="flex h-full items-center justify-center text-sm text-destructive">Error loading tokens.</div>}
        {!isLoading && !isError && (!data || data.length === 0) && (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No token data available.</div>
        )}
        {!isLoading && !isError && data && data.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ left: -16, right: 8, top: 8, bottom: 0 }}>
              <XAxis dataKey="idx" tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8, fontSize: 12 }}
                formatter={(v: number, _n: any, p: any) => [`${v} ms`, `"${p.payload.token}"`]}
              />
              <Line type="monotone" dataKey="ms" stroke="var(--color-primary)" strokeWidth={2} dot={{ r: 3, fill: "var(--color-primary)" }} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1 font-mono text-xs">
          {data.map((t) => (
            <span key={t.idx} className="rounded border border-border bg-secondary/60 px-1.5 py-0.5 text-foreground" title={`${t.ms}ms`}>
              {t.token.trim() || "·"}
            </span>
          ))}
        </div>
      )}
    </Panel>
  );
}
