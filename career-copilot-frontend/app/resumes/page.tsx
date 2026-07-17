"use client";

import { useState } from "react";
import AppNavbar from "../../components/AppNavbar";
import AILoader from "../../components/AILoader";

type ToolMode = "resume" | "job" | "coach";

export default function AIToolsPage() {
  const [mode, setMode] = useState<ToolMode>("resume");

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const token = localStorage.getItem("token");

      let endpoint = "";
      let options: RequestInit = {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      if (mode === "resume") {
        if (!resumeFile) throw new Error("Please upload a resume.");

        endpoint = "/analysis/resume-feedback";

        const formData = new FormData();
        formData.append("file", resumeFile);

        options.body = formData;
      }

      if (mode === "job") {
        if (!resumeFile) throw new Error("Please upload a resume.");

        endpoint = "/analysis/job-match";

        const formData = new FormData();
        formData.append("file", resumeFile);
        formData.append("job_description", jobDescription);

        options.body = formData;
      }

      if (mode === "coach") {
        endpoint = "/coach/questions";

        options.headers = {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        };

        options.body = JSON.stringify({
          role,
          company,
          job_description: jobDescription,
          question_type: "technical",
          count: 10,
        });
      }

      const res = await fetch(`${API_URL}${endpoint}`, options);
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "AI request failed");
      }

      if (mode === "coach") {
        setResult(data.questions || []);
      } else {
        setResult(data.feedback ?? data.analysis ?? data.response ?? data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function resetMode(nextMode: ToolMode) {
    setMode(nextMode);
    setResult(null);
    setError("");
  }

  return (
    <main className="app-page text-slate-950">
      <div className="absolute inset-0 -z-10">
        <div className="absolute right-[-120px] top-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 opacity-40 blur-3xl" />
        <div className="absolute bottom-[-120px] left-[-120px] h-[420px] w-[420px] rounded-full bg-blue-300 opacity-40 blur-3xl" />
      </div>

      <div className="app-container">
        <AppNavbar />

        <div className="mb-8">
          <p className="eyebrow">Career Copilot intelligence</p>
          <h1 className="mt-3 text-4xl font-black tracking-[-0.04em] sm:text-5xl">
            Sharper tools. <span className="gradient-text">Stronger moves.</span>
          </h1>
          <p className="mt-2 text-slate-600">
            Upload your resume, compare it to jobs, or generate interview questions.
          </p>
        </div>

        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <ToolCard
            active={mode === "resume"}
            title="Resume Feedback"
            description="Upload your resume and get feedback."
            onClick={() => resetMode("resume")}
          />

          <ToolCard
            active={mode === "job"}
            title="Job Match"
            description="Upload resume + paste job description."
            onClick={() => resetMode("job")}
          />

          <ToolCard
            active={mode === "coach"}
            title="Interview Coach"
            description="Generate sample interview questions."
            onClick={() => resetMode("coach")}
          />
        </div>

        <section className="grid gap-8 lg:grid-cols-[0.85fr_1.15fr]">
          <form
            onSubmit={handleSubmit}
            className="surface-card rounded-[2rem] p-6"
          >
            <h2 className="text-2xl font-black">
              {mode === "resume" && "Upload Resume"}
              {mode === "job" && "Resume vs Job Description"}
              {mode === "coach" && "Interview Question Generator"}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {mode === "resume" &&
                "Upload your resume and get AI feedback on impact, clarity, and structure."}
              {mode === "job" &&
                "Upload your resume and paste the job description for targeted feedback."}
              {mode === "coach" &&
                "Enter the role/company and optionally paste the job description."}
            </p>

            <div className="mt-6 space-y-5">
              {(mode === "resume" || mode === "job") && (
                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Resume File
                  </label>

                  <input
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={(e) =>
                      setResumeFile(e.target.files?.[0] || null)
                    }
                    className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 outline-none transition file:mr-4 file:rounded-xl file:border-0 file:bg-gradient-to-r file:from-violet-600 file:to-blue-600 file:px-4 file:py-2 file:font-bold file:text-white hover:file:opacity-90"
                    required
                  />

                  {resumeFile && (
                    <p className="mt-2 text-sm text-slate-500">
                      Selected:{" "}
                      <span className="font-semibold text-slate-700">
                        {resumeFile.name}
                      </span>
                    </p>
                  )}
                </div>
              )}

              {mode === "coach" && (
                <div className="grid gap-4 md:grid-cols-2">
                  <Input
                    label="Role"
                    value={role}
                    setValue={setRole}
                    placeholder="Software Engineer Intern"
                  />
                  <Input
                    label="Company"
                    value={company}
                    setValue={setCompany}
                    placeholder="Google"
                  />
                </div>
              )}

              {(mode === "job" || mode === "coach") && (
                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Job Description
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here..."
                    className="min-h-48 w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                    required={mode === "job"}
                  />
                </div>
              )}

              {error && (
                <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-2xl bg-gradient-to-r from-violet-600 to-blue-600 px-6 py-4 font-bold text-white shadow-2xl shadow-blue-200 transition hover:scale-[1.02] disabled:opacity-50"
              >
                {loading ? "Generating..." : "Generate"}
              </button>
            </div>
          </form>

          <div className="surface-card rounded-[2rem] p-6">
            <h2 className="text-2xl font-black">AI Output</h2>
            <p className="mt-1 text-sm text-slate-500">
              Your results will appear here.
            </p>

            <div className="mt-6 min-h-[420px] rounded-3xl border border-slate-100 bg-slate-50 p-5">
              {loading ? (
                <AILoader messages={mode === "coach" ? ["Reviewing the role and company", "Choosing relevant interview themes", "Balancing technical depth and clarity", "Preparing your question set"] : mode === "job" ? ["Reading your résumé", "Comparing it with the role", "Identifying strengths and missing signals", "Building targeted recommendations"] : ["Reading your résumé", "Evaluating clarity and impact", "Looking for measurable achievements", "Preparing your feedback"]} />
              ) : result ? (
                mode === "coach" && Array.isArray(result) ? (
                  <div className="space-y-4">
                    {result.map((q: any, index: number) => (
                      <div
                        key={index}
                        className="rounded-xl border border-slate-200 bg-white p-4"
                      >
                        <h3 className="font-semibold text-slate-900">
                          {index + 1}. {q.question_text}
                        </h3>

                        {q.reason && (
                          <p className="mt-2 text-sm text-slate-500">
                            {q.reason}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <AnalysisResult data={result} mode={mode} />
                )
              ) : (
                <div className="flex h-full min-h-[360px] items-center justify-center text-center">
                  <div>
                    <div className="mx-auto mb-4 h-14 w-14 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500 shadow-xl shadow-blue-200" />
                    <p className="font-bold text-slate-700">No output yet</p>
                    <p className="mt-1 text-sm text-slate-500">
                      Choose a tool, upload/fill the form, and submit.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function ToolCard({
  active,
  title,
  description,
  onClick,
}: {
  active: boolean;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-3xl border p-6 text-left shadow-xl transition hover:scale-[1.02] ${active
          ? "border-violet-300 bg-gradient-to-r from-violet-600 to-blue-600 text-white shadow-blue-200"
          : "border-slate-200 bg-white/80 text-slate-950"
        }`}
    >
      <h3 className="text-xl font-black">{title}</h3>
      <p className={`mt-2 text-sm ${active ? "text-blue-50" : "text-slate-500"}`}>
        {description}
      </p>
    </button>
  );
}

function Input({
  label,
  value,
  setValue,
  placeholder,
}: {
  label: string;
  value: string;
  setValue: (value: string) => void;
  placeholder: string;
}) {
  return (
    <div>
      <label className="mb-2 block text-sm font-semibold text-slate-700">
        {label}
      </label>
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 outline-none transition focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
        required
      />
    </div>
  );
}

function AnalysisResult({ data, mode }: { data: any; mode: ToolMode }) {
  if (!data || typeof data !== "object") {
    return <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-700">{String(data)}</p>;
  }

  const isJobMatch = mode === "job";
  if (data.is_resume === false) {
    const summary = isJobMatch ? data.summary : data.feedback;
    return (
      <ResultCard icon="!" title="This document is not a resume" colors="border-amber-200 bg-amber-50 text-amber-950">
        <p className="text-sm leading-7 text-slate-700">{summary || "The uploaded document could not be evaluated as a resume. Please upload a resume or CV."}</p>
      </ResultCard>
    );
  }
  const score = Number(isJobMatch ? data.overall_score : data.quality_score) || 0;
  const summary = isJobMatch ? data.summary : data.feedback;
  const scoreColor = score >= 80 ? "from-emerald-500 to-teal-500" : score >= 60 ? "from-amber-400 to-orange-500" : "from-rose-500 to-pink-500";

  return (
    <div className="space-y-5">
      <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${scoreColor} p-6 text-white shadow-xl`}>
        <div className="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-white/15" />
        <p className="text-xs font-black uppercase tracking-[0.2em] text-white/80">
          {isJobMatch ? "Match score" : "Resume score"}
        </p>
        <div className="mt-2 flex items-end gap-2">
          <span className="text-6xl font-black leading-none">{score}</span>
          <span className="mb-1 text-xl font-bold text-white/75">/100</span>
        </div>
        {data.recommendation && (
          <span className="mt-4 inline-flex rounded-full bg-white/20 px-3 py-1 text-xs font-bold backdrop-blur">
            {data.recommendation}
          </span>
        )}
      </div>

      {summary && (
        <ResultCard icon="✦" title="Career Coach Summary" colors="border-violet-200 bg-violet-50 text-violet-950">
          <p className="text-sm leading-7 text-slate-700">{summary}</p>
        </ResultCard>
      )}

      {isJobMatch ? (
        <>
          <ResultList title="Your strengths" items={data.strengths} colors="border-emerald-200 bg-emerald-50 text-emerald-950" bullet="✓" />
          <ResultList title="Gaps to close" items={data.gaps} colors="border-amber-200 bg-amber-50 text-amber-950" bullet="→" />
          <ResultList title="Missing keywords" items={data.missing_keywords} colors="border-blue-200 bg-blue-50 text-blue-950" bullet="#" compact />
        </>
      ) : (
        <>
          {data.rewrite_ats && (
            <ResultCard icon="◎" title="ATS Game Plan" colors="border-blue-200 bg-blue-50 text-blue-950">
              <p className="text-sm leading-7 text-slate-700">{data.rewrite_ats}</p>
            </ResultCard>
          )}
          {data.rewrite_strong && (
            <ResultCard icon="↗" title="Make It Stand Out" colors="border-fuchsia-200 bg-fuchsia-50 text-fuchsia-950">
              <p className="text-sm leading-7 text-slate-700">{data.rewrite_strong}</p>
            </ResultCard>
          )}
          <ResultList title="Priority improvements" items={data.suggestions} colors="border-amber-200 bg-amber-50 text-amber-950" bullet="→" />
          <ResultList title="Numbers to add" items={data.quantification_suggestions} colors="border-emerald-200 bg-emerald-50 text-emerald-950" bullet="+" />
        </>
      )}
    </div>
  );
}

function ResultCard({ icon, title, colors, children }: { icon: string; title: string; colors: string; children: React.ReactNode }) {
  return (
    <section className={`rounded-2xl border p-5 ${colors}`}>
      <h3 className="mb-3 flex items-center gap-2 text-base font-black">
        <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-white/80 shadow-sm">{icon}</span>
        {title}
      </h3>
      {children}
    </section>
  );
}

function ResultList({ title, items, colors, bullet, compact = false }: { title: string; items?: string[]; colors: string; bullet: string; compact?: boolean }) {
  if (!Array.isArray(items) || items.length === 0) return null;
  return (
    <ResultCard icon={bullet} title={title} colors={colors}>
      <div className={compact ? "flex flex-wrap gap-2" : "space-y-2"}>
        {items.map((item, index) => compact ? (
          <span key={index} className="rounded-full bg-white px-3 py-1.5 text-xs font-bold text-slate-700 shadow-sm">{item}</span>
        ) : (
          <div key={index} className="flex gap-3 rounded-xl bg-white/70 p-3 text-sm leading-6 text-slate-700">
            <span className="font-black">{bullet}</span><span>{item}</span>
          </div>
        ))}
      </div>
    </ResultCard>
  );
}
