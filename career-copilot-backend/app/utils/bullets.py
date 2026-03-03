import re
from typing import List 

BULLET_CHARS = r"[\-\*\u2022\u25E6\u2219\u2043\u00B7]"    # Common bullet characters

def extract_bullets(resume_text: str) -> List[str]: 
  '''
  Heuristic bullet extractor: 
  - Prefer lines that start with bullet characters
  -Also capture "Action verb..." lines if they look like bullets
  '''

  lines = [ln.strip() for ln in resume_text.splitlines() if ln.strip()]
  lines = [ln for ln in lines if ln]

  bullets: List[str] = []

  bullet_re = re.compile(rf"^({BULLET_CHARS})\s+(.*)")

  for ln in lines: 
    m = bullet_re.match(ln)
    if m: 
      text = m.group(1).strip() 
      if len(text) >= 10: 
        bullets.append(text)
      continue 

     # fallback: treat short “sentence-like” lines as bullets if they look like accomplishments
    if 20 <= len(ln) <= 220 and ln[0].isalpha() and (ln.endswith(".") or "," in ln or "%" in ln):
        bullets.append(ln)


    seen = set() 
    out = []
    for b in bullets: 
      key = b.lower()
      if key not in seen: 
        seen.add(key)
        out.append(b)
    
    return out[:30]
  
