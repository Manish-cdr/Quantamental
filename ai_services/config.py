import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional

load_dotenv()  # Load .env automatically

API_TITLE = "Lysa"
API_DESCRIPTION = "AI powered investment advisory"
API_VERSION = "1.0.0"

_raw_origins = os.getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = (
    [origin.strip() for origin in _raw_origins.split(",") if origin.strip()]
    if _raw_origins
    else []
)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b")

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

MAX_RETRY_ATTEMPTS = 3
RETRY_MIN_WAIT = 4
RETRY_MAX_WAIT = 10

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    """Get or initialize the OpenAI client"""
    global _client
    if _client is None:
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable is required. "
                "Please set it before running the application."
            )
        try:
            _client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url=OPENROUTER_BASE_URL
            )
        except Exception:
            # Fallback in case constructor signature changes
            _client = OpenAI(api_key=OPENROUTER_API_KEY)
            _client.base_url = OPENROUTER_BASE_URL

    return _client
