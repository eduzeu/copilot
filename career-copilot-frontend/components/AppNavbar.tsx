"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { apiFetch } from "../lib/api";
import BrandMark from "./BrandMark";

const links = [
  { href: "/dashboard", label: "Overview", icon: "⌂" },
  { href: "/applications", label: "Applications", icon: "↗" },
  { href: "/resumes", label: "AI tools", icon: "✦" },
  { href: "/coach", label: "Coach", icon: "◌" },
  { href: "/profile", label: "Profile", icon: "◎" },
];

export default function AppNavbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const updateNavbar = () => setScrolled(window.scrollY > 24);
    updateNavbar();
    window.addEventListener("scroll", updateNavbar, { passive: true });
    return () => window.removeEventListener("scroll", updateNavbar);
  }, []);

  async function logout() {
    await apiFetch<void>("/auth/logout", { method: "POST", redirectOnUnauthorized: false }).catch(() => undefined);
    localStorage.removeItem("token");
    router.push("/auth/login");
  }

  return (
    <nav
      className={`surface-card-strong sticky top-2 z-40 mb-7 flex items-center gap-2 overflow-hidden rounded-[1.35rem] p-2 transition-[background-color,border-color,box-shadow,backdrop-filter] duration-300 sm:top-4 sm:mb-10 sm:gap-4 sm:p-2.5 ${scrolled ? "navbar-scrolled" : ""}`}
    >
      <Link href="/dashboard" className="group flex shrink-0 items-center gap-3 pr-1 md:pr-3">
        <BrandMark compact />
        <span className="hidden font-black tracking-[-0.03em] text-slate-950 md:block">Career <span className="gradient-text">Copilot</span></span>
      </Link>

      <div className="flex min-w-0 flex-1 items-center justify-start gap-1 overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden md:justify-center">
        {links.map((link) => {
          const active = pathname === link.href;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`relative flex shrink-0 items-center gap-1.5 rounded-xl px-2.5 py-2 text-xs font-bold transition duration-200 sm:px-3 sm:py-2.5 sm:text-sm md:px-4 ${active
                ? "bg-slate-950 text-white shadow-lg shadow-slate-300"
                : "text-slate-500 hover:bg-slate-100 hover:text-slate-950"
                }`}
            >
              <span className={active ? "text-cyan-300" : "text-slate-400"}>{link.icon}</span>
              {link.label}
            </Link>
          );
        })}

      </div>
      <button
        onClick={logout}
        aria-label="Log out"
        className="shrink-0 rounded-xl border border-slate-200 bg-white px-2.5 py-2.5 text-xs font-bold text-slate-500 transition hover:border-red-200 hover:bg-red-50 hover:text-red-600 sm:px-4 sm:text-sm"
      >
        <span className="hidden sm:inline">Logout</span><span className="sm:hidden">Exit</span>
      </button>
    </nav>
  );
}
