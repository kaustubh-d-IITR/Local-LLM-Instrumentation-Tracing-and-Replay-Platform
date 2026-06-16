import { Panel } from "./Panel";
import { useAnomalies } from "@/lib/queries";
import { AlertTriangle, Info, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

const ICON: Record<string, React.ElementType> = { info: Info, warn: AlertTriangle, error: XCircle };

export function AnomalyLedger({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useAnomalies(sessionId);

  return (
    <Panel title="Anomaly Ledger" subtitle={data ? `${data.length} events` : "Waiting for events"} className="h-full" contentClassName="p-0">
      <ul className="max-h-72 divide-y divide-border overflow-auto">
        {isLoading && <li className="p-4 text-center text-sm text-muted-foreground">Loading anomalies...</li>}
        {isError && <li className="p-4 text-center text-sm text-destructive">Error loading anomalies.</li>}
        {!isLoading && !isError && (!data || data.length === 0) && (
          <li className="p-4 text-center text-sm text-muted-foreground">No anomalies detected.</li>
        )}
        {!isLoading && !isError && data?.map((a) => {
          const Icon = ICON[a.severity] || Info;
          return (
            <li key={a.id} className="flex items-start gap-3 px-4 py-3">
              <Icon
                className={cn(
                  "mt-0.5 h-4 w-4 shrink-0",
                  a.severity === "info" && "text-[color:var(--color-info)]",
                  a.severity === "warn" && "text-[color:var(--color-warning)]",
                  a.severity === "error" && "text-destructive",
                )}
              />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm text-foreground">{a.message}</p>
                <p className="mt-0.5 font-mono text-[10px] text-muted-foreground">
                  layer {a.layer} · {new Date(a.t).toLocaleTimeString()}
                </p>
              </div>
            </li>
          );
        })}
      </ul>
    </Panel>
  );
}
