"""Main OpenClaw skill: summarize daily chat and upload to hoyodo."""

from __future__ import annotations

import sys
from datetime import date as _date
from typing import TYPE_CHECKING

from .config import Config
from .hoyodo_client import HoyodoClient
from .summarizer import Summarizer

if TYPE_CHECKING:
    pass


class DailyWorkSummarySkill:
    """OpenClaw skill that summarizes daily chat content and posts it to hoyodo.

    Typical usage::

        skill = DailyWorkSummarySkill()
        result = skill.run(chat_content="...", date="2024-03-15")
    """

    def __init__(
        self,
        config: Config | None = None,
        summarizer: Summarizer | None = None,
        hoyodo_client: HoyodoClient | None = None,
    ) -> None:
        if summarizer is None or hoyodo_client is None:
            # Only build Config (which reads env vars) when we actually need it.
            _config = config or Config()
            self._summarizer = summarizer or Summarizer(_config)
            self._hoyodo_client = hoyodo_client or HoyodoClient(_config)
        else:
            self._summarizer = summarizer
            self._hoyodo_client = hoyodo_client

    def run(
        self,
        chat_content: str,
        date: str | None = None,
        title: str | None = None,
    ) -> dict:
        """Summarize *chat_content* with AI and upload the result to hoyodo.

        Args:
            chat_content: Raw chat / conversation text to summarize.
            date: ISO-8601 date string (``"YYYY-MM-DD"``).  Defaults to today.
            title: Optional diary entry title.  A sensible default is used when
                not provided.

        Returns:
            The response payload returned by the hoyodo server after creating
            the diary entry.

        Raises:
            ValueError: If *chat_content* is empty.
            openai.OpenAIError: If the AI summarization step fails.
            requests.HTTPError: If the hoyodo upload step fails.
        """
        if date is None:
            date = _date.today().isoformat()

        summary = self._summarizer.summarize(chat_content, date)
        result = self._hoyodo_client.upload_entry(date, summary, title)
        return result


def main() -> None:
    """Command-line entry point.

    Reads chat content from stdin and prints the server response to stdout.

    Usage::

        echo "Today I fixed the login bug..." | python -m daily_work_summary
    """
    chat_content = sys.stdin.read()
    if not chat_content.strip():
        print("Error: no chat content provided via stdin.", file=sys.stderr)
        sys.exit(1)

    skill = DailyWorkSummarySkill()
    result = skill.run(chat_content)
    print(f"Diary entry created successfully: {result}")


if __name__ == "__main__":
    main()
