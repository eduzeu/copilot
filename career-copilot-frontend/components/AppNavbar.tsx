"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/applications", label: "Applications" },
  { href: "/resumes", label: "AI Tools" },
];

export default function AppNavbar() {
  const pathname = usePathname();
  const router = useRouter();

  function logout() {
    localStorage.removeItem("token");
    router.push("/auth/login");
  }

  return (
    <nav className="mb-8 flex items-center justify-between rounded-3xl border border-slate-200 bg-white/80 px-6 py-4 shadow-xl backdrop-blur-xl">
      <Link href="/dashboard" className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500 shadow-lg shadow-blue-200" />
        <span className="font-black text-slate-950">Career Copilot</span>
      </Link>

      <div className="flex items-center gap-2">
        {links.map((link) => {
          const active = pathname === link.href;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-full px-4 py-2 text-sm font-bold transition ${active
                ? "bg-gradient-to-r from-violet-600 to-blue-600 text-white shadow-lg shadow-blue-200"
                : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
                }`}
            >
              {link.label}
            </Link>
          );
        })}

        <button
          onClick={logout}
          className="ml-2 rounded-full border border-slate-200 px-4 py-2 text-sm font-bold text-slate-600 hover:bg-red-50 hover:text-red-600"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}