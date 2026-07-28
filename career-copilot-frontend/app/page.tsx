import Link from "next/link";
import BrandMark from "../components/BrandMark";

const features = [
  { number: "01", title: "Organize the search", text: "Keep every role, follow-up, interview, and decision in one calm pipeline." },
  { number: "02", title: "Tailor every move", text: "Compare your resume to each job and find the gaps that actually matter." },
  { number: "03", title: "Prepare with context", text: "Practice questions and get coaching grounded in your goals and progress." },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen overflow-hidden bg-[#f8fafc] text-slate-950">
      <section className="relative">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-28 -top-36 h-[34rem] w-[34rem] rounded-full bg-violet-200/60 blur-3xl" />
          <div className="absolute -left-40 top-[34rem] h-[30rem] w-[30rem] rounded-full bg-cyan-100/80 blur-3xl" />
        </div>

        <nav className="relative mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-5 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
            <BrandMark />
            <span className="text-lg font-black tracking-[-0.035em]">Career Copilot</span>
          </Link>
          <div className="flex items-center gap-2 sm:gap-3">
            <Link href="/auth/login" className="hidden rounded-full px-4 py-2.5 text-sm font-bold text-slate-600 transition hover:bg-white hover:text-slate-950 sm:inline-flex">
              Sign in
            </Link>
            <Link href="/auth/account" className="button-primary !px-5 !py-2.5 text-sm">
              Build my plan <span aria-hidden="true">→</span>
            </Link>
          </div>
        </nav>

        <div className="relative mx-auto grid max-w-7xl items-center gap-14 px-4 pb-24 pt-14 sm:px-6 sm:pt-20 lg:grid-cols-[1.02fr_.98fr] lg:px-8 lg:pb-32 lg:pt-24">
          <div>
            <div className="eyebrow">A clearer way to find your next role</div>
            <h1 className="mt-6 max-w-3xl text-[clamp(3.35rem,7vw,6.7rem)] font-black leading-[.9] tracking-[-0.072em]">
              Turn the job search into a <span className="gradient-text">system.</span>
            </h1>
            <p className="mt-7 max-w-xl text-lg leading-8 text-slate-600 sm:text-xl">
              One focused workspace to track opportunities, sharpen your resume, prepare for interviews, and know what to do next.
            </p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link href="/auth/account" className="button-primary">
                Start your workspace <span aria-hidden="true">→</span>
              </Link>
              <Link href="#how-it-works" className="button-secondary">
                See how it works <span aria-hidden="true">↓</span>
              </Link>
            </div>
            <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm font-semibold text-slate-500">
              <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-emerald-400" /> Free to start</span>
              <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-violet-400" /> Private by design</span>
              <span className="flex items-center gap-2"><i className="h-2 w-2 rounded-full bg-cyan-400" /> Built for momentum</span>
            </div>
          </div>

          <ProductPreview />
        </div>
      </section>

      <section id="how-it-works" className="relative border-y border-slate-200/80 bg-white/70">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-28">
          <div className="grid gap-10 lg:grid-cols-[.72fr_1.28fr] lg:gap-20">
            <div>
              <p className="eyebrow">Your weekly rhythm</p>
              <h2 className="mt-5 text-4xl font-black tracking-[-0.05em] sm:text-5xl">
                Less guessing.<br />More momentum.
              </h2>
              <p className="mt-5 max-w-md leading-7 text-slate-600">
                Career Copilot connects the pieces of your search, so every action builds on the last one.
              </p>
            </div>
            <div className="grid gap-px overflow-hidden rounded-[2rem] border border-slate-200 bg-slate-200 md:grid-cols-3">
              {features.map((feature) => (
                <article key={feature.number} className="group bg-white p-7 transition hover:bg-slate-950 md:min-h-72">
                  <span className="font-mono text-xs font-bold text-violet-500">{feature.number}</span>
                  <div className="mt-14 flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-lg transition group-hover:border-slate-700 group-hover:text-cyan-300">↗</div>
                  <h3 className="mt-6 text-xl font-black tracking-tight transition group-hover:text-white">{feature.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-500 transition group-hover:text-slate-400">{feature.text}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="relative mx-auto max-w-7xl overflow-hidden rounded-[2rem] bg-slate-950 px-6 py-12 text-white sm:px-12 sm:py-16">
          <div className="absolute right-0 top-0 h-72 w-72 rounded-full bg-violet-500/30 blur-3xl" />
          <div className="relative flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-sm font-bold uppercase tracking-[.18em] text-cyan-300">Make the next move count</p>
              <h2 className="mt-4 max-w-3xl text-4xl font-black tracking-[-0.05em] sm:text-5xl">Your next opportunity deserves a better process.</h2>
            </div>
            <Link href="/auth/account" className="inline-flex shrink-0 items-center justify-center rounded-full bg-white px-6 py-3.5 font-black text-slate-950 transition hover:-translate-y-1">
              Get started free <span className="ml-2">→</span>
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

function ProductPreview() {
  return (
    <div className="relative mx-auto w-full max-w-[39rem] lg:ml-auto">
      <div className="absolute -inset-8 rounded-[3rem] bg-gradient-to-br from-violet-300/30 via-transparent to-cyan-200/40 blur-2xl" />
      <div className="surface-card-strong relative overflow-hidden rounded-[1.75rem] p-3 shadow-[0_40px_100px_-45px_rgba(15,23,42,.7)] sm:p-4">
        <div className="flex items-center justify-between px-2 pb-4 pt-1">
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-red-300" />
            <span className="h-2.5 w-2.5 rounded-full bg-amber-300" />
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-300" />
          </div>
          <span className="text-[10px] font-black uppercase tracking-[.18em] text-slate-400">Weekly command center</span>
        </div>
        <div className="rounded-[1.35rem] bg-slate-950 p-5 text-white sm:p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-bold text-cyan-300">MONDAY · JUL 27</p>
              <h2 className="mt-2 text-2xl font-black tracking-tight sm:text-3xl">Good morning, Alex.</h2>
              <p className="mt-1 text-sm text-slate-400">Here’s the move that matters today.</p>
            </div>
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-xs font-bold text-slate-300">72% profile</span>
          </div>
          <div className="mt-6 grid gap-3 sm:grid-cols-[1.3fr_.7fr]">
            <div className="rounded-2xl bg-white p-5 text-slate-950">
              <div className="flex items-center justify-between">
                <span className="text-xs font-black uppercase tracking-wider text-violet-600">Next best action</span>
                <span className="text-slate-400">01</span>
              </div>
              <h3 className="mt-6 text-xl font-black">Tailor your resume for Stripe</h3>
              <p className="mt-2 text-sm leading-6 text-slate-500">Your experience matches well. Strengthen two impact bullets before applying.</p>
              <div className="mt-5 flex items-center justify-between border-t border-slate-100 pt-4 text-xs font-bold">
                <span className="text-slate-400">~12 minutes</span>
                <span className="text-violet-600">Start action →</span>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-1">
              <Metric label="Active roles" value="08" accent="text-cyan-300" />
              <Metric label="Interviews" value="03" accent="text-violet-300" />
            </div>
          </div>
        </div>
        <div className="grid grid-cols-3 gap-2 p-2 pt-4 text-center">
          {["Pipeline", "Resume lab", "Coach"].map((label, index) => (
            <div key={label} className={`rounded-xl px-2 py-2.5 text-xs font-bold ${index === 0 ? "bg-violet-50 text-violet-700" : "text-slate-400"}`}>{label}</div>
          ))}
        </div>
      </div>
      <div className="absolute -bottom-5 -left-5 hidden rounded-2xl border border-white/70 bg-white/90 px-4 py-3 shadow-xl backdrop-blur sm:block">
        <p className="text-[10px] font-black uppercase tracking-wider text-slate-400">This week</p>
        <p className="mt-1 text-sm font-black text-slate-900"><span className="text-emerald-500">↑ 18%</span> more momentum</p>
      </div>
    </div>
  );
}

function Metric({ label, value, accent }: { label: string; value: string; accent: string }) {
  return (
    <div className="rounded-2xl bg-white/10 p-4">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{label}</p>
      <p className={`mt-2 text-2xl font-black ${accent}`}>{value}</p>
    </div>
  );
}
