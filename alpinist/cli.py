"""Typer CLI entrypoint for the Alpinist agent package."""

from __future__ import annotations

import typer

from alpinist.agent import Agent
from alpinist.config import Config, ConfigError
from alpinist.logging_setup import configure_logging
from alpinist.telegram_bot.app import start_bot

app = typer.Typer(help="CLI + Telegram wrapper for the Alpinist agent.")

DEMO_PROMPTS = [
    "hello alpinist",
    "what is demo mode?",
    "give me an end-to-end summary",
]


def _load_config(force_demo: bool = False) -> Config:
    config = Config.from_env()
    if force_demo:
        return config.with_overrides(demo_mode=True)
    return config


def _print_config_health(config: Config) -> list[str]:
    issues: list[str] = []
    mode = "demo" if config.demo_mode else "real"
    gemini_key_present = bool(config.gemini_api_key)
    telegram_token_present = bool(config.telegram_bot_token)

    typer.echo(f"mode={mode}")
    typer.echo(f"log_level={config.log_level}")
    typer.echo(f"gemini_model={config.gemini_model}")
    typer.echo(f"gemini_api_key_present={gemini_key_present}")
    typer.echo(f"telegram_bot_token_present={telegram_token_present}")

    if not config.demo_mode and not gemini_key_present:
        issues.append("GEMINI_API_KEY is required in real mode (DEMO_MODE=0).")

    if config.demo_mode and not telegram_token_present:
        typer.echo("telegram_status=local simulator available (token optional in demo mode)")
    elif telegram_token_present:
        typer.echo("telegram_status=ready")
    else:
        typer.echo("telegram_status=missing token (required for real Telegram polling)")

    return issues


@app.command()
def demo() -> None:
    """Run fixed deterministic prompts in demo mode (no external API calls)."""
    config = _load_config(force_demo=True)
    configure_logging(config.log_level)
    agent = Agent(config=config)

    typer.echo("Running deterministic demo prompts (fixtures + local fallback).")
    for prompt in DEMO_PROMPTS:
        typer.echo(f"\n> {prompt}")
        typer.echo(agent.run_once(prompt))


@app.command("run")
def run_command(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Single prompt to send to the agent."),
) -> None:
    """Run one prompt in demo or real mode depending on DEMO_MODE."""
    try:
        config = _load_config()
        configure_logging(config.log_level)
        agent = Agent(config=config)
        typer.echo(agent.run_once(prompt))
    except ConfigError as exc:
        typer.echo(f"Configuration error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@app.command()
def chat() -> None:
    """Start interactive terminal chat."""
    try:
        config = _load_config()
        configure_logging(config.log_level)
        agent = Agent(config=config)
        agent.chat_loop()
    except ConfigError as exc:
        typer.echo(f"Configuration error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@app.command()
def health() -> None:
    """Check current mode and whether required environment variables are present."""
    try:
        config = _load_config()
    except ConfigError as exc:
        typer.echo(f"Configuration error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    issues = _print_config_health(config)
    if issues:
        for issue in issues:
            typer.echo(f"error: {issue}", err=True)
        raise typer.Exit(code=1)

    typer.echo("status=ok")


@app.command()
def telegram() -> None:
    """Start Telegram wrapper in demo or real mode."""
    try:
        config = _load_config()
        configure_logging(config.log_level)
        start_bot(config)
    except ConfigError as exc:
        typer.echo(f"Configuration error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


def app_main() -> None:
    app()


if __name__ == "__main__":
    app_main()
