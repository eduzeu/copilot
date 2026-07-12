import json
from typing import Optional

from google import genai

from app.core.config import settings


MODEL = "gemini-2.5-flash"


def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    json_response: bool = False,
) -> str:
    full_prompt = prompt

    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    if not settings.ai_key:
        raise RuntimeError("AI_KEY is not configured")
    client = genai.Client(api_key=settings.ai_key)
    config = {
        "max_output_tokens": max_tokens,
        "temperature": 0.3,
    }
    if json_response:
        config["response_mime_type"] = "application/json"
        # Gemini 2.5 thinking tokens share the output budget. Resume analysis
        # needs the budget for the JSON payload itself.
        config["thinking_config"] = {"thinking_budget": 0}

    response = client.models.generate_content(
        model=MODEL,
        contents=full_prompt,
        config=config,
    )

    return response.text


def call_llm_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
):
    raw = call_llm(
        prompt,
        system_prompt,
        max(max_tokens, 8192),
        json_response=True,
    ).strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("AI returned an incomplete response. Please try again.") from exc
    if not isinstance(result, dict):
        raise RuntimeError("AI returned an unexpected response. Please try again.")
    return result
