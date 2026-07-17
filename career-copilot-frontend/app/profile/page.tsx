"use client";

import { useEffect, useState } from "react";
import AppNavbar from "../../components/AppNavbar";
import { apiFetch } from "../../lib/api";

type Experience = {
  category: string; title: string; organization: string; start_date: string;
  end_date: string; description: string; skills: string[]; url: string;
};

type Profile = {
  status: "college" | "recent_graduate" | "professional";
  school: string; degree: string; major: string; current_year: string;
  graduation_year: number | null; current_role: string; years_experience: number | null;
  current_industry: string; experiences: Experience[]; technical_skills: string[];
  dsa_level: string; system_design_level: string; behavioral_confidence: string;
  preferred_language: string; improvement_areas: string[]; certifications: string[];
  target_roles: string[]; target_companies: string[]; target_industries: string[];
  target_locations: string[]; position_types: string[]; workplace_preferences: string[];
  application_timeline: string; primary_goal: string; salary_expectations: string;
  completeness?: number;
};

const emptyProfile: Profile = {
  status: "college", school: "", degree: "", major: "", current_year: "",
  graduation_year: null, current_role: "", years_experience: null, current_industry: "",
  experiences: [], technical_skills: [], dsa_level: "not_started",
  system_design_level: "not_started", behavioral_confidence: "not_started",
  preferred_language: "", improvement_areas: [], certifications: [], target_roles: [],
  target_companies: [], target_industries: [], target_locations: [], position_types: [],
  workplace_preferences: [], application_timeline: "", primary_goal: "", salary_expectations: "",
};

