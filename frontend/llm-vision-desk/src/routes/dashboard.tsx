import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { Activity, ArrowLeft, Circle } from "lucide-react";
import { useCurrentSessionId } from "@/lib/queries";
import { ModelTopology } from "@/components/dashboard/ModelTopology";
import { LiveExecutionStream } from "@/components/dashboard/LiveExecutionStream";
import { AttentionHeatmap } from "@/components/dashboard/AttentionHeatmap";
import { RuntimeMetrics } from "@/components/dashboard/RuntimeMetrics";
import { ActivationStatistics } from "@/components/dashboard/ActivationStatistics";
import { AnomalyLedger } from "@/components/dashboard/AnomalyLedger";
import { MemoryMonitor } from "@/components/dashboard/MemoryMonitor";
import { TokenTimeline } from "@/components/dashboard/TokenTimeline";
import { LayerRanking } from "@/components/dashboard/LayerRanking";
import { HeadComparison } from "@/components/dashboard/HeadComparison";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — LLM Inspector" },
      { name: "description", content: "Real-time observability for local LLM inference." },
    ],
  }),
  component: DashboardPage,
});

function DashboardPage() {
  const navigate = useNavigate({ from: "/dashboard" });
  const sessionId = useCurrentSessionId();

  if (!sessionId) {
    // Cannot redirect easily in render without causing warnings in React Router,
    // but in this setup, a simple return or useEffect navigate works.
    return (
      <div className="grid h-screen place-items-center text-center">
        <div>
          <h2 className="text-lg font-semibold">No active session</h2>
          <p className="text-sm text-muted-foreground mb-4">Please start a tracing session first.</p>
          <Link to="/" className="text-primary hover:underline">Go back home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-20 border-b border-border bg-background/80 backdrop-blur">
        <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 px-4 py-3 sm:flex sm:flex-wrap sm:justify-between sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <Link to="/" className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-border bg-secondary text-muted-foreground transition-colors hover:text-foreground">
              <ArrowLeft className="h-4 w-4" />
            </Link>
            <div className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-primary/40 bg-primary/10">
              <Activity className="h-4 w-4 text-primary" />
            </div>
            <div className="min-w-0">
              <h1 className="truncate text-sm font-semibold sm:text-base">
                LLM <span className="text-gradient">Inspector</span>
              </h1>
              <p className="truncate font-mono text-[11px] text-muted-foreground">
                {sessionId}
              </p>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-3 text-xs">
            <span className="flex items-center gap-1.5 rounded-full border border-[color:var(--color-success)]/40 bg-[color:var(--color-success)]/10 px-2.5 py-1 text-[color:var(--color-success)]">
              <Circle className="h-2 w-2 fill-current" />
              Live Connected
            </span>
          </div>
        </div>
      </header>

      <main className="p-4 sm:p-6">
        <div className="mb-4">
          <RuntimeMetrics sessionId={sessionId} />
        </div>

        <div className="grid gap-4 lg:grid-cols-3">
          <ModelTopology sessionId={sessionId} />
          <div className="lg:col-span-2">
            <LiveExecutionStream sessionId={sessionId} />
          </div>
        </div>

        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <AttentionHeatmap sessionId={sessionId} />
          <HeadComparison sessionId={sessionId} />
        </div>

        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <MemoryMonitor sessionId={sessionId} />
          <ActivationStatistics sessionId={sessionId} />
        </div>

        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <TokenTimeline sessionId={sessionId} />
          </div>
          <AnomalyLedger sessionId={sessionId} />
        </div>

        <div className="mt-4">
          <LayerRanking sessionId={sessionId} />
        </div>

        <footer className="mt-8 text-center text-[11px] text-muted-foreground">
          LLM Inspector · Backend Source of Truth · WebSockets ready
        </footer>
      </main>
    </div>
  );
}
