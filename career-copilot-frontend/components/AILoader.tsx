"use client";

import { useEffect, useState } from "react";

const defaultMessages = [
  "Reading the context you shared",
  "Finding the strongest signals",
  "Turning insights into useful next steps",
  "Polishing your personalized response",
];

export default function AILoader({
  messages = defaultMessages,
  compact = false,
}: {
  messages?: string[];
  compact?: boolean;
}) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setIndex((current) => (current + 1) % messages.length);
    }, 2200);
    return () => window.clearInterval(timer);
  }, [messages.length]);

  return (
    <div className={`flex items-center gap-4 ${compact ? "py-1" : "min-h-64 justify-center py-10 text-center"}`} role="status" aria-live="polite">
      <div className="relative h-12 w-12 shrink-0">
        <div className="absolute inset-0 animate-spin rounded-full border-[3px] border-violet-100 border-t-violet-600 border-r-blue-500" />
        <div className="absolute inset-[9px] animate-pulse rounded-full bg-gradient-to-br from-violet-500 to-blue-500 shadow-lg shadow-violet-200" />
      </div>
      <div className={compact ? "text-left" : "max-w-sm text-left"}>
        <div className="flex items-center gap-1.5 text-xs font-black uppercase tracking-[0.16em] text-violet-600">
          Career Copilot is working
          <span className="flex gap-1" aria-hidden="true"><i className="h-1 w-1 animate-bounce rounded-full bg-violet-500 [animation-delay:-.3s]" /><i className="h-1 w-1 animate-bounce rounded-full bg-blue-500 [animation-delay:-.15s]" /><i className="h-1 w-1 animate-bounce rounded-full bg-cyan-500" /></span>
        </div>
        <p key={index} className="mt-1.5 animate-[fadeIn_.35s_ease-out] text-sm font-semibold text-slate-700">
          {messages[index]}
        </p>
        {!compact && <p className="mt-1 text-xs text-slate-400">This can take a few moments.</p>}
      </div>
    </div>
  );
}
