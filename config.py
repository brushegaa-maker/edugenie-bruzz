import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    use_local_explainer: bool = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"
    local_explainer_model: str = os.getenv(
        "LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    ).strip()
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))


settings = Settings()


def require_gemini_key() -> str:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env "
            "and add your Google AI Studio API key."
        )
    return settings.gemini_api_key
