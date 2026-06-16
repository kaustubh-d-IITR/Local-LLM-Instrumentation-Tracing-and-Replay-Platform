import { Panel } from "./Panel";
import { useMetrics } from "@/lib/queries";
import { cn } from "@/lib/utils";

export function LiveExecutionStream({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useMetrics(sessionId);

  return (
    <Panel
      title="Live Execution Stream"
      subtitle={data ? `${data.length} events buffered` : "Waiting for stream..."}
      className="h-full"
      contentClassName="p-0"
    >
      <div className="max-h-[420px] overflow-auto font-mono text-[11px]">
        {isLoading && <div className="px-4 py-8 text-center text-muted-foreground">Loading stream...</div>}
        {isError && <div className="px-4 py-8 text-center text-destructive">Error loading execution stream.</div>}
        {!isLoading && !isError && (!data || data.length === 0) && (
          <div className="px-4 py-8 text-center text-muted-foreground">Waiting for execution events…</div>
        )}
        {!isLoading && !isError && data?.map((e) => (
          <div
            key={e.id}
            className={cn(
              "flex items-center gap-2 border-b border-border/60 px-3 py-1.5",
              e.level === "warn" && "bg-[color:var(--color-warning)]/5",
              e.level === "error" && "bg-destructive/10",
            )}
          >
            <span
              className={cn(
                "h-1.5 w-1.5 shrink-0 rounded-full",
                e.level === "info" && "bg-[color:var(--color-success)]",
                e.level === "warn" && "bg-[color:var(--color-warning)]",
                e.level === "error" && "bg-destructive",
              )}
            />
            <span className="w-12 shrink-0 text-muted-foreground">L{e.layer.toString().padStart(2, "0")}</span>
            <span className="w-20 shrink-0 truncate text-primary">{e.op}</span>
            <span className="w-14 shrink-0 text-right text-foreground">{e.dur_ms}ms</span>
            <span className="hidden flex-1 truncate text-muted-foreground sm:inline">{e.shape}</span>
            <span className="hidden w-12 shrink-0 text-muted-foreground md:inline">{e.dtype}</span>
            <span className="hidden w-14 shrink-0 text-muted-foreground md:inline">{e.device}</span>
          </div>
        ))}
      </div>
    </Panel>
  );
}
