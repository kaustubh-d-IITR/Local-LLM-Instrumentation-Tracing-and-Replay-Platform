import { useState, useMemo } from "react";
import { Panel } from "./Panel";
import { useAttention, useTopology } from "@/lib/queries";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function AttentionHeatmap({ sessionId }: { sessionId: string }) {
  const [layer, setLayer] = useState(0);
  const [head, setHead] = useState(0);
  
  const { data: topology } = useTopology(sessionId);
  const { data: attentions, isLoading, isError } = useAttention(sessionId);

  const numLayers = topology?.blocks?.length || 32;
  const numHeads = 32; // Fallback since backend doesn't explicitly serve head count yet

  // Find the specific matrix for the selected layer and head
  const matrixData = useMemo(() => {
    if (!attentions) return null;
    const match = attentions.find((a) => a.layer === layer && a.head === head);
    return match?.matrix || null;
  }, [attentions, layer, head]);

  const max = matrixData ? Math.max(...matrixData.flat()) : 0;

  return (
    <Panel
      title="Attention Heatmap"
      subtitle={`Layer ${layer} · Head ${head}`}
      className="h-full"
      actions={
        <div className="flex gap-2">
          <Select value={String(layer)} onValueChange={(v) => setLayer(+v)}>
            <SelectTrigger className="h-7 w-20 text-xs"><SelectValue /></SelectTrigger>
            <SelectContent className="max-h-60">
              {Array.from({ length: numLayers }).map((_, i) => (
                <SelectItem key={i} value={String(i)}>L{i}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={String(head)} onValueChange={(v) => setHead(+v)}>
            <SelectTrigger className="h-7 w-20 text-xs"><SelectValue /></SelectTrigger>
            <SelectContent className="max-h-60">
              {Array.from({ length: numHeads }).map((_, i) => (
                <SelectItem key={i} value={String(i)}>H{i}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      }
    >
      {isLoading && <div className="p-8 text-center text-sm text-muted-foreground">Loading attention matrices...</div>}
      {isError && <div className="p-8 text-center text-sm text-destructive">Error loading attention data.</div>}
      {!isLoading && !isError && !matrixData && (
        <div className="p-8 text-center text-sm text-muted-foreground">No attention data available for L{layer} H{head}.</div>
      )}
      {!isLoading && !isError && matrixData && (
        <>
          <div className="grid gap-px" style={{ gridTemplateColumns: `repeat(${matrixData.length}, minmax(0, 1fr))` }}>
            {matrixData.map((row, i) =>
              row.map((v, j) => {
                const intensity = max > 0 ? v / max : 0;
                return (
                  <div
                    key={`${i}-${j}`}
                    title={`q${i} → k${j}: ${v.toFixed(3)}`}
                    className="aspect-square rounded-[2px]"
                    style={{
                      backgroundColor: `color-mix(in oklab, var(--color-primary) ${Math.round(intensity * 100)}%, var(--color-secondary))`,
                    }}
                  />
                );
              }),
            )}
          </div>
          <div className="mt-3 flex items-center justify-between text-[10px] text-muted-foreground">
            <span className="font-mono">queries → keys</span>
            <div className="flex items-center gap-1">
              <span>low</span>
              <div className="h-2 w-24 rounded-full" style={{ background: "linear-gradient(90deg, var(--color-secondary), var(--color-primary))" }} />
              <span>high</span>
            </div>
          </div>
        </>
      )}
    </Panel>
  );
}
