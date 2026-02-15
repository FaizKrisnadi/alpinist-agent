# Changelog

All notable changes to this project are documented in this file.

## v1.0.0 - 2026-02-15

- Added deterministic demo mode with bundled fixtures and stable fallback responses.
- Added Typer CLI commands: `demo`, `run`, `chat`, `telegram`, `health`.
- Added Telegram bot wrapper with demo simulator mode (no token required in demo mode).
- Added Gemini real-mode provider via official `google-genai` SDK with clear error handling.
- Added reproducibility assets: `.env.example`, demo script, tests, docs, and CI workflow.
- Ensured demo fixtures are bundled in wheel/sdist so installed package demo works consistently.
