# v1.0.0

First stable public release of the Alpinist replication package.

## What's Included

- Deterministic demo mode with no secrets and no external API calls.
- Typer CLI: `alpinist demo`, `run`, `chat`, `telegram`, `health`.
- Telegram wrapper with:
  - local demo simulator when `DEMO_MODE=1` and no `TELEGRAM_BOT_TOKEN`
  - real Telegram polling mode when token is provided
- Gemini real mode via official `google-genai` SDK.
- CI checks (`ruff`, `pytest`) and bundled fixtures for reproducible installs.

## Run Demo

```bash
bash scripts/run_demo.sh
```

## Run Real Mode

```bash
source .venv/bin/activate
export DEMO_MODE=0
export GEMINI_API_KEY="your_api_key_here"
alpinist run --prompt "Hello from real mode"
```

## Compatibility

- Python `>=3.11`
- Tested with clean clone, editable install, and built wheel install.

## Security

- No real secrets are committed.
- Use environment variables only (`GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`).
- `.env.example` is template-only.
