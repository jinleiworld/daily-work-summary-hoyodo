"""AI summarization of daily chat / work records using the OpenAI API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from openai import OpenAI

if TYPE_CHECKING:
    from .config import Config

_SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes daily work chat records. "
    "Given the raw chat content for one day, produce a concise, well-structured "
    "diary entry written in the first person. "
    "Highlight key accomplishments, decisions made, blockers encountered, and next steps. "
    "Write in clear, professional language. "
    "Return plain text only – no markdown formatting."
)


class Summarizer:
    """Summarizes chat content into a diary entry using an OpenAI chat model."""

    def __init__(self, config: "Config") -> None:
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)

    def summarize(self, chat_content: str, date: str) -> str:
        """Return an AI-generated summary of *chat_content* for the given *date*.

        Args:
            chat_content: Raw text of the chat messages for the day.
            date: The date these messages belong to (ISO-8601, e.g. ``"2024-03-15"``).

        Returns:
            A plain-text diary entry summarizing the day's work.

        Raises:
            openai.OpenAIError: If the API call fails.
            ValueError: If *chat_content* is empty.
        """
        if not chat_content or not chat_content.strip():
            raise ValueError("chat_content must not be empty")

        user_message = (
            f"Date: {date}\n\n"
            f"Chat content:\n{chat_content.strip()}"
        )

        response = self._client.chat.completions.create(
            model=self._config.openai_model,
            max_tokens=self._config.openai_max_tokens,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )

        summary = response.choices[0].message.content
        if summary is None:
            raise RuntimeError("OpenAI returned an empty response")
        return summary.strip()
