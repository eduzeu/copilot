import re

BULLET_CHARS = r"[\-\*\u2022\u25E6\u2219\u2043\u00B7]"


def extract_bullets(resume_text: str) -> list[str]:
    """Extract and de-duplicate likely accomplishment bullets."""
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    bullet_re = re.compile(rf"^({BULLET_CHARS})\s+(.*)")
    bullets: list[str] = []

    for line in lines:
        match = bullet_re.match(line)
        if match:
            text = match.group(2).strip()
            if len(text) >= 10:
                bullets.append(text)
            continue
        if 20 <= len(line) <= 220 and line[0].isalpha() and (
            line.endswith(".") or "," in line or "%" in line
        ):
            bullets.append(line)

    seen: set[str] = set()
    unique: list[str] = []
    for bullet in bullets:
        key = bullet.casefold()
        if key not in seen:
            seen.add(key)
            unique.append(bullet)
    return unique[:30]
