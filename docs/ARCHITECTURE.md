# Architecture

## Components

- `alpinist.cli`: Typer entrypoint exposing `demo`, `run`, `chat`, `health`, `telegram`.
- `alpinist.config`: environment parsing and mode validation.
- `alpinist.agent`: mode-based provider selection and chat/history orchestration.
- `alpinist.providers.mock_provider`: deterministic fixture-backed provider.
- `alpinist.providers.gemini_provider`: real provider using `google-genai`.
- `alpinist.telegram_bot`: async Telegram handlers and startup wrapper.

## Flow

- CLI command starts and loads `Config` from environment variables.
- `Agent` selects `MockProvider` when `DEMO_MODE=1`, else `GeminiProvider`.
- `run/chat/demo` call `Agent.run_once()` and print responses.
- `telegram` command:
  - Uses Telegram polling when `TELEGRAM_BOT_TOKEN` is present.
  - Falls back to a local simulator in demo mode when token is missing.
- Per-chat lock in Telegram handlers prevents concurrent race conditions per chat.

## Deterministic Demo Guarantees

- Runtime fixture file: `alpinist/fixtures/demo_responses.jsonl` (bundled in wheel)
- Source mirror fixture: `examples/fixtures/demo_responses.jsonl`
- Unknown prompts return deterministic hash-based fallback text.
- No network calls or API keys are required in demo mode.
