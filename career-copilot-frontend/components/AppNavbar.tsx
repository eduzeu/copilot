"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { apiFetch } from "../lib/api";

const links = [
  { href: "/dashboard", label: "Overview" },
  { href: "/applications", label: "Applications" },
  { href: "/resumes", label: "AI tools" },
  { href: "/coach", label: "Career Coach" },
  { href: "/profile", label: "Profile" },
];

export default function AppNavbar() {
  const pathname = usePathname();
  const router = useRouter();

  async function logout() {
    await apiFetch<void>("/auth/logout", { method: "POST", redirectOnUnauthorized: false }).catch(() => undefined);
    localStorage.removeItem("token");
    router.push("/auth/login");
  }

  return (
    <nav className="surface-card sticky top-2 z-40 mb-7 flex items-center gap-2 overflow-hidden rounded-[1.6rem] p-2 shadow-[0_20px_60px_-32px_rgba(76,29,149,.55)] sm:top-4 sm:mb-10 sm:gap-3 sm:p-2.5">
      <Link href="/dashboard" className="group flex shrink-0 items-center gap-3 pr-1 md:pr-3">
        <div className="relative flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 via-indigo-600 to-blue-500 text-[11px] font-black tracking-tight text-white shadow-lg shadow-violet-200 transition duration-300 group-hover:-rotate-3 group-hover:scale-105 sm:h-11 sm:w-11 sm:text-xs"><span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border-2 border-white bg-cyan-400" />CC</div>
        <span className="hidden font-black tracking-[-0.03em] text-slate-950 md:block">Career <span className="gradient-text">Copilot</span></span>
      </Link>

      <div className="flex min-w-0 flex-1 items-center gap-1 overflow-x-auto rounded-2xl bg-slate-100/80 p-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {links.map((link) => {
          const active = pathname === link.href;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`relative shrink-0 rounded-xl px-2.5 py-2 text-xs font-bold transition duration-200 sm:px-3 sm:py-2.5 sm:text-sm md:px-4 ${active
                ? "bg-gradient-to-r from-violet-600 to-blue-600 text-white shadow-lg shadow-violet-200"
                : "text-slate-500 hover:bg-white hover:text-slate-950 hover:shadow-sm"
                }`}
            >
              {link.label}
            </Link>
          );
        })}

      </div>
      <button
        onClick={logout}
        aria-label="Log out"
        className="shrink-0 rounded-2xl border border-slate-200 bg-white px-2.5 py-2.5 text-xs font-bold text-slate-500 shadow-sm transition hover:-translate-y-0.5 hover:border-red-200 hover:bg-red-50 hover:text-red-600 sm:px-4 sm:text-sm"
      >
        <span className="hidden sm:inline">Logout</span><span className="sm:hidden">Exit</span>
      </button>
    </nav>
  );
}
