# Daily Work Summary Skill / 每日工作总结技能

[![hoyodo](https://img.shields.io/badge/基于-或有豆(hoyodo)-blue)](https://hoyodo.com)

## 简介 / Introduction

这是一个基于 **或有豆 (hoyodo)** 日记 App 的 OpenClaw 技能，用于自动总结当天与 AI 的聊天内容（工作记录），并上传到或有豆服务器。

This is an OpenClaw skill based on the **hoyodo** diary app, used to automatically summarize daily chat content with AI (work records) and upload to the hoyodo server.

---

## ⚠️ 前置要求 / Prerequisites

### 必须完成以下步骤 / Must complete the following steps:

1. **下载并安装或有豆 App**
   - iOS: App Store 搜索 "或有豆" 或 "hoyodo"

2. **注册账号**
   - 打开 App 完成注册流程

3. **获取 API 凭证**
   - 进入 App → 我的 → 开发者设置（或 API 设置）
   - 获取 `appId` 和 `appSecret`

---

## 功能 / Features

- 自动总结当天与 AI 的聊天内容
- 提取工作相关的对话记录
- 一键上传到或有豆服务器
- 支持自定义配置

---

## 安装 / Installation

### 方法一：通过 SkillHub 安装（推荐）/ Method 1: Install via SkillHub (Recommended)

```bash
skillhub install daily-work-summary
```

### 方法二：手动安装 / Method 2: Manual Installation

1. 从 [Releases](../../releases) 下载 `.skill` 文件
2. 放到你的 OpenClaw skills 目录：`~/.qclaw/workspace/skills/`

### 方法三：源码安装 / Method 3: Source Installation

```bash
git clone https://github.com/你的用户名/daily-work-summary-skill.git
cd daily-work-summary-skill
cp -r daily-work-summary ~/.qclaw/workspace/skills/
```

---

## 配置 / Configuration

创建配置文件 / Create config file:

**路径 / Path**: `~/.qclaw/daily-work-summary-config.json`

```json
{
  "appId": "从或有豆 App 获取的 appId",
  "appSecret": "从或有豆 App 获取的 appSecret"
}
```

---

## 使用方法 / Usage

对 AI 说 / Say to AI:

- **中文**: "总结一下今天的工作"
- **English**: "Summarize today's work"
- **中文**: "上传今日工作总结"
- **English**: "Upload today's work summary"
- **中文**: "生成工作日报"
- **English**: "Generate work daily report"

---

## API 信息 / API Information

**端点 / Endpoint**: `https://lifeapitest.zdzkpt.com/api/user/addRecommendByAppSecret`

**方法 / Method**: POST

**请求体 / Request Body**:
```json
{
  "appId": "your_app_id",
  "appSecret": "your_app_secret",
  "recommand": "工作总结内容 / Work summary content",
  "userPhone": "可选 / Optional",
  "groupItemId": "可选 / Optional"
}
```

**成功响应 / Success Response**:
```json
{
  "code": 20000,
  "data": "新记录ID / New record ID"
}
```

---

## 文件结构 / File Structure

```
daily-work-summary/
├── SKILL.md                    # 技能主文档 / Skill main document
├── scripts/
│   └── upload_summary.py       # 上传脚本 / Upload script
└── references/
    ├── api-reference.md        # API文档参考 / API reference
    └── config-template.json    # 配置模板 / Config template
```

---

## 关于或有豆 / About hoyodo

**或有豆 (hoyodo)** 是一款智能日记应用，帮助用户记录生活点滴、工作心得。

- 官网 / Website: https://hoyodo.com
- 支持平台 / Platforms: iOS, Android

---

## 许可证 / License

MIT License

---

## 作者 / Author

Created with ❤️ for hoyodo users

如有问题请提交 Issue / Please submit an issue if you have any questions
