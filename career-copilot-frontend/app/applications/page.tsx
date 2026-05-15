"use client";

import { useEffect, useMemo, useState } from "react";

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

const statuses: Status[] = ["applied", "pending", "interview", "rejected", "accepted"];

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [status, setStatus] = useState<Status>("applied");
  const [notes, setNotes] = useState("");
  const [filter, setFilter] = useState<"all" | Status>("all");
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
        throw new Error(data.detail || "Failed to load applications");
      }

      setApplications(data);
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function createApplication(e: React.FormEvent) {
    e.preventDefault();

    try {
      setError("");
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_URL}/applications/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          company,
          role,
          location,
          status,
          notes,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to create application");
      }

      setCompany("");
      setRole("");
      setLocation("");
      setStatus("applied");
      setNotes("");

      fetchApplications();
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function updateStatus(id: string, newStatus: Status) {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_URL}/applications/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: newStatus,
        }),
      });

      const data = await res.json().catch(() => null);

      if (!res.ok) {
        throw new Error(data?.detail || "Failed to update status");
      }

      setApplications((prev) =>
        prev.map((app) =>
          app.id === id ? { ...app, status: newStatus } : app
        )
      );
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function deleteApplication(id: string) {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`${API_URL}/applications/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || "Failed to delete application");
      }

      setApplications((prev) => prev.filter((app) => app.id !== id));
    } catch (err: any) {
      setError(err.message);
    }
  }

  useEffect(() => {
    fetchApplications();
  }, []);

  const filteredApplications = useMemo(() => {
    if (filter === "all") return applications;
    return applications.filter((app) => app.status === filter);
  }, [applications, filter]);

  const stats = useMemo(() => {
    return {
      total: applications.length,
      interviews: applications.filter((app) => app.status === "interview").length,
      accepted: applications.filter((app) => app.status === "accepted").length,
      rejected: applications.filter((app) => app.status === "rejected").length,
    };
  }, [applications]);

  return (
    <main className="min-h-screen bg-white text-slate-950 px-6 py-8">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-[-120px] right-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 blur-3xl opacity-40" />
        <div className="absolute bottom-[-120px] left-[-120px] h-[420px] w-[420px] rounded-full bg-blue-300 blur-3xl opacity-40" />
      </div>

      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold text-violet-600">
              Career Copilot
            </p>
            <h1 className="mt-2 text-4xl font-black tracking-tight">
              Job Applications
            </h1>
            <p className="mt-2 text-slate-600">
              Track every role, status, and note in one clean dashboard.
            </p>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-600">
            {error}
          </div>
        )}

        <section className="mb-8 grid gap-4 md:grid-cols-4">
          <StatCard label="Total Applications" value={stats.total} />
          <StatCard label="Interviews" value={stats.interviews} />
          <StatCard label="Accepted" value={stats.accepted} />
          <StatCard label="Rejected" value={stats.rejected} />
        </section>

        <section className="grid gap-8 lg:grid-cols-[420px_1fr]">
          <form
            onSubmit={createApplication}
            className="h-fit rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-2xl backdrop-blur-xl"
          >
            <h2 className="text-2xl font-black">Add application</h2>
            <p className="mt-1 text-sm text-slate-500">
              Save a new role you applied to or want to track.
            </p>

            <div className="mt-6 space-y-4">
              <Input label="Company" value={company} setValue={setCompany} placeholder="Google" />
              <Input label="Role" value={role} setValue={setRole} placeholder="Software Engineer Intern" />
              <Input label="Location" value={location} setValue={setLocation} placeholder="New York, NY" />

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value as Status)}
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 outline-none transition focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
                >
                  {statuses.map((s) => (
                    <option key={s} value={s}>
                      {formatStatus(s)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Notes
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Recruiter name, interview date, referral, etc."
                  className="min-h-28 w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                />
              </div>

              <button
                type="submit"
                className="w-full rounded-2xl bg-gradient-to-r from-violet-600 to-blue-600 px-6 py-4 font-bold text-white shadow-2xl shadow-blue-200 transition hover:scale-[1.02]"
              >
                Add application
              </button>
            </div>
          </form>

          <section className="rounded-[2rem] border border-slate-200 bg-white/80 p-6 shadow-2xl backdrop-blur-xl">
            <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-2xl font-black">Tracked roles</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Update statuses as your process moves forward.
                </p>
              </div>

              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as "all" | Status)}
                className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold outline-none focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
              >
                <option value="all">All statuses</option>
                {statuses.map((s) => (
                  <option key={s} value={s}>
                    {formatStatus(s)}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-4">
              {filteredApplications.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
                  <p className="font-bold text-slate-700">No applications yet</p>
                  <p className="mt-1 text-sm text-slate-500">
                    Add your first application using the form.
                  </p>
                </div>
              ) : (
                filteredApplications.map((app) => (
                  <div
                    key={app.id}
                    className="rounded-3xl border border-slate-100 bg-white p-5 shadow-sm transition hover:shadow-lg"
                  >
                    <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                      <div>
                        <div className="flex items-center gap-3">
                          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500" />
                          <div>
                            <h3 className="text-lg font-black">{app.company}</h3>
                            <p className="text-sm text-slate-500">{app.role}</p>
                          </div>
                        </div>

                        {app.location && (
                          <p className="mt-3 text-sm text-slate-500">
                            {app.location}
                          </p>
                        )}

                        {app.notes && (
                          <p className="mt-3 rounded-2xl bg-slate-50 p-3 text-sm text-slate-600">
                            {app.notes}
                          </p>
                        )}
                      </div>

                      <div className="flex flex-col gap-3 md:items-end">
                        <span className={`rounded-full px-3 py-1 text-xs font-bold ${statusStyle(app.status)}`}>
                          {formatStatus(app.status)}
                        </span>

                        <select
                          value={app.status}
                          onChange={(e) =>
                            updateStatus(app.id, e.target.value as Status)
                          }
                          className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none"
                        >
                          {statuses.map((s) => (
                            <option key={s} value={s}>
                              {formatStatus(s)}
                            </option>
                          ))}
                        </select>

                        <button
                          onClick={() => deleteApplication(app.id)}
                          className="text-sm font-semibold text-red-500 hover:text-red-600"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>
        </section>
      </div>
    </main>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-xl backdrop-blur-xl">
      <p className="text-sm font-semibold text-slate-500">{label}</p>
      <p className="mt-2 text-4xl font-black">{value}</p>
    </div>
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
        required={label !== "Location"}
      />
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