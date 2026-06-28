import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useCreateSession } from "@/lib/queries";
import { cn } from "@/lib/utils";
import { Activity, Cpu, Sparkles } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "LLM Inspector — Start a session" },
      { name: "description", content: "Trace, inspect, and replay local LLM inference in real time." },
      { property: "og:title", content: "LLM Inspector" },
      { property: "og:description", content: "Production-grade observability for local LLMs." },
    ],
  }),
  component: SessionCreatePage,
});

const MODELS = [
  { id: "gpt2", name: "GPT-2", layers: 12, heads: 12, hidden: 768, params: "124M" },
  { id: "tinyllama", name: "TinyLlama", layers: 22, heads: 32, hidden: 2048, params: "1.1B" },
];

function SessionCreatePage() {
  const navigate = useNavigate();
  const [model, setModel] = useState("gpt2");
  const [prompt, setPrompt] = useState("Explain how multi-head attention works in a transformer block.");
  
  const createSessionMutation = useCreateSession();

  const submit = () => {
    if (!prompt.trim()) return;
    createSessionMutation.mutate(
      { model_name: model, prompt: prompt.trim() },
      {
        onSuccess: () => {
          navigate({ to: "/dashboard" });
        },
      }
    );
  };

  return (
    <main className="relative min-h-screen overflow-hidden">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 0%, color-mix(in oklab, var(--color-primary) 25%, transparent), transparent 50%), radial-gradient(circle at 80% 100%, color-mix(in oklab, var(--color-info) 25%, transparent), transparent 50%)",
        }}
      />
      <div className="relative mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center px-6 py-12">
        <div className="mb-10 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl border border-primary/40 bg-primary/10">
            <Activity className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              LLM <span className="text-gradient">Inspector</span>
            </h1>
            <p className="text-xs text-muted-foreground">Local LLM instrumentation · tracing · replay</p>
          </div>
        </div>

        <section className="panel p-6 sm:p-8">
          <div className="mb-6">
            <label className="mb-3 block text-xs font-medium uppercase tracking-wider text-muted-foreground">
              <Cpu className="mr-1.5 -mt-0.5 inline h-3.5 w-3.5" />
              Select model
            </label>
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
              {MODELS.map((m) => (
                <button
                  key={m.id}
                  onClick={() => setModel(m.id)}
                  className={cn(
                    "group flex flex-col items-start gap-1 rounded-lg border px-3 py-3 text-left transition-all",
                    model === m.id
                      ? "border-primary bg-primary/10 glow-primary"
                      : "border-border bg-secondary/40 hover:border-primary/40 hover:bg-secondary",
                  )}
                >
                  <span className="text-sm font-semibold text-foreground">{m.name.split(" ")[0]}</span>
                  <span className="font-mono text-[10px] text-muted-foreground">
                    {m.params} · {m.layers}L · {m.heads}H
                  </span>
                </button>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <label htmlFor="prompt" className="mb-3 block text-xs font-medium uppercase tracking-wider text-muted-foreground">
              <Sparkles className="mr-1.5 -mt-0.5 inline h-3.5 w-3.5" />
              Prompt
            </label>
            <Textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={6}
              className="resize-none border-border bg-secondary/40 font-mono text-sm focus-visible:ring-primary"
              placeholder="Enter the prompt to trace…"
            />
          </div>

          <div className="flex items-center justify-between gap-3">
            <p className="text-xs text-muted-foreground">
              Connected to backend source of truth.
            </p>
            <Button onClick={submit} disabled={createSessionMutation.isPending || !prompt.trim()} className="gap-2">
              {createSessionMutation.isPending ? "Starting…" : "Start session"}
              <span aria-hidden>→</span>
            </Button>
          </div>
        </section>
      </div>
    </main>
  );
}
