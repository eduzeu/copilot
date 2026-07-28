import json
from typing import Optional, Type

from google import genai
from google.genai import errors, types
from pydantic import BaseModel, ValidationError

from app.core.config import settings


MODEL = settings.ai_model


class LLMRateLimitError(RuntimeError):
    """Raised when the configured AI provider has exhausted its quota."""


class LLMProviderError(RuntimeError):
    """Raised when the AI provider is temporarily unavailable."""


def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    json_response: bool = False,
    thinking_budget: int | None = None,
) -> str:
    full_prompt = prompt

    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    if not settings.ai_key:
        raise LLMProviderError("The AI provider is not configured.")
    client = genai.Client(
        api_key=settings.ai_key,
        http_options=types.HttpOptions(timeout=settings.ai_timeout_seconds * 1000),
    )
    config = {
        "max_output_tokens": max_tokens,
        "temperature": 0.3,
    }
    if json_response:
        config["response_mime_type"] = "application/json"
        # Gemini 2.5 thinking tokens share the output budget. Resume analysis
        # needs the budget for the JSON payload itself.
        config["thinking_config"] = {"thinking_budget": 0}
    elif thinking_budget is not None:
        config["thinking_config"] = {"thinking_budget": thinking_budget}

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt,
            config=config,
        )
    except errors.ClientError as exc:
        status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if status_code == 429 or "RESOURCE_EXHAUSTED" in str(exc):
            raise LLMRateLimitError(
                "Career Coach has reached today's Gemini free-tier limit. "
                "Please try again after the quota resets."
            ) from exc
        raise LLMProviderError("The AI provider rejected the request. Please try again.") from exc
    except errors.ServerError as exc:
        raise LLMProviderError("The AI provider is temporarily unavailable. Please try again shortly.") from exc
    except TimeoutError as exc:
        raise LLMProviderError("The AI provider took too long to respond. Please try again.") from exc

    if not response.text:
        raise LLMProviderError("The AI provider returned an empty response. Please try again.")
    return response.text


def call_llm_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    schema: Type[BaseModel] | None = None,
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
    if schema is not None:
        try:
            return schema.model_validate(result).model_dump()
        except ValidationError as exc:
            raise RuntimeError("AI returned an invalid structured response. Please try again.") from exc
    return result
