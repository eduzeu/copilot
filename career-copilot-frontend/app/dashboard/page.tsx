"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import AppNavbar from "../../components/AppNavbar";

type Status = "applied" | "pending" | "interview" | "rejected" | "accepted";

type Application = {
  id: string;
  company: string;
  role: string;
  location?: string;
  status: Status;
  applied_date?: string;
  notes?: string;
};

export default function DashboardPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:8000";

  async function fetchApplications() {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_URL}/applications/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to load dashboard");
      }

      setApplications(data);
    } catch (err: any) {
      setError(err.message);
    }
  }

  useEffect(() => {
    fetchApplications();
  }, []);

  const stats = useMemo(() => {
    const total = applications.length;
    const applied = applications.filter((a) => a.status === "applied").length;
    const pending = applications.filter((a) => a.status === "pending").length;
    const interviews = applications.filter((a) => a.status === "interview").length;
    const accepted = applications.filter((a) => a.status === "accepted").length;
    const rejected = applications.filter((a) => a.status === "rejected").length;

    const responseRate =
      total > 0 ? Math.round(((interviews + accepted + rejected) / total) * 100) : 0;

    const successRate =
      total > 0 ? Math.round((accepted / total) * 100) : 0;

    return {
      total,
      applied,
      pending,
      interviews,
      accepted,
      rejected,
      responseRate,
      successRate,
    };
  }, [applications]);

  const recentApplications = applications.slice(0, 5);

  return (
    <main className="relative min-h-screen overflow-hidden bg-white px-6 py-8 text-slate-950">
      <div className="absolute inset-0 -z-10">
        <div className="absolute right-[-120px] top-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 opacity-40 blur-3xl" />
        <div className="absolute bottom-[-120px] left-[-120px] h-[420px] w-[420px] rounded-full bg-blue-300 opacity-40 blur-3xl" />
      </div>

      <div className="mx-auto max-w-7xl">
        <AppNavbar />
        <nav className="mb-10 flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-violet-600">
            </p>
            <h1 className="mt-2 text-4xl font-black tracking-tight">
              Dashboard
            </h1>
            <p className="mt-2 text-slate-600">
              Your job search performance at a glance.
            </p>
          </div>

          <Link
            href="/applications"
            className="rounded-full bg-gradient-to-r from-violet-600 to-blue-600 px-6 py-3 font-bold text-white shadow-xl shadow-blue-200 transition hover:scale-105"
          >
            Track applications
          </Link>
        </nav>

        {error && (
          <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-600">
            {error}
          </div>
        )}

        <section className="grid gap-4 md:grid-cols-4">
          <StatCard title="Total Applications" value={stats.total} subtitle="Roles tracked" />
          <StatCard title="Interviews" value={stats.interviews} subtitle="Interview stage" />
          <StatCard title="Response Rate" value={`${stats.responseRate}%`} subtitle="Any response received" />
          <StatCard title="Success Rate" value={`${stats.successRate}%`} subtitle="Accepted offers" />
        </section>

        <section className="mt-8 grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-2xl backdrop-blur-xl">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-black">Pipeline breakdown</h2>
                <p className="mt-1 text-sm text-slate-500">
                  See where your applications currently stand.
                </p>
              </div>
            </div>

            <div className="space-y-5">
              <ProgressRow label="Applied" value={stats.applied} total={stats.total} />
              <ProgressRow label="Pending" value={stats.pending} total={stats.total} />
              <ProgressRow label="Interview" value={stats.interviews} total={stats.total} />
              <ProgressRow label="Accepted" value={stats.accepted} total={stats.total} />
              <ProgressRow label="Rejected" value={stats.rejected} total={stats.total} />
            </div>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-2xl backdrop-blur-xl">
            <h2 className="text-2xl font-black">AI insight</h2>
            <p className="mt-2 text-sm text-slate-500">
              Based on your current pipeline.
            </p>

            <div className="mt-6 rounded-3xl bg-gradient-to-r from-violet-600 to-blue-600 p-6 text-white shadow-xl shadow-blue-200">
              <p className="text-lg font-black">Recommendation</p>
              <p className="mt-2 text-sm leading-relaxed text-blue-50">
                {stats.total === 0
                  ? "Start by adding your first applications so Career Copilot can track your progress."
                  : stats.interviews === 0
                    ? "You have applications tracked, but no interviews yet. Focus on improving resume targeting and referral outreach."
                    : stats.accepted > 0
                      ? "Strong progress. You already have accepted roles, so prioritize comparing offers and keeping backup options warm."
                      : "You are getting interviews. Keep tracking follow-ups and prepare targeted interview questions for each company."}
              </p>
            </div>

            <Link
              href="/applications"
              className="mt-6 block rounded-2xl border border-slate-200 bg-white px-5 py-4 text-center font-bold text-slate-800 shadow-sm transition hover:shadow-lg"
            >
              Manage applications
            </Link>
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-2xl backdrop-blur-xl">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-black">Recent applications</h2>
              <p className="mt-1 text-sm text-slate-500">
                Your latest tracked roles.
              </p>
            </div>

            <Link
              href="/applications"
              className="text-sm font-bold text-violet-600 hover:text-violet-700"
            >
              View all
            </Link>
          </div>

          {recentApplications.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
              <p className="font-bold text-slate-700">No applications yet</p>
              <p className="mt-1 text-sm text-slate-500">
                Add your first role to start seeing dashboard stats.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {recentApplications.map((app) => (
                <div
                  key={app.id}
                  className="flex items-center justify-between rounded-2xl border border-slate-100 bg-white p-4 shadow-sm"
                >
                  <div>
                    <p className="font-black">{app.company}</p>
                    <p className="text-sm text-slate-500">{app.role}</p>
                  </div>

                  <span className={`rounded-full px-3 py-1 text-xs font-bold ${statusStyle(app.status)}`}>
                    {formatStatus(app.status)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

function StatCard({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: number | string;
  subtitle: string;
}) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-xl backdrop-blur-xl">
      <p className="text-sm font-semibold text-slate-500">{title}</p>
      <p className="mt-2 text-4xl font-black">{value}</p>
      <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
    </div>
  );
}

function ProgressRow({
  label,
  value,
  total,
}: {
  label: string;
  value: number;
  total: number;
}) {
  const percentage = total > 0 ? Math.round((value / total) * 100) : 0;

  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm">
        <span className="font-bold text-slate-700">{label}</span>
        <span className="text-slate-500">
          {value} / {total}
        </span>
      </div>

      <div className="h-3 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-gradient-to-r from-violet-600 to-blue-600"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

function formatStatus(status: Status) {
  return status.charAt(0).toUpperCase() + status.slice(1);
}

function statusStyle(status: Status) {
  switch (status) {
    case "applied":
      return "bg-blue-50 text-blue-700";
    case "pending":
      return "bg-yellow-50 text-yellow-700";
    case "interview":
      return "bg-violet-50 text-violet-700";
    case "accepted":
      return "bg-green-50 text-green-700";
    case "rejected":
      return "bg-red-50 text-red-700";
    default:
      return "bg-slate-50 text-slate-700";
  }
}