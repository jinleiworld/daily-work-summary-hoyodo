"""Tests for Summarizer."""

import pytest
from unittest.mock import MagicMock, patch

from daily_work_summary.config import Config
from daily_work_summary.summarizer import Summarizer


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("HOYODO_API_TOKEN", "hoyodo-token")
    return Config()


def _make_openai_response(content: str):
    """Build a minimal mock that looks like an OpenAI ChatCompletion response."""
    choice = MagicMock()
    choice.message.content = content
    response = MagicMock()
    response.choices = [choice]
    return response


def test_summarize_returns_summary(config):
    fake_summary = "Today I fixed the authentication bug and attended the sprint review."

    with patch("daily_work_summary.summarizer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = _make_openai_response(fake_summary)

        summarizer = Summarizer(config)
        result = summarizer.summarize("Fixed auth bug. Sprint review at 3pm.", "2024-03-15")

    assert result == fake_summary


def test_summarize_strips_whitespace_from_response(config):
    with patch("daily_work_summary.summarizer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = _make_openai_response(
            "  Summary with surrounding whitespace.  "
        )

        summarizer = Summarizer(config)
        result = summarizer.summarize("Some chat", "2024-03-15")

    assert result == "Summary with surrounding whitespace."


def test_summarize_raises_on_empty_content(config):
    with patch("daily_work_summary.summarizer.OpenAI"):
        summarizer = Summarizer(config)

        with pytest.raises(ValueError, match="chat_content must not be empty"):
            summarizer.summarize("", "2024-03-15")

        with pytest.raises(ValueError, match="chat_content must not be empty"):
            summarizer.summarize("   ", "2024-03-15")


def test_summarize_raises_on_none_openai_response(config):
    with patch("daily_work_summary.summarizer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = _make_openai_response(None)

        summarizer = Summarizer(config)

        with pytest.raises(RuntimeError, match="OpenAI returned an empty response"):
            summarizer.summarize("Some chat", "2024-03-15")


def test_summarize_passes_correct_model_and_tokens(config):
    with patch("daily_work_summary.summarizer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = _make_openai_response("ok")

        summarizer = Summarizer(config)
        summarizer.summarize("chat content", "2024-03-15")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == config.openai_model
        assert call_kwargs["max_tokens"] == config.openai_max_tokens


def test_summarize_includes_date_and_chat_in_user_message(config):
    with patch("daily_work_summary.summarizer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = _make_openai_response("ok")

        summarizer = Summarizer(config)
        summarizer.summarize("Finished the report", "2024-03-15")

        messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
        user_msg = next(m for m in messages if m["role"] == "user")
        assert "2024-03-15" in user_msg["content"]
        assert "Finished the report" in user_msg["content"]
