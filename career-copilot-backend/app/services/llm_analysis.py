import re

def _keywords_from_jd(jd: str) -> set[str]:
    # tiny keyword heuristic: keep tech-ish tokens
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\+\#\.\-]{1,}", jd.lower())
    stop = {"and","or","the","a","an","to","of","in","for","with","on","as","is","are","be","you","we","our"}
    return {t for t in tokens if t not in stop and len(t) >= 3}

def analyze_bullet_with_stub(bullet: str, job_description: str) -> dict:
    jd_keys = _keywords_from_jd(job_description)
    b = bullet.lower()

    hits = [k for k in jd_keys if k in b]
    missing = sorted(list(jd_keys - set(hits)))[:10]

    # simple score: hits relative to jd keywords
    score = int(min(100, (len(hits) / max(1, min(25, len(jd_keys)))) * 100))

    feedback = "Good alignment with the job description." if score >= 60 else \
               "This bullet is vague or missing key skills from the job description."

    rewrite_ats = bullet
    if score < 60 and missing:
        rewrite_ats = f"{bullet} (Include: {', '.join(missing[:3])})"

    rewrite_strong = bullet
    if score < 80:
        rewrite_strong = f"{bullet} — quantified impact and relevant tools."

    return {
        "relevance_score": score,
        "feedback": feedback,
        "rewrite_ats": rewrite_ats,
        "rewrite_strong": rewrite_strong,
        "missing_keywords": missing,
    }