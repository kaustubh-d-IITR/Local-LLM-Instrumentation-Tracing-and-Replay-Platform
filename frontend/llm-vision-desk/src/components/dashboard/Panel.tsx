import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface PanelProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
  contentClassName?: string;
}

export function Panel({ title, subtitle, actions, children, className, contentClassName }: PanelProps) {
  return (
    <section className={cn("panel flex flex-col", className)}>
      <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
        <div className="min-w-0">
          <h2 className="truncate text-sm font-semibold tracking-tight text-foreground">{title}</h2>
          {subtitle && <p className="truncate text-xs text-muted-foreground">{subtitle}</p>}
        </div>
        {actions && <div className="shrink-0">{actions}</div>}
      </header>
      <div className={cn("flex-1 p-4", contentClassName)}>{children}</div>
    </section>
  );
}
