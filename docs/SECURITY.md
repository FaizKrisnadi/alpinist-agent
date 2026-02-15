# Security

## Secret Handling Rules

- Never commit real secrets or tokens.
- Do not create a real `.env` file in this repository.
- Keep only `.env.example` as a template.
- Pass secrets via environment variables at runtime:
  - `GEMINI_API_KEY`
  - `TELEGRAM_BOT_TOKEN`

## Logging

- Logging never prints secret values.
- Health checks report only presence/absence booleans for secret variables.

## Demo Mode Safety

- Default mode is demo (`DEMO_MODE=1`), which uses local fixtures only.
- Demo mode can run end to end with zero external keys and no API calls.
