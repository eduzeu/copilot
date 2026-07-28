export default function BrandMark({ compact = false }: { compact?: boolean }) {
  return (
    <span
      aria-hidden="true"
      className={`${compact ? "h-10 w-10 rounded-[14px]" : "h-11 w-11 rounded-2xl"} relative inline-flex shrink-0 items-center justify-center overflow-hidden bg-slate-950 text-white shadow-[0_12px_28px_-12px_rgba(15,23,42,.65)]`}
    >
      <span className="absolute inset-[3px] rounded-[inherit] bg-gradient-to-br from-violet-500 via-indigo-500 to-cyan-400" />
      <svg className="relative h-6 w-6" viewBox="0 0 24 24" fill="none">
        <path d="M7 7.5h6.25a3.75 3.75 0 0 1 0 7.5H11" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
        <path d="M10.5 4.75 7 7.5l3.5 2.75M13.5 13.75 17 16.5l-3.5 2.75" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  );
}
