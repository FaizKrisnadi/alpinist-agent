"""Telegram bot startup and demo simulator."""

from __future__ import annotations

import asyncio
import logging

from telegram.ext import Application

from alpinist.agent import Agent
from alpinist.config import Config, ConfigError
from alpinist.telegram_bot.handlers import TelegramHandlers

LOGGER = logging.getLogger(__name__)


async def _run_local_demo_simulator(agent: Agent) -> None:
    print("Starting local Telegram simulator (demo mode, no token required).")
    print("Commands: /start, /help, /reset, /q")

    while True:
        try:
            incoming = await asyncio.to_thread(input, "telegram-demo> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        message = incoming.strip()
        if not message:
            continue
        if message in {"/q", "/quit", "quit", "exit"}:
            break
        if message == "/start":
            print("bot> Alpinist demo bot is online (local simulator).")
            continue
        if message == "/help":
            print("bot> /start /help /reset plus plain text prompts.")
            continue
        if message == "/reset":
            agent.reset_history()
            print("bot> History reset.")
            continue

        try:
            response = agent.run_once(message)
        except Exception as exc:  # noqa: BLE001 - do not crash interactive demo
            LOGGER.exception("Local simulator failed")
            print(f"bot> Internal error: {exc}")
            continue
        print(f"bot> {response}")


def start_bot(config: Config) -> None:
    """Start Telegram polling, or a local simulator when in demo mode without token."""
    if not config.demo_mode:
        config.validate_for_telegram()

    agent = Agent(config=config)
    if not config.telegram_bot_token:
        if config.demo_mode:
            LOGGER.info("TELEGRAM_BOT_TOKEN missing in demo mode; using local simulator.")
            asyncio.run(_run_local_demo_simulator(agent))
            return
        raise ConfigError(
            "TELEGRAM_BOT_TOKEN is required to start Telegram in real mode (DEMO_MODE=0)."
        )

    handlers = TelegramHandlers(agent=agent, demo_mode=config.demo_mode)
    application = Application.builder().token(config.telegram_bot_token).build()
    handlers.register(application)

    mode = "demo" if config.demo_mode else "real"
    LOGGER.info("Starting Telegram bot polling in %s mode.", mode)
    application.run_polling(drop_pending_updates=True)
