"""Tests for DailyWorkSummarySkill."""

import pytest
from unittest.mock import MagicMock, patch

from daily_work_summary.skill import DailyWorkSummarySkill


@pytest.fixture
def mock_summarizer():
    summarizer = MagicMock()
    summarizer.summarize.return_value = "AI-generated summary of the day."
    return summarizer


@pytest.fixture
def mock_hoyodo_client():
    client = MagicMock()
    client.upload_entry.return_value = {"id": "entry-001", "date": "2024-03-15"}
    return client


def test_run_summarizes_and_uploads(mock_summarizer, mock_hoyodo_client):
    skill = DailyWorkSummarySkill(
        summarizer=mock_summarizer,
        hoyodo_client=mock_hoyodo_client,
    )
    result = skill.run("Chat content here", date="2024-03-15")

    mock_summarizer.summarize.assert_called_once_with("Chat content here", "2024-03-15")
    mock_hoyodo_client.upload_entry.assert_called_once_with(
        "2024-03-15", "AI-generated summary of the day.", None
    )
    assert result == {"id": "entry-001", "date": "2024-03-15"}


def test_run_defaults_to_today(mock_summarizer, mock_hoyodo_client):
    skill = DailyWorkSummarySkill(
        summarizer=mock_summarizer,
        hoyodo_client=mock_hoyodo_client,
    )
    with patch("daily_work_summary.skill._date") as mock_date:
        mock_date.today.return_value.isoformat.return_value = "2024-03-15"
        skill.run("Some chat")

    call_date = mock_summarizer.summarize.call_args.args[1]
    assert call_date == "2024-03-15"


def test_run_passes_custom_title(mock_summarizer, mock_hoyodo_client):
    skill = DailyWorkSummarySkill(
        summarizer=mock_summarizer,
        hoyodo_client=mock_hoyodo_client,
    )
    skill.run("Chat content", date="2024-03-15", title="My Custom Title")

    mock_hoyodo_client.upload_entry.assert_called_once_with(
        "2024-03-15", "AI-generated summary of the day.", "My Custom Title"
    )


def test_run_raises_on_empty_chat_content(mock_summarizer, mock_hoyodo_client):
    mock_summarizer.summarize.side_effect = ValueError("chat_content must not be empty")

    skill = DailyWorkSummarySkill(
        summarizer=mock_summarizer,
        hoyodo_client=mock_hoyodo_client,
    )

    with pytest.raises(ValueError, match="chat_content must not be empty"):
        skill.run("", date="2024-03-15")

    mock_hoyodo_client.upload_entry.assert_not_called()


def test_run_propagates_upload_error(mock_summarizer, mock_hoyodo_client):
    import requests
    mock_hoyodo_client.upload_entry.side_effect = requests.HTTPError("401 Unauthorized")

    skill = DailyWorkSummarySkill(
        summarizer=mock_summarizer,
        hoyodo_client=mock_hoyodo_client,
    )

    with pytest.raises(requests.HTTPError):
        skill.run("Some chat", date="2024-03-15")
