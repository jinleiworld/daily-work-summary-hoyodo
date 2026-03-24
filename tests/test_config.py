"""Tests for Config."""

import os
import pytest

from daily_work_summary.config import Config


def test_config_reads_required_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("HOYODO_API_TOKEN", "hoyodo-token")
    monkeypatch.delenv("HOYODO_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_MAX_TOKENS", raising=False)
    monkeypatch.delenv("HOYODO_BOOK_ID", raising=False)

    cfg = Config()
    assert cfg.openai_api_key == "sk-test-key"
    assert cfg.hoyodo_api_token == "hoyodo-token"
    assert cfg.hoyodo_base_url == "https://api.hoyodo.com"
    assert cfg.openai_model == "gpt-4o"
    assert cfg.openai_max_tokens == 800
    assert cfg.hoyodo_book_id == "default"


def test_config_reads_optional_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("HOYODO_API_TOKEN", "hoyodo-token")
    monkeypatch.setenv("HOYODO_BASE_URL", "https://custom.hoyodo.example.com/")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("OPENAI_MAX_TOKENS", "500")
    monkeypatch.setenv("HOYODO_BOOK_ID", "work-journal")

    cfg = Config()
    assert cfg.hoyodo_base_url == "https://custom.hoyodo.example.com"  # trailing slash stripped
    assert cfg.openai_model == "gpt-3.5-turbo"
    assert cfg.openai_max_tokens == 500
    assert cfg.hoyodo_book_id == "work-journal"


def test_config_raises_when_openai_key_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("HOYODO_API_TOKEN", "hoyodo-token")

    with pytest.raises(KeyError):
        Config()


def test_config_raises_when_hoyodo_token_missing(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.delenv("HOYODO_API_TOKEN", raising=False)

    with pytest.raises(KeyError):
        Config()
