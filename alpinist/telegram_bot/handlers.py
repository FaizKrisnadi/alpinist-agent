"""Async Telegram command/message handlers."""

from __future__ import annotations

import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from alpinist.agent import Agent

LOGGER = logging.getLogger(__name__)


class TelegramHandlers:
    """Collection of handlers with per-chat history and locks."""

    def __init__(self, agent: Agent, demo_mode: bool) -> None:
        self._agent = agent
        self._demo_mode = demo_mode
        self._chat_histories: dict[int, list[dict[str, str]]] = {}
        self._locks: dict[int, asyncio.Lock] = {}

    def register(self, application: Application) -> None:
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("reset", self.reset))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

    def _lock_for(self, chat_id: int) -> asyncio.Lock:
        lock = self._locks.get(chat_id)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[chat_id] = lock
        return lock

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _ = context
        if not update.message:
            return
        mode = "demo" if self._demo_mode else "real"
        await update.message.reply_text(
            "Alpinist bot is online.\n"
            f"Mode: {mode}\n"
            "Send any text to chat, or use /help for commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _ = context
        if not update.message:
            return
        await update.message.reply_text(
            "/start - show bot status\n"
            "/help - show commands\n"
            "/reset - clear chat history for this chat\n"
            "Send plain text to get a response."
        )

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _ = context
        if not update.message or not update.effective_chat:
            return
        chat_id = update.effective_chat.id
        history = self._chat_histories.setdefault(chat_id, [])
        self._agent.reset_history(history=history)
        await update.message.reply_text("History reset for this chat.")

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _ = context
        if not update.message or not update.effective_chat:
            return

        chat_id = update.effective_chat.id
        prompt = (update.message.text or "").strip()
        if not prompt:
            await update.message.reply_text("Please send a non-empty message.")
            return

        lock = self._lock_for(chat_id)
        async with lock:
            history = self._chat_histories.setdefault(chat_id, [])
            try:
                response = await asyncio.to_thread(self._agent.run_once, prompt, history)
            except Exception:  # noqa: BLE001 - keep bot alive on any processing failures
                LOGGER.exception("Failed to process message for chat_id=%s", chat_id)
                await update.message.reply_text("Sorry, I hit an internal error. Please try again.")
                return
            await update.message.reply_text(response)
