import { Panel } from "./Panel";
import { useTopology } from "@/lib/queries";
import { cn } from "@/lib/utils";

const KIND_COLOR: Record<string, string> = {
  attn: "bg-[color:var(--color-info)]/20 text-[color:var(--color-info)] border-[color:var(--color-info)]/40",
  mlp: "bg-primary/15 text-primary border-primary/40",
  norm: "bg-muted text-muted-foreground border-border",
  embed: "bg-[color:var(--color-warning)]/15 text-[color:var(--color-warning)] border-[color:var(--color-warning)]/40",
};

export function ModelTopology({ sessionId }: { sessionId: string }) {
  const { data, isLoading, isError } = useTopology(sessionId);

  return (
    <Panel title="Model Topology" subtitle={data ? `${data.blocks?.length || 0} transformer blocks` : "Loading..."} className="h-full">
      <div className="max-h-[420px] space-y-1.5 overflow-auto pr-1">
        {isLoading && <div className="p-4 text-center text-sm text-muted-foreground">Loading topology...</div>}
        {isError && <div className="p-4 text-center text-sm text-destructive">Error loading topology</div>}
        {!isLoading && !isError && (!data?.blocks || data.blocks.length === 0) && (
          <div className="p-4 text-center text-sm text-muted-foreground">No topology data available.</div>
        )}
        {!isLoading && !isError && data?.blocks?.map((b: any, i: number) => (
          <div key={b.index || i} className="rounded-md border border-border bg-secondary/40 px-3 py-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-muted-foreground">{b.name}</span>
              <span
                className={cn(
                  "h-1.5 w-1.5 rounded-full",
                  b.status === "ok" && "bg-[color:var(--color-success)]",
                  b.status === "warn" && "bg-[color:var(--color-warning)]",
                  b.status === "error" && "bg-destructive",
                )}
              />
            </div>
            <div className="mt-1.5 flex flex-wrap gap-1">
              {b.components?.map((c: any) => (
                <span key={c.name} className={cn("rounded border px-1.5 py-0.5 font-mono text-[10px]", KIND_COLOR[c.kind] || KIND_COLOR.norm)}>
                  {c.name}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
}
