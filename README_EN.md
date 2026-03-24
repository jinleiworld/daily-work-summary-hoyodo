# Daily Work Summary Skill

[![hoyodo](https://img.shields.io/badge/Based%20on-hoyodo-blue)](https://hoyodo.com)

## Introduction

This is an OpenClaw skill based on the **hoyodo** diary app, used to automatically summarize daily chat content with AI (work records) and upload to the hoyodo server.

---

## ⚠️ Prerequisites

### Must complete the following steps:

1. **Download and install hoyodo App**
   - iOS: Search "hoyodo" or "或有豆" in App Store
   - Android: Search "hoyodo" or "或有豆" in app stores

2. **Register an account**
   - Open the app and complete the registration process

3. **Get API credentials**
   - Go to App → My → Developer Settings (or API Settings)
   - Get your `appId` and `appSecret`

---

## Features

- Automatically summarize daily chat content with AI
- Extract work-related conversation records
- One-click upload to hoyodo server
- Support custom configuration

---

## Installation

### Method 1: Install via SkillHub (Recommended)

```bash
skillhub install daily-work-summary
```

### Method 2: Manual Installation

1. Download `.skill` file from [Releases](../../releases)
2. Place it in your OpenClaw skills directory: `~/.qclaw/workspace/skills/`

### Method 3: Source Installation

```bash
git clone https://github.com/your-username/daily-work-summary-skill.git
cd daily-work-summary-skill
cp -r daily-work-summary ~/.qclaw/workspace/skills/
```

---

## Configuration

Create config file:

**Path**: `~/.qclaw/daily-work-summary-config.json`

```json
{
  "appId": "your_app_id_from_hoyodo_app",
  "appSecret": "your_app_secret_from_hoyodo_app"
}
```

---

## Usage

Say to AI:

- "Summarize today's work"
- "Upload today's work summary"
- "Generate work daily report"

---

## API Information

**Endpoint**: `https://lifeapitest.zdzkpt.com/api/user/addRecommendByAppSecret`

**Method**: POST

**Request Body**:
```json
{
  "appId": "your_app_id",
  "appSecret": "your_app_secret",
  "recommand": "Work summary content",
  "userPhone": "Optional",
  "groupItemId": "Optional"
}
```

**Success Response**:
```json
{
  "code": 20000,
  "data": "New record ID"
}
```

---

## File Structure

```
daily-work-summary/
├── SKILL.md                    # Skill main document
├── scripts/
│   └── upload_summary.py       # Upload script
└── references/
    ├── api-reference.md        # API reference
    └── config-template.json    # Config template
```

---

## About hoyodo

**hoyodo (或有豆)** is an intelligent diary application that helps users record life moments and work insights.

- Website: https://hoyodo.com
- Platforms: iOS, Android

---

## License

MIT License

---

## Author

Created with ❤️ for hoyodo users

Please submit an issue if you have any questions
