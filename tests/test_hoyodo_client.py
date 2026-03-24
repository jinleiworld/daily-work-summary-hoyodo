"""Tests for HoyodoClient."""

import pytest
import responses as resp_lib
import requests

from daily_work_summary.config import Config
from daily_work_summary.hoyodo_client import HoyodoClient, _DIARY_PATH


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("HOYODO_API_TOKEN", "hoyodo-test-token")
    monkeypatch.setenv("HOYODO_BASE_URL", "https://api.hoyodo.test")
    monkeypatch.setenv("HOYODO_BOOK_ID", "work-journal")
    return Config()


@resp_lib.activate
def test_upload_entry_success(config):
    expected_url = f"https://api.hoyodo.test{_DIARY_PATH}"
    resp_lib.add(
        resp_lib.POST,
        expected_url,
        json={"id": "entry-123", "date": "2024-03-15", "title": "Work Summary – 2024-03-15"},
        status=201,
    )

    client = HoyodoClient(config)
    result = client.upload_entry("2024-03-15", "Fixed the auth bug today.")

    assert result["id"] == "entry-123"
    assert len(resp_lib.calls) == 1
    call = resp_lib.calls[0]
    assert call.request.headers["Authorization"] == "Bearer hoyodo-test-token"


@resp_lib.activate
def test_upload_entry_sends_correct_payload(config):
    expected_url = f"https://api.hoyodo.test{_DIARY_PATH}"
    resp_lib.add(resp_lib.POST, expected_url, json={"id": "entry-456"}, status=201)

    client = HoyodoClient(config)
    client.upload_entry("2024-03-15", "Completed sprint planning.", "Sprint Planning")

    import json
    body = json.loads(resp_lib.calls[0].request.body)
    assert body["date"] == "2024-03-15"
    assert body["content"] == "Completed sprint planning."
    assert body["title"] == "Sprint Planning"
    assert body["book_id"] == "work-journal"


@resp_lib.activate
def test_upload_entry_uses_default_title(config):
    expected_url = f"https://api.hoyodo.test{_DIARY_PATH}"
    resp_lib.add(resp_lib.POST, expected_url, json={"id": "entry-789"}, status=201)

    client = HoyodoClient(config)
    client.upload_entry("2024-03-15", "Some content")

    import json
    body = json.loads(resp_lib.calls[0].request.body)
    assert body["title"] == "Work Summary – 2024-03-15"


@resp_lib.activate
def test_upload_entry_raises_on_http_error(config):
    expected_url = f"https://api.hoyodo.test{_DIARY_PATH}"
    resp_lib.add(resp_lib.POST, expected_url, json={"error": "Unauthorized"}, status=401)

    client = HoyodoClient(config)
    with pytest.raises(requests.HTTPError):
        client.upload_entry("2024-03-15", "Some content")


@resp_lib.activate
def test_upload_entry_raises_on_server_error(config):
    expected_url = f"https://api.hoyodo.test{_DIARY_PATH}"
    resp_lib.add(resp_lib.POST, expected_url, json={"error": "Internal server error"}, status=500)

    client = HoyodoClient(config)
    with pytest.raises(requests.HTTPError):
        client.upload_entry("2024-03-15", "Some content")
