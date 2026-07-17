"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import AppNavbar from "../../components/AppNavbar";

type Status = "applied" | "pending" | "interview" | "rejected" | "accepted";

type Application = {
  id: number;
  company: string;
  role_title: string;
  location: string;
  date_applied: string;
  status: Status;
};

const statuses: Status[] = ["applied", "interview", "rejected", "accepted"];

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [company, setCompany] = useState("");
  const [role_title, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [dateApplied, setDateApplied] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [status, setStatus] = useState<Status>("applied");
  const [filter, setFilter] = useState<"all" | Status>("all");
  const [error, setError] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

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
          role_title,
          date_applied: dateApplied,
          status,
          location,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to create application");
      }

      setCompany("");
      setRole("");
      setLocation("");
      setDateApplied(new Date().toISOString().split("T")[0]);
      setStatus("applied");

      fetchApplications();
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function updateStatus(id: number, newStatus: Status) {
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

  async function deleteApplication(id: number) {
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
    <main className="app-page text-slate-950">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-[-120px] right-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 blur-3xl opacity-40" />
        <div className="absolute bottom-[-120px] left-[-120px] h-[420px] w-[420px] rounded-full bg-blue-300 blur-3xl opacity-40" />
      </div>

      <div className="app-container">
        <AppNavbar />

        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="eyebrow">Your opportunity pipeline</p>
            <h1 className="mt-3 text-4xl font-black tracking-[-0.04em] sm:text-5xl">
              Every role. <span className="gradient-text">One clear view.</span>
            </h1>
            <p className="mt-2 text-slate-600">
              Track every role and status in one clean dashboard.
            </p>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-600">
            {error}
          </div>
        )}

        <section className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total Applications" value={stats.total} />
          <StatCard label="Interviews" value={stats.interviews} />
          <StatCard label="Accepted" value={stats.accepted} />
          <StatCard label="Rejected" value={stats.rejected} />
        </section>

        <section className="grid gap-6 xl:grid-cols-[minmax(340px,420px)_1fr] xl:gap-8">
          <form
            onSubmit={createApplication}
            className="surface-card h-fit rounded-[2rem] p-6"
          >
            <h2 className="text-2xl font-black">Add application</h2>
            <p className="mt-1 text-sm text-slate-500">
              Save a new role you applied to or want to track.
            </p>

            <div className="mt-6 space-y-4">
              <Input label="Company" value={company} setValue={setCompany} placeholder="Google" />
              <Input label="Role" value={role_title} setValue={setRole} placeholder="Software Engineer Intern" />
              <Input label="Location" value={location} setValue={setLocation} placeholder="New York, NY" />

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Date Applied
                </label>
                <input
                  type="date"
                  value={dateApplied}
                  onChange={(e) => setDateApplied(e.target.value)}
                  className="field-control"
                  required
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value as Status)}
                  className="field-control"
                >
                  {statuses.map((s) => (
                    <option key={s} value={s}>
                      {formatStatus(s)}
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                className="w-full rounded-2xl bg-gradient-to-r from-violet-600 to-blue-600 px-6 py-4 font-bold text-white shadow-2xl shadow-blue-200 transition hover:scale-[1.02]"
              >
                Add application
              </button>
            </div>
          </form>

          <section className="surface-card rounded-[2rem] p-6">
            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-black">Tracked roles</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Update statuses as your process moves forward.
                </p>
              </div>

              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as "all" | Status)}
                className="field-control w-full text-sm font-semibold sm:w-auto"
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
                    className="group rounded-3xl border border-slate-100 bg-white p-5 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:border-violet-200 hover:shadow-xl"
                  >
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                      <div>
                        <div className="flex items-center gap-3">
                          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500" />
                          <div>
                            <h3 className="text-lg font-black">{app.company}</h3>
                            <p className="text-sm text-slate-500">
                              {app.role_title}
                            </p>
                          </div>
                        </div>

                        <p className="mt-3 text-sm text-slate-500">
                          {app.location}
                        </p>

                        <p className="mt-2 text-sm text-slate-500">
                          Applied: {new Date(app.date_applied).toLocaleDateString()}
                        </p>
                      </div>

                      <div className="flex flex-row items-center justify-between gap-3 sm:flex-col sm:items-end">
                        <StatusSelect
                          value={app.status}
                          onChange={(nextStatus) => updateStatus(app.id, nextStatus)}
                        />

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
    <div className="surface-card rounded-3xl p-6">
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
        className="field-control"
        required
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

function StatusSelect({ value, onChange }: { value: Status; onChange: (status: Status) => void }) {
  const detailsRef = useRef<HTMLDetailsElement>(null);
  const displayedValue: Status = value === "pending" ? "applied" : value;

  function closeOtherMenus() {
    document.querySelectorAll<HTMLDetailsElement>("details[data-status-menu][open]").forEach((menu) => {
      if (menu !== detailsRef.current) menu.open = false;
    });
  }

  function choose(status: Status) {
    onChange(status);
    if (detailsRef.current) detailsRef.current.open = false;
  }

  return (
    <details ref={detailsRef} data-status-menu className="group/status w-44">
      <summary onClick={closeOtherMenus} className={`flex min-w-36 cursor-pointer list-none items-center justify-between gap-3 rounded-full border border-current/10 px-4 py-2.5 text-sm font-bold shadow-sm transition hover:shadow-md [&::-webkit-details-marker]:hidden ${statusStyle(displayedValue)}`}>
        {formatStatus(displayedValue)}
        <span className="text-xs transition group-open/status:rotate-180">⌄</span>
      </summary>
      <div className="mt-2 max-h-72 w-44 overflow-y-auto rounded-2xl border border-slate-200 bg-white p-1.5 shadow-xl shadow-slate-300/40">
        {statuses.map((status) => (
          <button
            key={status}
            type="button"
            onClick={() => choose(status)}
            className={`flex w-full items-center justify-between rounded-xl px-3.5 py-2.5 text-left text-sm font-semibold transition ${status === displayedValue ? statusStyle(status) : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"}`}
          >
            {formatStatus(status)}
            {status === displayedValue && <span aria-hidden="true">✓</span>}
          </button>
        ))}
      </div>
    </details>
  );
}
