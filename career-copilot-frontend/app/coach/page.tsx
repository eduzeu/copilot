"use client";

import Link from "next/link";
import { useState } from "react";
import AppNavbar from "../../components/AppNavbar";
import { apiFetch } from "../../lib/api";

type Mode = "general" | "weekly_plan" | "application_strategy" | "interview_prep" | "profile_gaps";
type Message = { role: "user" | "assistant"; content: string };

const actions: { mode: Mode; title: string; prompt: string; description: string }[] = [
  { mode: "weekly_plan", title: "Plan my week", prompt: "Create my highest-impact career plan for the next seven days.", description: "A realistic, prioritized action plan" },
  { mode: "application_strategy", title: "Application strategy", prompt: "Review my current application strategy and tell me what to change.", description: "Use your actual pipeline and targets" },
  { mode: "interview_prep", title: "Interview preparation", prompt: "Build an interview preparation plan based on my profile and target roles.", description: "Technical and behavioral preparation" },
  { mode: "profile_gaps", title: "Analyze my gaps", prompt: "What are the most important gaps between my current profile and my target roles?", description: "Focus on the improvements that matter" },
];

export default function CoachPage() {
  const [messages, setMessages] = useState<Message[]>([{ role: "assistant", content: "Hi! I’m your Career Coach. I can use your profile, latest résumé, and application pipeline to help you decide what to do next." }]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<Mode>("general");
  const [loading, setLoading] = useState(false);
  const [completeness, setCompleteness] = useState<number | null>(null);
  const [context, setContext] = useState<string[]>([]);

  async function send(text = input, selectedMode = mode) {
    if (!text.trim() || loading) return;
    const userMessage: Message = { role: "user", content: text.trim() };
    const history = [...messages, userMessage];
    setMessages(history); setInput(""); setMode(selectedMode); setLoading(true);
    try {
      const result = await apiFetch<{ answer: string; profile_completeness: number; context_used: string[] }>("/coach/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage.content, mode: selectedMode, history: messages.slice(-10) }),
      });
      setMessages([...history, { role: "assistant", content: result.answer }]);
      setCompleteness(result.profile_completeness); setContext(result.context_used);
    } catch (e: any) {
      setMessages([...history, { role: "assistant", content: `I couldn’t generate advice: ${e.message}` }]);
    } finally { setLoading(false); }
  }

  return <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-950"><div className="mx-auto max-w-7xl"><AppNavbar />
    <div className="mb-7"><p className="text-sm font-bold text-violet-600">Your fourth AI tool</p><h1 className="mt-2 text-4xl font-black">Career Coach</h1><p className="mt-2 text-slate-600">Personalized guidance based on your profile and current job search.</p></div>
    <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
      <aside className="space-y-4">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="font-black">Quick actions</h2><div className="mt-4 space-y-3">{actions.map((action) => <button key={action.mode} onClick={() => send(action.prompt, action.mode)} disabled={loading} className="w-full rounded-2xl border border-slate-200 p-4 text-left transition hover:border-violet-300 hover:bg-violet-50"><span className="block font-bold">{action.title}</span><span className="mt-1 block text-xs leading-5 text-slate-500">{action.description}</span></button>)}</div></div>
        <div className="rounded-3xl bg-gradient-to-br from-violet-600 to-blue-600 p-5 text-white"><h2 className="font-black">Coach context</h2>{completeness === null ? <p className="mt-2 text-sm text-blue-100">Start a conversation to see what the coach uses.</p> : <><p className="mt-2 text-sm text-blue-100">Profile completeness: {completeness}%</p><p className="mt-2 text-xs text-blue-100">Using: {context.join(", ")}</p></>}<Link href="/profile" className="mt-4 inline-block rounded-xl bg-white/15 px-4 py-2 text-sm font-bold">Update profile</Link></div>
      </aside>
      <section className="flex min-h-[680px] flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-xl">
        <div className="border-b border-slate-100 px-6 py-4"><h2 className="font-black">Conversation</h2><p className="text-xs text-slate-500">Current mode: {mode.replaceAll("_", " ")}</p></div>
        <div className="flex-1 space-y-5 overflow-y-auto bg-slate-50/60 p-6">{messages.map((message, index) => <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}><div className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-5 py-4 text-sm leading-7 ${message.role === "user" ? "bg-gradient-to-r from-violet-600 to-blue-600 text-white" : "border border-slate-200 bg-white text-slate-700 shadow-sm"}`}>{message.content}</div></div>)}{loading && <div className="inline-block rounded-2xl border border-slate-200 bg-white px-5 py-4 text-sm text-slate-500">Thinking about your profile and search...</div>}</div>
        <form onSubmit={(e) => { e.preventDefault(); send(); }} className="border-t border-slate-100 p-4"><div className="flex gap-3"><textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} placeholder="Ask about your search, preparation, targets, or next steps..." className="min-h-14 flex-1 resize-none rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-violet-500" /><button disabled={loading || !input.trim()} className="rounded-2xl bg-slate-950 px-6 font-bold text-white disabled:opacity-40">Send</button></div><p className="mt-2 px-1 text-xs text-slate-400">Career Coach may make mistakes. Verify important company and hiring information.</p></form>
      </section>
    </div>
  </div></main>;
}
