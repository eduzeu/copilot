import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-white text-slate-950 overflow-hidden">
      <section className="relative min-h-screen flex flex-col">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-[-120px] right-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 blur-3xl opacity-40" />
          <div className="absolute bottom-[-140px] left-[-100px] h-[420px] w-[420px] rounded-full bg-blue-300 blur-3xl opacity-40" />
        </div>

        <nav className="mx-auto flex w-full max-w-7xl items-center justify-between gap-3 px-4 py-5 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500 shadow-lg" />
            <span className="hidden text-xl font-bold sm:block">Career Copilot</span>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/auth/login" className="text-sm font-medium text-slate-600 hover:text-slate-950">
              Login
            </Link>

            <Link href="/auth/account" className="rounded-full bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white">
              Get Started
            </Link>
          </div>
        </nav>

        <div className="mx-auto grid max-w-7xl flex-1 items-center gap-10 px-4 py-10 sm:px-6 sm:py-16 lg:grid-cols-2 lg:gap-12 lg:px-8">
          <div>
            <div className="inline-flex rounded-full border border-violet-200 bg-violet-50 px-4 py-2 text-sm font-medium text-violet-700 mb-6">
              AI-powered job search assistant
            </div>

            <h1 className="text-4xl font-black leading-[1.05] tracking-tight sm:text-5xl md:text-6xl xl:text-7xl">
              Land your next role with an{" "}
              <span className="bg-gradient-to-r from-violet-600 via-blue-600 to-cyan-500 bg-clip-text text-transparent">
                AI career copilot.
              </span>
            </h1>

            <p className="mt-6 text-lg md:text-xl text-slate-600 max-w-xl">
              Track applications, analyze resumes, generate interview questions,
              and improve your job search workflow.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:gap-4">
              <Link href="/auth/account" className="rounded-full bg-gradient-to-r from-violet-600 to-blue-600 px-8 py-4 text-white font-bold">
                Start for free
              </Link>

              <Link href="/auth/login" className="rounded-full border border-slate-200 bg-white px-8 py-4 font-bold">
                Login
              </Link>
            </div>
          </div>

          <div className="relative rounded-[2rem] border border-slate-200 bg-white shadow-2xl p-6">
            <p className="text-sm text-slate-500">Dashboard</p>
            <h2 className="text-2xl font-bold mb-6">Job Search Overview</h2>

            <div className="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-3 sm:gap-4">
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Applications</p>
                <p className="text-2xl font-black">14</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Interviews</p>
                <p className="text-2xl font-black">3</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Score</p>
                <p className="text-2xl font-black">87%</p>
              </div>
            </div>

            <div className="rounded-2xl bg-gradient-to-r from-violet-600 to-blue-600 p-5 text-white">
              <p className="font-bold">AI Suggestion</p>
              <p className="text-sm mt-1">
                Your resume is strong, but your impact bullets can be more quantified.
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
