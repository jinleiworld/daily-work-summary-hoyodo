# daily-work-summary-hoyodo

An **OpenClaw skill** for the [hoyodo](https://hoyodo.com) diary app.  
It automatically summarises your daily chat / work-record content with AI and uploads the result as a diary entry to the hoyodo server.

---

## How it works

```
Daily chat text  ──►  AI Summarizer (OpenAI)  ──►  hoyodo diary entry
```

1. You pass the raw chat messages for a given day (stdin or Python API).  
2. The **Summarizer** calls OpenAI's Chat Completions API and produces a concise, first-person work diary entry.  
3. The **HoyodoClient** authenticates with your hoyodo server and POSTs the entry via the REST API.

---

## Requirements

* Python 3.10+
* An [OpenAI API key](https://platform.openai.com/account/api-keys)
* A hoyodo account with an API token and a running hoyodo server

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

| Variable             | Required | Default                    | Description                                        |
|----------------------|----------|----------------------------|----------------------------------------------------|
| `OPENAI_API_KEY`     | ✅        | –                          | Your OpenAI secret key                             |
| `HOYODO_API_TOKEN`   | ✅        | –                          | Bearer token for the hoyodo API                    |
| `HOYODO_BASE_URL`    | ❌        | `https://api.hoyodo.com`   | Base URL of your hoyodo server                     |
| `OPENAI_MODEL`       | ❌        | `gpt-4o`                   | OpenAI chat model to use                           |
| `OPENAI_MAX_TOKENS`  | ❌        | `800`                      | Max tokens in the AI summary                       |
| `HOYODO_BOOK_ID`     | ❌        | `default`                  | Target diary book / journal ID on hoyodo           |

---

## Usage

### Command line (stdin)

Pipe your chat content to the module and it will summarise and upload it automatically:

```bash
echo "Fixed the login bug. Attended sprint review at 3 pm. Planned next sprint." \
  | python -m daily_work_summary
```

You can also redirect from a file:

```bash
python -m daily_work_summary < today_chat.txt
```

### Python API

```python
from daily_work_summary import DailyWorkSummarySkill

skill = DailyWorkSummarySkill()

result = skill.run(
    chat_content="Fixed the login bug. Attended sprint review at 3 pm.",
    date="2024-03-15",          # defaults to today when omitted
    title="Work Summary",       # optional – a sensible default is used when omitted
)

print(result)  # JSON response from the hoyodo server
```

---

## Project structure

```
daily_work_summary/
├── __init__.py        # Public API exports
├── __main__.py        # python -m daily_work_summary entry point
├── config.py          # Configuration (reads environment variables)
├── summarizer.py      # AI summarization via OpenAI Chat Completions
├── hoyodo_client.py   # REST client for the hoyodo diary server
└── skill.py           # Orchestration – run summarize + upload in one call

tests/
├── test_config.py
├── test_hoyodo_client.py
├── test_skill.py
└── test_summarizer.py
```

---

## Running tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

---

## License

MIT – see [LICENSE](LICENSE).