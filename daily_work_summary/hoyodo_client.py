"""HTTP client for the hoyodo diary server."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests

if TYPE_CHECKING:
    from .config import Config

_DIARY_PATH = "/v1/diary/entries"


class HoyodoClient:
    """Thin REST client for uploading diary entries to the hoyodo server.

    The client authenticates using a bearer token supplied via :class:`~.Config`
    and targets the ``/v1/diary/entries`` endpoint.
    """

    def __init__(self, config: "Config", session: requests.Session | None = None) -> None:
        self._config = config
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {config.hoyodo_api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def upload_entry(self, date: str, content: str, title: str | None = None) -> dict[str, Any]:
        """Create a new diary entry on the hoyodo server.

        Args:
            date: Entry date in ISO-8601 format (``"YYYY-MM-DD"``).
            content: The diary text to upload.
            title: Optional title for the entry.  Defaults to
                ``"Work Summary – <date>"`` when not provided.

        Returns:
            The JSON response body returned by the server (typically the created
            entry object).

        Raises:
            requests.HTTPError: When the server returns a 4xx or 5xx status code.
            requests.ConnectionError: When the server cannot be reached.
        """
        if title is None:
            title = f"Work Summary – {date}"

        payload: dict[str, Any] = {
            "date": date,
            "title": title,
            "content": content,
            "book_id": self._config.hoyodo_book_id,
        }

        url = f"{self._config.hoyodo_base_url}{_DIARY_PATH}"
        response = self._session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
