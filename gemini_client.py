from functools import lru_cache

from google import genai
from google.genai import types

from config import require_gemini_key, settings


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    return genai.Client(api_key=require_gemini_key())


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    response_mime_type: str | None = None,
) -> str:
    config_kwargs = {
        "temperature": temperature,
    }
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction
    if response_mime_type:
        config_kwargs["response_mime_type"] = response_mime_type

    response = get_client().models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
