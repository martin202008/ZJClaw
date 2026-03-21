# ZJClaw Skills

This directory contains built-in skills that extend ZJClaw's capabilities.

## Skill Format

Each skill is a directory containing a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Markdown instructions for the agent

## Attribution

These skills are adapted from [OpenClaw](https://github.com/openclaw/openclaw)'s skill system.
The skill format and metadata structure follow OpenClaw's conventions to maintain compatibility.

## Available Skills

### Commercial Management Skills

| Skill | Description |
|-------|-------------|
| `recruitment` | 商业招商 - Business recruitment and tenant management |
| `operations` | 商业运营 - Daily operations and customer service |
| `marketing` | 数字营销 - Digital marketing and member management |
| `engineering` | 工程物管 - Engineering and property management |
| `finance` | 财务管理 - Financial management and budgeting |
| `hr` | 人事行政 - HR and administration |

### Utility Skills

| Skill | Description |
|-------|-------------|
| `github` | Interact with GitHub using the `gh` CLI |
| `weather` | Get weather info using wttr.in and Open-Meteo |
| `summarize` | Summarize URLs, files, and YouTube videos |
| `tmux` | Remote-control tmux sessions |
| `clawhub` | Search and install skills from ClawHub registry |
| `skill-creator` | Create new skills |
