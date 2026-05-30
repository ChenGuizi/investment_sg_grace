import { clsx } from "clsx";
import type { PropsWithChildren } from "react";

export function Panel({ children, className }: PropsWithChildren<{ className?: string }>) {
  return <section className={clsx("rounded-md border border-line bg-panel/95 p-4 shadow-xl shadow-black/10", className)}>{children}</section>;
}

export function SectionTitle({ title, meta }: { title: string; meta?: string }) {
  return (
    <div className="mb-3 flex items-center justify-between gap-3">
      <h2 className="text-sm font-semibold uppercase text-text">{title}</h2>
      {meta ? <span className="text-xs text-muted">{meta}</span> : null}
    </div>
  );
}

export function Metric({ label, value, tone }: { label: string; value: string; tone?: "good" | "bad" | "warn" }) {
  const toneClass = tone === "good" ? "text-buy" : tone === "bad" ? "text-sell" : tone === "warn" ? "text-hold" : "text-text";
  return (
    <div className="min-w-0">
      <div className="truncate text-xs text-muted">{label}</div>
      <div className={`mt-1 truncate text-lg font-semibold ${toneClass}`}>{value}</div>
    </div>
  );
}

export function RecommendationBadge({ action }: { action: "BUY" | "HOLD" | "SELL" }) {
  const classes = {
    BUY: "border-buy/40 bg-buy/10 text-buy",
    HOLD: "border-hold/40 bg-hold/10 text-hold",
    SELL: "border-sell/40 bg-sell/10 text-sell"
  };
  return <span className={`rounded border px-2 py-1 text-xs font-semibold ${classes[action]}`}>{action}</span>;
}
