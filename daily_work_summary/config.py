"""Configuration management for the daily-work-summary skill."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Holds all configuration needed to run the skill.

    Values are read from environment variables (see .env.example).
    A ``KeyError`` is raised at construction time if any required variable
    is missing so failures surface early.
    """

    openai_api_key: str = field(default_factory=lambda: os.environ["OPENAI_API_KEY"])
    openai_model: str = field(
        default_factory=lambda: os.environ.get("OPENAI_MODEL", "gpt-4o")
    )
    openai_max_tokens: int = field(
        default_factory=lambda: int(os.environ.get("OPENAI_MAX_TOKENS", "800"))
    )

    hoyodo_api_token: str = field(
        default_factory=lambda: os.environ["HOYODO_API_TOKEN"]
    )
    hoyodo_base_url: str = field(
        default_factory=lambda: os.environ.get(
            "HOYODO_BASE_URL", "https://api.hoyodo.com"
        ).rstrip("/")
    )
    hoyodo_book_id: str = field(
        default_factory=lambda: os.environ.get("HOYODO_BOOK_ID", "default")
    )
