"use client";
import Link from "next/link";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "../../../lib/api";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const data = await apiFetch<{ access_token: string }>("/auth/login", {
          method: "POST",
          body: JSON.stringify({
            email,
            password,
          }),
          redirectOnUnauthorized: false,
        });

      router.push("/dashboard");
      router.refresh();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-white px-4 py-8 sm:px-6">
      {/* Background blur gradients */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-[-120px] right-[-120px] h-[420px] w-[420px] rounded-full bg-violet-300 blur-3xl opacity-40" />

        <div className="absolute bottom-[-120px] left-[-120px] h-[420px] w-[420px] rounded-full bg-blue-300 blur-3xl opacity-40" />

        <div className="absolute top-[40%] left-[45%] h-[300px] w-[300px] rounded-full bg-cyan-200 blur-3xl opacity-30" />
      </div>

      <div className="w-full max-w-md">
        {/* Logo / heading */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 h-16 w-16 rounded-3xl bg-gradient-to-br from-violet-600 to-blue-500 shadow-2xl shadow-violet-300" />

          <h1 className="text-4xl font-black tracking-tight">
            Career Copilot
          </h1>

          <p className="mt-3 text-slate-600">
            AI-powered job search assistant
          </p>
        </div>

        {/* Card */}
        <div className="surface-card rounded-[2rem] p-5 sm:p-8">
          <div className="mb-6">
            <h2 className="text-3xl font-black text-slate-950">
              Welcome back
            </h2>

            <p className="mt-2 text-slate-500">
              Login to continue your job search journey.
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Email
              </label>

              <input
                type="email"
                placeholder="example@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="field-control py-4"
                required
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Password
              </label>

              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="field-control py-4"
                required
              />
            </div>

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
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-500">
            Don&apos;t have an account?{" "}
            <Link href="/auth/account" className="font-semibold text-violet-600 cursor-pointer hover:text-violet-700">
              Create one
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
