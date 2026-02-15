# alpinist-agent

[![CI](https://github.com/FaizKrisnadi/alpinist-agent/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/FaizKrisnadi/alpinist-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/FaizKrisnadi/alpinist-agent)](https://github.com/FaizKrisnadi/alpinist-agent/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

Reproducible replication package for the Alpinist agent:

- CLI wrapper (`alpinist`)
- Telegram bot wrapper
- Gemini integration via official `google-genai`
- Deterministic demo mode that runs without secrets and without network API calls

## Quickstart Demo (No Keys)

```bash
git clone https://github.com/FaizKrisnadi/alpinist-agent.git
cd alpinist-agent
bash scripts/run_demo.sh
```

`scripts/run_demo.sh` creates `.venv`, installs dependencies, and runs `alpinist demo`.

## Real Mode CLI (Gemini)

```bash
cd alpinist-agent
source .venv/bin/activate
export DEMO_MODE=0
export GEMINI_API_KEY="your_api_key_here"
# Optional override. Default is gemini-2.5-flash.
export GEMINI_MODEL="gemini-2.5-flash"

alpinist run --prompt "Summarize this repository."
alpinist chat
```

If `DEMO_MODE=0` and `GEMINI_API_KEY` is missing, commands fail fast with a clear error.

## Telegram

Demo mode without Telegram token (local simulator, no Telegram network calls):

```bash
cd alpinist-agent
source .venv/bin/activate
export DEMO_MODE=1
unset TELEGRAM_BOT_TOKEN
alpinist telegram
```

Demo mode with Telegram transport (fixture responses through Telegram):

```bash
export DEMO_MODE=1
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
alpinist telegram
```

Real mode with Gemini + Telegram:

```bash
export DEMO_MODE=0
export GEMINI_API_KEY="your_api_key_here"
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
alpinist telegram
```

If `DEMO_MODE=0` and `TELEGRAM_BOT_TOKEN` is missing, `alpinist telegram` fails fast.

## Deterministic vs Non-Deterministic

- Deterministic (`DEMO_MODE=1`): responses come from bundled fixtures plus a stable hash-based fallback for unknown prompts.
- Non-deterministic (`DEMO_MODE=0`): responses come from live Gemini API calls and may vary.

## Command List

- `alpinist demo`
- `alpinist run --prompt "..."`
- `alpinist chat`
- `alpinist telegram`
- `alpinist health`

## Project Structure

```text
alpinist/
  config.py
  agent.py
  cli.py
  providers/
  telegram_bot/
  fixtures/
examples/fixtures/
docs/
tests/
.github/workflows/
```

## Security

- Never commit secrets.
- Use environment variables for `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN`.
- Only `.env.example` is provided as a template.
- See `docs/SECURITY.md`.

## How to Cite

- Citation metadata is in `CITATION.cff`.
- After enabling Zenodo, each GitHub Release gets a DOI; see `docs/ZENODO.md`.

## Versioning

This repository is release-ready for `v1.0.0`. Use Git tags for immutable replication snapshots.
