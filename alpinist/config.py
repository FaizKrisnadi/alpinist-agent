"""Configuration loading and validation."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace

# Reasonable default that users can override via GEMINI_MODEL.
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


class ConfigError(ValueError):
    """Raised when environment configuration is invalid."""


def _clean_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _parse_bool(name: str, raw: str) -> bool:
    normalized = raw.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise ConfigError(f"{name} must be one of 1/0/true/false/yes/no/on/off, got: {raw!r}")


@dataclass(slots=True)
class Config:
    """Runtime configuration for the Alpinist agent."""

    demo_mode: bool = True
    gemini_api_key: str | None = None
    gemini_model: str = DEFAULT_GEMINI_MODEL
    telegram_bot_token: str | None = None
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Config:
        demo_mode = _parse_bool("DEMO_MODE", os.getenv("DEMO_MODE", "1"))
        return cls(
            demo_mode=demo_mode,
            gemini_api_key=_clean_env("GEMINI_API_KEY"),
            gemini_model=_clean_env("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL,
            telegram_bot_token=_clean_env("TELEGRAM_BOT_TOKEN"),
            log_level=(_clean_env("LOG_LEVEL") or "INFO").upper(),
        )

    def with_overrides(self, **changes: object) -> Config:
        return replace(self, **changes)

    def validate_for_agent(self) -> None:
        if not self.demo_mode and not self.gemini_api_key:
            raise ConfigError("GEMINI_API_KEY is required when DEMO_MODE=0 (real mode).")

    def validate_for_telegram(self) -> None:
        self.validate_for_agent()
        if not self.demo_mode and not self.telegram_bot_token:
            raise ConfigError(
                "TELEGRAM_BOT_TOKEN is required when starting Telegram in real mode (DEMO_MODE=0)."
            )
