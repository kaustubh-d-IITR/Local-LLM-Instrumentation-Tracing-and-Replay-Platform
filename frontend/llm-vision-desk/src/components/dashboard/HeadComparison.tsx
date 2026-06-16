import { useState, useMemo } from "react";
import { Panel } from "./Panel";
import { useAttention, useTopology } from "@/lib/queries";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";

export function HeadComparison({ sessionId }: { sessionId: string }) {
  const [layer, setLayer] = useState(0);
  const { data: topology } = useTopology(sessionId);
  const { data: attentions, isLoading, isError } = useAttention(sessionId);

  const numLayers = topology?.blocks?.length || 32;

  // Derive head stats from attention matrices
  const stats = useMemo(() => {
    if (!attentions) return [];
    const layerAttns = attentions.filter((a) => a.layer === layer);
    
    return layerAttns.map((a) => {
      // Calculate basic entropy and max heuristics from the matrix
      const flat = a.matrix.flat();
      const maxAttn = Math.max(...flat);
      // Rough pseudo-entropy calculation for the visualization
      const entropy = flat.reduce((acc, val) => acc - (val > 0 ? val * Math.log(val) : 0), 0);
      const sparsity = flat.filter(v => v < 0.01).length / flat.length;

      return {
        head: a.head,
        entropy: entropy || 0,
        max_attn: maxAttn || 0,
        sparsity: sparsity || 0
      };
    });
  }, [attentions, layer]);

  const sampled = useMemo(() => {
    if (!stats.length) return [];
    const step = Math.max(1, Math.floor(stats.length / 8));
    return stats.filter((_, i) => i % step === 0).slice(0, 8);
  }, [stats]);

  return (
    <Panel
      title="Head Comparison"
      subtitle={`Layer ${layer}`}
      className="h-full"
      actions={
        <Select value={String(layer)} onValueChange={(v) => setLayer(+v)}>
          <SelectTrigger className="h-7 w-20 text-xs"><SelectValue /></SelectTrigger>
          <SelectContent className="max-h-60">
            {Array.from({ length: numLayers }).map((_, i) => (
              <SelectItem key={i} value={String(i)}>L{i}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      }
    >
      <div className="h-48">
        {isLoading && <div className="flex h-full items-center justify-center text-sm text-muted-foreground">Loading head stats...</div>}
        {isError && <div className="flex h-full items-center justify-center text-sm text-destructive">Error loading head stats.</div>}
        {!isLoading && !isError && sampled.length === 0 && (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">No attention data available.</div>
        )}
        {!isLoading && !isError && sampled.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={sampled.map((s) => ({ head: `H${s.head}`, entropy: s.entropy, max: s.max_attn * 3, sparsity: s.sparsity * 3 }))}>
              <PolarGrid stroke="var(--color-border)" />
              <PolarAngleAxis dataKey="head" tick={{ fill: "var(--color-muted-foreground)", fontSize: 10 }} />
              <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8, fontSize: 12 }} />
              <Radar dataKey="entropy" stroke="var(--color-primary)" fill="var(--color-primary)" fillOpacity={0.3} />
              <Radar dataKey="max" stroke="var(--color-info)" fill="var(--color-info)" fillOpacity={0.2} />
              <Radar dataKey="sparsity" stroke="var(--color-warning)" fill="var(--color-warning)" fillOpacity={0.2} />
            </RadarChart>
          </ResponsiveContainer>
        )}
      </div>
      <div className="mt-2 flex flex-wrap items-center justify-center gap-3 text-[11px] text-muted-foreground">
        <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-primary" />entropy</span>
        <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-[color:var(--color-info)]" />max attn</span>
        <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-[color:var(--color-warning)]" />sparsity</span>
      </div>
    </Panel>
  );
}
