"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type ReactNode } from "react";
import AppNavbar from "../../components/AppNavbar";
import AILoader from "../../components/AILoader";
import { apiFetch } from "../../lib/api";

type Mode = "general" | "weekly_plan" | "application_strategy" | "interview_prep" | "profile_gaps";
type Message = { role: "user" | "assistant"; content: string; interactionId?: number; feedback?: boolean };

const actions: { mode: Mode; title: string; prompt: string; description: string }[] = [
  { mode: "weekly_plan", title: "Plan my week", prompt: "Create my highest-impact career plan for the next seven days.", description: "A realistic, prioritized action plan" },
  { mode: "application_strategy", title: "Application strategy", prompt: "Review my current application strategy and tell me what to change.", description: "Use your actual pipeline and targets" },
  { mode: "interview_prep", title: "Interview preparation", prompt: "Build an interview preparation plan based on my profile and target roles.", description: "Technical and behavioral preparation" },
  { mode: "profile_gaps", title: "Analyze my gaps", prompt: "What are the most important gaps between my current profile and my target roles?", description: "Focus on the improvements that matter" },
];

export default function CoachPage() {
  const [messages, setMessages] = useState<Message[]>([{ role: "assistant", content: "Hey! What are we working on today?" }]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<Mode>("general");
  const [loading, setLoading] = useState(false);
  const [completeness, setCompleteness] = useState<number | null>(null);
  const [context, setContext] = useState<string[]>([]);
  const messageViewportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const viewport = messageViewportRef.current;
    if (!viewport) return;
    window.requestAnimationFrame(() => {
      viewport.scrollTo({ top: viewport.scrollHeight, behavior: "smooth" });
    });
  }, [messages, loading]);

  async function send(text = input, selectedMode = mode) {
    if (!text.trim() || loading) return;
    const userMessage: Message = { role: "user", content: text.trim() };
    const history = [...messages, userMessage];
    setMessages(history); setInput(""); setMode(selectedMode); setLoading(true);
    try {
      const result = await apiFetch<{ answer: string; profile_completeness: number; context_used: string[]; interaction_id: number; strategy: string }>("/coach/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage.content, mode: selectedMode, history: messages.slice(-10) }),
      });
      setMessages([...history, { role: "assistant", content: result.answer, interactionId: result.interaction_id }]);
      setCompleteness(result.profile_completeness); setContext(result.context_used);
    } catch (e: any) {
      setMessages([...history, { role: "assistant", content: `I couldn’t generate advice: ${e.message}` }]);
    } finally { setLoading(false); }
  }

  async function rateMessage(interactionId: number, helpful: boolean) {
    try {
      await apiFetch(`/coach/interactions/${interactionId}/feedback`, {
        method: "PUT",
        body: JSON.stringify({ helpful }),
      });
      setMessages((current) => current.map((message) =>
        message.interactionId === interactionId ? { ...message, feedback: helpful } : message
      ));
    } catch (e: any) {
      setMessages((current) => [...current, { role: "assistant", content: `I couldn't save that feedback: ${e.message}` }]);
    }
  }

  return <main className="app-page text-slate-950"><div className="app-container"><AppNavbar />
    <div className="mb-8"><p className="eyebrow">Personalized guidance</p><h1 className="mt-3 text-4xl font-black tracking-[-0.04em] sm:text-5xl">Meet your <span className="gradient-text">Career Coach.</span></h1><p className="mt-3 max-w-2xl text-slate-600">Turn your profile and real job-search activity into clear, practical next steps.</p></div>
    <div className="grid items-start gap-6 lg:grid-cols-[300px_minmax(0,1fr)] xl:grid-cols-[320px_minmax(0,1fr)]">
      <aside className="space-y-4 lg:sticky lg:top-28">
        <div className="surface-card rounded-3xl p-4 sm:p-5"><div className="flex items-center justify-between"><h2 className="font-black">Choose a focus</h2><span className="rounded-full bg-violet-50 px-2.5 py-1 text-[10px] font-black uppercase tracking-wider text-violet-600">AI powered</span></div><div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-1">{actions.map((action, index) => <button key={action.mode} onClick={() => send(action.prompt, action.mode)} disabled={loading} className="group flex w-full items-start gap-3 rounded-2xl border border-slate-200 p-4 text-left transition duration-200 hover:-translate-y-0.5 hover:border-violet-300 hover:bg-violet-50/70 hover:shadow-md"><span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-xs font-black text-slate-500 transition group-hover:bg-violet-600 group-hover:text-white">0{index + 1}</span><span><span className="block font-bold">{action.title}</span><span className="mt-1 block text-xs leading-5 text-slate-500">{action.description}</span></span></button>)}</div></div>
        <div className="rounded-3xl bg-gradient-to-br from-violet-600 to-blue-600 p-5 text-white"><h2 className="font-black">Coach context</h2>{completeness === null ? <p className="mt-2 text-sm text-blue-100">Start a conversation to see what the coach uses.</p> : <><p className="mt-2 text-sm text-blue-100">Profile completeness: {completeness}%</p><p className="mt-2 text-xs text-blue-100">Using: {context.join(", ")}</p></>}<Link href="/profile" className="mt-4 inline-block rounded-xl bg-white/15 px-4 py-2 text-sm font-bold">Update profile</Link></div>
      </aside>
      <section className="surface-card flex h-[72dvh] min-h-[420px] min-w-0 flex-col overflow-hidden rounded-3xl sm:min-h-[520px] lg:h-[calc(100dvh-15rem)] lg:max-h-[780px]">
        <div className="flex shrink-0 items-center justify-between border-b border-slate-100 px-6 py-4"><div><h2 className="font-black">Conversation</h2><p className="mt-0.5 text-xs capitalize text-slate-500">{mode.replaceAll("_", " ")}</p></div><span className="flex items-center gap-2 text-xs font-bold text-emerald-600"><span className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_0_4px_rgba(16,185,129,.12)]" />Ready</span></div>
        <div ref={messageViewportRef} className="chat-scroll min-h-0 flex-1 space-y-5 overflow-y-auto overscroll-contain bg-slate-50/60 p-3 sm:p-6">{messages.map((message, index) => <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}><div className={`max-w-[92%] break-words rounded-2xl px-4 py-3 text-sm leading-7 sm:max-w-[85%] sm:px-5 sm:py-4 ${message.role === "user" ? "whitespace-pre-wrap bg-gradient-to-r from-violet-600 to-blue-600 text-white" : "border border-slate-200 bg-white text-slate-700 shadow-sm"}`}>{message.role === "assistant" ? <><MarkdownMessage content={message.content} />{message.interactionId && <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-slate-100 pt-3"><span className="mr-1 text-xs font-semibold text-slate-400">Help me learn:</span><button type="button" onClick={() => rateMessage(message.interactionId!, true)} className={`rounded-full px-3 py-1 text-xs font-bold transition ${message.feedback === true ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500 hover:bg-emerald-50 hover:text-emerald-700"}`}>Helpful</button><button type="button" onClick={() => rateMessage(message.interactionId!, false)} className={`rounded-full px-3 py-1 text-xs font-bold transition ${message.feedback === false ? "bg-amber-100 text-amber-700" : "bg-slate-100 text-slate-500 hover:bg-amber-50 hover:text-amber-700"}`}>Needs work</button></div>}</> : message.content}</div></div>)}{loading && <div className="inline-block max-w-[92%] rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm"><AILoader compact messages={["Reviewing your career profile", "Connecting your goals with your search", "Prioritizing the highest-impact actions", "Writing a practical recommendation"]} /></div>}</div>
        <form onSubmit={(e) => { e.preventDefault(); send(); }} className="shrink-0 border-t border-slate-100 bg-white p-3 sm:p-4"><div className="flex flex-col gap-2 sm:flex-row sm:gap-3"><textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} placeholder="Ask about your search, preparation, targets, or next steps..." className="field-control min-h-14 flex-1 resize-none" /><button disabled={loading || !input.trim()} className="min-h-12 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-600 px-6 font-bold text-white shadow-lg shadow-blue-200 transition hover:scale-[1.02] disabled:opacity-40">Send</button></div><p className="mt-2 px-1 text-xs text-slate-400">Career Coach may make mistakes. Verify important company and hiring information.</p></form>
      </section>
    </div>
  </div></main>;
}

function MarkdownMessage({ content }: { content: string }) {
  return <div className="space-y-2.5">{content.split("\n").map((raw, index) => {
    const line = raw.trim();
    if (!line) return <div key={index} className="h-1" />;

    const heading = line.match(/^(#{1,4})\s+(.+)$/);
    if (heading) return <h3 key={index} className="pt-2 text-base font-black tracking-tight text-slate-950">{inlineMarkdown(heading[2])}</h3>;

    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) return <div key={index} className="flex gap-2.5 pl-1"><span className="mt-[11px] h-1.5 w-1.5 shrink-0 rounded-full bg-violet-500" /><p>{inlineMarkdown(bullet[1])}</p></div>;

    const numbered = line.match(/^(\d+)\.\s+(.+)$/);
    if (numbered) return <div key={index} className="flex gap-2.5"><span className="flex h-6 min-w-6 items-center justify-center rounded-lg bg-violet-50 text-xs font-black text-violet-700">{numbered[1]}</span><p>{inlineMarkdown(numbered[2])}</p></div>;

    return <p key={index}>{inlineMarkdown(line)}</p>;
  })}</div>;
}

function inlineMarkdown(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((part, index) =>
    part.startsWith("**") && part.endsWith("**")
      ? <strong key={index} className="font-extrabold text-slate-900">{part.slice(2, -2)}</strong>
      : part
  );
}
