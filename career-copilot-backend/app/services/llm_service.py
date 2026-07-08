import json
from typing import Optional

from google import genai

from app.core.config import settings


client = genai.Client(api_key=settings.AI_KEY)

MODEL = "gemini-2.5-flash"


def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
) -> str:
    full_prompt = prompt

    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    response = client.models.generate_content(
        model=MODEL,
        contents=full_prompt,
        config={
            "max_output_tokens": max_tokens,
            "temperature": 0.3,
        },
    )

    return response.text


def call_llm_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
):
    raw = call_llm(prompt, system_prompt, max_tokens).strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw