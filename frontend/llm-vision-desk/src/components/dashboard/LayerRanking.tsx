import { useMemo, useState } from "react";
import { Panel } from "./Panel";
import { useMetrics } from "@/lib/queries";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function LayerRanking({ sessionId }: { sessionId: string }) {
  const [sort, setSort] = useState<"latency_ms" | "mem_mb">("latency_ms");
  const { data: metrics, isLoading, isError } = useMetrics(sessionId);

  const data = useMemo(() => {
    if (!metrics) return [];
    
    // Group metrics by layer to derive latency and mem_mb per layer
    const layerMap: Record<number, { latency_ms: number; mem_mb: number }> = {};
    metrics.forEach(m => {
      if (!layerMap[m.layer]) {
        layerMap[m.layer] = { latency_ms: 0, mem_mb: 0 };
      }
      layerMap[m.layer].latency_ms += m.dur_ms;
      // Synthesize 0 for memory since we don't have layer memory tracking yet
      layerMap[m.layer].mem_mb += 0;
    });

    const list = Object.entries(layerMap).map(([layer, stats]) => ({
      layer: parseInt(layer),
      latency_ms: stats.latency_ms,
      mem_mb: stats.mem_mb,
    }));

    return list.sort((a, b) => b[sort] - a[sort]).slice(0, 10);
  }, [metrics, sort]);

  const max = data.length > 0 ? Math.max(...data.map((d) => d[sort])) : 0;

  return (
    <Panel
      title="Layer Ranking"
      subtitle="Top 10 layers"
      className="h-full"
      actions={
        <Tabs value={sort} onValueChange={(v) => setSort(v as typeof sort)}>
          <TabsList className="h-7">
            <TabsTrigger value="latency_ms" className="h-5 px-2 text-[11px]">Slowest</TabsTrigger>
            <TabsTrigger value="mem_mb" className="h-5 px-2 text-[11px]">Heaviest</TabsTrigger>
          </TabsList>
        </Tabs>
      }
    >
      <div className="h-full min-h-32">
        {isLoading && <div className="flex h-full items-center justify-center text-sm text-muted-foreground">Loading layer ranking...</div>}
        {isError && <div className="flex h-full items-center justify-center text-sm text-destructive">Error loading ranking.</div>}
        {!isLoading && !isError && data.length === 0 && (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No layer data available.</div>
        )}
        {!isLoading && !isError && data.length > 0 && (
          <ul className="space-y-1.5">
            {data.map((d) => (
              <li key={d.layer} className="flex items-center gap-3">
                <span className="w-12 shrink-0 font-mono text-xs text-muted-foreground">L{d.layer}</span>
                <div className="relative h-5 flex-1 overflow-hidden rounded bg-secondary/60">
                  <div
                    className="h-full rounded bg-gradient-to-r from-primary/80 to-[color:var(--color-info)]/80"
                    style={{ width: max > 0 ? `${(d[sort] / max) * 100}%` : '0%' }}
                  />
                </div>
                <span className="w-20 shrink-0 text-right font-mono text-xs text-foreground">
                  {d[sort].toFixed(2)} {sort === "latency_ms" ? "ms" : "MB"}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </Panel>
  );
}