const categories = [
  ["internship", "Internship"], ["professional", "Professional experience"],
  ["project", "Personal or academic project"], ["hackathon", "Hackathon or competition"],
  ["research_open_source_volunteering", "Research, open source, or volunteering (optional)"],
  ["club_organization", "Club, organization, or leadership (optional)"],
];

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile>(emptyProfile);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiFetch<Profile>("/profile/").then((data) => setProfile({ ...emptyProfile, ...data }))
      .catch((e) => setMessage(e.message)).finally(() => setLoading(false));
  }, []);

  function field<K extends keyof Profile>(key: K, value: Profile[K]) {
    setProfile((current) => ({ ...current, [key]: value }));
  }

  async function save() {
    setSaving(true); setMessage("");
    try {
      const saved = await apiFetch<Profile>("/profile/", {
        method: "PUT", body: JSON.stringify(profile),
      });
      setProfile({ ...emptyProfile, ...saved });
      setMessage("Career profile saved.");
    } catch (e: any) { setMessage(e.message); }
    finally { setSaving(false); }
  }

  function addExperience() {
    field("experiences", [...profile.experiences, {
      category: "internship", title: "", organization: "", start_date: "", end_date: "",
      description: "", skills: [], url: "",
    }]);
  }

  function updateExperience(index: number, changes: Partial<Experience>) {
    field("experiences", profile.experiences.map((item, i) => i === index ? { ...item, ...changes } : item));
  }

  if (loading) return <main className="p-10 text-slate-600">Loading your career profile...</main>;

  return (
    <main className="app-page text-slate-950">
      <div className="app-container"><AppNavbar />
        <div className="mb-8 flex flex-wrap items-end justify-between gap-5">
          <div><p className="eyebrow">Persistent AI context</p>
            <h1 className="mt-3 text-4xl font-black tracking-[-0.04em] sm:text-5xl">Your career, <span className="gradient-text">in context.</span></h1>
            <p className="mt-2 max-w-2xl text-slate-600">Tell Career Copilot where you are and where you want to go. You can update this anytime.</p>
          </div>
          <div className="w-full rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:min-w-64 sm:w-auto">
            <div className="flex justify-between text-sm font-bold"><span>Profile completeness</span><span>{profile.completeness || 0}%</span></div>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full bg-gradient-to-r from-violet-600 to-blue-600" style={{ width: `${profile.completeness || 0}%` }} /></div>
          </div>
        </div>

        <div className="space-y-6">
          <Section title="1. Career stage" subtitle="Your current professional context.">
            <Select label="Current status" value={profile.status} onChange={(v) => field("status", v as Profile["status"])} options={[["college", "College student"], ["recent_graduate", "Recent graduate"], ["professional", "Professional"]]} />
            {profile.status === "college" || profile.status === "recent_graduate" ? <>
              <Text label="School" value={profile.school} onChange={(v) => field("school", v)} />
              <Text label="Degree" value={profile.degree} onChange={(v) => field("degree", v)} placeholder="B.S." />
              <Text label="Major" value={profile.major} onChange={(v) => field("major", v)} />
              <Text label="Current year" value={profile.current_year} onChange={(v) => field("current_year", v)} placeholder="Junior" />
              <NumberField label="Graduation year" value={profile.graduation_year} onChange={(v) => field("graduation_year", v)} />
            </> : <>
              <Text label="Current or recent role" value={profile.current_role} onChange={(v) => field("current_role", v)} />
              <NumberField label="Years of experience" value={profile.years_experience} onChange={(v) => field("years_experience", v)} />
              <Text label="Current industry" value={profile.current_industry} onChange={(v) => field("current_industry", v)} />
            </>}
          </Section>

          <Section title="2. Experience" subtitle="Add internships, work, projects, hackathons, and optional activities.">
            <div className="col-span-full space-y-4">
              {profile.experiences.map((item, index) => <div key={index} className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  <Select label="Type" value={item.category} onChange={(v) => updateExperience(index, { category: v })} options={categories} />
                  <Text label="Title" value={item.title} onChange={(v) => updateExperience(index, { title: v })} />
                  <Text label="Organization" value={item.organization} onChange={(v) => updateExperience(index, { organization: v })} />
                  <Text label="Start date" value={item.start_date} onChange={(v) => updateExperience(index, { start_date: v })} placeholder="May 2025" />
                  <Text label="End date" value={item.end_date} onChange={(v) => updateExperience(index, { end_date: v })} placeholder="August 2025 or Present" />
                  <Text label="URL (optional)" value={item.url} onChange={(v) => updateExperience(index, { url: v })} />
                  <ListField label="Skills (optional)" value={item.skills} onChange={(v) => updateExperience(index, { skills: v })} />
                  <Text label="Description (optional)" value={item.description} onChange={(v) => updateExperience(index, { description: v })} />
                </div>
                <button onClick={() => field("experiences", profile.experiences.filter((_, i) => i !== index))} className="mt-4 text-sm font-bold text-red-600">Remove entry</button>
              </div>)}
              <button onClick={addExperience} className="rounded-xl border border-violet-200 bg-violet-50 px-5 py-3 font-bold text-violet-700">+ Add experience</button>
            </div>
          </Section>

          <Section title="3. Skills and preparation" subtitle="Self-assessments give the coach a useful starting point.">
            <ListField label="Technical skills" value={profile.technical_skills} onChange={(v) => field("technical_skills", v)} />
            <Select label="DSA level" value={profile.dsa_level} onChange={(v) => field("dsa_level", v)} options={levelOptions} />
            <Select label="System design level" value={profile.system_design_level} onChange={(v) => field("system_design_level", v)} options={levelOptions} />
            <Select label="Behavioral interview confidence" value={profile.behavioral_confidence} onChange={(v) => field("behavioral_confidence", v)} options={levelOptions} />
            <Text label="Preferred programming language" value={profile.preferred_language} onChange={(v) => field("preferred_language", v)} />
            <ListField label="Areas to improve" value={profile.improvement_areas} onChange={(v) => field("improvement_areas", v)} />
            <ListField label="Certifications (optional)" value={profile.certifications} onChange={(v) => field("certifications", v)} />
          </Section>

          <Section title="4. Career targets" subtitle="The coach uses these priorities to make its advice relevant.">
            <ListField label="Target roles" value={profile.target_roles} onChange={(v) => field("target_roles", v)} />
            <ListField label="Target companies" value={profile.target_companies} onChange={(v) => field("target_companies", v)} />
            <ListField label="Target industries" value={profile.target_industries} onChange={(v) => field("target_industries", v)} placeholder="Tech, fintech, government" />
            <ListField label="Target locations" value={profile.target_locations} onChange={(v) => field("target_locations", v)} />
            <ListField label="Position types" value={profile.position_types} onChange={(v) => field("position_types", v)} placeholder="Internship, new grad" />
            <ListField label="Workplace preferences" value={profile.workplace_preferences} onChange={(v) => field("workplace_preferences", v)} placeholder="Remote, hybrid, on-site" />
            <Text label="Application timeline" value={profile.application_timeline} onChange={(v) => field("application_timeline", v)} />
            <Text label="Primary career goal" value={profile.primary_goal} onChange={(v) => field("primary_goal", v)} />
            <Text label="Salary expectations (optional)" value={profile.salary_expectations} onChange={(v) => field("salary_expectations", v)} />
          </Section>
        </div>
        <div className="sticky bottom-2 mt-6 flex flex-col items-stretch gap-3 rounded-2xl border border-slate-200 bg-white/90 p-3 shadow-xl backdrop-blur sm:bottom-4 sm:flex-row sm:items-center sm:justify-end sm:gap-4 sm:p-4">
          {message && <p className="mr-auto text-sm font-semibold text-slate-600">{message}</p>}
          <button onClick={save} disabled={saving} className="rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 px-7 py-3 font-bold text-white disabled:opacity-50">{saving ? "Saving..." : "Save profile"}</button>
        </div>
      </div>
    </main>
  );
}

