"""Configuration shared by the CLI, analyzer, and TUI."""
import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "http://127.0.0.1:1976/v1"
DEFAULT_MODEL = "system"
DEFAULT_API_KEY = "not-needed"


def get_model_config(*, model=None, base_url=None, api_key=None):
    """Return normalized provider settings with explicit arguments taking precedence."""
    configured_base_url = base_url or os.getenv("WHATSURNAME_BASE_URL", DEFAULT_BASE_URL)
    configured_model = model or os.getenv("WHATSURNAME_MODEL", DEFAULT_MODEL)
    configured_api_key = api_key or os.getenv("WHATSURNAME_API_KEY", DEFAULT_API_KEY)
    return {
        "base_url": configured_base_url.rstrip("/"),
        "model": configured_model,
        "api_key": configured_api_key,
    }