const levelOptions = [["not_started", "Not started"], ["beginner", "Beginner"], ["intermediate", "Intermediate"], ["advanced", "Advanced"]];
const split = (value: string) => value.split(",").map((x) => x.trim()).filter(Boolean);

function Section({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) { return <section className="surface-card rounded-3xl p-6 md:p-7"><h2 className="text-2xl font-black tracking-tight">{title}</h2><p className="mt-1 text-sm text-slate-500">{subtitle}</p><div className="mt-6 grid gap-5 md:grid-cols-2 lg:grid-cols-3">{children}</div></section>; }
function Text({ label, value, onChange, placeholder = "" }: { label: string; value: string; onChange: (v: string) => void; placeholder?: string }) { return <label className="block text-sm font-bold text-slate-700">{label}<input value={value || ""} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className="field-control mt-2 font-normal" /></label>; }
function NumberField({ label, value, onChange }: { label: string; value: number | null; onChange: (v: number | null) => void }) { return <label className="block text-sm font-bold text-slate-700">{label}<input type="number" value={value ?? ""} onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)} className="field-control mt-2 font-normal" /></label>; }
function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[][] }) { return <label className="block text-sm font-bold text-slate-700">{label}<select value={value} onChange={(e) => onChange(e.target.value)} className="field-control mt-2 font-normal">{options.map(([v, n]) => <option key={v} value={v}>{n}</option>)}</select></label>; }
function ListField({ label, value, onChange, placeholder = "Comma-separated" }: { label: string; value: string[]; onChange: (v: string[]) => void; placeholder?: string }) {
  const [draft, setDraft] = useState(() => (value || []).join(", "));

  function update(raw: string) {
    setDraft(raw);
    onChange(split(raw));
  }

  return <label className="block text-sm font-bold text-slate-700">{label} <span className="font-medium text-slate-400">· comma separated</span><input value={draft} onChange={(e) => update(e.target.value)} onBlur={() => setDraft((current) => split(current).join(", "))} placeholder={placeholder} className="field-control mt-2 font-normal" /></label>;
}
